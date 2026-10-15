#!/usr/bin/env python3
"""Collect standalone agent skills from multiple source directories and vendor into projects.

Requires only Python 3.9+. Safe defaults: no local source modification; no
unexpected overwrite of project-specific skills; refuse embedded symlinks and
potential secret files; no deletion of removed skills unless explicitly asked.
"""
import argparse
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / 'config.json'
SKILLS = ROOT / 'skills'
PROJECT_MANIFEST = '.shared-skills-manifest.json'
IGNORED = {'.git', '.DS_Store', '__pycache__', '.pytest_cache', '.mypy_cache', 'node_modules', '.venv'}
BLOCKED = {'auth.json', 'credentials.json', 'id_rsa', 'id_ed25519', '.env', '.aws', '.ssh'}
BLOCK_PATTERNS = ('*.pem', '*.key', '*.p12', '*.pfx', '.env.*')


def fail(message):
    raise ValueError(message)


def load_config():
    data = json.loads(CONFIG.read_text(encoding='utf-8'))
    if not isinstance(data.get('sources'), list) or not data['sources']:
        fail('config.json must have a nonempty sources array')
    return data


def clean_name(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', value):
        fail(f'Invalid skill folder name: {value!r}')
    return value


def frontmatter_name(path):
    contents = path.read_text(encoding='utf-8')
    if not contents.startswith('---\n'):
        fail(f'Missing YAML frontmatter: {path}')
    end = contents.find('\n---', 4)
    if end < 0:
        fail(f'Unterminated YAML frontmatter: {path}')
    matter = contents[4:end]
    vals = {}
    for line in matter.splitlines():
        m = re.match(r'^(name|description):\s*(.*)$', line)
        if m:
            vals[m.group(1)] = m.group(2).strip().strip('"\'')
    if not vals.get('name') or not vals.get('description'):
        fail(f'Expected name and description metadata: {path}')
    return vals['name']


def is_ignored(name):
    return name in IGNORED


def check_tree(path):
    # Check before exporting to Git. Files named like secrets are rejected.
    # Folder symlinks at the root are okay; symlinks inside a skill are not.
    for directory, dirs, files in os.walk(path, followlinks=False):
        for name in dirs + files:
            item = Path(directory) / name
            if item.is_symlink():
                fail(f'Nested symlink needs manual review: {item}')
            if name in BLOCKED or any(fnmatch.fnmatch(name, p) for p in BLOCK_PATTERNS):
                if name not in ('.env.example', '.env.sample'):
                    fail(f'Possible secret inside skill. Review before publishing: {item}')
        dirs[:] = [d for d in dirs if not is_ignored(d)]


def copy_skill(src, dest):
    check_tree(src)
    def ignore(path, names):
        return [n for n in names if is_ignored(n)]
    shutil.copytree(src, dest, ignore=ignore)


def digest(path):
    sha = hashlib.sha256()
    for file in sorted(p for p in path.rglob('*') if p.is_file()):
        sha.update(str(file.relative_to(path)).encode())
        sha.update(b'\x00')
        sha.update(file.read_bytes())
        sha.update(b'\x00')
    return sha.hexdigest()


def discover(data):
    found = {}
    metadata_names = {}
    for entry in data['sources']:
        source_id = entry.get('id', '<unnamed>')
        src = Path(os.path.expanduser(entry['path'])).resolve()
        if not src.is_dir():
            fail(f'Source directory does not exist: {src}')
        count = 0
        # Every immediate child directory containing SKILL.md is a package.
        # This deliberate boundary avoids treating nested examples as skills.
        for item in sorted(src.iterdir()):
            if item.name.startswith('.') or not item.is_dir():
                continue
            manifest = item / 'SKILL.md'
            if not manifest.is_file():
                continue
            name = clean_name(item.name)
            skill_name = frontmatter_name(manifest)
            if name in found:
                fail(f'Duplicate folder name {name!r}: {found[name]} and {item}. Rename one before collecting.')
            if skill_name in metadata_names:
                fail(f'Duplicate skill metadata name {skill_name!r}: {metadata_names[skill_name]} and {item}')
            found[name] = item
            metadata_names[skill_name] = item
            count += 1
        print(f'Source {source_id}: {count} skill(s) from {src}')
    return found


def collect(data):
    found = discover(data)
    if not found:
        fail('No skills were found. No changes made.')
    with tempfile.TemporaryDirectory(dir=ROOT, prefix='.skills-build-') as scratch:
        staged = Path(scratch) / 'skills'
        staged.mkdir()
        for name, source in sorted(found.items()):
            copy_skill(source, staged / name)
        # Completed staging: replace prior snapshot, restore if swap fails.
        backup = ROOT / '.skills-previous'
        if backup.exists():
            fail(f'Backup path already exists, resolve manually: {backup}')
        if SKILLS.exists():
            SKILLS.rename(backup)
        try:
            staged.rename(SKILLS)
        except Exception:
            if backup.exists():
                backup.rename(SKILLS)
            raise
        if backup.exists():
            shutil.rmtree(backup)
    print(f'Collected {len(found)} skill(s) into {SKILLS}')
    print('Review with git status/diff before pushing to a PRIVATE GitHub repository.')


def deploy(project, prune=False):
    if not SKILLS.is_dir():
        fail('Run collect first (no skills/ snapshot exists).')
    project = Path(os.path.expanduser(str(project))).resolve()
    if not project.is_dir() or not (project / '.git').exists():
        fail(f'Project must point to a Git repository root containing .git: {project}')
    destroot = project / '.agents' / 'skills'
    if destroot.is_symlink():
        fail(f'Destination directory is a symlink (unsupported): {destroot}')
    manifest_file = destroot / PROJECT_MANIFEST
    managed = json.loads(manifest_file.read_text()) if manifest_file.is_file() else {}
    if not isinstance(managed, dict):
        fail(f'Invalid existing deployment manifest: {manifest_file}')
    originals = {p.name: p for p in SKILLS.iterdir() if p.is_dir() and (p / 'SKILL.md').is_file()}
    # Validate everything before changing any files.
    for name in originals:
        target = destroot / name
        if target.exists() or target.is_symlink():
            if name not in managed:
                fail(f'Refusing to overwrite existing unmanaged project skill: {target}')
            if target.is_symlink() or digest(target) != managed[name]:
                fail(f'Project skill edited since last deployment. Resolve locally first: {target}')
    stale = set(managed) - set(originals)
    for name in stale:
        target = destroot / name
        if target.exists() and (target.is_symlink() or digest(target) != managed[name]):
            fail(f'Previously deployed skill was changed: {target}')
    destroot.mkdir(parents=True, exist_ok=True)
    updated = dict(managed)
    for name, source in sorted(originals.items()):
        target = destroot / name
        with tempfile.TemporaryDirectory(dir=destroot, prefix='.deploy-') as tmp:
            staged = Path(tmp) / name
            copy_skill(source, staged)
            if target.exists():
                shutil.rmtree(target)
            staged.rename(target)
        updated[name] = digest(target)
    if prune:
        for name in stale:
            shutil.rmtree(destroot / name, ignore_errors=True)
            updated.pop(name, None)
    manifest_file.write_text(json.dumps(updated, indent=2, sort_keys=True) + '\n')
    print(f'Deployed {len(originals)} skill(s) to {destroot}')
    if stale and not prune:
        print(f'Left {len(stale)} old managed skill(s) untouched; use --prune to remove them.')
    print('Commit and push these project repository changes for Codex Cloud to see them.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('collect', help='Aggregate skills from all configured sources')
    deploy_parser = sub.add_parser('deploy', help='Copy the collected snapshot to one Git project')
    deploy_parser.add_argument('project', help='Absolute or ~ path to your application Git repository root')
    deploy_parser.add_argument('--prune', action='store_true', help='Also delete previously managed skills removed from the hub')
    all_parser = sub.add_parser('deploy-all', help='Deploy to every Git project in config.json.projects')
    all_parser.add_argument('--prune', action='store_true')
    args = parser.parse_args()
    config = load_config()
    if args.action == 'collect':
        collect(config)
    elif args.action == 'deploy':
        deploy(args.project, args.prune)
    else:
        projects = config.get('projects', [])
        if not projects:
            fail('No projects configured. Add project Git repo paths to config.json.projects.')
        for project in projects:
            deploy(project, args.prune)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, UnicodeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(1)

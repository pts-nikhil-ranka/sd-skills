# SD Skills Sync Kit

A local-to-Cloud synchronization helper for macOS/Linux, Python 3.9+.

## Assumptions

- Your currently authored personal skills are stored as immediate subdirectories
  of `~/.codex/skills`: for example `~/.codex/skills/my-skill/SKILL.md`.
- Your application source lives in Git repos that you can push to GitHub.
- You want personal source directories to stay untouched. Sync is one-way:
  **source directories -> skills/ snapshot -> each project's `.agents/skills/`**.
- The kit does not upload files automatically or authenticate to GitHub.

## Initial commands

Extract this directory to `~/sd-skills`.

```sh
cd ~/sd-skills
python3 skills_sync.py collect
ls skills
```

Inspect generated files, including checking for sensitive data, before publishing.
Create a PRIVATE GitHub repository for the hub (using `gh`, if available):

```sh
cd ~/sd-skills
git init
git add .
git diff --cached --stat
git commit -m 'Initial skill snapshot'
gh repo create sd-skills --private --source=. --remote=origin --push
```

## Deploy to each application repository

```sh
python3 skills_sync.py deploy ~/code/my-app
git -C ~/code/my-app status --short
# Inspect diffs and verify skill files, then:
git -C ~/code/my-app add .agents/skills
git -C ~/code/my-app commit -m 'Sync shared Codex skills'
git -C ~/code/my-app push
```

Codex Cloud normally discovers skills committed to the application's
`.agents/skills/<skill-folder>/SKILL.md`. Test in a NEW Cloud task. If an existing
published environment has stale state, edit/republish or create a new task as
necessary. Note that open Codex bug reports describe some Cloud skill discovery
failures; if the files exist but skills don't appear, it's not proof that the
copy failed.

## Future source directories

Edit `config.json`:

```json
{
  "sources": [
    {"id":"codex", "path":"~/.codex/skills"},
    {"id":"claude", "path":"~/.claude/skills"},
    {"id":"other", "path":"~/skills/other"}
  ],
  "projects": ["~/code/my-app", "~/code/another-app"]
}
```

Each source is **one skills root** with immediate child folders that each
contain `SKILL.md`. If yours are nested more deeply, add the actual root
containing those folders to `sources` rather than scanning your entire home.

Then:

```sh
python3 skills_sync.py collect
# Review, commit and push the hub repo as above
python3 skills_sync.py deploy-all
# Review, commit and push EACH project repo
```

## Safeguards

- Won't copy all of `~/.codex`; only skill packages in configured roots.
- Rejects conflicting skill folder names and duplicate frontmatter names.
- Refuses embedded symlinks and possible sensitive files; never stores tokens.
- Leaves source skills untouched.
- Refuses to overwrite pre-existing project-specific skill folders or edited
  previously managed skill folders.
- Does not remove obsolete deployed skills unless you pass `--prune`.
- Do not sync bundled `.system` skills; hidden source entries are ignored.
- **Not** live/two-way synchronization. Run collection after local edits, then
  deploy and push your application repos. Automate later if desired.
- Back up the repository before first deployment if you already have
  `.agents/skills` in a project.

## Verify

```sh
find ~/sd-skills/skills -mindepth 2 -maxdepth 2 -name SKILL.md
find ~/code/my-app/.agents/skills -mindepth 2 -maxdepth 2 -name SKILL.md
```

Current official references:

- https://learn.chatgpt.com/docs/build-skills
- https://learn.chatgpt.com/docs/environments/cloud-environments

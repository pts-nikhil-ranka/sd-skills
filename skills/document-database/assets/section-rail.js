// Load after the navigation markup. Generate links only for existing sections.
if (document.querySelector('.section-rail')) {
const rail=document.querySelector('.section-rail'),railToggle=rail.querySelector('button'),links=[...rail.querySelectorAll('a')],sections=links.map(a=>document.querySelector(a.hash));
function centerRail(){const v=window.visualViewport;rail.style.setProperty('--rail-viewport-center',((v?.offsetTop||0)+(v?.height||innerHeight)/2)+'px');}
function setRailOpen(open){rail.classList.toggle('is-open',open);railToggle.setAttribute('aria-expanded',String(open));}
railToggle.addEventListener('click',()=>setRailOpen(!rail.classList.contains('is-open')));document.addEventListener('pointerdown',e=>{if(!rail.contains(e.target))setRailOpen(false);});rail.addEventListener('keydown',e=>{if(e.key==='Escape'){setRailOpen(false);document.activeElement.blur();}});links.forEach(a=>a.addEventListener('click',()=>setRailOpen(false)));
function trackSection(){let active=sections[0];for(const s of sections)if(s.getBoundingClientRect().top<=150)active=s;if(scrollY+innerHeight>=document.documentElement.scrollHeight-4)active=sections.at(-1);links.forEach(a=>a.hash==='#'+active.id?a.setAttribute('aria-current','location'):a.removeAttribute('aria-current'));}
let scheduled=false;addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(()=>{trackSection();scheduled=false;});}},{passive:true});addEventListener('resize',()=>{centerRail();trackSection();});addEventListener('pageshow',centerRail);window.visualViewport?.addEventListener('resize',centerRail);window.visualViewport?.addEventListener('scroll',centerRail);centerRail();trackSection();
}

const header=document.querySelector('.site-header');
const menuButton=document.querySelector('.menu-toggle');
const reveals=document.querySelectorAll('.reveal');
const onScroll=()=>header.classList.toggle('is-scrolled',window.scrollY>24);
onScroll();window.addEventListener('scroll',onScroll,{passive:true});
menuButton.addEventListener('click',()=>{const open=header.classList.toggle('menu-open');menuButton.setAttribute('aria-expanded',String(open))});
document.querySelectorAll('nav a').forEach(link=>link.addEventListener('click',()=>{header.classList.remove('menu-open');menuButton.setAttribute('aria-expanded','false')}));
if('IntersectionObserver' in window){const io=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('visible');io.unobserve(entry.target)}}),{threshold:.12});reveals.forEach(el=>io.observe(el))}else{reveals.forEach(el=>el.classList.add('visible'))}
document.querySelectorAll('.accordion details').forEach(detail=>detail.addEventListener('toggle',()=>{if(detail.open)document.querySelectorAll('.accordion details').forEach(other=>{if(other!==detail)other.removeAttribute('open')})}));
document.getElementById('ano').textContent=new Date().getFullYear();

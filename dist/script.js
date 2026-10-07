document.getElementById('year').textContent = new Date().getFullYear();

const projects = [...document.querySelectorAll('.project')];
const filters = [...document.querySelectorAll('[data-filter]')];
const count = document.getElementById('project-count');
function selectFilter(value) {
  let visible = 0;
  projects.forEach(project => {
    project.hidden = value !== 'all' && project.dataset.category !== value;
    if (!project.hidden) visible++;
  });
  filters.forEach(button => {
    const selected = button.dataset.filter === value;
    button.classList.toggle('active', selected);
    button.setAttribute('aria-pressed', String(selected));
  });
  count.textContent = `${visible} projet${visible > 1 ? 's' : ''} à explorer`;
}
filters.forEach(button => button.addEventListener('click', () => selectFilter(button.dataset.filter)));
document.querySelectorAll('.hero-project-switch a').forEach(link => {
  link.addEventListener('click', () => selectFilter('all'));
});

const dialog = document.getElementById('project-dialog');
document.querySelectorAll('[data-preview]').forEach(button => {
  button.addEventListener('click', () => {
    const project = document.getElementById(button.dataset.preview);
    document.getElementById('dialog-title').textContent = project.querySelector('h3').firstChild.textContent;
    document.getElementById('dialog-visual').replaceChildren(project.querySelector('.project-visual').cloneNode(true));
    document.getElementById('dialog-links').replaceChildren(...[...project.querySelector('.project-links').children].map(link => link.cloneNode(true)));
    dialog.showModal();
  });
});
dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => {
  if (event.target === dialog) {
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
  }
});

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!reducedMotion && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        observer.unobserve(entry.target);
      }
    });
  }, {threshold: 0.08});
  document.querySelectorAll('.section-head, .project, .approach-grid > div, .profile > div, .journey-grid > div').forEach(element => {
    element.classList.add('reveal');
    observer.observe(element);
  });
}
const progress = document.querySelector('.scroll-progress');
let scrollFrame = false;
function updateProgress() {
  const total = document.documentElement.scrollHeight - window.innerHeight;
  progress.style.transform = `scaleX(${total > 0 ? Math.min(1, Math.max(0, window.scrollY / total)) : 0})`;
  scrollFrame = false;
}
window.addEventListener('scroll', () => {
  if (!scrollFrame) { scrollFrame = true; requestAnimationFrame(updateProgress); }
}, {passive: true});
window.addEventListener('resize', updateProgress);
updateProgress();

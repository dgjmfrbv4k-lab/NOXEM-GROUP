// Header scroll state
const header = document.getElementById('header');
window.addEventListener('scroll', () => {
  header.classList.toggle('scrolled', window.scrollY > 10);
});

// Mobile nav toggle
const burger = document.getElementById('burger');
const nav = document.getElementById('nav');
burger.addEventListener('click', () => {
  nav.classList.toggle('open');
});
nav.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => nav.classList.remove('open'));
});

// Scroll reveal
const revealEls = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.15 }
);
revealEls.forEach((el) => observer.observe(el));

// Animated stat counters
const counters = document.querySelectorAll('[data-count]');
const counterObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = parseInt(el.dataset.count, 10);
      const duration = 1200;
      const start = performance.now();
      function tick(now) {
        const progress = Math.min((now - start) / duration, 1);
        el.textContent = Math.floor(progress * target);
        if (progress < 1) requestAnimationFrame(tick);
        else el.textContent = target;
      }
      requestAnimationFrame(tick);
      counterObserver.unobserve(el);
    });
  },
  { threshold: 0.5 }
);
counters.forEach((el) => counterObserver.observe(el));

// Contact form (front-end only demo)
const form = document.getElementById('contact-form');
const status = document.getElementById('form-status');
form.addEventListener('submit', (e) => {
  e.preventDefault();
  status.textContent = 'Merci ! Votre message a bien été pris en compte.';
  form.reset();
});

// Footer year
document.getElementById('year').textContent = new Date().getFullYear();

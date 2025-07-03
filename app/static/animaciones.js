// Simple animation utilities
// Fade in elements with class .fade
window.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.fade').forEach(el => {
    el.style.opacity = 0;
    el.style.transition = 'opacity 0.8s ease-in';
    setTimeout(() => (el.style.opacity = 1), 200);
  });

  // Navbar shrink on scroll
  const header = document.querySelector('header');
  if (header) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 50) {
        header.classList.add('shrink');
      } else {
        header.classList.remove('shrink');
      }
    });
  }
});
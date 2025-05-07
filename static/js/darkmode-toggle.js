// Wait for the DOM to load before adding event listeners
document.addEventListener('DOMContentLoaded', function () {
  // Check if dark mode is saved in localStorage
  if (localStorage.getItem('dark-mode') === 'true') {
      document.body.classList.add('dark-mode');
      document.querySelector('header').classList.add('dark-mode');
      const navLinks = document.querySelectorAll('.rd-navbar-nav .rd-nav-item a');
      navLinks.forEach(link => link.classList.add('dark-mode'));
  }

  // Add event listener for the toggle button
  document.getElementById('toggle-btn').addEventListener('click', function () {
      // Toggle the dark mode class on body and header
      document.body.classList.toggle('dark-mode');
      document.querySelector('header').classList.toggle('dark-mode');
      
      // Toggle the dark-mode class on navigation links
      const navLinks = document.querySelectorAll('.rd-navbar-nav .rd-nav-item a');
      navLinks.forEach(link => link.classList.toggle('dark-mode'));
      
      // Save the mode in localStorage
      const isDarkMode = document.body.classList.contains('dark-mode');
      localStorage.setItem('dark-mode', isDarkMode);
  });
});

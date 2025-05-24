// Toggle menu script
function toggleMenu(event) {
    if (event) {
      event.stopPropagation();
    }
    document.getElementById("mobileMenu").classList.toggle("hidden");
  }

  // Close menu script
  function closeMenu(event) {
    if (event) {
      event.stopPropagation();
    }
    document.getElementById("mobileMenu").classList.add("hidden");
  }

  // Close menu when clicking outside
  document.addEventListener('click', function(event) {
    const mobileMenu = document.getElementById("mobileMenu");
    const menuButton = document.querySelector('button[onclick="toggleMenu()"]');
    
    if (!menuButton.contains(event.target) && !mobileMenu.contains(event.target)) {
      mobileMenu.classList.add("hidden");
    }
  });

  // Smooth scroll with offset
  document.addEventListener('DOMContentLoaded', function() {
    const headerHeight = document.querySelector('header').offsetHeight;
    const marqueeHeight = document.querySelector('.bg-yellow-100').offsetHeight;
    const offset = headerHeight + marqueeHeight;

    // Handle all navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
          const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
          window.scrollTo({
            top: targetPosition - offset,
            behavior: 'smooth'
          });
        }
      });
    });

    // Tab navigation functionality
    const tabLinks = document.querySelectorAll('.tab-link');
    const sections = document.querySelectorAll('section[id]');

    function setActiveTab() {
      const scrollPosition = window.scrollY + offset;
      
      sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        const sectionId = section.getAttribute('id');
        
        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
          tabLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${sectionId}`) {
              link.classList.add('active');
            }
          });
        }
      });
    }

    // Add active state styles
    const style = document.createElement('style');
    style.textContent = `
      .tab-link.active {
        color: #059669;
        background-color: #ecfdf5;
      }
    `;
    document.head.appendChild(style);

    // Scroll progress bar
    const scrollProgress = document.getElementById('scrollProgress');
    if (scrollProgress) {
      window.addEventListener('scroll', () => {
        const scrollable = document.documentElement.scrollHeight - window.innerHeight;
        const scrolled = window.scrollY;
        const progress = (scrolled / scrollable) * 100;
        scrollProgress.style.width = progress + '%';
      });
    }

    // Carousel functionality
    const items = document.querySelectorAll('.carousel-item');
    const indicators = document.querySelectorAll('.carousel-indicator');
    const prevBtn = document.querySelector('.carousel-prev');
    const nextBtn = document.querySelector('.carousel-next');
    let currentIndex = 0;

    function showSlide(index) {
      items.forEach((item, i) => {
        item.style.opacity = i === index ? '1' : '0';
      });
      indicators.forEach((indicator, i) => {
        indicator.style.backgroundColor = i === index ? 'white' : 'rgba(255, 255, 255, 0.5)';
      });
    }

    function nextSlide() {
      currentIndex = (currentIndex + 1) % items.length;
      showSlide(currentIndex);
    }

    function prevSlide() {
      currentIndex = (currentIndex - 1 + items.length) % items.length;
      showSlide(currentIndex);
    }

    // Event listeners
    nextBtn.addEventListener('click', nextSlide);
    prevBtn.addEventListener('click', prevSlide);
    indicators.forEach((indicator, index) => {
      indicator.addEventListener('click', () => {
        currentIndex = index;
        showSlide(currentIndex);
      });
    });

    // Auto-advance slides
    setInterval(nextSlide, 5000);
  });

  // Add click effect to tab links
  document.querySelectorAll('.tab-link').forEach(link => {
    link.addEventListener('click', function() {
      // Remove active class from all links
      document.querySelectorAll('.tab-link').forEach(l => l.classList.remove('active'));
      // Add active class to clicked link
      this.classList.add('active');
    });
  });
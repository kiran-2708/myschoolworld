
  // Menu toggle for mobile menu
  function toggleMenu(event) {
    if (event) {
      event.stopPropagation();
    }
    const menu = document.getElementById("mobileMenu");
    if (menu) {
      menu.classList.toggle("hidden");
    }
  }

  // Close menu manually
  function closeMenu(event) {
    if (event) {
      event.stopPropagation();
    }
    const menu = document.getElementById("mobileMenu");
    if (menu) {
      menu.classList.add("hidden");
    }
  }

  // Run after DOM is fully loaded
  document.addEventListener('DOMContentLoaded', function () {
    // Handle closing the mobile menu when clicking outside
    const mobileMenu = document.getElementById("mobileMenu");
    const menuButton = document.querySelector('button[onclick="toggleMenu()"]');

    if (mobileMenu && menuButton) {
      document.addEventListener('click', function (event) {
        if (!menuButton.contains(event.target) && !mobileMenu.contains(event.target)) {
          mobileMenu.classList.add("hidden");
        }
      });
    }

    // Profile dropdown handling
    const profileDropdown = document.getElementById('profileDropdown');
    const dropdownMenu = document.getElementById('dropdownMenu');

    if (profileDropdown && dropdownMenu) {
      profileDropdown.addEventListener('click', () => {
        dropdownMenu.classList.toggle('hidden');
      });

      window.addEventListener('click', (e) => {
        if (!profileDropdown.contains(e.target) && !dropdownMenu.contains(e.target)) {
          dropdownMenu.classList.add('hidden');
        }
      });
    }

    // Academic year dropdown
    const dropdownBtn = document.getElementById('academicDropdownButton');
    const academicDropdownMenu = document.getElementById('academicDropdownMenu');
    const hiddenInput = document.getElementById('academicYearInput');
    const selectedSpan = document.getElementById('selectedAcademicYear');

    if (dropdownBtn && academicDropdownMenu && hiddenInput && selectedSpan) {
      // Toggle dropdown
      dropdownBtn.addEventListener('click', () => {
        academicDropdownMenu.classList.toggle('hidden');
      });

      // Handle selection
      academicDropdownMenu.querySelectorAll('li').forEach(item => {
        item.addEventListener('click', () => {
          const value = item.getAttribute('data-value');
          hiddenInput.value = value;
          selectedSpan.textContent = value;
          academicDropdownMenu.classList.add('hidden');

          // Auto-submit form
          const form = dropdownBtn.closest('form');
          if (form) {
            form.submit();
          }
        });
      });

      // Close dropdown when clicking outside
      document.addEventListener('click', function (e) {
        if (!dropdownBtn.contains(e.target) && !academicDropdownMenu.contains(e.target)) {
          academicDropdownMenu.classList.add('hidden');
        }
      });
    }

    // Live date and time updater
    function updateDateTime() {
      const now = new Date();
      const options = {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: true,
      };
      const dateTimeEl = document.getElementById("datetime");
      if (dateTimeEl) {
        dateTimeEl.textContent = now.toLocaleDateString("en-US", options);
      }
    }

    updateDateTime(); // Initial call
    setInterval(updateDateTime, 1000); // Update every second
  });


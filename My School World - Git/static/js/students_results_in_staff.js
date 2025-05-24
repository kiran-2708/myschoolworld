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
      document.addEventListener("click", function (event) {
        const mobileMenu = document.getElementById("mobileMenu");
        const menuButton = document.querySelector(
          'button[onclick="toggleMenu()"]'
        );

        if (
          !menuButton.contains(event.target) &&
          !mobileMenu.contains(event.target)
        ) {
          mobileMenu.classList.add("hidden");
        }
      });

      const profileDropdown = document.getElementById("profileDropdown");
      const dropdownMenu = document.getElementById("dropdownMenu");

      profileDropdown.addEventListener("click", () => {
        dropdownMenu.classList.toggle("hidden");
      });

      // Close dropdown when clicking outside
      window.addEventListener("click", (e) => {
        if (!profileDropdown.contains(e.target)) {
          dropdownMenu.classList.add("hidden");
        }
      });

      // Clock functionality
      function updateClock() {
        const now = new Date();
        const timeString = now.toLocaleTimeString("en-US", {
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
          hour12: true,
        });
        const dateString = now.toLocaleDateString("en-US", {
          weekday: "long",
          year: "numeric",
          month: "long",
          day: "numeric",
        });

        document.getElementById("clock").textContent = timeString;
        document.getElementById("date").textContent = dateString;
      }

      // Update clock every second
      setInterval(updateClock, 1000);
      updateClock(); // Initial call

      // Roll Number Dropdown
      const rollNumberButton = document.getElementById("rollNumberButton");
      const rollNumberMenu = document.getElementById("rollNumberMenu");
      const rollNumberSelected = document.getElementById("rollNumberSelected");
      const rollNumberInput = document.getElementById("rollNumberInput");

      rollNumberButton.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        rollNumberMenu.classList.toggle("hidden");
      });

      rollNumberMenu.querySelectorAll("li").forEach(function (item) {
        item.addEventListener("click", function (e) {
          e.preventDefault();
          e.stopPropagation();
          const selectedValue = this.textContent.trim();
          rollNumberSelected.textContent = selectedValue;
          rollNumberInput.value = selectedValue;
          rollNumberMenu.classList.add("hidden");
        });
      });

      // Close dropdowns when clicking outside
      document.addEventListener("click", function (e) {
        if (
          !rollNumberButton.contains(e.target) &&
          !rollNumberMenu.contains(e.target)
        ) {
          rollNumberMenu.classList.add("hidden");
        }
      });
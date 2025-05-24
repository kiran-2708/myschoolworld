tailwind.config = {
        theme: {
          extend: {
            colors: {
              primary: {
                50: "#f0f9ff",
                100: "#e0f2fe",
                500: "#0ea5e9",
                600: "#0284c7",
                700: "#0369a1",
              },
              secondary: {
                50: "#f8fafc",
                100: "#f1f5f9",
                500: "#64748b",
                600: "#475569",
                700: "#334155",
              },
            },
          },
        },
      };

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
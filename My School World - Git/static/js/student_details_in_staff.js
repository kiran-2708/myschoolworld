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

      // Update Details functionality
      const updateDetailsBtn = document.getElementById("updateDetailsBtn");
      const form = document.getElementById("studentRegistrationForm");
      let isEditMode = false;

      updateDetailsBtn.addEventListener("click", function () {
        // Get all inputs except School ID and Staff ID
        const inputs = form.querySelectorAll(
          'input:not([name="schoolId"]):not([name="staffId"]), textarea, select'
        );

        if (!isEditMode) {
          // Enter edit mode
          inputs.forEach((input) => {
            // Enable all fields except School ID and Staff ID
            input.classList.remove("bg-gray-100", "cursor-not-allowed");
            input.classList.add("bg-white", "cursor-text");
            input.readOnly = false;
            if (input.tagName === "SELECT") {
              input.disabled = false;
            }
          });
          updateDetailsBtn.textContent = "Save Changes";
          updateDetailsBtn.classList.remove("from-blue-600", "to-purple-600");
          updateDetailsBtn.classList.add("from-green-600", "to-green-700");
          isEditMode = true;
        } else {
          // Save changes
          const formData = new FormData(form);
          const data = Object.fromEntries(formData.entries());

          // Show success message using SweetAlert
          Swal.fire({
            title: "Success!",
            text: "Details updated successfully!",
            icon: "success",
            confirmButtonText: "OK",
            confirmButtonColor: "#0ea5e9",
            timer: 2000,
            timerProgressBar: true,
          }).then(() => {
            // Exit edit mode
            inputs.forEach((input) => {
              input.classList.add("bg-gray-100", "cursor-not-allowed");
              input.classList.remove("bg-white", "cursor-text");
              input.readOnly = true;
              if (input.tagName === "SELECT") {
                input.disabled = true;
              }
            });
            updateDetailsBtn.textContent = "Update Details";
            updateDetailsBtn.classList.remove("from-green-600", "to-green-700");
            updateDetailsBtn.classList.add("from-blue-600", "to-purple-600");
            isEditMode = false;
          });
        }
      });

      // Add validation for specific fields
      const aadharInputs = form.querySelectorAll(
        'input[type="text"][pattern="[0-9]{12}"]'
      );
      aadharInputs.forEach((input) => {
        input.addEventListener("input", function (e) {
          if (this.value.length > 12) {
            this.value = this.value.slice(0, 12);
          }
        });
      });
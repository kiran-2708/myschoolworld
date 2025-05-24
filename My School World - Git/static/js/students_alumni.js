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

      // Download class details as Excel
      function downloadClassDetails() {
        // Get the table data
        const table = document.querySelector("table");
        if (!table) {
          alert("No table found!");
          return;
        }

        // Extract dynamic table rows
        const tableData = Array.from(table.querySelectorAll("tbody tr")).map((row) =>
          Array.from(row.cells).map((cell) => cell.textContent.trim())
        );

        // Static headers (unchanged)
        const headers = [
                      // Staff Basic Information
                      'Staff ID',
                      
                      // Student Basic Information
                      'Student Roll No',
                      'Student Name',
                      'Date of Birth',
                      'Blood Group',
                      'Gender',
                      'Standard',
                      
                      // Student Contact Information
                      'Student Aadhar Number',
                      'Student Email',
                      'Student Mobile Number',
                      'Resident Type',
                      'Date of Joining',
                      'Contact Email',
                      
                      // Father's Information
                      'Father\'s Name',
                      'Father\'s Aadhar Number',
                      'Father\'s Mobile Number',
                      
                      // Mother's Information
                      'Mother\'s Name',
                      'Mother\'s Aadhar Number',
                      'Mother\'s Mobile Number',
                      
                      // Guardian Information
                      'Guardian\'s Name',
                      'Guardian\'s Aadhar Number',
                      'Guardian\'s Mobile Number',
                      'Relationship with Student',
                      
                      // Address Information
                      'Address'
        ];

        // Static example row (unchanged)
        

        // Prepare final data array (headers + static + dynamic)
        const data = [headers, ...tableData];

        // Create workbook and worksheet
        const wb = XLSX.utils.book_new();
        const ws = XLSX.utils.aoa_to_sheet(data);

        // Add worksheet to workbook
        XLSX.utils.book_append_sheet(wb, ws, "Student Details");

        // Generate Excel file and trigger download
        XLSX.writeFile(wb, "student_details.xlsx");
      }



      document.addEventListener('DOMContentLoaded', function() {
    // Initialize all dropdowns
    document.querySelectorAll('.custom-standard-dropdown').forEach(dropdown => {
        const button = dropdown.querySelector('.dropdown-button');
        const menu = dropdown.querySelector('.dropdown-menu');
        const selectedOption = dropdown.querySelector('.selected-option');
        const input = dropdown.querySelector('.standard-input');

        // Toggle dropdown on button click
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            // Close all other dropdowns
            document.querySelectorAll('.dropdown-menu').forEach(otherMenu => {
                if (otherMenu !== menu) {
                    otherMenu.classList.add('hidden');
                }
            });
            menu.classList.toggle('hidden');
        });

        // Handle option selection
        menu.querySelectorAll('li').forEach(item => {
            item.addEventListener('click', function(e) {
                e.stopPropagation();
                selectedOption.textContent = this.textContent;
                input.value = this.textContent;
                menu.classList.add('hidden');

                // ✅ Submit the parent form
                const form = dropdown.closest('form');
                if (form) form.submit();
            });
        });
    });

    // ✅ Close dropdowns when clicking outside
    document.addEventListener("click", function () {
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            menu.classList.add('hidden');
        });
    });
});

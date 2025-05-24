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
              vibrant: {
                purple: "#8B5CF6",
                pink: "#EC4899",
                orange: "#F97316",
                green: "#10B981",
                blue: "#3B82F6",
              },
            },
          },
        },
      };

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
       
        const profileDropdown = document.getElementById('profileDropdown');
        const dropdownMenu = document.getElementById('dropdownMenu');
    
        profileDropdown.addEventListener('click', () => {
            dropdownMenu.classList.toggle('hidden');
        });
    
        // Close dropdown when clicking outside
        window.addEventListener('click', (e) => {
            if (!profileDropdown.contains(e.target)) {
                dropdownMenu.classList.add('hidden');
            }
        });

        // Standard Dropdown
        const standardDropdownButton = document.getElementById('standardDropdownButton');
        const standardDropdownMenu = document.getElementById('standardDropdownMenu');
        const standardSelectedOption = document.getElementById('standardSelectedOption');
        const standardInput = document.getElementById('standardInput');

        standardDropdownButton.addEventListener('click', function(e) {
            e.stopPropagation();
            standardDropdownMenu.classList.toggle('hidden');
        });

        standardDropdownMenu.querySelectorAll('li').forEach(function(item) {
            item.addEventListener('click', function() {
                standardSelectedOption.textContent = this.textContent;
                standardInput.value = this.textContent;
                standardDropdownMenu.classList.add('hidden');
            });
        });

        // Timetable Dropdown
        const timetableDropdownButton = document.getElementById('timetableDropdownButton');
        const timetableDropdownMenu = document.getElementById('timetableDropdownMenu');
        const timetableSelectedOption = document.getElementById('timetableSelectedOption');
        const timetableInput = document.getElementById('timetableInput');

        timetableDropdownButton.addEventListener('click', function(e) {
            e.stopPropagation();
            timetableDropdownMenu.classList.toggle('hidden');
        });

        timetableDropdownMenu.querySelectorAll('li').forEach(function(item) {
            item.addEventListener('click', function() {
                timetableSelectedOption.textContent = this.textContent;
                timetableInput.value = this.textContent;
                timetableDropdownMenu.classList.add('hidden');
            });
        });

        // Staff Dropdown
        const staffDropdownButton = document.getElementById('staffDropdownButton');
        const staffDropdownMenu = document.getElementById('staffDropdownMenu');
        const staffSelectedOption = document.getElementById('staffSelectedOption');
        const staffInput = document.getElementById('staffInput');

        staffDropdownButton.addEventListener('click', function(e) {
            e.stopPropagation();
            staffDropdownMenu.classList.toggle('hidden');
        });

        staffDropdownMenu.querySelectorAll('li').forEach(function(item) {
            item.addEventListener('click', function() {
                staffSelectedOption.textContent = this.textContent;
                staffInput.value = this.textContent;
                staffDropdownMenu.classList.add('hidden');
            });
        });

        // Close dropdowns when clicking outside
        window.addEventListener('click', function(e) {
            if (!standardDropdownButton.contains(e.target)) {
                standardDropdownMenu.classList.add('hidden');
            }
            if (!timetableDropdownButton.contains(e.target)) {
                timetableDropdownMenu.classList.add('hidden');
            }
            if (!staffDropdownButton.contains(e.target)) {
                staffDropdownMenu.classList.add('hidden');
            }
        });

        let fileToDelete = null;
        let deleteType = null;

        function deleteFile(type, filename) {
          fileToDelete = filename;
          deleteType = type;
          document.getElementById('deleteModal').classList.remove('hidden');
          document.getElementById('deleteModal').classList.add('flex');
        }

        function closeDeleteModal() {
          document.getElementById('deleteModal').classList.add('hidden');
          document.getElementById('deleteModal').classList.remove('flex');
          fileToDelete = null;
          deleteType = null;
        }

        function confirmDelete() {
          // Here you would typically make an API call to delete the file
          console.log(`Deleting ${deleteType} file: ${fileToDelete}`);
          
          // Remove the row from the table
          const rows = document.querySelectorAll('tr');
          rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            if (cells.length > 0) {
              const fileNameCell = cells[deleteType === 'student' ? 2 : 1];
              if (fileNameCell && fileNameCell.textContent === fileToDelete) {
                row.remove();
              }
            }
          });

          // Show success message
          alert('File deleted successfully!');
          
          // Close the modal
          closeDeleteModal();
        }

        // Close modal when clicking outside
        document.getElementById('deleteModal').addEventListener('click', function(e) {
          if (e.target === this) {
            closeDeleteModal();
          }
        });
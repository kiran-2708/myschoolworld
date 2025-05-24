 // Mobile Menu Toggle
      function toggleMenu(event) {
        if (event) {
          event.stopPropagation();
        }
        document.getElementById("mobileMenu").classList.toggle("hidden");
      }

      function closeMenu(event) {
        if (event) {
          event.stopPropagation();
        }
        document.getElementById("mobileMenu").classList.add("hidden");
      }

      // Close mobile menu when clicking outside
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

      // Profile Dropdown Toggle
      const profileDropdown = document.getElementById("profileDropdown");
      const dropdownMenu = document.getElementById("dropdownMenu");

      profileDropdown.addEventListener("click", () => {
        dropdownMenu.classList.toggle("hidden");
      });

      // Close profile dropdown when clicking outside
      window.addEventListener("click", (e) => {
        if (!profileDropdown.contains(e.target)) {
          dropdownMenu.classList.add("hidden");
        }
      });

      // Clock Functionality
      function updateClock() {
        const clockElement = document.getElementById('clock');
        const dateElement = document.getElementById('date');
        
        if (!clockElement || !dateElement) return;
        
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

        clockElement.textContent = timeString;
        dateElement.textContent = dateString;
      }

      function startClock() {
        updateClock(); // Initial clock update
        setInterval(updateClock, 1000);
      }

      // Function to handle roll number selection
      function selectRollNumber(rollNumber) {
          document.getElementById('rollNumberSelected').textContent = rollNumber;
          document.getElementById('rollNumberInput').value = rollNumber;
          document.getElementById('rollNumberMenu').classList.add('hidden');
          
          // Get form data
          const form = document.getElementById('resultsForm');
          const formData = new FormData(form);
          
          // Log form data for debugging
          console.log('Form values before submission:', {
              academic_year: formData.get('academic_year'),
              standard: formData.get('standard'),
              roll_number: formData.get('roll_number')
          });
          
          // Validate required fields
          if (!formData.get('academic_year') || !formData.get('standard') || !formData.get('roll_number')) {
              console.error('Missing required fields:', {
                  academic_year: formData.get('academic_year'),
                  standard: formData.get('standard'),
                  roll_number: formData.get('roll_number')
              });
              return;
          }
          
          // Show loading state
          const resultsContainer = document.querySelector('.max-w-5xl.mx-auto.bg-white.shadow-md.rounded-xl');
          if (!resultsContainer) {
              console.error('Results container not found');
              return;
          }
          
          resultsContainer.innerHTML = '<div class="text-center py-8"><div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div><p class="mt-4 text-gray-600">Loading results...</p></div>';
          
          // Submit using fetch
          fetch('/students_results_in_admin', {
              method: 'POST',
              body: formData
          })
          .then(response => {
              if (!response.ok) {
                  throw new Error('Network response was not ok');
              }
              return response.text();
          })
          .then(html => {
              // Create a temporary div to parse the HTML
              const tempDiv = document.createElement('div');
              tempDiv.innerHTML = html;
              
              // Extract the results container from the response
              const newResultsContainer = tempDiv.querySelector('.max-w-5xl.mx-auto.bg-white.shadow-md.rounded-xl');
              if (newResultsContainer) {
                  resultsContainer.innerHTML = newResultsContainer.innerHTML;
              } else {
                  resultsContainer.innerHTML = '<p class="text-center text-gray-600">No results found for the selected criteria.</p>';
              }
          })
          .catch(error => {
              console.error('Error fetching results:', error);
              resultsContainer.innerHTML = '<p class="text-center text-red-600">Error loading results. Please try again.</p>';
          });
      }

      // Function to reattach event listeners
      function attachEventListeners() {
          // Academic Year Dropdown
          const academicYearButton = document.getElementById('academicYearButton');
          const academicYearMenu = document.getElementById('academicYearMenu');
          
          if (academicYearButton) {
              academicYearButton.addEventListener('click', () => {
                  academicYearMenu.classList.toggle('hidden');
              });
          }

          // Close academic year dropdown when clicking outside
          document.addEventListener('click', (e) => {
              if (academicYearButton && academicYearMenu && 
                  !academicYearButton.contains(e.target) && 
                  !academicYearMenu.contains(e.target)) {
                  academicYearMenu.classList.add('hidden');
              }
          });

          // Standard Dropdown
          const standardButton = document.getElementById('standardButton');
          const standardMenu = document.getElementById('standardMenu');
          
          if (standardButton) {
              standardButton.addEventListener('click', () => {
                  standardMenu.classList.toggle('hidden');
              });
          }

          // Close standard dropdown when clicking outside
          document.addEventListener('click', (e) => {
              if (standardButton && standardMenu && 
                  !standardButton.contains(e.target) && 
                  !standardMenu.contains(e.target)) {
                  standardMenu.classList.add('hidden');
              }
          });

          // Roll Number Dropdown
          const rollNumberButton = document.getElementById('rollNumberButton');
          const rollNumberMenu = document.getElementById('rollNumberMenu');
          
          if (rollNumberButton) {
              rollNumberButton.addEventListener('click', () => {
                  rollNumberMenu.classList.toggle('hidden');
              });
          }

          // Close roll number dropdown when clicking outside
          document.addEventListener('click', (e) => {
              if (rollNumberButton && rollNumberMenu && 
                  !rollNumberButton.contains(e.target) && 
                  !rollNumberMenu.contains(e.target)) {
                  rollNumberMenu.classList.add('hidden');
              }
          });
      }

      // Function to handle standard selection
      function selectStandard(standard) {
          document.getElementById('standardSelected').textContent = standard;
          document.getElementById('standardInput').value = standard;
          document.getElementById('standardMenu').classList.add('hidden');
          
          // Show roll number dropdown
          document.getElementById('rollNumberContainer').classList.remove('hidden');
          
          // Get selected academic year
          const academicYear = document.getElementById('academicYearInput').value;
          
          // Fetch roll numbers
          fetch(`/get_roll_numbers/${academicYear}/${standard}`, {
              method: 'GET',
              headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json'
              }
          })
          .then(response => response.json())
          .then(rollNumbers => {
              const rollNumberMenu = document.getElementById('rollNumberMenu');
              rollNumberMenu.innerHTML = '';
              
              if (!rollNumbers || rollNumbers.length === 0) {
                  const li = document.createElement('li');
                  li.className = 'px-4 py-2 text-gray-500';
                  li.textContent = 'No roll numbers available';
                  rollNumberMenu.appendChild(li);
              } else {
                  rollNumbers.forEach(rollNumber => {
                      const li = document.createElement('li');
                      li.className = 'px-4 py-2 hover:bg-gray-100 cursor-pointer';
                      li.textContent = rollNumber;
                      li.onclick = () => selectRollNumber(rollNumber);
                      rollNumberMenu.appendChild(li);
                  });
              }
          })
          .catch(error => {
              console.error('Error fetching roll numbers:', error);
              const rollNumberMenu = document.getElementById('rollNumberMenu');
              rollNumberMenu.innerHTML = '<li class="px-4 py-2 text-red-500">Error loading roll numbers</li>';
          });
      }

      // Function to handle academic year selection
      function selectAcademicYear(year) {
          document.getElementById('academicYearSelected').textContent = year;
          document.getElementById('academicYearInput').value = year;
          document.getElementById('academicYearMenu').classList.add('hidden');
          
          // Show standard dropdown
          document.getElementById('standardContainer').classList.remove('hidden');
          
          // Reset and hide roll number dropdown
          document.getElementById('rollNumberContainer').classList.add('hidden');
          document.getElementById('rollNumberSelected').textContent = 'Select Roll Number';
          document.getElementById('rollNumberInput').value = '';
          
          // Fetch standards
          fetch(`/get_standards/${year}`, {
              method: 'GET',
              headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json'
              }
          })
          .then(response => response.json())
          .then(data => {
              const standardMenu = document.getElementById('standardMenu');
              standardMenu.innerHTML = '';
              
              if (!data || data.length === 0) {
                  const li = document.createElement('li');
                  li.className = 'px-4 py-2 text-gray-500';
                  li.textContent = 'No standards available for this academic year';
                  standardMenu.appendChild(li);
              } else {
                  data.forEach(standard => {
                      const li = document.createElement('li');
                      li.className = 'px-4 py-2 hover:bg-gray-100 cursor-pointer';
                      li.textContent = standard;
                      li.onclick = () => selectStandard(standard);
                      standardMenu.appendChild(li);
                  });
              }
          })
          .catch(error => {
              console.error('Error fetching standards:', error);
              const standardMenu = document.getElementById('standardMenu');
              standardMenu.innerHTML = '<li class="px-4 py-2 text-red-500">Error loading standards</li>';
          });
      }

      // Initial attachment of event listeners
      attachEventListeners();
      startClock();
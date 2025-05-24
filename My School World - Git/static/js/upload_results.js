tailwind.config = {
      theme: {
        extend: {
          colors: {
            primary: {
              50: '#f0f9ff',
              100: '#e0f2fe',
              500: '#0ea5e9',
              600: '#0284c7',
              700: '#0369a1',
            },
            secondary: {
              50: '#f8fafc',
              100: '#f1f5f9',
              500: '#64748b',
              600: '#475569',
              700: '#334155',
            }
          }
        }
      }
    }

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
 



  profileDropdown.addEventListener('click', () => {
      dropdownMenu.classList.toggle('hidden');
  });

  // Close dropdown when clicking outside
  window.addEventListener('click', (e) => {
      if (!profileDropdown.contains(e.target)) {
          dropdownMenu.classList.add('hidden');
      }
  });

    document.addEventListener('DOMContentLoaded', () => {
      const subjectsContainer = document.getElementById('subjectsContainer');
      const addSubjectButton = document.getElementById('addSubject');
      const totalDisplay = document.getElementById('totalMarksDisplay');
      const pctDisplay = document.getElementById('percentage');
      const form = document.getElementById('resultForm');
  
      // Set Academic Year
      const today = new Date();
      const y = today.getFullYear();
      document.getElementById('academicYear').textContent = (today.getMonth() < 5) ? `${y - 1}-${y}` : `${y}-${y + 1}`;
  
      // Grade Calculation
      function calculateGrade(percentage) {
          if (percentage >= 90 || percentage >= 90.00) return 'A+';
          if (percentage >= 80 || percentage >= 80.00) return 'A';
          if (percentage >= 70 || percentage >= 70.00) return 'B+';
          if (percentage >= 60 || percentage >= 60.00) return 'B';
          if (percentage >= 50 || percentage >= 50.00) return 'C';
          if (percentage >= 35 || percentage >= 35.00) return 'D';
          if (percentage < 35 || percentage < 35.00) return 'F';
      }
  
      // Calculate Total Marks, Percentage and Grade
      function updateCalculations() {
          const obtFields = subjectsContainer.querySelectorAll('.obtained-marks');
          const totFields = subjectsContainer.querySelectorAll('.total-marks');
          const gradeFields = subjectsContainer.querySelectorAll('.grade-input');
          let totalObtained = 0;
          let totalMarks = 0;
          let validSubjects = 0;
  
          obtFields.forEach((obtInput, index) => {
              const obtained = parseFloat(obtInput.value) || 0;
              const total = parseFloat(totFields[index].value) || 0;
  
              if (total > 0 && obtained >= 0) {
                  const subjectPercentage = (obtained / total) * 100;
                  gradeFields[index].value = calculateGrade(subjectPercentage);
                  totalObtained += obtained;
                  totalMarks += total;
                  validSubjects++;
              } else {
                  gradeFields[index].value = '';
              }
          });
  
          if (validSubjects > 0) {
            totalDisplay.value = `${totalObtained} / ${totalMarks}`;
            const overallPercentage = (totalObtained / totalMarks) * 100;
            const rawCgpa = overallPercentage / 9.5;
            const cgpa = Math.min(rawCgpa, 10).toFixed(2); // Cap CGPA at 10
            pctDisplay.value = `${overallPercentage.toFixed(2)}% / CGPA: ${cgpa}`;
        } else {
            totalDisplay.value = '0 / 0';
            pctDisplay.value = '0.00% / CGPA: 0.00';
        }

      }
  
      // Attach listeners to inputs
      function addInputListeners() {
          const inputs = subjectsContainer.querySelectorAll('.obtained-marks, .total-marks');
          inputs.forEach(input => {
              input.removeEventListener('input', updateCalculations); // Clean up
              input.addEventListener('input', () => {
                  const value = parseFloat(input.value);
                  if (value < 0) input.value = 0;
                  setTimeout(updateCalculations, 0);
              });
          });
      }
  
      // Initialize subject index based on existing rows
      let subjectIndex = subjectsContainer.querySelectorAll('tr').length;
  
      // Add new subject row
      addSubjectButton.addEventListener('click', () => {
          const row = document.createElement('tr');
          row.className = 'hover:bg-gray-50';
          row.innerHTML = `
              <td class="px-4 py-2">
                  <input type="date" name="date_${subjectIndex}" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:border-green-500 focus:outline-none" placeholder="Conducted Date" required />
              </td>
              <td class="px-4 py-2">
                  <input type="text" name="subject_name_${subjectIndex}" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:border-green-500 focus:outline-none" placeholder="Subject Name" required />
              </td>
              <td class="px-4 py-2">
                  <input type="number" name="obtained_${subjectIndex}" min="0" class="obtained-marks w-full border border-gray-300 rounded-md px-3 py-2 focus:border-green-500 focus:outline-none" placeholder="Obtained Marks" />
              </td>
              <td class="px-4 py-2">
                  <input type="number" name="total_${subjectIndex}" min="0" class="total-marks w-full border border-gray-300 rounded-md px-3 py-2 focus:border-green-500 focus:outline-none" placeholder="Subject Total" required />
              </td>
              <td class="px-4 py-2">
                  <input type="text" name="grade_${subjectIndex}" class="grade-input w-full border border-gray-300 cursor-not-allowed rounded-md px-3 py-2 bg-gray-50" placeholder="Grade" maxlength="2" readonly />
              </td>
              <td class="px-4 py-2">
                  <button type="button" class="text-red-500 hover:text-red-700 transition-colors" onclick="deleteRow(this)">
                      <i class="fas fa-trash-alt"></i>
                  </button>
              </td>
          `;
          subjectsContainer.appendChild(row);
          subjectIndex++;
          addInputListeners();
          updateCalculations();
      });
  
      // Delete subject row
      window.deleteRow = function (button) {
          const row = button.closest('tr');
          if (row) {
              row.remove();
              updateCalculations();
          }
      };
  
      // Submit form
      form.addEventListener('submit', (e) => {
          updateCalculations(); // Final calculation before submit
      });
  
      // Initial setup
      addInputListeners();
      updateCalculations();
  });


  const rollNumberButton = document.getElementById("rollNumberButton");
  const rollNumberMenu = document.getElementById("rollNumberMenu");
  const rollNumberSelected = document.getElementById("rollNumberSelected");
  const rollNumberInput = document.getElementById("rollNumberInput");

  // Toggle menu visibility
  rollNumberButton.addEventListener("click", function (e) {
    e.preventDefault();
    e.stopPropagation();
    rollNumberMenu.classList.toggle("hidden");
  });

  // Set selected value
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

  // Close menu when clicking outside
  document.addEventListener("click", function (e) {
    if (!rollNumberButton.contains(e.target) && !rollNumberMenu.contains(e.target)) {
      rollNumberMenu.classList.add("hidden");
    }
  });
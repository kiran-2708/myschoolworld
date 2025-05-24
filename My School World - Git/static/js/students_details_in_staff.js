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
       
        // Add real-time date and time
        function updateDateTime() {
            const now = new Date();
            const dateTimeString = now.toLocaleString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: true
            });
            document.getElementById('currentDateTime').textContent = dateTimeString;
        }

        // Update time every second
        setInterval(updateDateTime, 1000);
        // Initial call
        updateDateTime();


        // Excel download functionality
        function downloadExcel() {
            // Get table data
            const table = document.querySelector('table');
            const rows = Array.from(table.querySelectorAll('tbody tr'));
            
            // Prepare data for Excel with all details
            const excelData = rows.map(row => {
                const cells = Array.from(row.querySelectorAll('td'));
                const studentName = cells[1].querySelector('a').textContent.trim();
                
                return [
                
                    // School and Staff Information
                    cells[2].textContent.trim(), // School ID,
                    cells[3].textContent.trim(), // Staff ID,
                    
                    // Student Basic Information
                    cells[0].textContent.trim(), // Student Roll No
                    studentName, // Student Name
                    cells[4].textContent.trim(), // Date of Birth
                    cells[5].textContent.trim(), // Blood Group
                    cells[6].textContent.trim(), // Gender
                    cells[7].textContent.trim(), // Standard

                    // Student Contact Information
                    cells[8].textContent.trim(), // Student Aadhar Number
                    cells[9].textContent.trim(), // Student Email
                    cells[10].textContent.trim(), // Student Mobile Number
                    cells[11].textContent.trim(), // Resident Type
                    cells[12].textContent.trim(), // Date of Joining
                    cells[13].textContent.trim(), // Contact Email

                    cells[14].textContent.trim(), // Father's Name
                    cells[15].textContent.trim(), // Father's Aadhar Number
                    cells[16].textContent.trim(), // Father's Mobile Number

                    cells[17].textContent.trim(), // Mother's Name
                    cells[18].textContent.trim(), // Mother's Aadhar Number
                    cells[19].textContent.trim(), // Mother's Mobile Number

                    cells[20].textContent.trim(), // Guardian's Name  
                    cells[21].textContent.trim(), // Guardian's Aadhar Number
                    cells[22].textContent.trim(), // Guardian's Mobile Number
                    cells[23].textContent.trim(), // Relationship with Student

                    cells[24].textContent.trim() // Address
                    
                ];
            });

            // Add headers with sections
            const headers = [
                // School and Staff Information
                'School ID',
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
            excelData.unshift(headers);

            // Create worksheet
            const ws = XLSX.utils.aoa_to_sheet(excelData);

            // Set column widths
            const colWidths = [
                { wch: 10 }, // School ID
                { wch: 10 }, // Staff ID
                { wch: 15 }, // Student Roll No
                { wch: 20 }, // Student Name
                { wch: 15 }, // Date of Birth
                { wch: 12 }, // Blood Group
                { wch: 10 }, // Gender
                { wch: 10 }, // Standard
                { wch: 20 }, // Student Aadhar Number
                { wch: 25 }, // Student Email
                { wch: 20 }, // Student Mobile Number
                { wch: 15 }, // Resident Type
                { wch: 20 }, // Father's Name
                { wch: 20 }, // Father's Aadhar Number
                { wch: 20 }, // Father's Mobile Number
                { wch: 20 }, // Mother's Name
                { wch: 20 }, // Mother's Aadhar Number
                { wch: 20 }, // Mother's Mobile Number
                { wch: 20 }, // Guardian's Name
                { wch: 20 }, // Guardian's Aadhar Number
                { wch: 20 }, // Guardian's Mobile Number
                { wch: 25 }, // Relationship with Student
                { wch: 40 }  // Address
            ];
            ws['!cols'] = colWidths;

            // Add some styling to the headers
            const range = XLSX.utils.decode_range(ws['!ref']);
            for (let C = range.s.c; C <= range.e.c; ++C) {
                const cell = XLSX.utils.encode_cell({ r: 0, c: C });
                if (!ws[cell]) continue;
                ws[cell].s = {
                    font: { bold: true, color: { rgb: "FFFFFF" } },
                    fill: { fgColor: { rgb: "4472C4" } },
                    alignment: { horizontal: "center" }
                };
            }

            // Create workbook
            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, ws, "Student Details");

            // Generate current date and time for filename
            const currentDateTime = new Date().toLocaleString('en-US', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: false
            }).replace(/[/:, ]/g, '_');

            // Save the file
            XLSX.writeFile(wb, `student_details_${currentDateTime}.xlsx`);
        }

        // Remove the old event listener and modal code
        document.addEventListener('DOMContentLoaded', function() {
            const downloadButton = document.getElementById('downloadButton');
              if (downloadButton) {
                downloadButton.setAttribute('onclick', 'downloadExcel()');
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
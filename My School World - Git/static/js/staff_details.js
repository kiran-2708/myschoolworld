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

const profileDropdown = document.getElementById("profileDropdown");
const dropdownMenu = document.getElementById("dropdownMenu");
const updateModal = document.getElementById("updateModal");

// Function to show confirmation toast
function showConfirmationToast(message, onConfirm) {
  const toast = Toastify({
    text: message,
    duration: -1, // Don't auto-dismiss
    gravity: "top",
    position: "right",
    backgroundColor: "#4CAF50",
    style: {
      background: "linear-gradient(to right, #00b09b, #96c93d)",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      padding: "10px 20px",
    },
  }).showToast();

  // Create button container
  const buttonContainer = document.createElement("div");
  buttonContainer.style.cssText = `
            display: flex;
            gap: 10px;
            margin-left: 10px;
        `;

  // Add Yes button
  const yesButton = document.createElement("button");
  yesButton.textContent = "Yes";
  yesButton.style.cssText = `
            background: white;
            color: #00b09b;
            padding: 5px 15px;
            border-radius: 4px;
            cursor: pointer;
            border: none;
            font-weight: bold;
        `;
  yesButton.onclick = (e) => {
    e.stopPropagation();
    toast.hideToast();
    onConfirm(true);
  };

  // Add No button
  const noButton = document.createElement("button");
  noButton.textContent = "No";
  noButton.style.cssText = `
            background: white;
            color: #ff4444;
            padding: 5px 15px;
            border-radius: 4px;
            cursor: pointer;
            border: none;
            font-weight: bold;
        `;
  noButton.onclick = (e) => {
    e.stopPropagation();
    toast.hideToast();
    onConfirm(false);
  };

  // Add buttons to container
  buttonContainer.appendChild(yesButton);
  buttonContainer.appendChild(noButton);

  // Add container to toast
  const toastElement = document.querySelector(".toastify");
  toastElement.appendChild(buttonContainer);
}

profileDropdown.addEventListener("click", () => {
  dropdownMenu.classList.toggle("hidden");
});

// Close dropdown when clicking outside
window.addEventListener("click", (e) => {
  if (!profileDropdown.contains(e.target)) {
    dropdownMenu.classList.add("hidden");
  }
});

document.getElementById("deleteButton").addEventListener("click", function () {
  showConfirmationToast(
    "Are you sure you want to delete this staff record?",
    (confirmed) => {
      if (confirmed) {
        Toastify({
          text: "Staff record deleted successfully",
          duration: 3000,
          gravity: "top",
          position: "right",
          backgroundColor: "#4CAF50",
          style: {
            background: "linear-gradient(to right, #00b09b, #96c93d)",
          },
        }).showToast();
      }
    }
  );
});

function deleteStaff(button) {
  const row = button.closest("tr");
  const staffId = row.cells[0].textContent;
  const form = button.closest("form");

  showConfirmationToast(
    `Are you sure you want to delete staff ID ${staffId}?`,
    (confirmed) => {
      if (confirmed) {
        // Submit the form to call Flask backend
        form.submit();

        // Optionally show toast immediately (or move to Flask response)
        Toastify({
          text: `Deleting staff ID ${staffId}...`,
          duration: 3000,
          gravity: "top",
          position: "right",
          backgroundColor: "#4CAF50",
          style: {
            background: "linear-gradient(to right, #00b09b, #96c93d)",
          },
        }).showToast();
      }
    }
  );
}

function openUpdateModal(button) {
  const row = button.closest("tr");
  const cells = row.cells;

  document.getElementById("updateSchoolId").value =
    cells[0].getAttribute("data-school-id") || ""; // Add if data attr is used
  document.getElementById("updateStaffId").value = cells[1].textContent;
  document.getElementById("updateStaffName").value = cells[2].textContent;
  document.getElementById("updateQualification").value = cells[3].textContent;
  document.getElementById("updateDoj").value = cells[4].textContent;
  document.getElementById("updateEmail").value = cells[5].textContent;
  document.getElementById("updateMobile").value = cells[6].textContent;
  document.getElementById("updateAadhar").value = cells[7].textContent;
  document.getElementById("updateGender").value = cells[8].textContent;

  updateModal.classList.remove("hidden");
}
function closeUpdateModal() {
  updateModal.classList.add("hidden");
}

function saveUpdate() {
  const staffId = document.getElementById("updateStaffId").value;
  const form = document.getElementById("updateForm");
  const formData = new FormData(form);
  const updateButton = document.querySelector('button[onclick="saveUpdate()"]');

  // Disable the button to prevent multiple clicks
  updateButton.disabled = true;
  updateButton.innerText = "Updating...";

  fetch(`/update_staff/${staffId}`, {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.redirected) {
        // Show toast first, then redirect
        Toastify({
          text: "Data updated successfully",
          duration: 2000,
          gravity: "top",
          position: "right",
          style: {
            background: "linear-gradient(to right, #00b09b, #96c93d)",
          },
        }).showToast();

        setTimeout(() => {
          window.location.href = response.url;
        }, 1500);
      } else if (response.ok) {
        Toastify({
          text: "Data updated successfully",
          duration: 3000,
          gravity: "top",
          position: "right",
          style: {
            background: "linear-gradient(to right, #00b09b, #96c93d)",
          },
        }).showToast();
        closeUpdateModal();
      } else {
        return response.text().then((text) => {
          console.error("Update failed:", text);
          alert("Failed to update staff details.");
        });
      }
    })
    .catch((error) => {
      console.error("Error during update:", error);
      alert("An unexpected error occurred.");
    })
    .finally(() => {
      // Re-enable the button
      updateButton.disabled = false;
      updateButton.innerHTML = '<i class="fas fa-save mr-2"></i>Update';
    });
}

// Close modal when clicking outside
window.addEventListener("click", (e) => {
  if (e.target === updateModal) {
    closeUpdateModal();
  }
});

// Function to show staff details in popup
function showStaffDetails(button) {
  // Read values from data attributes
  const dataset = button.dataset;

  document.getElementById("detailSchoolId").textContent =
    dataset.schoolId || "";
  document.getElementById("detailStaffId").textContent = dataset.staffId || "";
  document.getElementById("detailStaffName").textContent = dataset.name || "";
  document.getElementById("detailStandard").textContent =
    dataset.standard || "";
  document.getElementById("detailAadhar").textContent = dataset.aadhar || "";
  document.getElementById("detailQualification").textContent =
    dataset.qualification || "";
  document.getElementById("detailDoj").textContent = dataset.doj || "";
  document.getElementById("detailEmail").textContent = dataset.email || "";
  document.getElementById("detailMobile").textContent = dataset.mobile || "";
  document.getElementById("detailGender").textContent = dataset.gender || "";

  // Show modal
  document.getElementById("staffDetailsModal").classList.remove("hidden");
}

function closeStaffDetailsModal() {
  document.getElementById("staffDetailsModal").classList.add("hidden");
}

function openUpdateModalFromDetails() {
  // Get values from the details modal
  const schoolId = document.getElementById("detailSchoolId").textContent;
  const staffId = document.getElementById("detailStaffId").textContent;
  const staffName = document.getElementById("detailStaffName").textContent;
  const standard = document.getElementById("detailStandard").textContent;
  const aadhar = document.getElementById("detailAadhar").textContent;
  const qualification = document.getElementById("detailQualification").textContent;
  const doj = document.getElementById("detailDoj").textContent;
  const email = document.getElementById("detailEmail").textContent;
  const mobile = document.getElementById("detailMobile").textContent;
  const gender = document.getElementById("detailGender").textContent;

  // Set values in the update modal
  document.getElementById("updateSchoolId").value = schoolId;
  document.getElementById("updateStaffId").value = staffId;
  document.getElementById("updateStaffName").value = staffName;
  document.getElementById("detailStandard").value = standard;
  document.getElementById("updateAadhar").value = aadhar;
  document.getElementById("updateQualification").value = qualification;
  document.getElementById("updateDoj").value = doj;
  document.getElementById("updateEmail").value = email;
  document.getElementById("updateMobile").value = mobile;
  document.getElementById("updateGender").value = gender;

  // Set the standard value in the select dropdown
  const updateStandard = document.getElementById("updateStandard");
  updateStandard.value = standard;

  // Close the details modal and open the update modal
  closeStaffDetailsModal();
  document.getElementById("updateModal").classList.remove("hidden");
}

// Update the PDF download function
function downloadPDF() {
  const container = document.createElement("div");
  container.style.padding = "20px";

  // Header
  const header = document.createElement("div");
  header.style.textAlign = "center";
  header.style.marginBottom = "30px";

  // // LOGO
  // const logo = document.createElement('div');
  // logo.innerHTML = `
  //     <svg class="w-12 h-12 mx-auto text-yellow-400" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  //         <path d="M12 3L1 9L12 15L21 10.09V17H23V9M5 13.18V17.18L12 21L19 17.18V13.18L12 17L5 13.18Z" fill="currentColor"/>
  //     </svg>`;
  // header.appendChild(logo);

  const schoolName = document.createElement("h1");
  schoolName.textContent = "Greenwood High School";
  schoolName.style.fontSize = "24px";
  schoolName.style.fontWeight = "bold";
  schoolName.style.color = "#333";
  schoolName.style.marginTop = "10px";
  header.appendChild(schoolName);

  const subtitle = document.createElement("p");
  subtitle.textContent = "Staff Details Report";
  subtitle.style.fontSize = "16px";
  subtitle.style.color = "#666";
  subtitle.style.marginTop = "5px";
  header.appendChild(subtitle);

  container.appendChild(header);

  // Date
  const dateDiv = document.createElement("div");
  dateDiv.style.textAlign = "right";
  dateDiv.style.marginBottom = "20px";
  dateDiv.style.color = "#666";
  dateDiv.textContent = "Generated on: " + new Date().toLocaleDateString();
  container.appendChild(dateDiv);

  // Table
  const table = document.createElement("table");
  table.style.width = "100%";
  table.style.borderCollapse = "collapse";
  table.style.marginTop = "20px";
  table.style.fontSize = "12px";

  const headers = [
    "Staff ID",
    "Staff Name",
    "Standard",
    "Staff Aadhar",
    "Qualification",
    "Date of Joining",
    "Staff Email",
    "Staff Mobile Number",
    "Gender",
  ];
  const headerRow = document.createElement("tr");
  headers.forEach((headerText) => {
    const th = document.createElement("th");
    th.textContent = headerText;
    th.style.border = "1px solid #ddd";
    th.style.padding = "12px 8px";
    th.style.backgroundColor = "#f5f5f5";
    th.style.textAlign = "left";
    th.style.fontWeight = "bold";
    th.style.color = "#333";
    headerRow.appendChild(th);
  });
  table.appendChild(headerRow);

  // Extract data from HTML table
  const tableRows = document.querySelectorAll("#staffTable tbody tr");

  tableRows.forEach((row) => {
    const cells = row.querySelectorAll("td");
    const staffId = cells[0].innerText.trim();
    const button = cells[1].querySelector("button");

    const name = button.dataset.name || "";
    const standard = button.dataset.standard || "";
    const aadhar = button.dataset.aadhar || "";
    const qualification = button.dataset.qualification || "";
    const doj = button.dataset.doj || "";
    const email = button.dataset.email || "";
    const mobile = button.dataset.mobile || "";
    const gender = button.dataset.gender || "";

    const data = [
      staffId,
      name,
      standard,
      aadhar,
      qualification,
      doj,
      email,
      mobile,
      gender,
    ];

    const dataRow = document.createElement("tr");
    data.forEach((item) => {
      const td = document.createElement("td");
      td.textContent = item;
      td.style.border = "1px solid #ddd";
      td.style.padding = "12px 8px";
      td.style.textAlign = "left";
      dataRow.appendChild(td);
    });
    table.appendChild(dataRow);
  });

  container.appendChild(table);

  // Footer
  const footer = document.createElement("div");
  footer.style.marginTop = "30px";
  footer.style.textAlign = "center";
  footer.style.color = "#666";
  footer.style.fontSize = "12px";
  footer.innerHTML = "This is a computer-generated document.";
  container.appendChild(footer);

  // Generate PDF
  const opt = {
    margin: [0.5, 0.5, 0.5, 0.5],
    filename: "staff_details.pdf",
    image: { type: "jpeg", quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: "in", format: "letter", orientation: "landscape" },
  };

  html2pdf().set(opt).from(container).save();
}

// Close staff details modal when clicking outside
window.addEventListener("click", (e) => {
  const modal = document.getElementById("staffDetailsModal");
  if (e.target === modal) {
    closeStaffDetailsModal();
  }
});

// Dropdown logic - only once
(function () {
  document.addEventListener("DOMContentLoaded", function () {
    const dropdownButton = document.getElementById("dropdownButton");
    const dropdownMenu = document.getElementById("dropdownMenu");
    const selectedOption = document.getElementById("selectedOption");
    const updateStandard = document.getElementById("updateStandard");

    // Function to set selected standard
    function setSelectedStandard(standard) {
      selectedOption.textContent = standard;
      updateStandard.value = standard;
    }

    // Initialize dropdown click handlers
    dropdownButton.addEventListener("click", function (e) {
      e.stopPropagation();
      dropdownMenu.classList.toggle("hidden");
    });

    // Handle option selection
    dropdownMenu.addEventListener("click", function (e) {
      if (e.target.tagName === "LI") {
        setSelectedStandard(e.target.textContent);
        dropdownMenu.classList.add("hidden");
      }
    });

    // Close dropdown when clicking outside
    document.addEventListener("click", function (e) {
      if (
        !dropdownButton.contains(e.target) &&
        !dropdownMenu.contains(e.target)
      ) {
        dropdownMenu.classList.add("hidden");
      }
    });

    // Make setSelectedStandard available globally
    window.setSelectedStandard = setSelectedStandard;
  });
})();
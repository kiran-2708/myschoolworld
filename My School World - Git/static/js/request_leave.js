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


  function getMinDate() {
    const now = new Date();
    // If current time is 00:00:00, move to next day
    if (now.getHours() === 0 && now.getMinutes() === 0 && now.getSeconds() === 0) {
      now.setDate(now.getDate() + 1);
    }
    return now.toISOString().split('T')[0];
  }

  const minDate = getMinDate();
  document.getElementById('startDate').min = minDate;
  document.getElementById('endDate').min = minDate;




  document.querySelectorAll(".action-btn").forEach((button) => {
    button.addEventListener("click", function () {
      const row = this.closest("tr");
      const actionContainer = row.querySelector(".action-container");
      const newStatus = this.getAttribute("data-status");

      // Create status text element
      const statusText = document.createElement("span");
      statusText.className =
        newStatus === "Approved"
          ? "bg-green-500 text-white px-3 py-1 rounded text-xs sm:text-sm"
          : "bg-red-500 text-white px-3 py-1 rounded text-xs sm:text-sm";
      statusText.textContent = newStatus;

      // Clear container and add status text
      actionContainer.innerHTML = "";
      actionContainer.appendChild(statusText);

      // Show toast notification instead of alert
      Toastify({
        text: `Leave request has been ${newStatus.toLowerCase()}`,
        duration: 3000,
        gravity: "top",
        position: "right",
        backgroundColor: newStatus === "Approved" ? "#22c55e" : "#ef4444",
        stopOnFocus: true,
      }).showToast();
    },1000);
  });



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

  window.addEventListener("click", (e) => {
    if (!profileDropdown.contains(e.target)) {
      dropdownMenu.classList.add("hidden");
    }
  });

  // Form submission handler
  function handleSubmit(event) {
    event.preventDefault();

    const form = document.getElementById("leaveRequestForm");
    const formData = {
      staffId: document.getElementById("staffId").value,
      staffName: document.getElementById("staffName").value,
      startDate: document.getElementById("startDate").value,
      endDate: document.getElementById("endDate").value,
      leaveType: document.getElementById("leaveType").value,
    };

    if (
      !formData.staffId ||
      !formData.staffName ||
      !formData.startDate ||
      !formData.endDate ||
      !formData.leaveType
    ) {
      Toastify({
        text: "Please fill in all required fields",
        duration: 3000,
        gravity: "top",
        position: "right",
        style: {
          background: "linear-gradient(to right, #ff5f6d, #ffc371)",
        },
      }).showToast();
      return;
    }

    const start = new Date(formData.startDate);
    const end = new Date(formData.endDate);

    if (end < start) {
      Toastify({
        text: "End date cannot be before start date",
        duration: 3000,
        gravity: "top",
        position: "right",
        style: {
          background: "linear-gradient(to right, #ff5f6d, #ffc371)",
        },
      }).showToast();
      return;
    }

    const confirmToast = Toastify({
      text: "Are you sure you want to submit this leave request?",
      duration: -1,
      gravity: "top",
      position: "center",
      style: {
        background: "linear-gradient(to right, #4a90e2, #67b26f)",
        padding: "16px",
        borderRadius: "8px",
        boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
        minWidth: "300px",
      },
      onClick: function () {
        confirmToast.hideToast();
      },
    });

    confirmToast.showToast();

    const toastElement = document.querySelector(".toastify");
    const buttonContainer = document.createElement("div");
    buttonContainer.className = "flex gap-4 justify-center mt-4";

    const confirmButton = document.createElement("button");
    confirmButton.className =
      "px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition-colors";
    confirmButton.textContent = "Confirm";
    confirmButton.onclick = function () {
      confirmToast.hideToast();
      form.submit(); // SUBMIT FORM TO BACKEND
    };

    const cancelButton = document.createElement("button");
    cancelButton.className =
      "px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors";
    cancelButton.textContent = "Cancel";
    cancelButton.onclick = function () {
      confirmToast.hideToast();
      Toastify({
        text: "Leave request cancelled",
        duration: 2000,
        gravity: "top",
        position: "right",
        style: {
          background: "linear-gradient(to right, #ff5f6d, #ffc371)",
        },
      }).showToast();
    };

    buttonContainer.appendChild(confirmButton);
    buttonContainer.appendChild(cancelButton);
    toastElement.appendChild(buttonContainer);
  }
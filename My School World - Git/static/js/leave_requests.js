// Tailwind config
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
      },
      fontFamily: {
        times: ['"Times New Roman"', 'serif'],
      },
    }
  }
};

// Toggle mobile menu
function toggleMenu(event) {
  if (event) event.stopPropagation();
  document.getElementById("mobileMenu").classList.toggle("hidden");
}

function closeMenu(event) {
  if (event) event.stopPropagation();
  document.getElementById("mobileMenu").classList.add("hidden");
}

document.addEventListener('DOMContentLoaded', function () {
  // === Profile Dropdown ===
  const profileDropdown = document.getElementById("profileDropdown");
  const dropdownMenu = document.getElementById("dropdownMenu");

  if (profileDropdown) {
    profileDropdown.addEventListener("click", () => {
      dropdownMenu.classList.toggle("hidden");
    });

    window.addEventListener("click", (e) => {
      if (!profileDropdown.contains(e.target)) {
        dropdownMenu.classList.add("hidden");
      }
    });
  }

  // === Custom Staff Dropdown ===
  const customStaffBtn = document.getElementById('staffDropdownButton');
  const customStaffMenu = document.getElementById('staffDropdownMenu');
  const selectedStaffOption = document.getElementById('selectedStaffOption');
  const staffInput = document.getElementById('staffInput');
  const parentForm = customStaffBtn ? customStaffBtn.closest('form') : null;

  if (customStaffBtn && customStaffMenu && selectedStaffOption && staffInput) {
    customStaffBtn.addEventListener('click', () => {
      customStaffMenu.classList.toggle('hidden');
    });

    customStaffMenu.querySelectorAll('li').forEach(item => {
      item.addEventListener('click', () => {
        const value = item.getAttribute('data-value');
        selectedStaffOption.textContent = value;
        staffInput.value = value;
        customStaffMenu.classList.add('hidden');
        if (parentForm) parentForm.submit();
      });
    });

    document.addEventListener('click', (e) => {
      if (!customStaffBtn.contains(e.target) && !customStaffMenu.contains(e.target)) {
        customStaffMenu.classList.add('hidden');
      }
    });
  }

  // === Leave Approval Buttons
  document.querySelectorAll('.action-btn').forEach(button => {
    button.addEventListener('click', function () {
      const newStatus = this.getAttribute('data-status');
      const leaveId = this.getAttribute('data-leave-id');

      const formData = new FormData();
      formData.append('leave_id', leaveId);
      formData.append('status', newStatus);

      // === 1. Show "Updating..." toast
      Toastify({
        text: "Updating leave request...",
        duration: 3000,
        gravity: "top",
        position: "right",
        backgroundColor: "#facc15",
        stopOnFocus: false
      }).showToast();

      // === 2. Immediately make the request
      fetch('/update_leave_status', {
        method: 'POST',
        body: formData
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to update');
        }

        // === 3. Show second toast immediately
        Toastify({
          text: `Leave request has been ${newStatus.toLowerCase()}`,
          duration: 3000,
          gravity: "top",
          position: "right",
          backgroundColor: newStatus === "Approved" ? "#22c55e" : "#ef4444",
          stopOnFocus: false
        }).showToast();

        // === 4. Reload after second toast duration
        setTimeout(() => {
          window.location.reload(true);
        }, 3000);
      })
      .catch(error => {
        console.error('Error:', error);
        Toastify({
          text: "An error occurred while updating.",
          duration: 3000,
          gravity: "top",
          position: "right",
          backgroundColor: "#ef4444",
          stopOnFocus: true
        }).showToast();
      });
    });
  });

  // === Search auto-submit
  const searchForm = document.getElementById('searchForm');
  const searchStaffId = document.getElementById('searchStaffId');
  if (searchForm && searchStaffId) {
    searchStaffId.addEventListener('change', function () {
      searchForm.submit();
    });
  }
});

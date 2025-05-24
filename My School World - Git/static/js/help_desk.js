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

  document.addEventListener("DOMContentLoaded", () => {
    const profileDropdown = document.getElementById("profileDropdown");
    const dropdownMenu = document.getElementById("dropdownMenu");
    const resolveModal = document.getElementById("resolveModal");
    const closeModal = document.getElementById("closeModal");
    const modalName = document.getElementById("modalName");
    const modalEmail = document.getElementById("modalEmail");
    const modalMessage = document.getElementById("modalMessage");
    const responseText = document.getElementById("responseText");

    // Toggle profile dropdown
    profileDropdown?.addEventListener("click", () => {
      dropdownMenu.classList.toggle("hidden");
    });

    // Hide dropdown if clicked outside
    window.addEventListener("click", (e) => {
      if (!profileDropdown.contains(e.target) && !dropdownMenu.contains(e.target)) {
        dropdownMenu.classList.add("hidden");
      }
    });

    // Handle "Resolve" button clicks
    document.querySelectorAll("button").forEach((button) => {
      if (button.textContent.trim() === "Resolve") {
        button.addEventListener("click", (e) => {
          const row = e.target.closest("tr");
          const name = row.cells[0].textContent.trim();
          const email = row.cells[1].textContent.trim();
          const message = row.cells[3].textContent.trim();
          const issueId = row.getAttribute("data-issue-id");

          // Fill modal fields
          modalName.textContent = name;
          modalEmail.textContent = email;
          modalMessage.textContent = message;
          responseText.value = "";

          // Set form action dynamically
          resolveModal.action = `/resolve_issue/${issueId}`;

          // Show modal
          resolveModal.classList.remove("hidden");
          resolveModal.classList.add("flex");
        });
      }
    });

    // Close modal on button click
    closeModal?.addEventListener("click", () => {
      resolveModal.classList.add("hidden");
      resolveModal.classList.remove("flex");
    });

    // Prevent submission if no response is entered
    document.getElementById("resolveIssue")?.addEventListener("click", (e) => {
      if (!responseText.value.trim()) {
        e.preventDefault();
        Toastify({
          text: "Please write a response before resolving the issue.",
          duration: 3000,
          gravity: "top",
          position: "right",
          backgroundColor: "linear-gradient(to right, #ff416c, #ff4b2b)",
          stopOnFocus: true,
        }).showToast();
      }
    });

    // Close modal if clicking outside the modal box
    window.addEventListener("click", (e) => {
      if (e.target === resolveModal) {
        resolveModal.classList.add("hidden");
        resolveModal.classList.remove("flex");
      }
    });
  });
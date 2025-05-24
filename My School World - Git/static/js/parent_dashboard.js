// Navigation items in order
const navItems = [
  { name: "Child Info", url: "/child_info" },
  { name: "Child Results", url: "/child_results" },
  { name: "Time Tables", url: "/child_time_tables" },
  { name: "Help Desk", url: "/parents_help_desk" },
  { name: "Complaints Raised", url: "/raised_complaints" },
  { name: "Study Materials", url: "/child_materials" },
  { name: "Question Papers", url: "/child_question_papers" },
];

let currentIndex = 0;
const contentFrame = document.getElementById("contentFrame");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");

// Set initial state
function initializeNavigation() {
  // Set initial page to Student Info
  currentIndex = 0;
  contentFrame.src = "https://png.pngtree.com/background/20210709/original/pngtree-school-season-welcome-new-students-blackboard-hand-painted-picture-image_923676.jpg;"
  updateNavigationButtons();
}

function updateNavigationButtons() {
  prevBtn.disabled = currentIndex === 0;
  nextBtn.disabled = currentIndex === navItems.length - 1;
}

function loadContent(index) {
  currentIndex = index;
  contentFrame.src = navItems[index].url;
  updateNavigationButtons();

  // Enable scrolling on the iframe
  contentFrame.onload = function () {
    try {
      const iframeDoc = contentFrame.contentWindow.document;
      iframeDoc.body.style.overflow = "auto";
      iframeDoc.documentElement.style.overflow = "auto";
      iframeDoc.body.style.height = "auto";
      iframeDoc.documentElement.style.height = "auto";
    } catch (e) {
      console.log("Could not access iframe content");
    }
  };
}

prevBtn.addEventListener("click", () => {
  if (currentIndex > 0) {
    loadContent(currentIndex - 1);
  }
});

nextBtn.addEventListener("click", () => {
  if (currentIndex < navItems.length - 1) {
    loadContent(currentIndex + 1);
  }
});

// Handle sidebar and mobile navigation
function handleNavigation(menuItem) {
  const index = navItems.findIndex((item) => item.name === menuItem);
  if (index !== -1) {
    loadContent(index);
  }
  // Close mobile menu if open
  document.getElementById("mobileMenu").classList.add("hidden");
}

// Add click handlers to all navigation links
document.querySelectorAll(".nav-link, #mobileMenu nav a").forEach((link) => {
  link.addEventListener("click", (e) => {
    const span = e.currentTarget.querySelector("span");
    const menuItem = span ? span.textContent.trim() : "";

    if (menuItem === "Logout") {
      // Let the browser handle it — do not prevent default
      return;
    }

    e.preventDefault();
    handleNavigation(menuItem);
  });
});
// Existing menu toggle functions
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

// Close menu when clicking outside
document.addEventListener("click", function (event) {
  const mobileMenu = document.getElementById("mobileMenu");
  const menuButton = document.querySelector('button[onclick="toggleMenu()"]');

  if (
    !menuButton.contains(event.target) &&
    !mobileMenu.contains(event.target)
  ) {
    mobileMenu.classList.add("hidden");
  }
});

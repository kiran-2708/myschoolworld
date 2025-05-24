const navItems = [
  { name: "Student Info", url: "/student_info" },
  { name: "Results", url: "/student_results" },
  { name: "Time Table", url: "/student_time_tables" },
  { name: "Study Materials", url: "/materials" },
  { name: "Question Papers", url: "/question_papers" },
];

const contentFrame = document.getElementById("contentFrame");
const mobileMenu = document.getElementById("mobileMenu");

function initializeNavigation() {
  contentFrame.src = "https://png.pngtree.com/background/20210709/original/pngtree-school-season-welcome-new-students-blackboard-hand-painted-picture-image_923676.jpg";
}

function handleMenuClick(menuItem) {
  const item = navItems.find((item) => item.name === menuItem);
  if (item) {
    contentFrame.src = item.url;
    mobileMenu.classList.add("hidden");
  }
}

document.querySelectorAll(".nav-item").forEach((item) => {
  item.addEventListener("click", (e) => {
    e.preventDefault();
    handleMenuClick(item.getAttribute("data-menu"));
  });
});

function toggleMenu() {
  mobileMenu.classList.toggle("hidden");
}

document.addEventListener("click", function (e) {
  const menuBtn = document.querySelector('button[onclick="toggleMenu()"]');
  if (!menuBtn.contains(e.target) && !mobileMenu.contains(e.target)) {
    mobileMenu.classList.add("hidden");
  }
});

// Initialize on load
initializeNavigation();

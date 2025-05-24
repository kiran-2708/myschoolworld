    function togglePassword() {
  const passwordField = document.getElementById("password");
  const toggleIcon = document.querySelector(".toggle-password");
  if (passwordField.type === "password") {
    passwordField.type = "text";
    toggleIcon.textContent = "🙈";
  } else {
    passwordField.type = "password";
    toggleIcon.textContent = "👁️";
  }
}

document.getElementById("loginForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const regNumber = document.getElementById("regNumber").value.trim();
  const standard = document.getElementById("standard").value;
  const password = document.getElementById("password").value.trim();
  const errorMessage = document.getElementById("error-message");

  if (!regNumber || !standard || !password) {
    errorMessage.textContent = "Please fill in all fields.";
    return;
  }

  // Dummy login check
  if (regNumber === "ABC123" && standard === "Grade 3" && password === "parent123") {
    alert("Login successful! Redirecting to dashboard...");
    errorMessage.textContent = "";
    // window.location.href = "/dashboard.html"; // Optional redirect
  } else {
    errorMessage.textContent = "Invalid credentials. Please try again.";
  }
});
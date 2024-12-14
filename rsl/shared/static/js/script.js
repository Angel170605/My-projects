const darkMode = () => {
  document.querySelector("body").setAttribute("data-bs-theme", "dark");
  localStorage.setItem("theme", "dark");
};

const lightMode = () => {
  document.querySelector("body").setAttribute("data-bs-theme", "light");
  localStorage.setItem("theme", "light");
};

const changeTheme = () => {
  const currentTheme = document.querySelector("body").getAttribute("data-bs-theme");
  if (currentTheme === "light") {
      darkMode();
  } else {
      lightMode();
  }
};

document.addEventListener("DOMContentLoaded", () => {
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme) {
      if (savedTheme === "dark") {
          darkMode();
      } else {
          lightMode();
      }
  }
});
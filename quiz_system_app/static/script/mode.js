const body = document.body;
    const toggleBtn = document.getElementById("modeToggle");

    if (localStorage.getItem("mode") === "dark") {
      body.classList.replace("bg-light", "bg-dark");
      body.classList.replace("text-dark", "text-light");
      toggleBtn.textContent = "☀️ Light Mode";
    }

    toggleBtn.addEventListener("click", () => {
      if (body.classList.contains("bg-light")) {
        body.classList.replace("bg-light", "bg-dark");
        body.classList.replace("text-dark", "text-light");
        toggleBtn.textContent = "☀️ Light Mode";
        localStorage.setItem("mode", "dark");
      } else {
        body.classList.replace("bg-dark", "bg-light");
        body.classList.replace("text-light", "text-dark");
        toggleBtn.textContent = "🌙 Dark Mode";
        localStorage.setItem("mode", "light");
      }
    });
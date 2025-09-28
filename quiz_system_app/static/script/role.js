document.getElementById("role").addEventListener("change", function () {
    let selected = this.value;
    if (selected === "admin") {
      console.log("Role = Teacher → Saved as 'admin'");
    } else if (selected === "student") {
      console.log("Role = Student → Saved as 'student'");
    }
  });
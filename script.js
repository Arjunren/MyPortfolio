document.addEventListener("DOMContentLoaded", function () {
  const sendButton = document.getElementById("Send");
  const fullNameInput = document.getElementById("Fname");
  const emailInput = document.getElementById("Ename");
  const descriptionInput = document.getElementById("Description");

  sendButton.addEventListener("click", function (event) {
    event.preventDefault();

    const fullName = fullNameInput.value.trim();
    const email = emailInput.value.trim();
    const description = descriptionInput.value.trim();

    if (!fullName || !email || !description) {
      alert("All fields are required. Please fill in all the details.");
      return;
    }

    if (description.length < 20 || description.length > 300) {
      alert("Description must be between 20 and 300 characters.");
      return;
    }

    const formData = {
      fullName: fullName,
      email: email,
      description: description,
    };

    fetch("https://arjunrenvon.pythonanywhere.com/send-inquiry", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message === "Inquiry sent successfully!") {
          alert("Your inquiry was sent successfully!");
          fullNameInput.value = "";
          emailInput.value = "";
          descriptionInput.value = "";
        } else {
          alert(
            data.message ||
              "There was an error sending your inquiry. Please try again."
          );
        }
      })
      .catch((error) => {
        alert("An error occurred: " + error);
      });
  });
  ("use strict")

});

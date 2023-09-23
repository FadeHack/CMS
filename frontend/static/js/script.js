// Add JavaScript code as needed for your frontend interactions

// Example: Display a confirmation dialog
document.querySelector("#delete-button").addEventListener("click", function () {
    if (confirm("Are you sure you want to delete this item?")) {
        // Perform the delete action
    } else {
        // Do nothing or handle cancel
    }
});

// Example: Fetch data from an API and update the page
fetch("/api/data")
    .then(response => response.json())
    .then(data => {
        // Update the page with the fetched data
    })
    .catch(error => {
        console.error("Error fetching data:", error);
    });

    // Get references to the sign-in and sign-up buttons
    const signInButton = document.getElementById('signIn');
    const signUpButton = document.getElementById('signUp');

    // Get references to the form containers
    const signInContainer = document.querySelector('.sign-in-container');
    const signUpContainer = document.querySelector('.sign-up-container');

    // Add event listeners to the buttons
    signInButton.addEventListener('click', () => {
        signInContainer.style.transform = 'translateX(0)';
        signUpContainer.style.transform = 'translateX(100%)';
    });

    signUpButton.addEventListener('click', () => {
        signInContainer.style.transform = 'translateX(-100%)';
        signUpContainer.style.transform = 'translateX(0)';
    });


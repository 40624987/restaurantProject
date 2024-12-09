//validation.js

document.addEventListener('DOMContentLoaded', function () {
    const reservationForm = document.getElementById('reservation-form');

    reservationForm.addEventListener('submit', function (event) {
        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const date = document.getElementById('date').value;
        const time = document.getElementById('time').value;
        const guests = document.getElementById('guests').value;

        const errors = [];

		// Clear previous error messages
        document.querySelectorAll('.error-message').forEach(error => error.textContent = '');

        // Validate name (only letters and spaces)
        const namePattern = /^[a-zA-Z\s]+$/;
        if (!namePattern.test(name)) {
             document.getElementById('name-error').textContent = "Name should only contain letters and spaces.";
            errors.push("name");
        }

        // Validate email
        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!emailPattern.test(email)) {
             document.getElementById('email-error').textContent = "Please enter a valid email address.";
            errors.push("email");
        }

        // Validate date
        const selectedDate = new Date(date);
        const today = new Date();
        today.setHours(0, 0, 0, 0); // Ensure time is ignored in date comparison
        const maxDate = new Date();
        maxDate.setMonth(today.getMonth() + 3); // Three months into the future

        if (isNaN(selectedDate.getTime())) {
            document.getElementById('date-error').textContent = "Please select a valid date.";
            errors.push("date");
        } else if (selectedDate < today) {
            document.getElementById('date-error').textContent = "Date cannot be in the past.";
            errors.push("date");
        } else if (selectedDate > maxDate) {
            document.getElementById('date-error').textContent = "Date cannot be more than three months from today.";
            errors.push("date");
        }

        // Validate time (3:00 PM to 10:00 PM)
        const timePattern = /^([0-9]{2}):([0-9]{2})$/;
        const [hours, minutes] = timePattern.test(time)
            ? time.split(":").map((t) => parseInt(t, 10))
            : [-1, -1];

        if (hours < 15 || hours > 22 || (hours === 22 && minutes > 0)) {
            document.getElementById('time-error').textContent = "Time must be between 3:00 PM and 10:00 PM.";
            errors.push("time");
        }

        // Validate guests
        if (isNaN(guests) || guests <= 0) {
            document.getElementById('guests-error').textContent = "Please enter a valid number of guests.";
            errors.push("guests");
        }

        // If there are errors, prevent form submission and show them
        if (errors.length > 0) {
            event.preventDefault();

        }
    });
});

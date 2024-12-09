//scripts.js
let currentSlide = 0;
const slides = document.querySelectorAll('.image-slide');
const totalSlides = slides.length;

function showSlide(index) {
    // Hide all slides
    slides.forEach(slide => slide.style.display = 'none');

    // Show the current slide
    slides[index].style.display = 'block';
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    showSlide(currentSlide);
}

function prevSlide() {
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    showSlide(currentSlide);
}

// Initialize the slideshow
showSlide(currentSlide);

// Change slides every 3 seconds
setInterval(nextSlide, 3000);

// Add event listeners to navigation buttons
document.querySelector('.prev').addEventListener('click', prevSlide);
document.querySelector('.next').addEventListener('click', nextSlide);

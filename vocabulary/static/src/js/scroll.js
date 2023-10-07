// Smooth scroll to the target position with an offset
function scrollToPosition(targetOffset) {
  window.scrollTo({
    top: targetOffset - 90, // Adjust the offset as needed
    behavior: "smooth", // Enable smooth scrolling
  });
}

// Handle click event on the letter link
var letterLinks = document.querySelectorAll(".letter-link");
letterLinks.forEach(function (link) {
  link.addEventListener("click", function (e) {
    e.preventDefault();
    var targetId = link.getAttribute("href"); 
    var targetOffset = document.querySelector(targetId).offsetTop; 
    scrollToPosition(targetOffset);
  });
});

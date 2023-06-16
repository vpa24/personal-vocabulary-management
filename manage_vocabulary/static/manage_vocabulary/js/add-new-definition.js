document.addEventListener("DOMContentLoaded", function () {
  // Handle click event on "Add other definition" button
  var addButton = document.getElementById("add_other_definition");
  addButton.addEventListener("click", function () {
    // Select the target div to clone
    var targetDiv = document.querySelector(
      ".row.mt-3.p-4.bg-secondary.rounded"
    );

    if (targetDiv) {
      // Clone the target div with its content
      var clonedDiv = targetDiv.cloneNode(true);

      // Clear any user input values in the cloned div
      var clonedInputs = clonedDiv.querySelectorAll("input, textarea");
      clonedInputs.forEach(function (input) {
        input.value = "";
      });

      // Append the cloned div after the last occurrence of the target div
      targetDiv.parentNode.appendChild(clonedDiv);
    }
  });
});

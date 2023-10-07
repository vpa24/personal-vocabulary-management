document.addEventListener("DOMContentLoaded", function () {
  var addButton = document.querySelector("#add_other_definition");
  if (addButton) {
    addButton.addEventListener("click", function () {
      // Select the target div to clone
      var targetDiv = document.querySelectorAll(".clone_div");
      var last = targetDiv[targetDiv.length - 1];

      if (last) {
        // Clone the target div with its content
        var clonedDiv = last.cloneNode(true);

        // Clear any user input values in the cloned div
        var clonedInputs = clonedDiv.querySelectorAll("input, textarea");
        var selectElement = clonedDiv.querySelector("select");
        selectElement.selectedIndex = 0;
        clonedInputs.forEach(function (input) {
          input.value = "";
        });
        last.parentElement.append(clonedDiv);
      }
    });
  }
});

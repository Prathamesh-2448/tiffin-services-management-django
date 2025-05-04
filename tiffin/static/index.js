//document.addEventListener("DOMContentLoaded", function () {
//    // Select all checkboxes inside the container
//    const checkboxes = document.querySelectorAll(".container_checks input[type='checkbox']");
//
//    checkboxes.forEach((checkbox) => {
//        const checkboxId = checkbox.id;
//        const index = checkboxId.replace("checkbox", ""); // Extract the number
//        const spinbox = document.getElementById(`spinbox${index}`);
//
//        if (!spinbox) return; // Ensure elements exist
//
//        // Handle checkbox change event
//        checkbox.addEventListener("change", function () {
//            if (this.checked) {
//                spinbox.style.display = "inline";
//            } else {
//                spinbox.style.display = "none";
//            }
//        });
//    });
//});

document.addEventListener("DOMContentLoaded", function () {
    const checkboxes = document.querySelectorAll(".container_checks input[type='checkbox']");

    checkboxes.forEach((checkbox) => {
        const checkboxId = checkbox.id;
        const index = checkboxId.replace("checkbox", ""); // Extract the number
        const spinbox = document.getElementById(`spinbox${index}`);

        if (!spinbox) return; // Ensure elements exist

        // Handle checkbox change event
        checkbox.addEventListener("change", function () {
            if (this.checked) {
                spinbox.style.display = "inline";  // Show quantity input
            } else {
                spinbox.style.display = "none";  // Hide quantity input
            }
        });
    });

    // Ensure only selected extras with quantities are sent
    document.getElementById("form").addEventListener("submit", function () {
        const selectedExtras = [];  // To store selected extras
        const selectedQuantities = [];  // To store quantities for selected extras

        // Loop through all checkboxes
        document.querySelectorAll(".container_checks input[type='checkbox']").forEach((checkbox) => {
            if (checkbox.checked) {
                const extraValue = checkbox.value;
                const quantityInput = document.getElementById(`spinbox${checkbox.id.replace("checkbox", "")}`);

                selectedExtras.push(extraValue);  // Store selected extras in order
                selectedQuantities.push(quantityInput.value);  // Store corresponding quantities
            }
        });

        // Create hidden inputs to store selected extras and quantities
        let hiddenExtrasInput = document.createElement("input");
        hiddenExtrasInput.type = "hidden";
        hiddenExtrasInput.name = "ordered_extras";  // Name to be accessed in Django view
        hiddenExtrasInput.value = selectedExtras.join(",");  // Convert array to comma-separated string
        this.appendChild(hiddenExtrasInput);

        let hiddenQuantitiesInput = document.createElement("input");
        hiddenQuantitiesInput.type = "hidden";
        hiddenQuantitiesInput.name = "ordered_quantities";  // Name to be accessed in Django view
        hiddenQuantitiesInput.value = selectedQuantities.join(",");  // Convert array to comma-separated string
        this.appendChild(hiddenQuantitiesInput);
    });
});















function previewOrder() {
    // Get the selected customer name
    let name = document.getElementById("nameInput").value;
    document.getElementById("modalCustomerName").innerText = name;

    // Get the selected meal date
    let mealDate = document.getElementById("mealdate").value;

    // Check if meal date is empty
    if (!mealDate) {
        alert("Please select a meal date before proceeding!");
        return; // Stop execution if no date is selected
    }
    document.getElementById("modalMealDate").innerText = mealDate;

    // Get the selected meal
    let mealSelected = document.querySelector("select[name='meal_selected']").value;
    document.getElementById("modalMeal").innerText = mealSelected;

    // Get the selected extras and their quantities
    let extrasList = document.getElementById("modalExtras");
    extrasList.innerHTML = ""; // Clear only the display, not the form inputs

    let checkboxes = document.querySelectorAll("input[name='extras_taken']:checked");

    checkboxes.forEach(checkbox => {
        let quantityInput = checkbox.closest(".checkbox-wrapper").querySelector("input[name='extras_quantity']");

        // Only read values, don't change them
        let quantity = quantityInput && quantityInput.value.trim() !== "" ? quantityInput.value : "0";

        if (quantity > 0) {
            let listItem = document.createElement("li");
            listItem.textContent = `${checkbox.value} (Qty: ${quantity})`;
            extrasList.appendChild(listItem);
        }
    });

    // Open the modal programmatically (only if validation passes)
    let modal = new bootstrap.Modal(document.getElementById("exampleModal"));
    modal.show();
}

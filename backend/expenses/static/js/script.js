document.getElementById("expense-form").addEventListener("submit", function(event) {
    if (!document.getElementById("name").value || !document.getElementById("amount").value) {
        alert("All fields are required!");
        event.preventDefault(); // Prevent submission only if fields are empty
    }
});

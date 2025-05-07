let totalCost = 0;
const buildComponents = {};

function addComponent(type, name, price) {
    if (!buildComponents[type]) {
        buildComponents[type] = { name, price };
        totalCost += price;
        updateTotalCost();
    } else {
        alert(`${type} is already added.`);
    }
}

function updateTotalCost() {
    document.getElementById("total-cost").innerText = totalCost;
}

function checkCompatibility() {
    // Add compatibility logic, for example:
    // If CPU and Motherboard are selected, check for socket compatibility.
    // If RAM is selected, check for RAM type compatibility with Motherboard.
    alert("Compatibility check is in progress.");
}

// pc_builder.js

// Sample data for components
const componentData = {
    processor: {
        "AMD Ryzen 9 7950X": { price: 700, image: "2.jpg", details: "16-core, 32-thread processor" },
        "Intel i9-12900K": { price: 600, image:  "1.jpg", details: "16-core, 24-thread processor" },
    },
    motherboard: {
        "MSI MAG X670E": { price: 300, image: "msi_x670e.jpg", details: "Supports AMD processors" },
        "ASUS ROG Strix B550-F": { price: 200, image: "asus_b550.jpg", details: "Supports AMD processors" },
        "ASUS TUF Z690": { price: 250, image: "asus_z690.jpg", details: "Supports Intel processors" },
        "MSI MPG Z590": { price: 220, image: "msi_z590.jpg", details: "Supports Intel processors" },
    },
    gpu: {
        "NVIDIA RTX 3080": { price: 800, image: "nvidia_rtx_3080.jpg", details: "High performance graphics card" },
        "AMD Radeon RX 6800": { price: 700, image: "amd_rx_6800.jpg", details: "Great for gaming" },
    },
    ram: {
        "Corsair Vengeance 16GB": { price: 80, image: "corsair_16gb.jpg", details: "DDR4 3200MHz" },
        "G.Skill Ripjaws 32GB": { price: 150, image: "gskill_32gb.jpg", details: "DDR4 3200MHz" },
    },
    ssd: {
        "Samsung 970 EVO 1TB": { price: 100, image: "samsung_970_evo.jpg", details: "Fast NVMe SSD" },
        "WD Blue 500GB": { price: 50, image: "wd_blue.jpg", details: "Reliable SATA SSD" },
    },
    psu: {
        "Corsair RM750x": { price: 120, image: "corsair_rm750x.jpg", details: "750W Power Supply" },
        "EVGA 650 GQ": { price: 90, image: "evga_650gq.jpg", details: "650W Power Supply" },
    }
};

// Total cost variable
let totalCost = 0;

// Function to filter motherboards based on selected processor
function filterMotherboards() {
    const processorSelect = document.getElementById("processor-select");
    const motherboardSelect = document.getElementById("motherboard-select");
    const selectedProcessor = processorSelect.value;

    // Clear current motherboard options
    motherboardSelect.innerHTML = '<option value="">Select Motherboard</option>';

    // Populate motherboard options based on selected processor
    for (const option of motherboardSelect.options) {
        const cpuType = option.getAttribute("data-cpu");
        if (selectedProcessor && cpuType && selectedProcessor.includes(cpuType)) {
            motherboardSelect.appendChild(option.cloneNode(true));
        }
    }
}

// Function to add selected component to the build list
function addComponent(componentType) {
    const selectElement = document.getElementById(`${componentType}-select`);
    const selectedComponent = selectElement.value;

    if (selectedComponent && componentData[componentType][selectedComponent]) {
        const componentDetails = componentData[componentType][selectedComponent];
        const buildList = document.getElementById("build-list");
        const row = document.createElement("tr");

        // Add component details to the row
        row.innerHTML = `
            <td>${componentType.charAt(0).toUpperCase() + componentType.slice(1)}</td>
            <td><img src="{% static 'images/${componentDetails.image}' %}" alt="${selectedComponent}" width="50"></td>
            <td>${selectedComponent}</td>
            <td>${componentDetails.details}</td>
            <td>$${componentDetails.price}</td>
            <td><a href="#">Link</a></td>
            <td><button onclick="removeComponent(this, ${componentDetails.price})">Remove</button></td>
        `;

        buildList.appendChild(row);
        totalCost += componentDetails.price;
        updateTotalCost();
    }
}

// Function to remove component from the build list
function removeComponent(button, price) {
    const row = button.parentElement.parentElement;
    row.remove();
    totalCost -= price;
    updateTotalCost();
}

// Function to update total cost display
function updateTotalCost() {
    const totalCostElement = document.getElementById("total-cost");
    totalCostElement.innerText = `Total Cost: $${totalCost}`;
}

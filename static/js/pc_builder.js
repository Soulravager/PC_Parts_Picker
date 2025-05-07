let totalCost = 0;
let budget = 1000; // Default budget

// Function to update the budget and filter items
function updateBudget(newBudget) {
    budget = newBudget;
    document.getElementById('budget-value').textContent = budget;
    filterComponents();
}

// Function to filter components based on budget
function filterComponents() {
    const components = document.querySelectorAll('.component');
    components.forEach(component => {
        const buttons = component.querySelectorAll('button');
        buttons.forEach(button => {
            const cost = parseInt(button.textContent.match(/\$(\d+)/)[1]);
            button.disabled = cost > budget; // Disable button if cost exceeds budget
        });
    });
}

// Function to toggle CPU options based on selection
function toggleCpuOptions() {
    const selectedCpu = document.querySelector('input[name="cpu-type"]:checked');
    const cpuOptions = document.getElementById('cpu-options');
    const intelSelect = document.getElementById('intel-cpu');
    const amdSelect = document.getElementById('amd-cpu');

    if (selectedCpu) {
        cpuOptions.style.display = 'block';
        intelSelect.style.display = selectedCpu.value === 'Intel' ? 'block' : 'none';
        amdSelect.style.display = selectedCpu.value === 'AMD' ? 'block' : 'none';
    } else {
        cpuOptions.style.display = 'none';
    }
}

// Function to add selected GPU
function addSelectedGpu() {
    const gpuSelect = document.getElementById('gpu-select');
    const gpuCost = parseInt(gpuSelect.value);
    const gpuName = gpuSelect.options[gpuSelect.selectedIndex].text;

    addComponent('GPU', gpuCost, gpuName);
}

// Function to add a component from a button click
function addComponent(type, cost, name) {
    const buildList = document.getElementById('build-list');
    const totalCostElement = document.getElementById('total-cost');

    // Create a list item
    const listItem = document.createElement('li');
    listItem.textContent = `${name}: $${cost}`;
    
    // Create a remove button
    const removeButton = document.createElement('button');
    removeButton.textContent = 'Remove';
    removeButton.onclick = function() {
        totalCost -= cost;
        totalCostElement.textContent = `Total Cost: $${totalCost}`;
        buildList.removeChild(listItem);
        filterComponents(); // Re-filter components after removal
    };

    // Append remove button to the list item
    listItem.appendChild(removeButton);
    buildList.appendChild(listItem);

    // Update total cost
    totalCost += cost;
    totalCostElement.textContent = `Total Cost: $${totalCost}`;
    filterComponents(); // Re-filter components after addition
}

// Function to add a selected component from a dropdown
function addSelectedComponent(type) {
    let selectElement;
    let cost, name;

    if (type === 'RAM') {
        selectElement = document.getElementById('ram-select');
    } else if (type === 'Motherboard') {
        selectElement = document.getElementById('motherboard-select');
    }

    // Get selected option
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    cost = parseInt(selectedOption.value);
    name = selectedOption.text;

    addComponent(type, cost, name); // Use a placeholder image for RAM and Motherboard
}

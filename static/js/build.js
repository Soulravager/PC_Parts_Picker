let totalPrice = 0;

function openModal(componentType) {
    document.getElementById(`modal-${componentType}`).style.display = 'flex';
}

function closeModal(componentType) {
    document.getElementById(`modal-${componentType}`).style.display = 'none';
}

function selectComponent(type, id, name, price) {
    // Display selected component
    document.getElementById(`${type}-selected`).innerText = `${name} - ₹${price}`;
    
    // Update total price
    totalPrice += price;
    document.getElementById('total-price').innerText = totalPrice;
    
    // Close the modal
    closeModal(type);
}

function addToCart() {
    alert("Added to cart!");
}

function removeAll() {
    totalPrice = 0;
    document.getElementById('total-price').innerText = totalPrice;
    
    // Clear selected components
    document.getElementById('cpu-selected').innerText = '';
    document.getElementById('motherboard-selected').innerText = '';
    document.getElementById('ram-selected').innerText = '';
}

function printBuild() {
    var printContent = document.getElementById('build-form').innerHTML;
    var printWindow = window.open('', '', 'height=600, width=800');
    printWindow.document.write('<html><head><title>Print Build</title></head><body>');
    printWindow.document.write(printContent);
    printWindow.document.write('</body></html>');
    printWindow.document.close();
    printWindow.print();
}
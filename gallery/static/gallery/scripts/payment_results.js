window.addEventListener('DOMContentLoaded', function() {
    fetch('/get_payment_details') // Replace with the appropriate URL to fetch the payment details from the server
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            // Populate the HTML elements with the payment details
            document.getElementById('amount').textContent = data.amount;
            document.getElementById('receipt-number').textContent = data.receiptNumber;
            document.getElementById('transaction-date').textContent = data.transactionDate;
            document.getElementById('phone-number').textContent = data.phoneNumber;
        })
        .catch(function(error) {
            console.error('Error fetching payment details:', error);
        });
});
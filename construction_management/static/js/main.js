// Main JavaScript file for the Construction Management System

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('input-error');
            
            // Create error message if it doesn't exist
            if (!field.nextElementSibling?.classList.contains('error-message')) {
                const errorMsg = document.createElement('p');
                errorMsg.className = 'error-message';
                errorMsg.textContent = 'This field is required';
                field.parentNode.insertBefore(errorMsg, field.nextSibling);
            }
        } else {
            field.classList.remove('input-error');
            const errorMsg = field.nextElementSibling;
            if (errorMsg?.classList.contains('error-message')) {
                errorMsg.remove();
            }
        }
    });

    return isValid;
}

// Dynamic table filtering
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    if (!input || !table) return;

    input.addEventListener('keyup', function() {
        const filter = input.value.toLowerCase();
        const rows = table.getElementsByTagName('tr');

        for (let i = 1; i < rows.length; i++) {
            const row = rows[i];
            const cells = row.getElementsByTagName('td');
            let found = false;

            for (let j = 0; j < cells.length; j++) {
                const cell = cells[j];
                if (cell) {
                    const text = cell.textContent || cell.innerText;
                    if (text.toLowerCase().indexOf(filter) > -1) {
                        found = true;
                        break;
                    }
                }
            }

            row.style.display = found ? '' : 'none';
        }
    });
}

// Date range picker initialization
function initializeDateRangePicker(startId, endId) {
    const startDate = document.getElementById(startId);
    const endDate = document.getElementById(endId);
    if (!startDate || !endDate) return;

    startDate.addEventListener('change', function() {
        endDate.min = startDate.value;
    });

    endDate.addEventListener('change', function() {
        startDate.max = endDate.value;
    });
}

// Confirmation dialog
function confirmAction(message) {
    return confirm(message || 'Are you sure you want to perform this action?');
}

// Toast notifications
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `fixed bottom-4 right-4 px-4 py-2 rounded-lg shadow-lg ${
        type === 'success' ? 'bg-green-500' :
        type === 'error' ? 'bg-red-500' :
        type === 'warning' ? 'bg-yellow-500' :
        'bg-blue-500'
    } text-white`;
    toast.textContent = message;

    document.body.appendChild(toast);
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Initialize all interactive elements
document.addEventListener('DOMContentLoaded', function() {
    // Initialize form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form.id)) {
                e.preventDefault();
            }
        });
    });

    // Initialize table filters
    const searchInputs = document.querySelectorAll('[id$="-search"]');
    searchInputs.forEach(input => {
        const tableId = input.getAttribute('data-table');
        if (tableId) {
            filterTable(input.id, tableId);
        }
    });

    // Initialize date range pickers
    const dateRangePickers = document.querySelectorAll('[id$="-date-range"]');
    dateRangePickers.forEach(picker => {
        const startId = picker.getAttribute('data-start');
        const endId = picker.getAttribute('data-end');
        if (startId && endId) {
            initializeDateRangePicker(startId, endId);
        }
    });

    // Initialize delete confirmations
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirmAction(this.getAttribute('data-confirm'))) {
                e.preventDefault();
            }
        });
    });
});

// Export functions for use in other scripts
window.CMS = {
    validateForm,
    filterTable,
    initializeDateRangePicker,
    confirmAction,
    showToast
};

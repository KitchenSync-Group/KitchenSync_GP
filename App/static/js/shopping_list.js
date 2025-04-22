/**
 * KitchenSync - Shopping List JavaScript
 * Handles shopping list item management and interaction
 */

document.addEventListener('DOMContentLoaded', function() {
    // Edit item modal functionality
    const editItemButtons = document.querySelectorAll('.edit-item');
    const editItemForm = document.getElementById('edit-item-form');
    const editNameInput = document.getElementById('edit-name');
    const editQuantityInput = document.getElementById('edit-quantity');
    const editUnitInput = document.getElementById('edit-unit');
    const saveItemBtn = document.getElementById('save-item-btn');
    
    // Set up edit item modal
    editItemButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.id;
            const itemName = this.dataset.name;
            const itemQuantity = this.dataset.quantity;
            const itemUnit = this.dataset.unit;
            
            // Set form action for the update
            editItemForm.action = `/shopping-list/update/${itemId}`;
            
            // Populate form fields
            editNameInput.value = itemName;
            editQuantityInput.value = itemQuantity;
            editUnitInput.value = itemUnit;
            
            // Show the modal
            const modal = new bootstrap.Modal(document.getElementById('editItemModal'));
            modal.show();
        });
    });
    
    // Handle save button click in the edit modal
    if (saveItemBtn) {
        saveItemBtn.addEventListener('click', function() {
            // Submit the form
            editItemForm.submit();
        });
    }
    
    // Checkbox functionality for marking items as purchased
    const itemCheckboxes = document.querySelectorAll('.item-checkbox');
    const markSelectedBtn = document.getElementById('mark-selected-btn');
    const selectAllBtn = document.getElementById('select-all-btn');
    
    // Enable/disable the "Mark Selected as Purchased" button based on checkbox state
    if (itemCheckboxes.length && markSelectedBtn) {
        // Function to update button state
        function updateMarkSelectedBtn() {
            const checkedCount = document.querySelectorAll('.item-checkbox:checked').length;
            markSelectedBtn.disabled = checkedCount === 0;
            markSelectedBtn.textContent = `Mark ${checkedCount} Item${checkedCount !== 1 ? 's' : ''} as Purchased`;
        }
        
        // Add event listeners to checkboxes
        itemCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', updateMarkSelectedBtn);
        });
        
        // Initialize button state
        updateMarkSelectedBtn();
        
        // Handle "Mark Selected as Purchased" button click
        markSelectedBtn.addEventListener('click', function() {
            const checkedItems = document.querySelectorAll('.item-checkbox:checked');
            if (checkedItems.length === 0) return;
            
            const itemIds = Array.from(checkedItems).map(checkbox => checkbox.value);
            
            // Mark items as purchased using AJAX
            Promise.all(itemIds.map(itemId => {
                return fetch(`/shopping-list/toggle/${itemId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: new URLSearchParams({
                        'purchased': 'true'
                    })
                }).then(response => response.json());
            }))
            .then(results => {
                // Reload the page to show the updated list
                window.location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
        });
        
        // Select All button functionality
        if (selectAllBtn) {
            selectAllBtn.addEventListener('click', function() {
                const allChecked = document.querySelectorAll('.item-checkbox:checked').length === itemCheckboxes.length;
                
                itemCheckboxes.forEach(checkbox => {
                    checkbox.checked = !allChecked;
                });
                
                updateMarkSelectedBtn();
                
                // Update button text
                this.textContent = allChecked ? 'Select All' : 'Deselect All';
            });
        }
    }
    
    // Add Item Form Validation
    const addItemForm = document.getElementById('add-item-form');
    if (addItemForm) {
        addItemForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Validate name field
            const nameInput = document.querySelector('#add-item-form input[name="name"]');
            if (!nameInput.value.trim()) {
                nameInput.classList.add('is-invalid');
                isValid = false;
            } else {
                nameInput.classList.remove('is-invalid');
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
    
    // Drop zones for draggable recipe ingredients
    const shoppingListDropZone = document.querySelector('.shopping-list-drop-zone');
    if (shoppingListDropZone) {
        shoppingListDropZone.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('drag-over');
        });
        
        shoppingListDropZone.addEventListener('dragleave', function() {
            this.classList.remove('drag-over');
        });
        
        shoppingListDropZone.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('drag-over');
            
            try {
                const data = JSON.parse(e.dataTransfer.getData('text/plain'));
                
                if (data.type === 'ingredient') {
                    // Add ingredient to shopping list via AJAX
                    fetch('/shopping-list/add', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'X-Requested-With': 'XMLHttpRequest'
                        },
                        body: new URLSearchParams({
                            'name': data.name,
                            'quantity': data.quantity || 1,
                            'unit': data.unit || ''
                        })
                    })
                    .then(response => {
                        if (response.ok) {
                            // Reload the page to show the new item
                            window.location.reload();
                        }
                    });
                }
            } catch (error) {
                console.error('Error parsing drag data:', error);
            }
        });
    }
});
/**
 * KitchenSync - Pantry Management JavaScript
 * Handles interaction with the pantry page
 */

document.addEventListener('DOMContentLoaded', function() {
    // Edit Item Modal Functionality
    const editItemButtons = document.querySelectorAll('.edit-item');
    const editItemForm = document.getElementById('edit-item-form');
    const editNameInput = document.getElementById('edit-name');
    const editQuantityInput = document.getElementById('edit-quantity');
    const editUnitInput = document.getElementById('edit-unit');
    const editCategorySelect = document.getElementById('edit-category');
    const saveItemBtn = document.getElementById('save-item-btn');
    
    // Show edit modal when edit button is clicked
    editItemButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.id;
            const itemName = this.dataset.name;
            const itemQuantity = this.dataset.quantity;
            const itemUnit = this.dataset.unit;
            const itemCategory = this.dataset.category;
            
            // Set form action for the update
            editItemForm.action = `/pantry/update/${itemId}`;
            
            // Populate form fields
            editNameInput.value = itemName;
            editQuantityInput.value = itemQuantity;
            editUnitInput.value = itemUnit;
            
            // Set the correct category in the dropdown
            for (let i = 0; i < editCategorySelect.options.length; i++) {
                if (editCategorySelect.options[i].value === itemCategory) {
                    editCategorySelect.selectedIndex = i;
                    break;
                }
            }
            
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
    
    // Add Ingredient Form Validation
    const addIngredientForm = document.getElementById('add-ingredient-form');
    if (addIngredientForm) {
        addIngredientForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Validate name field
            const nameInput = document.querySelector('#add-ingredient-form input[name="name"]');
            if (!nameInput.value.trim()) {
                nameInput.classList.add('is-invalid');
                isValid = false;
            } else {
                nameInput.classList.remove('is-invalid');
            }
            
            // Validate quantity field
            const quantityInput = document.querySelector('#add-ingredient-form input[name="quantity"]');
            if (!quantityInput.value.trim() || isNaN(parseFloat(quantityInput.value))) {
                quantityInput.classList.add('is-invalid');
                isValid = false;
            } else {
                quantityInput.classList.remove('is-invalid');
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
    
    // Category tabs functionality
    const categoryTabs = document.getElementById('categoryTabs');
    if (categoryTabs) {
        // Check if there's a stored active tab
        const activeTab = localStorage.getItem('activePantryTab');
        if (activeTab) {
            // Try to activate the tab
            const tab = document.querySelector(`#categoryTabs button[data-bs-target="${activeTab}"]`);
            if (tab) {
                new bootstrap.Tab(tab).show();
            }
        }
        
        // Store the active tab when it changes
        categoryTabs.addEventListener('shown.bs.tab', function(event) {
            const targetId = event.target.getAttribute('data-bs-target');
            localStorage.setItem('activePantryTab', targetId);
        });
    }
    
    // Add drag-and-drop for pantry items (e.g., to shopping list or meal plan)
    const pantryItems = document.querySelectorAll('.pantry-item');
    if (pantryItems.length) {
        pantryItems.forEach(item => {
            item.setAttribute('draggable', 'true');
            
            item.addEventListener('dragstart', function(e) {
                e.dataTransfer.setData('text/plain', JSON.stringify({
                    id: this.dataset.id,
                    name: this.dataset.name,
                    quantity: this.dataset.quantity,
                    unit: this.dataset.unit,
                    type: 'pantry-item'
                }));
            });
        });
    }
    
    // Quick add ingredients from search/suggestion
    const quickAddButtons = document.querySelectorAll('.quick-add-ingredient');
    if (quickAddButtons.length) {
        quickAddButtons.forEach(button => {
            button.addEventListener('click', function() {
                const ingredientName = this.dataset.name;
                const nameInput = document.querySelector('#add-ingredient-form input[name="name"]');
                
                if (nameInput) {
                    nameInput.value = ingredientName;
                    nameInput.focus();
                    
                    // Scroll to the add form
                    addIngredientForm.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    }
});
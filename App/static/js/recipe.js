/**
 * KitchenSync - Recipe Management JavaScript
 * Handles recipe search, filtering, and recipe details interaction
 */

document.addEventListener('DOMContentLoaded', function() {
    // Filter form submission
    const recipeFilterForm = document.getElementById('recipe-filter-form');
    
    if (recipeFilterForm) {
        // Auto-submit form when select inputs change
        const filterSelects = recipeFilterForm.querySelectorAll('select');
        filterSelects.forEach(select => {
            select.addEventListener('change', function() {
                recipeFilterForm.submit();
            });
        });
        
        // Auto-submit form when radio buttons change
        const filterRadios = recipeFilterForm.querySelectorAll('input[type="radio"]');
        filterRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                recipeFilterForm.submit();
            });
        });
    }
    
    // Recipe detail page - add to meal plan
    const addToMealPlanForm = document.getElementById('add-to-meal-plan-form');
    const addToMealPlanBtn = document.getElementById('add-to-meal-plan-btn');
    
    if (addToMealPlanForm && addToMealPlanBtn) {
        addToMealPlanBtn.addEventListener('click', function() {
            // Get form data
            const formData = {
                date: addToMealPlanForm.elements.date.value,
                meal_type: addToMealPlanForm.elements.meal_type.value,
                recipe_id: addToMealPlanForm.elements.recipe_id.value,
                recipe_title: addToMealPlanForm.elements.recipe_title.value,
                notes: addToMealPlanForm.elements.notes ? addToMealPlanForm.elements.notes.value : ''
            };
            
            // Validate required fields
            if (!formData.date || !formData.meal_type || !formData.recipe_id) {
                alert('Please fill all required fields.');
                return;
            }
            
            // Send AJAX request
            fetch(addToMealPlanForm.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Close the modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById('addToMealPlanModal'));
                    modal.hide();
                    
                    // Show success message
                    alert('Recipe added to meal plan!');
                } else {
                    alert('Error: ' + (data.error || 'Failed to add to meal plan'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
        });
    }
    
    // Add recipe form - dynamic ingredient fields
    const addRecipeForm = document.querySelector('form[action*="recipe/add"]');
    if (addRecipeForm) {
        // Set today as the default date for the meal plan
        const today = new Date().toISOString().split('T')[0];
        const dateInput = document.getElementById('meal-date');
        if (dateInput) {
            dateInput.value = today;
        }
        
        // Form validation before submission
        addRecipeForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Validate title
            const titleInput = document.querySelector('input[name="title"]');
            if (!titleInput.value.trim()) {
                titleInput.classList.add('is-invalid');
                isValid = false;
            } else {
                titleInput.classList.remove('is-invalid');
            }
            
            // Validate ingredients
            const ingredientsTextarea = document.querySelector('textarea[name="ingredients"]');
            if (!ingredientsTextarea.value.trim()) {
                ingredientsTextarea.classList.add('is-invalid');
                isValid = false;
            } else {
                ingredientsTextarea.classList.remove('is-invalid');
            }
            
            // Validate instructions
            const instructionsTextarea = document.querySelector('textarea[name="instructions"]');
            if (!instructionsTextarea.value.trim()) {
                instructionsTextarea.classList.add('is-invalid');
                isValid = false;
            } else {
                instructionsTextarea.classList.remove('is-invalid');
            }
            
            if (!isValid) {
                event.preventDefault();
                alert('Please fill all required fields.');
            }
        });
    }
    
    // Add ingredient substitution functionality on recipe detail page
    const substitutionButtons = document.querySelectorAll('.show-substitution');
    if (substitutionButtons.length) {
        substitutionButtons.forEach(button => {
            button.addEventListener('click', function() {
                const ingredientId = this.dataset.ingredient;
                const substitutionEl = document.getElementById(`substitution-${ingredientId}`);
                
                if (substitutionEl) {
                    if (substitutionEl.classList.contains('d-none')) {
                        substitutionEl.classList.remove('d-none');
                        this.textContent = 'Hide Substitution';
                    } else {
                        substitutionEl.classList.add('d-none');
                        this.textContent = 'Show Substitution';
                    }
                }
            });
        });
    }
    
    // Recipe card hover effects
    const recipeCards = document.querySelectorAll('.recipe-card');
    if (recipeCards.length) {
        recipeCards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.classList.add('shadow');
            });
            
            card.addEventListener('mouseleave', function() {
                this.classList.remove('shadow');
            });
        });
    }
    
    // Make recipe cards draggable for meal planning
    const draggableRecipes = document.querySelectorAll('.recipe-card[data-id]');
    if (draggableRecipes.length) {
        draggableRecipes.forEach(recipe => {
            recipe.setAttribute('draggable', 'true');
            
            recipe.addEventListener('dragstart', function(e) {
                e.dataTransfer.setData('text/plain', JSON.stringify({
                    id: this.dataset.id,
                    title: this.dataset.title,
                    type: 'recipe'
                }));
            });
        });
    }
});
/**
 * KitchenSync - Meal Plan JavaScript
 * Handles calendar rendering and interaction for meal planning
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the calendar
    const calendarEl = document.getElementById('meal-calendar');
    
    if (!calendarEl) return;
    
    // Initialize recipe selection
    const recipeSelect = document.getElementById('recipe-select');
    const recipeIdInput = document.getElementById('recipe-id-input');
    const recipeTitleInput = document.getElementById('recipe-title-input');
    
    if (recipeSelect && recipeIdInput && recipeTitleInput) {
        recipeSelect.addEventListener('change', function() {
            const selectedOption = recipeSelect.options[recipeSelect.selectedIndex];
            recipeIdInput.value = recipeSelect.value;
            recipeTitleInput.value = selectedOption.dataset.title || selectedOption.textContent;
        });
    }
    
    // Initialize FullCalendar
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridWeek',
        initialDate: startDate,
        height: 'auto',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,dayGridWeek'
        },
        events: calendarData,
        eventClassNames: function(arg) {
            return [`meal-type-${arg.event.extendedProps.meal_type}`];
        },
        eventContent: function(arg) {
            return {
                html: `
                    <div class="fc-event-title">${arg.event.title}</div>
                    <div class="fc-event-time">${arg.event.extendedProps.meal_type}</div>
                `
            };
        },
        eventClick: function(info) {
            // Open the event modal with details
            const modal = new bootstrap.Modal(document.getElementById('eventModal'));
            
            // Populate modal with event data
            document.getElementById('edit-event-id').value = info.event.id;
            document.getElementById('edit-event-title').value = info.event.title.split(':')[1].trim();
            document.getElementById('edit-event-date').value = info.event.start.toISOString().split('T')[0];
            document.getElementById('edit-event-meal-type').value = info.event.extendedProps.meal_type;
            document.getElementById('edit-event-notes').value = info.event.extendedProps.notes || '';
            
            // Set the form action for delete
            const deleteForm = document.getElementById('delete-event-form');
            deleteForm.action = `/meal-plan/delete/${info.event.id}`;
            
            modal.show();
        },
        datesSet: function(dateInfo) {
            // Update URL when calendar view changes
            const newStartDate = dateInfo.start.toISOString().split('T')[0];
            if (newStartDate !== startDate) {
                const url = new URL(window.location.href);
                url.searchParams.set('start', newStartDate);
                window.history.replaceState({}, '', url);
            }
        }
    });
    
    calendar.render();
    
    // Today button handler
    document.getElementById('today-btn').addEventListener('click', function() {
        calendar.today();
    });
    
    // Event handlers for the event modal
    const saveEventBtn = document.getElementById('save-event-btn');
    const deleteEventBtn = document.getElementById('delete-event-btn');
    
    if (saveEventBtn) {
        saveEventBtn.addEventListener('click', function() {
            const eventId = document.getElementById('edit-event-id').value;
            const mealType = document.getElementById('edit-event-meal-type').value;
            const notes = document.getElementById('edit-event-notes').value;
            
            // Send AJAX request to update the plan
            fetch(`/meal-plan/update/${eventId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: new URLSearchParams({
                    'meal_type': mealType,
                    'notes': notes
                })
            })
            .then(response => {
                if (response.ok) {
                    // Close the modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById('eventModal'));
                    modal.hide();
                    
                    // Refresh the page to see updated events
                    window.location.reload();
                } else {
                    alert('Failed to update meal plan. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
        });
    }
    
    if (deleteEventBtn) {
        deleteEventBtn.addEventListener('click', function() {
            if (confirm('Are you sure you want to remove this meal from your plan?')) {
                const form = document.getElementById('delete-event-form');
                
                fetch(form.action, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => {
                    if (response.ok) {
                        // Close the modal
                        const modal = bootstrap.Modal.getInstance(document.getElementById('eventModal'));
                        modal.hide();
                        
                        // Refresh the page to see updated events
                        window.location.reload();
                    } else {
                        alert('Failed to delete meal plan. Please try again.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                });
            }
        });
    }
});
/**
 * KitchenSync - Main JavaScript file
 * Contains general functions used across the application
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltips.length) {
        Array.from(tooltips).forEach(tooltip => {
            new bootstrap.Tooltip(tooltip);
        });
    }

    // Initialize all popovers
    const popovers = document.querySelectorAll('[data-bs-toggle="popover"]');
    if (popovers.length) {
        Array.from(popovers).forEach(popover => {
            new bootstrap.Popover(popover);
        });
    }

    // Flash message timeout - auto-hide after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    if (flashMessages.length) {
        Array.from(flashMessages).forEach(message => {
            setTimeout(() => {
                const alert = new bootstrap.Alert(message);
                alert.close();
            }, 5000);
        });
    }
    
    // Add active class to current nav item
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        // Get the link URL without query parameters
        const linkPath = link.getAttribute('href').split('?')[0];
        
        // Check if current path starts with the link path, excluding index
        if (linkPath !== '/' && currentLocation.startsWith(linkPath)) {
            link.classList.add('active');
        }
    });
});

/**
 * Format a date for display
 * @param {Date|string} date - The date to format
 * @param {boolean} includeTime - Whether to include the time
 * @returns {string} - Formatted date string
 */
function formatDate(date, includeTime = false) {
    const d = new Date(date);
    const options = {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
        year: 'numeric'
    };
    
    if (includeTime) {
        options.hour = '2-digit';
        options.minute = '2-digit';
    }
    
    return d.toLocaleDateString('en-US', options);
}

/**
 * Converts a form to JSON data
 * @param {HTMLFormElement} form - The form element
 * @returns {Object} - Form data as JSON object
 */
function formToJson(form) {
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    return data;
}

/**
 * Validate a form input element
 * @param {HTMLElement} input - The input element to validate
 * @returns {boolean} - Whether the input is valid
 */
function validateInput(input) {
    if (input.hasAttribute('required') && !input.value.trim()) {
        input.classList.add('is-invalid');
        return false;
    }
    
    if (input.type === 'email' && input.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(input.value)) {
            input.classList.add('is-invalid');
            return false;
        }
    }
    
    if (input.type === 'number' && input.value) {
        const min = parseFloat(input.getAttribute('min'));
        const max = parseFloat(input.getAttribute('max'));
        const value = parseFloat(input.value);
        
        if ((min != null && value < min) || (max != null && value > max)) {
            input.classList.add('is-invalid');
            return false;
        }
    }
    
    input.classList.remove('is-invalid');
    return true;
}

/**
 * Add event handlers to enable drag-and-drop functionality
 * @param {string} dragElementSelector - Selector for draggable elements
 * @param {string} dropZoneSelector - Selector for drop zones
 * @param {function} onDrop - Callback function when item is dropped
 */
function enableDragAndDrop(dragElementSelector, dropZoneSelector, onDrop) {
    const draggables = document.querySelectorAll(dragElementSelector);
    const dropZones = document.querySelectorAll(dropZoneSelector);
    
    draggables.forEach(draggable => {
        draggable.setAttribute('draggable', 'true');
        
        draggable.addEventListener('dragstart', e => {
            draggable.classList.add('dragging');
            e.dataTransfer.setData('text/plain', draggable.dataset.id);
            e.dataTransfer.effectAllowed = 'move';
        });
        
        draggable.addEventListener('dragend', () => {
            draggable.classList.remove('dragging');
        });
    });
    
    dropZones.forEach(zone => {
        zone.addEventListener('dragover', e => {
            e.preventDefault();
            zone.classList.add('drag-over');
            e.dataTransfer.dropEffect = 'move';
        });
        
        zone.addEventListener('dragleave', () => {
            zone.classList.remove('drag-over');
        });
        
        zone.addEventListener('drop', e => {
            e.preventDefault();
            zone.classList.remove('drag-over');
            const draggedId = e.dataTransfer.getData('text/plain');
            
            if (typeof onDrop === 'function') {
                onDrop(draggedId, zone);
            }
        });
    });
}
// API Configuration - will be proxied through nginx
const API_BASE_URL = '/api';

// DOM Elements - will be initialized after DOM loads
let searchForm, advancedToggle, advancedSettings, loadingElement, resultsElement;

// Initialize DOM elements and event listeners when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Get DOM Elements
    searchForm = document.getElementById('searchForm');
    advancedToggle = document.getElementById('advancedToggle');
    advancedSettings = document.getElementById('advancedSettings');
    loadingElement = document.getElementById('loading');
    resultsElement = document.getElementById('results');

    // Check if all elements exist
    if (!searchForm || !advancedToggle || !advancedSettings || !loadingElement || !resultsElement) {
        console.error('❌ Error: One or more required DOM elements not found!');
        return;
    }

    // Toggle advanced settings
    advancedToggle.addEventListener('click', () => {
        const isVisible = advancedSettings.style.display === 'block';
        advancedSettings.style.display = isVisible ? 'none' : 'block';
        advancedToggle.textContent = isVisible ? '⚙️ Advanced Settings' : '⚙️ Hide Advanced Settings';
    });

    // Form submission handler
    searchForm.addEventListener('submit', handleSubmit);
});

// Form submission handler
async function handleSubmit(event) {
    event.preventDefault();
    
    // Update loading message
    const loadingMessage = loadingElement.querySelector('p');
    loadingMessage.textContent = 'Searching for jobs...';
    
    // Show loading state
    loadingElement.style.display = 'block';
    resultsElement.innerHTML = '';
    
    try {
        // Get form data
        const formData = new FormData(searchForm);
        const searchData = {};
        
        // Convert form data to object, handling checkboxes and empty values
        for (const [key, value] of formData.entries()) {
            if (key === 'work_from_home') {
                searchData[key] = true;
            } else if (value && value.trim() !== '') {
                searchData[key] = value;
            }
        }
        
        // Make API request
        const response = await fetch(`${API_BASE_URL}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(searchData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Get the HTML response
        const htmlContent = await response.text();
        
        // Display the results
        displayResults(htmlContent);
        
    } catch (error) {
        console.error('Search error:', error);
        displayError(error.message);
    } finally {
        // Hide loading state
        loadingElement.style.display = 'none';
    }
}

// Display search results
function displayResults(htmlContent) {
    resultsElement.innerHTML = htmlContent;
    
    // Enhance the received HTML with our own functionality
    enhanceJobCards();
    
    // Add event listeners for export links
    addExportLinkListeners();
}

// Enhance job cards to ensure only one is expanded at a time
function enhanceJobCards() {
    const jobCards = document.querySelectorAll('.job-card');
    
    jobCards.forEach(card => {
        const checkbox = card.querySelector('.accordion-toggle');
        
        checkbox.addEventListener('change', (event) => {
            if (event.target.checked) {
                // Close all other job cards
                jobCards.forEach(otherCard => {
                    if (otherCard !== card) {
                        const otherCheckbox = otherCard.querySelector('.accordion-toggle');
                        if (otherCheckbox) {
                            otherCheckbox.checked = false;
                        }
                    }
                });
            }
        });
    });
}

// Add click handlers for export links
function addExportLinkListeners() {
    const exportLinks = document.querySelectorAll('.export-button');
    
    exportLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            // The link already has the correct href, so we just let it work normally
            // We could add tracking or other functionality here if needed
            console.log('Export link clicked:', event.target.href);
        });
    });
}

// Display error message
function displayError(message) {
    resultsElement.innerHTML = `
        <div class="error">
            <h3>❌ Search Failed</h3>
            <p>${message}</p>
            <p>Please check your connection and try again.</p>
        </div>
    `;
}

// Utility function to format form data for display
function formatFormData(formData) {
    const data = {};
    for (const [key, value] of formData.entries()) {
        data[key] = value;
    }
    return data;
}

// Add some helpful keyboard shortcuts
document.addEventListener('keydown', (event) => {
    // Ctrl/Cmd + Enter to submit form
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        const searchInput = document.getElementById('query');
        if (document.activeElement === searchInput) {
            searchForm.requestSubmit();
        }
    }
    
    // Escape to clear search
    if (event.key === 'Escape') {
        const searchInput = document.getElementById('query');
        if (document.activeElement === searchInput && searchInput.value) {
            searchInput.value = '';
        }
    }
});

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    // Focus on search input
    const searchInput = document.getElementById('query');
    if (searchInput) {
        searchInput.focus();
    }
    
    // Add some helpful tips
    console.log('Job Search Interface Ready!');
    console.log('Tips:');
    console.log('- Use Ctrl/Cmd + Enter to quickly submit search');
    console.log('- Press Escape to clear the search field');
    console.log('- Advanced settings are available for more specific searches');
});

// Handle potential CORS issues
function handleCorsError(error) {
    console.error('CORS or network error:', error);
    displayError(`
        Unable to connect to the job search API. This could be due to:
        <ul>
            <li>The backend server is not running</li>
            <li>CORS restrictions</li>
            <li>Network connectivity issues</li>
        </ul>
        Please ensure the backend server is running on http://localhost:8000
    `);
}

// Global error handler for uncaught errors
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

// Add some visual feedback for form interactions
searchForm.addEventListener('input', (event) => {
    if (event.target.type === 'text' || event.target.type === 'number') {
        event.target.style.borderColor = '#667eea';
        setTimeout(() => {
            event.target.style.borderColor = '';
        }, 1000);
    }
});

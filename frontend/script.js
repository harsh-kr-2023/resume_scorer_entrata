// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// Role descriptions
const roleDescriptions = {
    'backend_engineer': 'Evaluates: Python/Java/Go, REST APIs, SQL, Git, Cloud platforms, Docker, CI/CD',
    'frontend_engineer': 'Evaluates: JavaScript/TypeScript, React/Vue/Angular, HTML/CSS, Responsive design, Testing',
    'data_scientist': 'Evaluates: Python, ML libraries, Statistics, SQL, Data visualization, Deep learning',
    'engineering_manager': 'Evaluates: Team leadership, Technical background, Project delivery, People management'
};

// Update role description
function updateRoleDescription() {
    const role = document.getElementById('role').value;
    const description = roleDescriptions[role] || '';
    document.getElementById('role-description').textContent = description;
}

// Tab Management
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    event.target.classList.add('active');
    
    // Load rankings if switching to rankings tab
    if (tabName === 'rankings') {
        loadRankings();
    }
}

// File Upload Handler
const fileInput = document.getElementById('resume');
const fileUploadArea = document.getElementById('file-upload-area');
const fileNameDisplay = document.getElementById('file-name');

// Click to upload
fileUploadArea.addEventListener('click', function() {
    fileInput.click();
});

// File selected
fileInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        fileNameDisplay.textContent = file.name;
        fileUploadArea.classList.add('has-file');
    } else {
        fileNameDisplay.textContent = 'Click to upload or drag & drop PDF';
        fileUploadArea.classList.remove('has-file');
    }
});

// Drag and drop handlers
fileUploadArea.addEventListener('dragover', function(e) {
    e.preventDefault();
    e.stopPropagation();
    fileUploadArea.classList.add('dragover');
});

fileUploadArea.addEventListener('dragleave', function(e) {
    e.preventDefault();
    e.stopPropagation();
    fileUploadArea.classList.remove('dragover');
});

fileUploadArea.addEventListener('drop', function(e) {
    e.preventDefault();
    e.stopPropagation();
    fileUploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        if (file.type === 'application/pdf') {
            fileInput.files = files;
            fileNameDisplay.textContent = file.name;
            fileUploadArea.classList.add('has-file');
        } else {
            showError('Please upload a PDF file');
        }
    }
});

// Form Submission
document.getElementById('score-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Get form data
    const resume = document.getElementById('resume').files[0];
    const role = document.getElementById('role').value;
    let jdText = document.getElementById('jd').value.trim();
    
    // Validate
    if (!resume) {
        showError('Please select a resume file');
        return;
    }
    
    // If no job description provided, use a generic one based on role
    if (!jdText) {
        const roleDescriptions = {
            'backend_engineer': 'Evaluate this candidate for a backend engineering position based on the standard criteria.',
            'frontend_engineer': 'Evaluate this candidate for a frontend engineering position based on the standard criteria.',
            'data_scientist': 'Evaluate this candidate for a data science position based on the standard criteria.',
            'engineering_manager': 'Evaluate this candidate for an engineering manager position based on the standard criteria.'
        };
        jdText = roleDescriptions[role] || 'Evaluate this candidate based on the standard criteria for the selected role.';
    }
    
    // Show loading state
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.getElementById('btn-text');
    const btnLoader = document.getElementById('btn-loader');
    
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'block';
    
    // Hide previous results/errors
    document.getElementById('results').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    
    try {
        // Prepare form data
        const formData = new FormData();
        formData.append('resume', resume);
        formData.append('role', role);
        formData.append('jd_text', jdText);
        
        // Send request
        const response = await fetch(`${API_BASE_URL}/match`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
        } else {
            showError(`Error: ${data.error || 'Unknown error occurred'}`);
        }
        
    } catch (error) {
        showError(`Failed to connect to API: ${error.message}`);
    } finally {
        // Reset button state
        submitBtn.disabled = false;
        btnText.style.display = 'block';
        btnLoader.style.display = 'none';
    }
});

// Display Results
function displayResults(data) {
    // Show results section
    const resultsDiv = document.getElementById('results');
    resultsDiv.style.display = 'block';
    
    // Set score with color coding
    const scoreValue = document.getElementById('score-value');
    scoreValue.textContent = data.score;
    
    const scoreCircle = document.querySelector('.score-circle');
    if (data.score >= 80) {
        scoreCircle.style.background = 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)';
    } else if (data.score >= 60) {
        scoreCircle.style.background = 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)';
    } else {
        scoreCircle.style.background = 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)';
    }
    
    // Set justification
    document.getElementById('justification').textContent = data.justification;
    
    // Set gaps
    const gapsList = document.getElementById('gaps-list');
    gapsList.innerHTML = '';
    data.gaps.forEach(gap => {
        const li = document.createElement('li');
        li.textContent = gap;
        gapsList.appendChild(li);
    });
    
    // Set suggestions
    const suggestionsList = document.getElementById('suggestions-list');
    suggestionsList.innerHTML = '';
    data.suggestions.forEach(suggestion => {
        const li = document.createElement('li');
        li.textContent = suggestion;
        suggestionsList.appendChild(li);
    });
    
    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Show Error
function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Load Rankings
async function loadRankings() {
    const rankingsList = document.getElementById('rankings-list');
    const filterRole = document.getElementById('filter-role').value;
    
    // Show loading
    rankingsList.innerHTML = '<p class="loading">Loading rankings...</p>';
    
    try {
        const url = filterRole 
            ? `${API_BASE_URL}/rankings?role=${filterRole}`
            : `${API_BASE_URL}/rankings`;
            
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success && data.results.length > 0) {
            displayRankings(data.results);
        } else {
            rankingsList.innerHTML = '<p class="no-results">No results found</p>';
        }
        
    } catch (error) {
        rankingsList.innerHTML = `<p class="error">Failed to load rankings: ${error.message}</p>`;
    }
}

// Display Rankings
function displayRankings(results) {
    const rankingsList = document.getElementById('rankings-list');
    rankingsList.innerHTML = '';
    
    results.forEach((result, index) => {
        const item = document.createElement('div');
        item.className = 'rankings-item';
        
        // Format date
        const date = new Date(result.created_at);
        const dateStr = date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
        
        // Format role name
        const roleName = result.role.split('_').map(word => 
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
        
        item.innerHTML = `
            <div class="rankings-header">
                <div>
                    <div class="rankings-name">#${index + 1} ${result.resume_name}</div>
                    <span class="rankings-role">${roleName}</span>
                </div>
                <div class="rankings-score">${result.score}/100</div>
            </div>
            <div class="rankings-date">Evaluated on ${dateStr}</div>
        `;
        
        rankingsList.appendChild(item);
    });
}

// Load rankings on page load if on rankings tab
window.addEventListener('DOMContentLoaded', () => {
    // Check API health
    fetch(`${API_BASE_URL}/health`)
        .then(response => response.json())
        .then(data => {
            console.log('API Status:', data.status);
        })
        .catch(error => {
            console.error('API not reachable:', error);
            showError('Cannot connect to API. Make sure the server is running on http://localhost:8000');
        });
});

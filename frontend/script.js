// Global variables
let currentCode = '';
let currentLanguage = 'python';
let history = [];

// Particles system
let particles = [];
let mouseX = 0;
let mouseY = 0;
let animationId = null; // Track animation frame for cleanup

// API Configuration
const API_BASE_URL = 'http://localhost:5000';

// DOM Elements
const specInput = document.getElementById('specInput');
const generateBtn = document.getElementById('generateBtn');
const clearBtn = document.getElementById('clearBtn');
const codeSection = document.getElementById('codeSection');
const codeOutput = document.getElementById('codeOutput');
const languageLabel = document.getElementById('languageLabel');
const copyBtn = document.getElementById('copyBtn');
const runBtn = document.getElementById('runBtn');
const saveBtn = document.getElementById('saveBtn');
const executionSection = document.getElementById('executionSection');
const statusLabel = document.getElementById('statusLabel');
const executionOutput = document.getElementById('executionOutput');
const clearExecutionBtn = document.getElementById('clearExecutionBtn');
const historyContainer = document.getElementById('historyContainer');
const loadingModal = document.getElementById('loadingModal');
const successModal = document.getElementById('successModal');
const successMessage = document.getElementById('successMessage');
// Model selection elements
const languageSelect = document.getElementById('languageSelect');
const modelSelect = document.getElementById('modelSelect');

// Utility function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    generateBtn.addEventListener('click', generateCode);
    clearBtn.addEventListener('click', clearInput);
    copyBtn.addEventListener('click', copyCode);
    runBtn.addEventListener('click', runCode);
    saveBtn.addEventListener('click', saveCode);
    clearExecutionBtn.addEventListener('click', clearExecution);
    
    // Load history on page load
    loadHistory();
    
    // Initialize particles
    initParticles();
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            generateCode();
        }
    });
    
    // Track mouse movement for particles
    document.addEventListener('mousemove', function(e) {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });
});

// Generate code from specification
async function generateCode() {
    const spec = specInput.value.trim();
    const provider = 'huggingface';
    const language = languageSelect.value;
    const model = modelSelect.value;
    
    if (!spec) {
        showError('Please enter a specification');
        return;
    }
    
    showLoading();
    
    try {
        const body = { spec, provider, language, model };
        const response = await fetch(`${API_BASE_URL}/generate-code`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentCode = data.code;
            currentLanguage = detectLanguage(currentCode);
            
            displayCode(currentCode, currentLanguage);
            addToHistory(spec, currentCode);
            hideLoading();
        } else {
            throw new Error(data.error || 'Failed to generate code');
        }
    } catch (error) {
        hideLoading();
        showError('Error generating code: ' + error.message);
    }
}

// Display generated code
function displayCode(code, language) {
    codeOutput.textContent = code;
    languageLabel.textContent = language.charAt(0).toUpperCase() + language.slice(1);
    codeOutput.className = 'language-' + language;
    
    // Update Prism.js highlighting
    Prism.highlightElement(codeOutput);
    
    // Show code section
    codeSection.style.display = 'block';
    
    // Scroll to code section
    codeSection.scrollIntoView({ behavior: 'smooth' });
}

// Detect programming language from code
function detectLanguage(code) {
    const codeLower = code.toLowerCase();
    
    if (codeLower.includes('def ') || codeLower.includes('import ') || codeLower.includes('print(')) {
        return 'python';
    } else if (codeLower.includes('function ') || codeLower.includes('const ') || codeLower.includes('let ')) {
        return 'javascript';
    } else if (codeLower.includes('public class') || codeLower.includes('public static void')) {
        return 'java';
    } else if (codeLower.includes('<?php') || codeLower.includes('echo ')) {
        return 'php';
    } else if (codeLower.includes('def ') || codeLower.includes('end')) {
        return 'ruby';
    } else if (codeLower.includes('package ') || codeLower.includes('import ')) {
        return 'go';
    } else {
        return 'python'; // Default to Python
    }
}

// Run code execution
async function runCode() {
    if (!currentCode) {
        showError('No code to run');
        return;
    }
    
    updateStatus('running');
    executionSection.style.display = 'block';
    executionOutput.textContent = 'Executing code...\n';
    
    try {
        const response = await fetch(`${API_BASE_URL}/execute_code`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                code: currentCode,
                language: currentLanguage 
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            executionOutput.textContent = data.output;
            updateStatus('success');
        } else {
            executionOutput.textContent = `Error: ${data.error}`;
            updateStatus('error');
        }
    } catch (error) {
        executionOutput.textContent = `Error: ${error.message}`;
        updateStatus('error');
    }
    
    executionSection.scrollIntoView({ behavior: 'smooth' });
}

// Update execution status
function updateStatus(status) {
    statusLabel.textContent = status.charAt(0).toUpperCase() + status.slice(1);
    statusLabel.className = `status-label ${status}`;
}

// Copy code to clipboard
async function copyCode() {
    try {
        await navigator.clipboard.writeText(currentCode);
        showSuccess('Code copied to clipboard!');
    } catch (error) {
        showError('Failed to copy code');
    }
}

// Save code to file
function saveCode() {
    const blob = new Blob([currentCode], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `generated_code.${getFileExtension(currentLanguage)}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showSuccess('Code saved to file!');
}

// Get file extension for language
function getFileExtension(language) {
    const extensions = {
        'python': 'py',
        'javascript': 'js',
        'java': 'java',
        'php': 'php',
        'ruby': 'rb',
        'go': 'go',
        'cpp': 'cpp',
        'c': 'c'
    };
    return extensions[language] || 'txt';
}

// Add to history
function addToHistory(spec, code) {
    const historyItem = {
        id: Date.now(),
        spec: spec,
        code: code,
        language: currentLanguage,
        timestamp: new Date().toISOString()
    };
    
    history.unshift(historyItem);
    saveHistoryToStorage();
    displayHistory();
}

// Load history from storage
function loadHistory() {
    try {
        const savedHistory = localStorage.getItem('specToCodeHistory');
        if (savedHistory) {
            history = JSON.parse(savedHistory);
            displayHistory();
        }
    } catch (error) {
        console.error('Error loading history:', error);
        history = [];
    }
}

// Save history to storage
function saveHistoryToStorage() {
    try {
        // Keep only last 50 items
        if (history.length > 50) {
            history = history.slice(0, 50);
        }
        localStorage.setItem('specToCodeHistory', JSON.stringify(history));
    } catch (error) {
        console.error('Error saving history:', error);
    }
}

// Display history
function displayHistory() {
    if (history.length === 0) {
        historyContainer.innerHTML = `
            <div class="history-placeholder">
                <i class="fas fa-clock"></i>
                <p>No history yet. Generate some code to see it here!</p>
            </div>
        `;
        return;
    }
    
    historyContainer.innerHTML = history.map(item => `
        <div class="history-item" onclick="loadHistoryItem(${item.id})">
            <div class="history-item-header">
                <div class="history-item-title">
                    ${escapeHtml(item.spec.substring(0, 50))}${item.spec.length > 50 ? '...' : ''}
                </div>
                <div class="history-item-time">
                    ${formatTimestamp(item.timestamp)}
                </div>
            </div>
            <div class="history-item-spec">
                ${escapeHtml(item.spec)}
            </div>
            <div class="history-item-code">
                ${escapeHtml(item.code.substring(0, 200))}${item.code.length > 200 ? '...' : ''}
            </div>
        </div>
    `).join('');
}

// Load history item
function loadHistoryItem(id) {
    const item = history.find(h => h.id === id);
    if (item) {
        specInput.value = item.spec;
        currentCode = item.code;
        currentLanguage = item.language;
        displayCode(item.code, item.language);
    }
}

// Format timestamp
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) { // Less than 1 minute
        return 'Just now';
    } else if (diff < 3600000) { // Less than 1 hour
        const minutes = Math.floor(diff / 60000);
        return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    } else if (diff < 86400000) { // Less than 1 day
        const hours = Math.floor(diff / 3600000);
        return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    } else {
        return date.toLocaleDateString();
    }
}

// Clear input
function clearInput() {
    specInput.value = '';
    codeSection.style.display = 'none';
    executionSection.style.display = 'none';
}

// Clear execution
function clearExecution() {
    executionOutput.textContent = '';
    updateStatus('ready');
    executionSection.style.display = 'none';
}

// Show loading modal
function showLoading() {
    loadingModal.style.display = 'block';
}

// Hide loading modal
function hideLoading() {
    loadingModal.style.display = 'none';
}

// Show success modal
function showSuccess(message) {
    successMessage.textContent = message;
    successModal.style.display = 'block';
}

// Show error
function showError(message) {
    alert(message); // Simple error display - could be enhanced with a proper modal
}

// Initialize particles
function initParticles() {
    const container = document.getElementById('particlesContainer');
    const particleCount = 100;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 20 + 's';
        particle.style.animationDuration = (20 + Math.random() * 15) + 's';
        container.appendChild(particle);
        
        // Store particle reference
        particles.push(particle);
    }
    
    // Start particle animation
    animateParticles();
}

// Animate particles with mouse interaction
function animateParticles() {
    particles.forEach((particle, index) => {
        const rect = particle.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        // Calculate distance from mouse
        const distance = Math.sqrt(
            Math.pow(mouseX - centerX, 2) + Math.pow(mouseY - centerY, 2)
        );
        
        // Add subtle mouse interaction
        if (distance < 100) {
            const angle = Math.atan2(mouseY - centerY, mouseX - centerX);
            const force = (100 - distance) / 100;
            const moveX = Math.cos(angle) * force * 2;
            const moveY = Math.sin(angle) * force * 2;
            
            particle.style.transform += ` translate(${moveX}px, ${moveY}px)`;
        }
    });
    
    animationId = requestAnimationFrame(animateParticles);
}

// Cleanup function for particles
function cleanupParticles() {
    if (animationId) {
        cancelAnimationFrame(animationId);
        animationId = null;
    }
}

// Close modal
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Close modals when clicking outside
window.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', cleanupParticles); 
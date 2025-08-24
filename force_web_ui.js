// The Force Programming Language - JavaScript UI Controller

class ForceUI {
    constructor() {
        this.editor = null;
        this.examples = {};
        this.isLoading = false;
        this.forcePowerLevel = 0;
        
        this.init();
    }
    
    async init() {
        this.setupEditor();
        this.setupEventListeners();
        this.setupTheme();
        await this.loadExamples();
        this.updateStatus('Ready to explore The Force');
        this.animateForcePower(25); // Start with some base power
    }
    
    setupEditor() {
        const textarea = document.getElementById('force-editor');
        
        // Try to initialize CodeMirror for syntax highlighting
        if (typeof CodeMirror !== 'undefined') {
            this.editor = CodeMirror.fromTextArea(textarea, {
                lineNumbers: true,
                mode: 'text/x-csrc', // Closest mode for C-like syntax
                theme: 'dracula',
                indentUnit: 4,
                indentWithTabs: false,
                lineWrapping: true,
                matchBrackets: true,
                autoCloseBrackets: true,
                styleActiveLine: true,
                viewportMargin: Infinity
            });
            
            // Custom Force language highlighting
            this.setupForceHighlighting();
            
            this.editor.on('change', () => {
                this.updateForcePower();
            });
        } else {
            // Fallback to plain textarea
            console.warn('CodeMirror not loaded, using plain textarea');
            textarea.style.display = 'block';
            
            textarea.addEventListener('input', () => {
                this.updateForcePower();
            });
        }
    }
    
    setupForceHighlighting() {
        if (!this.editor) return;
        
        // Define Force language keywords
        const forceKeywords = [
            'order', 'ability', 'holocron', 'kyber', 'respond', 'sense', 'meditate', 
            'train', 'squadron', 'datapad', 'new', 'self', 'initiate', 'else',
            'try_use_force', 'catch_disturbance', 'finally_balance', 'transmission',
            'from', 'return', 'stack_tower', 'queue_line', 'tuple_coordinates',
            'protocol_droid', 'hologram_text', 'regex_pattern', 'galactic_time',
            'data_stream', 'force_encrypt', 'force_hash', 'jedi_mind_trick',
            'jedi_council', 'hyperspace_comm', 'rebellion'
        ];
        
        // Add custom highlighting overlay
        this.editor.addOverlay({
            token: function(stream, state) {
                if (stream.match(/\/\/.*$/)) {
                    return 'comment';
                }
                
                if (stream.match(/\/\*[\s\S]*?\*\//)) {
                    return 'comment';
                }
                
                for (let keyword of forceKeywords) {
                    if (stream.match(new RegExp('\\b' + keyword + '\\b'))) {
                        return 'keyword';
                    }
                }
                
                if (stream.match(/\b\d+\b/)) {
                    return 'number';
                }
                
                if (stream.match(/"([^"]|\\.)*"/)) {
                    return 'string';
                }
                
                if (stream.match(/'([^']|\\.)*'/)) {
                    return 'string';
                }
                
                stream.next();
                return null;
            }
        });
    }
    
    setupEventListeners() {
        // Action buttons
        document.getElementById('compile-btn').addEventListener('click', () => this.compileCode());
        document.getElementById('run-btn').addEventListener('click', () => this.runCode());
        document.getElementById('clear-btn').addEventListener('click', () => this.clearEditor());
        document.getElementById('theme-toggle').addEventListener('click', () => this.toggleTheme());
        document.getElementById('export-btn').addEventListener('click', () => this.exportCode());
        
        // Example buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('example-btn')) {
                const exampleKey = e.target.getAttribute('data-example');
                this.loadExample(exampleKey);
            }
        });
        
        // Modal close
        document.querySelector('.modal-close').addEventListener('click', () => {
            this.hideError();
        });
        
        // Close modal on backdrop click
        document.getElementById('error-modal').addEventListener('click', (e) => {
            if (e.target === document.getElementById('error-modal')) {
                this.hideError();
            }
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch(e.key) {
                    case 'Enter':
                        e.preventDefault();
                        this.runCode();
                        break;
                    case 'b':
                        e.preventDefault();
                        this.compileCode();
                        break;
                    case 'k':
                        e.preventDefault();
                        this.clearEditor();
                        break;
                    case 's':
                        e.preventDefault();
                        this.exportCode();
                        break;
                    case 't':
                        e.preventDefault();
                        this.toggleTheme();
                        break;
                }
            }
        });
    }
    
    async loadExamples() {
        try {
            const response = await fetch('/examples');
            if (response.ok) {
                this.examples = await response.json();
                console.log('Examples loaded:', Object.keys(this.examples));
            }
        } catch (error) {
            console.error('Failed to load examples:', error);
            // Fallback examples
            this.examples = {
                hello_galaxy: {
                    name: 'Hello Galaxy',
                    code: 'ability main() {\n    respond "Hello, Galaxy!"\n    respond "May the Force be with you"\n}\n\nmain()'
                }
            };
        }
    }
    
    getEditorContent() {
        if (this.editor) {
            return this.editor.getValue();
        } else {
            return document.getElementById('force-editor').value;
        }
    }
    
    setEditorContent(content) {
        if (this.editor) {
            this.editor.setValue(content);
        } else {
            document.getElementById('force-editor').value = content;
        }
    }
    
    async compileCode() {
        const code = this.getEditorContent().trim();
        if (!code) {
            this.updateStatus('No code to compile', 'warning');
            return;
        }
        
        this.setLoading(true);
        this.updateStatus('Compiling Force code...');
        
        try {
            const response = await fetch('/api/compile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: code })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.displayPythonCode(result.python_code);
                this.updateStatus('Code compiled successfully', 'success');
                this.animateForcePower(Math.min(100, this.forcePowerLevel + 15));
            } else {
                this.showError('Compilation Error', result.error);
                this.updateStatus('Compilation failed', 'error');
            }
        } catch (error) {
            this.showError('Network Error', `Failed to compile code: ${error.message}`);
            this.updateStatus('Network error during compilation', 'error');
        } finally {
            this.setLoading(false);
        }
    }
    
    async runCode() {
        const code = this.getEditorContent().trim();
        if (!code) {
            this.updateStatus('No code to run', 'warning');
            return;
        }
        
        this.setLoading(true);
        this.updateStatus('Running Force code...');
        
        try {
            const response = await fetch('/api/run', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: code })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.displayPythonCode(result.python_code);
                this.displayExecutionOutput(result.output, result.result);
                this.updateStatus('Code executed successfully', 'success');
                this.animateForcePower(Math.min(100, this.forcePowerLevel + 20));
            } else {
                this.showError('Execution Error', result.error);
                this.updateStatus('Code execution failed', 'error');
                this.animateForcePower(Math.max(0, this.forcePowerLevel - 10));
            }
        } catch (error) {
            this.showError('Network Error', `Failed to run code: ${error.message}`);
            this.updateStatus('Network error during execution', 'error');
        } finally {
            this.setLoading(false);
        }
    }
    
    clearEditor() {
        this.setEditorContent('');
        this.clearOutput();
        this.updateStatus('Editor cleared');
        this.animateForcePower(25); // Reset to base power
    }
    
    loadExample(exampleKey) {
        const example = this.examples[exampleKey];
        if (example) {
            this.setEditorContent(example.code);
            this.clearOutput(); // Clear previous output when loading new example
            this.updateStatus(`Loaded example: ${example.name}`);
            this.animateForcePower(40); // Boost power for loading examples
        }
    }
    
    displayPythonCode(pythonCode) {
        const output = document.getElementById('python-output');
        output.textContent = pythonCode;
        output.parentElement.parentElement.classList.add('success');
        
        // Remove success class after animation
        setTimeout(() => {
            output.parentElement.parentElement.classList.remove('success');
        }, 2000);
    }
    
    displayExecutionOutput(output, result) {
        const outputElement = document.getElementById('execution-output');
        let displayText = '';
        
        if (output) {
            displayText += output;
        }
        
        if (result && result !== 'None' && result !== 'Code executed successfully') {
            displayText += displayText ? '\\n\\nReturn value: ' + result : 'Return value: ' + result;
        }
        
        if (!displayText.trim()) {
            displayText = 'Program completed successfully (no output)';
        }
        
        outputElement.textContent = displayText;
        outputElement.parentElement.parentElement.classList.add('success');
        
        // Remove success class after animation
        setTimeout(() => {
            outputElement.parentElement.parentElement.classList.remove('success');
        }, 2000);
    }
    
    clearOutput() {
        document.getElementById('python-output').textContent = 'Compiled Python code will appear here...';
        document.getElementById('execution-output').textContent = 'Program output will appear here...';
        
        // Remove any status classes
        document.querySelectorAll('.output-panel').forEach(panel => {
            panel.classList.remove('success', 'error');
        });
    }
    
    showError(title, message) {
        const modal = document.getElementById('error-modal');
        const errorMessage = document.getElementById('error-message');
        
        modal.querySelector('.modal-header h3').textContent = title;
        errorMessage.textContent = message;
        
        modal.style.display = 'block';
        
        // Add error styling to output panels
        document.querySelectorAll('.output-panel').forEach(panel => {
            panel.classList.add('error');
        });
    }
    
    hideError() {
        document.getElementById('error-modal').style.display = 'none';
        
        // Remove error styling
        document.querySelectorAll('.output-panel').forEach(panel => {
            panel.classList.remove('error');
        });
    }
    
    updateStatus(message, type = 'info') {
        const statusText = document.getElementById('status-text');
        statusText.textContent = message;
        
        // Add visual feedback based on type
        statusText.className = `status-${type}`;
        
        // Remove status class after a delay
        setTimeout(() => {
            if (statusText.className === `status-${type}`) {
                statusText.className = '';
            }
        }, 3000);
    }
    
    setLoading(loading) {
        this.isLoading = loading;
        const buttons = document.querySelectorAll('.action-btn');
        
        buttons.forEach(btn => {
            btn.disabled = loading;
            if (loading) {
                btn.classList.add('loading');
            } else {
                btn.classList.remove('loading');
            }
        });
        
        if (loading) {
            document.querySelector('.container').style.cursor = 'wait';
        } else {
            document.querySelector('.container').style.cursor = 'default';
        }
    }
    
    updateForcePower() {
        const code = this.getEditorContent();
        const lines = code.split('\\n').filter(line => line.trim()).length;
        
        // Calculate force power based on code complexity
        let power = Math.min(100, Math.max(0, lines * 2));
        
        // Bonus points for using Force keywords
        const forceKeywords = ['order', 'ability', 'holocron', 'respond', 'sense', 'meditate', 'train'];
        let keywordCount = 0;
        
        forceKeywords.forEach(keyword => {
            const matches = (code.match(new RegExp('\\\\b' + keyword + '\\\\b', 'g')) || []).length;
            keywordCount += matches;
        });
        
        power = Math.min(100, power + keywordCount * 3);
        
        this.forcePowerLevel = power;
        this.animateForcePower(power);
    }
    
    animateForcePower(targetPower) {
        const powerFill = document.getElementById('power-level');
        const currentPower = this.forcePowerLevel;
        
        // Animate to target power
        const steps = 30;
        const increment = (targetPower - currentPower) / steps;
        let currentStep = 0;
        
        const animate = () => {
            if (currentStep < steps) {
                const newPower = currentPower + (increment * currentStep);
                powerFill.style.width = newPower + '%';
                
                // Change color based on power level
                if (newPower < 30) {
                    powerFill.style.background = 'linear-gradient(90deg, #ff073a, #ff4444)';
                    powerFill.style.boxShadow = '0 0 10px rgba(255, 7, 58, 0.5)';
                } else if (newPower < 70) {
                    powerFill.style.background = 'linear-gradient(90deg, #ffa500, #ffcc00)';
                    powerFill.style.boxShadow = '0 0 10px rgba(255, 165, 0, 0.5)';
                } else {
                    powerFill.style.background = 'linear-gradient(90deg, #00ff41, #00d4ff)';
                    powerFill.style.boxShadow = '0 0 10px rgba(0, 255, 65, 0.5)';
                }
                
                currentStep++;
                requestAnimationFrame(animate);
            } else {
                this.forcePowerLevel = targetPower;
                powerFill.style.width = targetPower + '%';
            }
        };
        
        animate();
    }
    
    setupTheme() {
        // Load saved theme or default to dark
        const savedTheme = localStorage.getItem('force-theme') || 'dark';
        this.setTheme(savedTheme);
    }
    
    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }
    
    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('force-theme', theme);
        
        const themeButton = document.getElementById('theme-toggle');
        const icon = themeButton.querySelector('.btn-icon');
        
        if (theme === 'light') {
            icon.textContent = '☀️';
            themeButton.title = 'Switch to Dark Theme';
        } else {
            icon.textContent = '🌙';
            themeButton.title = 'Switch to Light Theme';
        }
    }
    
    exportCode() {
        const code = this.getEditorContent();
        if (!code.trim()) {
            this.updateStatus('No code to export', 'warning');
            return;
        }
        
        // Create a downloadable file
        const blob = new Blob([code], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = 'force_program.force';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.updateStatus('Code exported successfully', 'success');
    }
}

// Initialize the UI when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.forceUI = new ForceUI();
    
    // Add some Star Wars flair
    console.log(`
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║              THE FORCE PROGRAMMING LANGUAGE                   ║
    ║                                                               ║
    ║              "Do or do not, there is no try"                  ║
    ║                        - Master Yoda                         ║
    ║                                                               ║
    ║              May the Force be with you, young developer!      ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    
    Keyboard Shortcuts:
    • Ctrl+Enter / Cmd+Enter: Run code
    • Ctrl+B / Cmd+B: Compile code  
    • Ctrl+K / Cmd+K: Clear editor
    • Ctrl+S / Cmd+S: Export code
    • Ctrl+T / Cmd+T: Toggle theme
    
    New Features Added:
    • Advanced data structures (stacks, queues)
    • JSON processing (data_stream)
    • Date/time operations (galactic_time)
    • Encryption functions (force_encrypt)
    • Regular expressions (regex_pattern)
    • Hash functions (force_hash)
    `);
});

// Export for potential module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ForceUI;
}
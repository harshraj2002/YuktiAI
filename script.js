//YuktiAI JavaScript Interface
class YuktiAI {
    constructor() {
        this.isConnected = false;
        this.isTyping = false;
        this.chatHistory = [];
        this.settings = {
            temperature: 0.7,
            maxLength: 1000
        };
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.updateWelcomeTime();
        this.checkConnection();
        this.loadSettings();
        
        //Auto-resize textarea
        this.setupTextareaAutoResize();
    }
    
    setupEventListeners() {
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');
        
        //Send message on Enter (but not Shift+Enter)
        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        //Character count
        messageInput.addEventListener('input', this.updateCharCount);
        
        //Settings
        const tempSlider = document.getElementById('temperatureSlider');
        tempSlider.addEventListener('input', (e) => {
            document.getElementById('temperatureValue').textContent = e.target.value;
        });
    }
    
    setupTextareaAutoResize() {
        const textarea = document.getElementById('messageInput');
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    }
    
    updateWelcomeTime() {
        const now = new Date();
        document.getElementById('welcomeTime').textContent = 
            now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    }
    
    async checkConnection() {
        try {
            const response = await fetch('http://localhost:11434/api/tags');
            if (response.ok) {
                this.setConnectionStatus(true);
            } else {
                this.setConnectionStatus(false);
            }
        } catch (error) {
            this.setConnectionStatus(false);
        }
    }
    
    setConnectionStatus(connected) {
        this.isConnected = connected;
        const statusDot = document.querySelector('.status-dot');
        const statusText = document.querySelector('.status-text');
        
        if (connected) {
            statusDot.className = 'status-dot';
            statusText.textContent = 'Connected';
        } else {
            statusDot.className = 'status-dot offline';
            statusText.textContent = 'Disconnected';
        }
    }
    
    async sendMessage() {
        const input = document.getElementById('messageInput');
        const message = input.value.trim();
        
        if (!message || this.isTyping) return;
        
        //Add user message
        this.addMessage('user', message);
        input.value = '';
        this.updateCharCount();
        
        //Show typing indicator
        this.showTypingIndicator();
        
        try {
            //Get AI response
            const response = await this.getAIResponse(message);
            this.hideTypingIndicator();
            this.addMessage('assistant', response);
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage('assistant', 'Sorry, I encountered an error. Please make sure Ollama is running and try again.');
        }
    }
    
    async getAIResponse(message) {
        //First check if it's a built-in command
        const builtInResponse = this.handleBuiltInCommands(message);
        if (builtInResponse) {
            return builtInResponse;
        }
        
        //Make request to Ollama
        const response = await fetch('http://localhost:11434/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                model: 'llama3.2:3b',
                prompt: this.buildPrompt(message),
                stream: false,
                options: {
                    temperature: this.settings.temperature,
                    num_predict: this.settings.maxLength,
                    top_p: 0.9,
                    top_k: 40
                }
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to get response from Ollama');
        }
        
        const data = await response.json();
        return this.formatResponse(data.response);
    }
    
    buildPrompt(message) {
        const systemPrompt = `You are YuktiAI, an intelligent and helpful AI assistant. You provide accurate, well-structured, and professional responses across all domains.

IMPORTANT GUIDELINES:
- You are YuktiAI - a standalone AI assistant
- NEVER redirect users to Google, other search engines, or external AI tools
- Provide complete, comprehensive answers based on your knowledge
- Use clear formatting with bullets, numbers, or sections when appropriate
- If uncertain, acknowledge limitations rather than making things up
- Stay professional and helpful at all times

Previous conversations:
${this.getRecentContext()}

Current question: ${message}

YuktiAI:`;
        
        return systemPrompt;
    }
    
    getRecentContext() {
        //Get last 4 messages for context
        const recent = this.chatHistory.slice(-4);
        return recent.map(msg => `${msg.role}: ${msg.content}`).join('\n');
    }
    
    formatResponse(response) {
        if (!response) return "I apologize, but I couldn't generate a response.";
        
        //Clean up the response
        let formatted = response.trim();
        
        //Add proper ending punctuation if missing
        if (formatted && !formatted.match(/[.!?:]$/)) {
            formatted += '.';
        }
        
        return formatted;
    }
    
    handleBuiltInCommands(message) {
        const lowerMessage = message.toLowerCase();
        
        if (lowerMessage.includes('what is yukti') || lowerMessage.includes('about yukti')) {
            return `**About YuktiAI:**

YuktiAI is an intelligent AI assistant that provides comprehensive answers without external redirections.

**🌟 Key Capabilities:**
• Answer questions across multiple domains
• Provide coding solutions and explanations
• Help with academic and business queries
• Maintain conversation context
• Format responses professionally

**⚠️ Current Limitations:**
• Cannot browse the internet
• Cannot access external APIs
• Knowledge cutoff applies
• Cannot perform real-time data retrieval`;
        }
        
        if (lowerMessage.includes('clear') && lowerMessage.includes('chat')) {
            this.clearChat();
            return "Chat history has been cleared!";
        }
        
        return null;
    }
    
    addMessage(role, content) {
        const message = { role, content, timestamp: new Date().toISOString() };
        this.chatHistory.push(message);
        
        const messagesContainer = document.getElementById('chatMessages');
        const messageElement = this.createMessageElement(message);
        messagesContainer.appendChild(messageElement);
        
        //Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    createMessageElement(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${message.role}-message`;
        
        const avatar = message.role === 'user' ? '👤' : '🤖';
        const name = message.role === 'user' ? 'You' : 'YuktiAI';
        const time = new Date(message.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        messageDiv.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                <div class="message-header">
                    <span class="sender-name">${name}</span>
                    <span class="message-time">${time}</span>
                </div>
                <div class="message-text">${this.parseMarkdown(message.content)}</div>
            </div>
        `;
        
        return messageDiv;
    }
    
    parseMarkdown(text) {
        //Simple markdown parsing
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/``````/g, '<pre><code>$1</code></pre>')
            .replace(/^• (.+)$/gm, '<ul><li>$1</li></ul>')
            .replace(/^\d+\. (.+)$/gm, '<ol><li>$1</li></ol>')
            .replace(/\n/g, '<br>');
    }
    
    showTypingIndicator() {
        this.isTyping = true;
        document.getElementById('loadingIndicator').style.display = 'flex';
        document.getElementById('sendButton').disabled = true;
        
        //Scroll to bottom
        const container = document.getElementById('chatMessages');
        container.scrollTop = container.scrollHeight;
    }
    
    hideTypingIndicator() {
        this.isTyping = false;
        document.getElementById('loadingIndicator').style.display = 'none';
        document.getElementById('sendButton').disabled = false;
    }
    
    updateCharCount() {
        const input = document.getElementById('messageInput');
        const count = input.value.length;
        document.getElementById('charCount').textContent = `${count}/2000`;
        
        //Change color if approaching limit
        const charCountElement = document.getElementById('charCount');
        if (count > 1800) {
            charCountElement.style.color = '#dc3545';
        } else if (count > 1500) {
            charCountElement.style.color = '#ffc107';
        } else {
            charCountElement.style.color = '#666';
        }
    }
    
    loadSettings() {
        const saved = localStorage.getItem('yuktiSettings');
        if (saved) {
            this.settings = { ...this.settings, ...JSON.parse(saved) };
            document.getElementById('temperatureSlider').value = this.settings.temperature;
            document.getElementById('temperatureValue').textContent = this.settings.temperature;
            document.getElementById('maxLengthSelect').value = this.settings.maxLength;
        }
    }
    
    saveSettings() {
        this.settings.temperature = parseFloat(document.getElementById('temperatureSlider').value);
        this.settings.maxLength = parseInt(document.getElementById('maxLengthSelect').value);
        
        localStorage.setItem('yuktiSettings', JSON.stringify(this.settings));
        alert('Settings saved!');
    }
}

//Global functions
function sendMessage() {
    yuktiAI.sendMessage();
}

function sendQuickMessage(message) {
    document.getElementById('messageInput').value = message;
    yuktiAI.sendMessage();
}

function clearChat() {
    yuktiAI.chatHistory = [];
    const messagesContainer = document.getElementById('chatMessages');
    //Keep only the welcome message
    const welcomeMessage = messagesContainer.firstElementChild;
    messagesContainer.innerHTML = '';
    messagesContainer.appendChild(welcomeMessage);
}

function toggleSettings() {
    const panel = document.getElementById('settingsPanel');
    panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
}

function saveSettings() {
    yuktiAI.saveSettings();
}

function exportChat() {
    const data = JSON.stringify(yuktiAI.chatHistory, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `yukti_chat_${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
}

function showAbout() {
    document.getElementById('modalTitle').textContent = 'About YuktiAI';
    document.getElementById('modalBody').innerHTML = `
        <h3>🤖 YuktiAI v1.0.0</h3>
        <p>Your intelligent AI assistant that provides comprehensive answers without external redirections.</p>
        
        <h4>Features:</h4>
        <ul>
            <li>Comprehensive answers across multiple domains</li>
            <li>No external redirections or dependencies</li>
            <li>Conversation memory and context</li>
            <li>Professional response formatting</li>
            <li>Offline operation with Ollama</li>
        </ul>
        
        <h4>Technology:</h4>
        <p>Built with Ollama (LLaMA 3.2), HTML5, CSS3, and vanilla JavaScript.</p>
    `;
    document.getElementById('infoModal').style.display = 'flex';
}

function showHelp() {
    document.getElementById('modalTitle').textContent = 'Help & Tips';
    document.getElementById('modalBody').innerHTML = `
        <h4>💡 Usage Tips:</h4>
        <ul>
            <li>Be specific in your questions for better results</li>
            <li>Ask follow-up questions for clarification</li>
            <li>Use clear, concise language</li>
            <li>Try different phrasings if needed</li>
        </ul>
        
        <h4>🎯 What YuktiAI can help with:</h4>
        <ul>
            <li>General knowledge questions</li>
            <li>Coding and programming help</li>
            <li>Academic subjects and research</li>
            <li>Business advice and analysis</li>
            <li>Step-by-step tutorials</li>
            <li>Comparisons and explanations</li>
        </ul>
        
        <h4>⚠️ Limitations:</h4>
        <ul>
            <li>Cannot browse the internet</li>
            <li>No real-time data access</li>
            <li>Requires Ollama to be running</li>
        </ul>
    `;
    document.getElementById('infoModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('infoModal').style.display = 'none';
}

//Initialize YuktiAI when page loads
let yuktiAI;
document.addEventListener('DOMContentLoaded', () => {
    yuktiAI = new YuktiAI();
});

//Check connection status periodically
setInterval(() => {
    if (yuktiAI) {
        yuktiAI.checkConnection();
    }
}, 30000); //Check every 30 seconds
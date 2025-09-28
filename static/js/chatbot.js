// AI Chatbot (Galgotias AI) with Enhanced Gemini API Integration
class AIChatbot {
    constructor() {
        this.apiKey = 'AIzaSyCvkXKq0NHwajkJd7u_4V2C2itq3nQpvyI';
        this.apiUrl = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent';
        this.isOpen = false;
        this.isTyping = false;
        
        console.log('Initializing Navya AI Chatbot with Gemini API...');
        this.init();
        this.bindEvents();
        this.showWelcomeMessage();
    }

    init() {
        this.toggle = document.querySelector('#chatbotToggle');
        this.window = document.querySelector('#chatbotWindow');
        this.closeBtn = document.querySelector('#chatbotClose');
        this.messagesContainer = document.querySelector('#chatbotMessages');
        this.inputField = document.querySelector('#chatbotInput');
        this.sendBtn = document.querySelector('#chatbotSend');
        this.quickBtns = document.querySelectorAll('.quick-btn');
        
        // Debug logging
        console.log('Chatbot elements found:', {
            toggle: !!this.toggle,
            window: !!this.window,
            closeBtn: !!this.closeBtn,
            messages: !!this.messagesContainer,
            input: !!this.inputField,
            sendBtn: !!this.sendBtn,
            quickBtns: this.quickBtns.length
        });
    }

    bindEvents() {
        // Add null checks and debugging
        if (this.toggle) {
            this.toggle.addEventListener('click', () => this.toggleChat());
            console.log('Toggle event bound');
        } else {
            console.error('Chatbot toggle button not found');
        }
        
        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', () => this.closeChat());
        }
        
        if (this.sendBtn) {
            this.sendBtn.addEventListener('click', () => this.sendMessage());
        }
        
        if (this.inputField) {
            this.inputField.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
        }
        
        this.quickBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const question = btn.getAttribute('data-question') || btn.textContent;
                if (this.inputField) {
                    this.inputField.value = question;
                    this.sendMessage();
                }
            });
        });
        
        console.log('Chatbot events bound successfully');
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        this.window.classList.toggle('active', this.isOpen);
        console.log('Chat toggled:', this.isOpen);
        
        if (this.isOpen && this.inputField) {
            setTimeout(() => this.inputField.focus(), 300);
        }
    }

    closeChat() {
        this.isOpen = false;
        this.window.classList.remove('active');
    }

    showWelcomeMessage() {
        // Clear existing messages and show initial welcome
        if (this.messagesContainer) {
            // Keep the existing HTML welcome message
            console.log('Welcome message container ready');
        }
    }

    addMessage(content, sender) {
        if (!this.messagesContainer) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const time = new Date().toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        
        messageDiv.innerHTML = `
            <div class="message-content">${content}</div>
            <div class="message-time">${time}</div>
        `;
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    showTypingIndicator() {
        if (this.isTyping || !this.messagesContainer) return;
        this.isTyping = true;
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-message';
        typingDiv.innerHTML = `
            <div class="typing-indicator">
                <span>Galgotias AI is thinking with Gemini AI...</span>
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        
        this.messagesContainer.appendChild(typingDiv);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        const typingMessage = this.messagesContainer?.querySelector('.typing-message');
        if (typingMessage) {
            typingMessage.remove();
        }
        this.isTyping = false;
    }

    scrollToBottom() {
        if (this.messagesContainer) {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }
    }

    async sendMessage() {
        const message = this.inputField?.value?.trim();
        if (!message) return;

        console.log('🚀 SENDING MESSAGE TO GEMINI AI:', message);

        // Add user message
        this.addMessage(message, 'user');
        this.inputField.value = '';

        // Show typing indicator
        this.showTypingIndicator();

        // FORCE GEMINI API CALL - NO FALLBACK INITIALLY
        console.log('⚡ CALLING GEMINI API DIRECTLY...');
        try {
            const response = await this.getGeminiResponse(message);
            this.hideTypingIndicator();
            console.log('✅ GEMINI API SUCCESS! Response received:', response.substring(0, 100) + '...');
            this.addMessage(response, 'bot');
        } catch (error) {
            console.error('❌ GEMINI API FAILED:', error);
            this.hideTypingIndicator();
            
            // Show detailed error info
            const errorMessage = `
                <div style="padding: 10px; border: 2px solid #ff4444; background: #ffe6e6; border-radius: 8px;">
                    <h6 style="color: #ff4444; margin: 0 0 10px 0;">🚨 Gemini API Error Details</h6>
                    <p><strong>Error:</strong> ${error.message}</p>
                    <p><strong>API Key Status:</strong> ${this.apiKey ? 'Present' : 'Missing'}</p>
                    <p><strong>API URL:</strong> ${this.apiUrl}</p>
                    <p><strong>Time:</strong> ${new Date().toLocaleString()}</p>
                </div>
                <br>
                ${this.getFallbackResponse(message, error)}
            `;
            this.addMessage(errorMessage, 'bot');
        }
    }

    async getGeminiResponse(userMessage) {
        console.log('🔄 GEMINI API CALL STARTING...');
        console.log('📝 User message:', userMessage);
        console.log('🔑 API Key:', this.apiKey ? 'PRESENT (' + this.apiKey.substring(0, 20) + '...)' : 'MISSING');
        console.log('🌐 API URL:', this.apiUrl);
        
        const simpleContext = `You are Galgotias AI, a helpful AI assistant for ICEIMS 2026 conference. 
        
Conference Info:
- Date: March 15-17, 2026
- Venue: Grand Convention Center, Tech City
- Theme: "Advancing Technology for Sustainable Innovation"
- Registration rates: Early Bird $150-450, Regular $200-550, Late $250-650
- Keynote Speakers: Dr. Sarah Chen (AI), Prof. Rodriguez (Sustainability), Dr. Patel (Innovation), Prof. Wilson (Digital)

Respond naturally and helpfully about the conference.`;

        const requestPayload = {
            contents: [{
                parts: [{
                    text: `${simpleContext}\n\nUser: ${userMessage}\n\nGalgotias AI:`
                }]
            }],
            generationConfig: {
                temperature: 0.8,
                maxOutputTokens: 500
            }
        };

        console.log('📤 REQUEST PAYLOAD:', JSON.stringify(requestPayload, null, 2));
        
        const fullUrl = `${this.apiUrl}?key=${this.apiKey}`;
        console.log('🎯 FULL REQUEST URL:', fullUrl.replace(this.apiKey, 'API_KEY_HIDDEN'));

        try {
            console.log('⏳ Making fetch request...');
            const response = await fetch(fullUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestPayload)
            });

            console.log('📥 RESPONSE STATUS:', response.status);
            console.log('📥 RESPONSE OK:', response.ok);
            console.log('📥 RESPONSE HEADERS:', [...response.headers.entries()]);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('❌ API ERROR RESPONSE:', errorText);
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }

            const data = await response.json();
            console.log('✅ GEMINI RESPONSE DATA:', JSON.stringify(data, null, 2));
            
            if (data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts && data.candidates[0].content.parts[0]) {
                const responseText = data.candidates[0].content.parts[0].text;
                console.log('🎉 GEMINI TEXT EXTRACTED:', responseText);
                return this.formatResponse(responseText);
            } else {
                console.error('❌ INVALID RESPONSE STRUCTURE:', data);
                throw new Error(`Invalid response structure: ${JSON.stringify(data)}`);
            }

        } catch (error) {
            console.error('🚨 GEMINI API CALL FAILED:', error);
            console.error('🚨 ERROR DETAILS:', {
                name: error.name,
                message: error.message,
                stack: error.stack
            });
            throw error;
        }
    }

    formatResponse(text) {
        // Convert markdown-style formatting to HTML
        let formatted = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>')
            .replace(/^/, '<p>')
            .replace(/$/, '</p>');
        
        // Fix multiple paragraph tags
        formatted = formatted.replace(/<p><\/p>/g, '');
        
        return formatted;
    }

    getFallbackResponse(userMessage, error) {
        console.log('Using fallback response for:', userMessage);
        
        const message = userMessage.toLowerCase();
        
        // Basic error acknowledgment
        let errorInfo = '';
        if (error.message.includes('API request failed')) {
            errorInfo = ' (API temporarily unavailable)';
        }
        
        // Simple pattern matching for key topics
        if (message.includes('registration') || message.includes('rate') || message.includes('price')) {
            return `
                <div style="padding: 10px; border-left: 4px solid #ff6b35; background: #fff8f5; margin: 10px 0; border-radius: 5px;">
                    <p><strong>🤖 Navya AI${errorInfo}</strong></p>
                    <h6 style="color: #ff6b35;">💰 Registration Rates for ICEIMS 2026</h6>
                    <p><strong>Early Bird (until Jan 15):</strong> Students $150 | Academics $300 | Industry $450</p>
                    <p><strong>Regular (until Feb 15):</strong> Students $200 | Academics $400 | Industry $550</p>
                    <p><strong>Late Registration:</strong> Students $250 | Academics $500 | Industry $650</p>
                    <p>� <strong>Registration Deadline:</strong> February 15, 2026</p>
                </div>
            `;
        }
        
        if (message.includes('speaker') || message.includes('keynote')) {
            return `
                <div style="padding: 10px; border-left: 4px solid #ff6b35; background: #fff8f5; margin: 10px 0; border-radius: 5px;">
                    <p><strong>🤖 Navya AI${errorInfo}</strong></p>
                    <h6 style="color: #ff6b35;">🎤 Keynote Speakers</h6>
                    <p><strong>🔬 Dr. Sarah Chen</strong> - AI & Robotics Expert</p>
                    <p><strong>🌱 Prof. Michael Rodriguez</strong> - Sustainability Researcher</p>
                    <p><strong>💡 Dr. Aisha Patel</strong> - Innovation Management</p>
                    <p><strong>🚀 Prof. James Wilson</strong> - Digital Transformation</p>
                </div>
            `;
        }
        
        if (message.includes('about') || message.includes('conference')) {
            return `
                <div style="padding: 10px; border-left: 4px solid #ff6b35; background: #fff8f5; margin: 10px 0; border-radius: 5px;">
                    <p><strong>🤖 Navya AI${errorInfo}</strong></p>
                    <h6 style="color: #ff6b35;">🎓 ICEIMS 2026</h6>
                    <p><strong>📅 Date:</strong> March 15-17, 2026</p>
                    <p><strong>🏢 Venue:</strong> Grand Convention Center, Tech City</p>
                    <p><strong>🎯 Theme:</strong> "Advancing Technology for Sustainable Innovation"</p>
                    <p>International Conference on Engineering, Innovation, Management, and Sciences</p>
                </div>
            `;
        }
        
        // Default fallback
        return `
            <div style="padding: 10px; border-left: 4px solid #ff6b35; background: #fff8f5; margin: 10px 0; border-radius: 5px;">
                <p><strong>🤖 Navya AI${errorInfo}</strong></p>
                <p>I'm your ICEIMS 2026 conference assistant! I can help with:</p>
                <ul style="margin: 10px 0; padding-left: 20px;">
                    <li>Registration rates and deadlines</li>
                    <li>Keynote speakers information</li>
                    <li>Conference details and schedule</li>
                    <li>Venue attractions and activities</li>
                </ul>
                <p style="color: #ff6b35;"><strong>What would you like to know about ICEIMS 2026?</strong></p>
            </div>
        `;
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Add a small delay to ensure all elements are rendered
    setTimeout(() => {
        console.log('Initializing Navya AI Chatbot with Gemini API...');
        try {
            new AIChatbot();
            console.log('✅ Gemini AI Chatbot initialized successfully!');
        } catch (error) {
            console.error('❌ Failed to initialize chatbot:', error);
        }
    }, 500);
});

// Handle chatbot visibility on mobile
window.addEventListener('resize', () => {
    const chatbot = document.querySelector('.ai-chatbot');
    if (chatbot) {
        if (window.innerWidth < 480) {
            chatbot.style.bottom = '15px';
            chatbot.style.right = '15px';
        } else {
            chatbot.style.bottom = '20px';
            chatbot.style.right = '20px';
        }
    }
});
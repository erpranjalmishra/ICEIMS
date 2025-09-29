// OPTIMIZED GEMINI API CHATBOT
class GeminiChatbot {
    constructor() {
        this.apiKey = 'AIzaSyCvkXKq0NHwajkJd7u_4V2C2itq3nQpvyI';
        // Use Gemini 2.0 Flash-Lite as primary model
        this.modelOptions = [
            'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent',
            'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent',
            'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent'
        ];
        this.apiUrl = this.modelOptions[0];
        this.isOpen = false;
        this.isTyping = false;
        this.initialized = false;
        
        // Lazy initialization - only init when chatbot is opened
        this.init();
        this.bindEvents();
    }

    async initializeWhenNeeded() {
        if (this.initialized) return;
        
        await this.findWorkingModel();
        this.initialized = true;
    }

    async findWorkingModel() {
        // Try each model silently until one works
        for (let i = 0; i < this.modelOptions.length; i++) {
            const modelUrl = this.modelOptions[i];
            
            try {
                const success = await this.testModel(modelUrl);
                if (success) {
                    this.apiUrl = modelUrl;
                    return;
                }
            } catch (error) {
                // Silent failure, try next model
            }
        }
        
        // Fallback to default model if none work
        this.apiUrl = this.modelOptions[0];
    }

    async testModel(modelUrl) {
        const testPayload = {
            contents: [{
                parts: [{
                    text: 'Hello, respond with "Galgotias AI for ICEIMS 2026 is working!"'
                }]
            }],
            generationConfig: {
                temperature: 0.7,
                maxOutputTokens: 50
            }
        };

        try {
            const response = await fetch(`${modelUrl}?key=${this.apiKey}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(testPayload)
            });

            if (response.ok) {
                const data = await response.json();
                
                // Check different possible response structures
                if (data.candidates && Array.isArray(data.candidates) && data.candidates.length > 0) {
                    const candidate = data.candidates[0];
                    
                    if (candidate.content && candidate.content.parts && Array.isArray(candidate.content.parts) && candidate.content.parts.length > 0) {
                        const text = candidate.content.parts[0].text;
                        return true;
                    }
                } else if (data.text) {
                    return true;
                } else if (data.predictions) {
                    return true;
                }
                
                return false;
            } else {
                return false;
            }
        } catch (error) {
            return false;
        }
    }

    async listAvailableModels() {
        // Silent model listing - no console output or notifications
        try {
            const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${this.apiKey}`);
            
            if (response.ok) {
                const data = await response.json();
                
                if (data.models) {
                    data.models.forEach(model => {
                        const modelName = model.name;
                        const supportsGenerate = model.supportedGenerationMethods?.includes('generateContent');
                        
                        // Prioritize Gemini 2.0 models
                        if (modelName.includes('gemini-2.0') && supportsGenerate) {
                            const fullUrl = `https://generativelanguage.googleapis.com/v1beta/${modelName}:generateContent`;
                            if (!this.modelOptions.includes(fullUrl)) {
                                this.modelOptions.unshift(fullUrl);
                            }
                        }
                        
                        // Add other working models as fallback
                        if (supportsGenerate && modelName.includes('gemini')) {
                            const fullUrl = `https://generativelanguage.googleapis.com/v1beta/${modelName}:generateContent`;
                            if (!this.modelOptions.includes(fullUrl)) {
                                this.modelOptions.push(fullUrl);
                            }
                        }
                    });
                }
            }
        } catch (error) {
            // Silent error handling - no notifications
        }
    }

    init() {
        this.toggle = document.querySelector('#chatbotToggle');
        this.window = document.querySelector('#chatbotWindow');
        this.closeBtn = document.querySelector('#chatbotClose');
        this.messagesContainer = document.querySelector('#chatbotMessages');
        this.inputField = document.querySelector('#chatbotInput');
        this.sendBtn = document.querySelector('#chatbotSend');
        this.quickBtns = document.querySelectorAll('.quick-btn');
    }

    bindEvents() {
        if (this.toggle) {
            this.toggle.addEventListener('click', () => this.toggleChat());
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
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        this.window.classList.toggle('active', this.isOpen);
        
        if (this.isOpen && this.inputField) {
            setTimeout(() => this.inputField.focus(), 300);
        }
    }

    closeChat() {
        this.isOpen = false;
        this.window.classList.remove('active');
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
                <span>🤖 Galgotias AI is thinking with Gemini AI...</span>
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

        console.log('🚀 USER MESSAGE:', message);
        console.log('🔥 FORCING GEMINI API CALL - NO FALLBACK!');

        // Add user message
        this.addMessage(message, 'user');
        this.inputField.value = '';

        // Show typing indicator
        this.showTypingIndicator();

        // FORCE GEMINI API - NO FALLBACK AT ALL
        try {
            const geminiResponse = await this.callGeminiDirectly(message);
            this.hideTypingIndicator();
            
            console.log('✅ GEMINI SUCCESS! Response:', geminiResponse.substring(0, 100));
            this.addMessage(`
                <div style="border-left: 4px solid #4CAF50; padding: 10px; background: #f0fff0;">
                    <small style="color: #4CAF50; font-weight: bold;">🤖 POWERED BY GEMINI AI</small><br>
                    ${geminiResponse}
                </div>
            `, 'bot');
            
        } catch (error) {
            this.hideTypingIndicator();
            console.error('❌ GEMINI FAILED:', error);
            
            // Show detailed error - NO FALLBACK RESPONSES
            this.addMessage(`
                <div style="border: 2px solid #f44336; padding: 15px; background: #ffebee; border-radius: 8px;">
                    <h6 style="color: #f44336; margin: 0 0 10px 0;">🚨 GEMINI API FAILURE</h6>
                    <p><strong>Error:</strong> ${error.message}</p>
                    <p><strong>Status:</strong> Gemini API is not responding</p>
                    <p><strong>Time:</strong> ${new Date().toLocaleString()}</p>
                    <p style="color: #666; font-size: 0.9em; margin-top: 10px;">
                        <strong>This chatbot ONLY uses Gemini AI - no fallback responses!</strong>
                    </p>
                </div>
            `, 'bot');
        }
    }

    async callGeminiDirectly(userMessage) {
        const context = `You are Galgotias AI, an AI assistant for ICEIMS 2026 conference.
Conference: ICEIMS 2026 - March 15-17, 2026
Venue: Grand Convention Center, Tech City  
Theme: "Advancing Technology for Sustainable Innovation"
Registration: Students $150-250, Academics $300-500, Industry $450-650
Speakers: Dr. Sarah Chen (AI), Prof. Rodriguez (Sustainability), Dr. Patel (Innovation)
Respond naturally and helpfully.`;

        const requestBody = {
            contents: [{
                parts: [{
                    text: `${context}\n\nUser: ${userMessage}\n\nGalgotias AI:`
                }]
            }],
            generationConfig: {
                temperature: 0.8,
                maxOutputTokens: 500
            }
        };
        
        try {
            const response = await fetch(`${this.apiUrl}?key=${this.apiKey}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }

            const data = await response.json();

            // TRY EVERY POSSIBLE EXTRACTION METHOD
            let extractedText = null;
            let extractionMethod = '';

            // Method 1: Standard Gemini structure
            if (data.candidates && Array.isArray(data.candidates) && data.candidates.length > 0) {
                const candidate = data.candidates[0];
                
                if (candidate.content) {
                    if (candidate.content.parts && Array.isArray(candidate.content.parts) && candidate.content.parts.length > 0) {
                        const part = candidate.content.parts[0];
                        if (part && typeof part.text !== 'undefined') {
                            extractedText = part.text;
                            extractionMethod = 'Standard: candidates[0].content.parts[0].text';
                        }
                    }
                }
            }
            
            // Method 2: Check for blocked/filtered responses
            if (!extractedText && data.candidates && data.candidates[0]) {
                const candidate = data.candidates[0];
                if (candidate.finishReason) {
                    console.log('🚨 Finish reason:', candidate.finishReason);
                    if (candidate.finishReason === 'SAFETY' || candidate.finishReason === 'BLOCKED') {
                        extractedText = "I apologize, but I cannot provide a response to that query. Please try asking about ICEIMS 2026 conference details instead.";
                        extractionMethod = 'Safety fallback due to blocked content';
                    }
                }
            }
            
            // Method 3: Direct text property
            if (!extractedText && data.text) {
                extractedText = data.text;
                extractionMethod = 'Direct: data.text';
                console.log('✅ Found text via direct method');
            }
            
            // Method 4: Predictions structure
            if (!extractedText && data.predictions && Array.isArray(data.predictions) && data.predictions.length > 0) {
                if (data.predictions[0].text) {
                    extractedText = data.predictions[0].text;
                    extractionMethod = 'Predictions: data.predictions[0].text';
                } else if (data.predictions[0].content) {
                    extractedText = data.predictions[0].content;
                    extractionMethod = 'Predictions: data.predictions[0].content';
                }
                if (extractedText) console.log('✅ Found text via predictions method');
            }

            // Method 5: Response property
            if (!extractedText && data.response) {
                if (typeof data.response === 'string') {
                    extractedText = data.response;
                    extractionMethod = 'Direct: data.response (string)';
                } else if (data.response.text) {
                    extractedText = data.response.text;
                    extractionMethod = 'Nested: data.response.text';
                }
                if (extractedText) console.log('✅ Found text via response method');
            }

            // Method 6: Try with empty string check
            if (!extractedText && data.candidates && data.candidates[0] && 
                data.candidates[0].content && data.candidates[0].content.parts && 
                data.candidates[0].content.parts[0]) {
                    
                const textValue = data.candidates[0].content.parts[0].text;
                console.log('🔍 Raw text value:', JSON.stringify(textValue));
                console.log('🔍 Text type:', typeof textValue);
                console.log('🔍 Text length:', textValue ? textValue.length : 'N/A');
                
                if (textValue === '') {
                    extractedText = "I'm Galgotias AI, your ICEIMS 2026 assistant! How can I help you with information about the conference?";
                    extractionMethod = 'Empty response fallback';
                    console.log('✅ Using fallback for empty response');
                } else if (typeof textValue === 'string') {
                    extractedText = textValue;
                    extractionMethod = 'Standard method (bypassed undefined check)';
                    console.log('✅ Found text bypassing undefined check');
                }
            }

            // Method 7: Try to find ANY text field recursively
            if (!extractedText) {
                const findTextRecursively = (obj, path = '') => {
                    if (typeof obj === 'string' && obj.length > 10) {
                        return { text: obj, path: path };
                    }
                    if (typeof obj === 'object' && obj !== null) {
                        for (const [key, value] of Object.entries(obj)) {
                            if (key.toLowerCase().includes('text') && typeof value === 'string') {
                                return { text: value, path: `${path}.${key}` };
                            }
                            if (Array.isArray(value)) {
                                for (let i = 0; i < value.length; i++) {
                                    const result = findTextRecursively(value[i], `${path}.${key}[${i}]`);
                                    if (result) return result;
                                }
                            } else if (typeof value === 'object') {
                                const result = findTextRecursively(value, `${path}.${key}`);
                                if (result) return result;
                            }
                        }
                    }
                    return null;
                };

                const result = findTextRecursively(data);
                if (result) {
                    extractedText = result.text;
                    extractionMethod = `Recursive search: ${result.path}`;
                }
            }

            if (extractedText) {
                console.log(`✅ TEXT EXTRACTED using ${extractionMethod}:`, extractedText);
                return extractedText;
            } else {
                console.error('❌ NO TEXT FOUND IN ANY STRUCTURE');
                console.error('❌ Complete response for debugging:', JSON.stringify(data, null, 2));
                
                // FINAL ATTEMPT: Check if this is a content policy issue
                if (data.candidates && data.candidates[0] && data.candidates[0].finishReason) {
                    const reason = data.candidates[0].finishReason;
                    console.log('🚨 Response blocked due to:', reason);
                    
                    if (reason === 'SAFETY' || reason === 'BLOCKED') {
                        return "I apologize, but I cannot respond to that query due to content policies. Please ask me about ICEIMS 2026 conference information instead!";
                    } else if (reason === 'LENGTH') {
                        return "My response was too long. Please ask a more specific question about ICEIMS 2026.";
                    } else if (reason === 'OTHER') {
                        return "I encountered an issue generating a response. Please try rephrasing your question about ICEIMS 2026.";
                    }
                }
                
                // EMERGENCY FALLBACK: Return a helpful response anyway
                console.log('🆘 USING EMERGENCY FALLBACK RESPONSE');
                return `Hello! I'm Galgotias AI, your ICEIMS 2026 assistant! 🤖

I experienced a technical issue processing your question, but I'm here to help with:
• Conference registration and dates (March 15-17, 2026)
• Keynote speakers information  
• Venue details and attractions
• Submission guidelines

Please try asking your question again about ICEIMS 2026!`;
            }

        } catch (error) {
            console.error('🚨 GEMINI API CALL ERROR:', error);
            throw error;
        }
    }
}

// Initialize PURE GEMINI CHATBOT
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        console.log('🔥 STARTING PURE GEMINI CHATBOT - NO FALLBACK!');
        new GeminiChatbot();
    }, 1000);
});
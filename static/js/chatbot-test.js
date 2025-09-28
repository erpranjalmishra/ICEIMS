// Simple test version of the chatbot
console.log('Chatbot test script loaded');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing test chatbot...');
    
    const toggle = document.getElementById('chatbotToggle');
    const window = document.getElementById('chatbotWindow');
    const closeBtn = document.getElementById('chatbotClose');
    const sendBtn = document.getElementById('chatbotSend');
    const input = document.getElementById('chatbotInput');
    const messages = document.getElementById('chatbotMessages');
    
    console.log('Elements found:', {
        toggle: !!toggle,
        window: !!window,
        closeBtn: !!closeBtn,
        sendBtn: !!sendBtn,
        input: !!input,
        messages: !!messages
    });
    
    if (!toggle || !window) {
        console.error('Critical chatbot elements not found!');
        return;
    }
    
    let isOpen = false;
    
    // Toggle chat
    toggle.addEventListener('click', function() {
        console.log('Toggle clicked');
        isOpen = !isOpen;
        window.classList.toggle('active', isOpen);
        if (isOpen && input) {
            input.focus();
        }
    });
    
    // Close chat
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            console.log('Close clicked');
            isOpen = false;
            window.classList.remove('active');
        });
    }
    
    // Send message function
    function sendMessage() {
        if (!input || !messages) return;
        
        const message = input.value.trim();
        if (!message) return;
        
        console.log('Sending message:', message);
        
        // Add user message
        const userDiv = document.createElement('div');
        userDiv.className = 'message user-message';
        userDiv.innerHTML = `
            <div class="message-content">${message}</div>
            <div class="message-time">${new Date().toLocaleTimeString('en-US', {hour: '2-digit', minute: '2-digit'})}</div>
        `;
        messages.appendChild(userDiv);
        
        input.value = '';
        
        // Add bot response
        setTimeout(() => {
            const botDiv = document.createElement('div');
            botDiv.className = 'message bot-message';
            
            let response = getSimpleResponse(message);
            
            botDiv.innerHTML = `
                <div class="message-content">${response}</div>
                <div class="message-time">${new Date().toLocaleTimeString('en-US', {hour: '2-digit', minute: '2-digit'})}</div>
            `;
            messages.appendChild(botDiv);
            messages.scrollTop = messages.scrollHeight;
        }, 500);
        
        messages.scrollTop = messages.scrollHeight;
    }
    
    // Enhanced multilingual response function
    function getSimpleResponse(message) {
        const msg = message.toLowerCase();
        
        // Language detection helper
        function detectLanguage(text) {
            const spanish = /\b(hola|qué|cómo|cuándo|dónde|precio|registro|conferencia|información)\b/i;
            const french = /\b(bonjour|comment|quand|où|prix|inscription|conférence|information)\b/i;
            const german = /\b(hallo|wie|wann|wo|preis|anmeldung|konferenz|information)\b/i;
            const chinese = /(你好|什么|怎么|什么时候|哪里|价格|注册|会议|信息)/;
            const japanese = /(こんにちは|何|どう|いつ|どこ|価格|登録|会議|情報)/;
            const hindi = /(नमस्ते|क्या|कैसे|कब|कहाँ|मूल्य|पंजीकरण|सम्मेलन|जानकारी)/;
            
            if (spanish.test(text)) return 'es';
            if (french.test(text)) return 'fr';
            if (german.test(text)) return 'de';
            if (chinese.test(text)) return 'zh';
            if (japanese.test(text)) return 'ja';
            if (hindi.test(text)) return 'hi';
            return 'en';
        }
        
        const language = detectLanguage(message);
        
        // Enhanced natural language patterns
        const patterns = {
            registration: /\b(registration|register|sign up|enroll|rates?|price|cost|fee|registro|inscription|anmeldung|पंजीकरण|注册|登録)\b/i,
            speakers: /\b(speaker|keynote|presenter|talk|presentation|orador|conférencier|redner|वक्ता|演讲者|講演者)\b/i,
            about: /\b(about|what is|tell me|information|conference|iceims|acerca|à propos|über|के बारे में|关于|について)\b/i,
            schedule: /\b(schedule|program|agenda|time|when|timing|horario|programme|zeitplan|कार्यक्रम|时间表|スケジュール)\b/i,
            location: /\b(where|location|venue|address|direction|place|dónde|où|wo|कहाँ|地点|場所)\b/i,
            attractions: /\b(attraction|tourist|visit|see|sightseeing|place|atracción|attraction|sehenswürdigkeit|आकर्षण|景点|観光)\b/i,
            submission: /\b(submit|paper|abstract|deadline|guideline|enviar|soumettre|einreichen|जमा|提交|提出)\b/i,
            awards: /\b(award|prize|recognition|winner|premio|prix|auszeichnung|पुरस्कार|奖项|賞)\b/i,
            contact: /\b(contact|help|support|email|phone|contacto|contact|kontakt|संपर्क|联系|連絡)\b/i,
            workshop: /\b(workshop|event|session|panel|taller|atelier|workshop|कार्यशाला|研讨会|ワークショップ)\b/i,
            tracks: /\b(track|topic|theme|area|subject|tema|sujet|thema|विषय|主题|トピック)\b/i,
            greeting: /\b(hello|hi|hey|good morning|good afternoon|hola|bonjour|hallo|नमस्ते|你好|こんにちは)\b/i,
            thanks: /\b(thank|thanks|great|good|excellent|gracias|merci|danke|धन्यवाद|谢谢|ありがとう)\b/i,
            help: /\b(help|assist|support|can you|could you|ayuda|aide|hilfe|मदद|帮助|助けて)\b/i
        };
        
        // Multi-language responses
        const responses = {
            en: {
                registration: {
                    title: "💰 Registration Rates for ICEIMS 2026",
                    earlyBird: "Early Bird (until Jan 15, 2026):",
                    regular: "Regular (until Feb 15, 2026):",
                    late: "Late Registration (after Feb 15, 2026):",
                    deadline: "📝 Registration Deadline: February 15, 2026"
                },
                greeting: {
                    title: "Hello! I'm Galgotias AI, your ICEIMS 2026 assistant! 🤖",
                    subtitle: "I can help you in multiple languages including English, Spanish, French, German, Hindi, Chinese, and Japanese!"
                },
                thanks: {
                    title: "😊 Thank You!",
                    message: "I'm glad I could help you with ICEIMS 2026 information!"
                }
            },
            es: {
                registration: {
                    title: "💰 Tarifas de Registro para ICEIMS 2026",
                    earlyBird: "Registro Temprano (hasta 15 de enero, 2026):",
                    regular: "Registro Regular (hasta 15 de febrero, 2026):",
                    late: "Registro Tardío (después del 15 de febrero, 2026):",
                    deadline: "📝 Fecha límite de registro: 15 de febrero, 2026"
                },
                greeting: {
                    title: "¡Hola! ¡Soy Galgotias AI, tu asistente de ICEIMS 2026! 🤖",
                    subtitle: "¡Puedo ayudarte en múltiples idiomas incluyendo inglés, español, francés, alemán, hindi, chino y japonés!"
                },
                thanks: {
                    title: "😊 ¡Gracias!",
                    message: "¡Me alegra poder ayudarte con información sobre ICEIMS 2026!"
                }
            },
            fr: {
                registration: {
                    title: "💰 Tarifs d'inscription pour ICEIMS 2026",
                    earlyBird: "Inscription anticipée (jusqu'au 15 janvier 2026):",
                    regular: "Inscription régulière (jusqu'au 15 février 2026):",
                    late: "Inscription tardive (après le 15 février 2026):",
                    deadline: "📝 Date limite d'inscription: 15 février 2026"
                },
                greeting: {
                    title: "Bonjour! Je suis Galgotias AI, votre assistant ICEIMS 2026! 🤖",
                    subtitle: "Je peux vous aider dans plusieurs langues dont l'anglais, l'espagnol, le français, l'allemand, l'hindi, le chinois et le japonais!"
                },
                thanks: {
                    title: "😊 Merci!",
                    message: "Je suis ravi de pouvoir vous aider avec les informations sur ICEIMS 2026!"
                }
            },
            de: {
                registration: {
                    title: "💰 Anmeldegebühren für ICEIMS 2026",
                    earlyBird: "Frühbucher (bis 15. Januar 2026):",
                    regular: "Reguläre Anmeldung (bis 15. Februar 2026):",
                    late: "Späte Anmeldung (nach 15. Februar 2026):",
                    deadline: "📝 Anmeldeschluss: 15. Februar 2026"
                },
                greeting: {
                    title: "Hallo! Ich bin Galgotias AI, Ihr ICEIMS 2026 Assistent! 🤖",
                    subtitle: "Ich kann Ihnen in mehreren Sprachen helfen, einschließlich Englisch, Spanisch, Französisch, Deutsch, Hindi, Chinesisch und Japanisch!"
                },
                thanks: {
                    title: "😊 Vielen Dank!",
                    message: "Ich freue mich, Ihnen mit Informationen zu ICEIMS 2026 helfen zu können!"
                }
            },
            hi: {
                registration: {
                    title: "💰 ICEIMS 2026 के लिए पंजीकरण दरें",
                    earlyBird: "अर्ली बर्ड (15 जनवरी, 2026 तक):",
                    regular: "नियमित (15 फरवरी, 2026 तक):",
                    late: "देर से पंजीकरण (15 फरवरी, 2026 के बाद):",
                    deadline: "📝 पंजीकरण की अंतिम तिथि: 15 फरवरी, 2026"
                },
                greeting: {
                    title: "नमस्ते! मैं नव्या हूँ, आपकी ICEIMS 2026 सहायक! 🤖",
                    subtitle: "मैं अंग्रेजी, स्पेनिश, फ्रेंच, जर्मन, हिंदी, चीनी और जापानी सहित कई भाषाओं में आपकी मदद कर सकती हूँ!"
                },
                thanks: {
                    title: "😊 धन्यवाद!",
                    message: "मुझे खुशी है कि मैं ICEIMS 2026 की जानकारी के साथ आपकी मदद कर सकी!"
                }
            },
            zh: {
                registration: {
                    title: "💰 ICEIMS 2026 注册费用",
                    earlyBird: "早鸟价 (截至2026年1月15日):",
                    regular: "常规价格 (截至2026年2月15日):",
                    late: "延期注册 (2026年2月15日之后):",
                    deadline: "📝 注册截止日期: 2026年2月15日"
                },
                greeting: {
                    title: "你好！我是Galgotias AI，你的ICEIMS 2026助手！🤖",
                    subtitle: "我可以用多种语言为您提供帮助，包括英语、西班牙语、法语、德语、印地语、中文和日语！"
                },
                thanks: {
                    title: "😊 谢谢！",
                    message: "我很高兴能为您提供ICEIMS 2026的信息！"
                }
            },
            ja: {
                registration: {
                    title: "💰 ICEIMS 2026 登録料金",
                    earlyBird: "早期割引 (2026年1月15日まで):",
                    regular: "通常料金 (2026年2月15日まで):",
                    late: "遅延登録 (2026年2月15日以降):",
                    deadline: "📝 登録締切日: 2026年2月15日"
                },
                greeting: {
                    title: "こんにちは！私はGalgotias AI、あなたのICEIMS 2026アシスタントです！🤖",
                    subtitle: "英語、スペイン語、フランス語、ドイツ語、ヒンディー語、中国語、日本語など、複数の言語でお手伝いできます！"
                },
                thanks: {
                    title: "😊 ありがとうございます！",
                    message: "ICEIMS 2026の情報をお手伝いできて嬉しいです！"
                }
            }
        };
        
        // Pattern matching with multilingual support
        if (patterns.greeting.test(msg)) {
            const lang = responses[language] || responses.en;
            return `
            <div class="response-content">
                <h6 style="color: #ff6b35; margin-bottom: 15px;">${lang.greeting.title}</h6>
                <p style="color: #333; margin-bottom: 15px;">${lang.greeting.subtitle}</p>
                
                <div style="margin-bottom: 12px;">
                    <strong style="color: #333;">I can help you with / Puedo ayudarte con / Je peux vous aider avec:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li>Conference information / Información de la conferencia / Informations sur la conférence</li>
                        <li>Registration rates / Tarifas de registro / Tarifs d'inscription</li>
                        <li>Keynote speakers / Oradores principales / Conférenciers principaux</li>
                        <li>Tourist attractions / Atracciones turísticas / Attractions touristiques</li>
                    </ul>
                </div>
                
                <p style="margin-top: 15px; color: #ff6b35; font-weight: 600;">
                    What would you like to know? / ¿Qué te gustaría saber? / Que voulez-vous savoir?
                </p>
            </div>`;
        }
        
        if (patterns.thanks.test(msg)) {
            const lang = responses[language] || responses.en;
            return `
            <div class="response-content">
                <h6 style="color: #ff6b35; margin-bottom: 15px;">${lang.thanks.title}</h6>
                <p style="color: #333; margin-bottom: 15px;">${lang.thanks.message}</p>
                
                <p style="color: #666; font-size: 0.9em; margin-bottom: 15px;">
                    Ask me anything in your preferred language! / ¡Pregúntame en tu idioma preferido! / Posez-moi des questions dans votre langue préférée!
                </p>
                
                <div style="margin-top: 15px;">
                    <strong style="color: #333;">🌍 Supported Languages:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.85em;">
                        <li>🇺🇸 English</li>
                        <li>🇪🇸 Español</li>
                        <li>🇫🇷 Français</li>
                        <li>🇩🇪 Deutsch</li>
                        <li>🇮🇳 हिंदी</li>
                        <li>🇨🇳 中文</li>
                        <li>🇯🇵 日本語</li>
                    </ul>
                </div>
            </div>`;
        }
        
        if (patterns.registration.test(msg)) {
            const lang = responses[language] || responses.en;
            return `
            <div class="response-content">
                <h6 style="color: #ff6b35; margin-bottom: 10px;">${lang.registration.title}</h6>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">${lang.registration.earlyBird}</strong>
                    <ul style="margin: 5px 0; padding-left: 20px;">
                        <li>Students: <strong>$150</strong></li>
                        <li>Academics: <strong>$300</strong></li>
                        <li>Industry: <strong>$450</strong></li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">${lang.registration.regular}</strong>
                    <ul style="margin: 5px 0; padding-left: 20px;">
                        <li>Students: <strong>$200</strong></li>
                        <li>Academics: <strong>$400</strong></li>
                        <li>Industry: <strong>$550</strong></li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong style="color: #333;">${lang.registration.late}</strong>
                    <ul style="margin: 5px 0; padding-left: 20px;">
                        <li>Students: <strong>$250</strong></li>
                        <li>Academics: <strong>$500</strong></li>
                        <li>Industry: <strong>$650</strong></li>
                    </ul>
                </div>
                
                <p style="margin-top: 15px; color: #666; font-size: 0.9em;">
                    ${lang.registration.deadline}
                </p>
            </div>`;
        }
        
        // Enhanced natural language understanding for speakers
        if (patterns.speakers.test(msg)) {
            const speakerTitles = {
                en: "🎤 Keynote Speakers at ICEIMS 2026",
                es: "🎤 Oradores Principales en ICEIMS 2026",
                fr: "🎤 Conférenciers Principaux à ICEIMS 2026",
                de: "🎤 Hauptredner bei ICEIMS 2026",
                hi: "🎤 ICEIMS 2026 में मुख्य वक्ता",
                zh: "🎤 ICEIMS 2026 主题演讲者",
                ja: "🎤 ICEIMS 2026 の基調講演者"
            };
            
            return `
            <div class="response-content">
                <h6 style="color: #ff6b35; margin-bottom: 15px;">${speakerTitles[language] || speakerTitles.en}</h6>
                
                <div style="margin-bottom: 12px;">
                    <strong style="color: #333;">🔬 Dr. Sarah Chen</strong>
                    <br><span style="color: #666; font-size: 0.9em;">AI & Robotics Expert</span>
                    <br><span style="font-size: 0.85em;">Leading researcher in artificial intelligence and autonomous systems</span>
                </div>
                
                <div style="margin-bottom: 12px;">
                    <strong style="color: #333;">🌱 Prof. Michael Rodriguez</strong>
                    <br><span style="color: #666; font-size: 0.9em;">Sustainability Researcher</span>
                    <br><span style="font-size: 0.85em;">Pioneering work in sustainable technology and green innovation</span>
                </div>
                
                <div style="margin-bottom: 12px;">
                    <strong style="color: #333;">💡 Dr. Aisha Patel</strong>
                    <br><span style="color: #666; font-size: 0.9em;">Innovation Management</span>
                    <br><span style="font-size: 0.85em;">Expert in technology transfer and startup ecosystems</span>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong style="color: #333;">🚀 Prof. James Wilson</strong>
                    <br><span style="color: #666; font-size: 0.9em;">Digital Transformation</span>
                    <br><span style="font-size: 0.85em;">Specialist in Industry 4.0 and digital business models</span>
                </div>
            </div>`;
        }
        
        // Handle natural conversational queries
        if (msg.includes('can you') || msg.includes('could you') || msg.includes('please') || patterns.help.test(msg)) {
            return `
            <div class="response-content">
                <h6 style="color: #ff6b35; margin-bottom: 15px;">🤝 Of course! I'm here to help!</h6>
                
                <p style="color: #333; margin-bottom: 15px;">
                    I can assist you with comprehensive information about ICEIMS 2026 in multiple languages!
                </p>
                
                <div style="margin-bottom: 12px;">
                    <strong style="color: #333;">🗣️ Natural Language Support:</strong>
                    <ul style="margin: 5px 0; padding-left: 20px; color: #666; font-size: 0.85em;">
                        <li>Ask questions naturally: "When is the conference?"</li>
                        <li>Use conversational language: "Can you tell me about speakers?"</li>
                        <li>Mix languages: "Hola, what are the registration rates?"</li>
                        <li>Ask follow-ups: "That's great! What about attractions?"</li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">🌍 Try asking in different languages:</strong>
                    <ul style="margin: 5px 0; padding-left: 20px; color: #666; font-size: 0.85em;">
                        <li>"¿Cuáles son las tarifas de registro?" (Spanish)</li>
                        <li>"Quels sont les tarifs d'inscription?" (French)</li>
                        <li>"Wann ist die Konferenz?" (German)</li>
                        <li>"पंजीकरण की दरें क्या हैं?" (Hindi)</li>
                        <li>"会议什么时候举行？" (Chinese)</li>
                        <li>"会議はいつですか？" (Japanese)</li>
                    </ul>
                </div>
                
                <p style="color: #ff6b35; font-weight: 600; margin-top: 15px;">
                    What would you like to know about ICEIMS 2026? 🎓
                </p>
            </div>`;
        }
        
        // Fallback to existing comprehensive responses for other patterns
        if (patterns.about.test(msg)) {
            const aboutTitles = {
                en: "🎓 ICEIMS 2026 - International Conference on Engineering, Innovation, Management, and Sciences",
                es: "🎓 ICEIMS 2026 - Conferencia Internacional sobre Ingeniería, Innovación, Gestión y Ciencias",
                fr: "🎓 ICEIMS 2026 - Conférence Internationale sur l'Ingénierie, l'Innovation, la Gestion et les Sciences"
            };
            
            return `
            <div class="response-content">
                <h6 style="color: #ff6b35; margin-bottom: 15px;">${aboutTitles[language] || aboutTitles.en}</h6>
                
                <div style="margin-bottom: 12px;">
                    <strong style="color: #333;">📅 Date:</strong> March 15-17, 2026
                </div>
                
                <div style="margin-bottom: 12px;">
                    <strong style="color: #333;">🏢 Venue:</strong> Grand Convention Center, Tech City
                </div>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">🎯 Theme:</strong> "Advancing Technology for Sustainable Innovation"
                </div>
                
                <p style="color: #666; font-size: 0.9em; line-height: 1.4;">
                    This premier conference brings together researchers, academics, and industry professionals to share cutting-edge insights in technology and innovation.
                </p>
                
                <div style="margin-top: 15px;">
                    <strong style="color: #333;">Conference Tracks:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li>Engineering & Technology</li>
                        <li>Innovation & Research</li>
                        <li>Management & Business</li>
                        <li>Applied Sciences</li>
                        <li>Sustainability & Environment</li>
                        <li>Digital Transformation</li>
                    </ul>
                </div>
            </div>`;
        }
        
        // Default multilingual welcome
        return `
        <div class="response-content">
            <h6 style="color: #ff6b35; margin-bottom: 15px;">🌍 Hello! I'm Galgotias AI - Your Multilingual ICEIMS 2026 Assistant! 🤖</h6>
            
            <p style="margin-bottom: 15px; color: #333;">
                I understand and respond in multiple languages with natural conversation patterns!
            </p>
            
            <div style="margin-bottom: 15px;">
                <strong style="color: #333;">🗣️ Talk to me naturally:</strong>
                <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.85em;">
                    <li>"Hey, when is the conference?" 🇺🇸</li>
                    <li>"Hola, ¿cuáles son los precios?" 🇪🇸</li>
                    <li>"Bonjour, où se déroule la conférence?" 🇫🇷</li>
                    <li>"Hallo, wann ist die Konferenz?" 🇩🇪</li>
                    <li>"नमस्ते, सम्मेलन कब है?" 🇮🇳</li>
                    <li>"你好，会议什么时候开始？" 🇨🇳</li>
                    <li>"こんにちは、会議はいつですか？" 🇯🇵</li>
                </ul>
            </div>
            
            <div style="margin-bottom: 15px;">
                <strong style="color: #333;">💡 I can help with:</strong>
                <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.85em;">
                    <li>Conference details & registration</li>
                    <li>Keynote speakers & schedule</li>
                    <li>Tourist attractions & venues</li>
                    <li>Submission guidelines & awards</li>
                    <li>Contact information & support</li>
                </ul>
            </div>
            
            <p style="color: #ff6b35; font-weight: 600; margin-top: 15px;">
                Ask me anything about ICEIMS 2026 in your preferred language! 🎓✨
            </p>
        </div>`;
    }
        
        // Registration and pricing
        if (msg.includes('registration') || msg.includes('rate') || msg.includes('price') || msg.includes('cost') || msg.includes('fee')) {
            return `
            <div class="response-content">
                <h6 style="color: #ff6b35; margin-bottom: 10px;">💰 Registration Rates for ICEIMS 2026</h6>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">Early Bird (until Jan 15, 2026):</strong>
                    <ul style="margin: 5px 0; padding-left: 20px;">
                        <li>Students: <strong>$150</strong></li>
                        <li>Academics: <strong>$300</strong></li>
                        <li>Industry: <strong>$450</strong></li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">Regular (until Feb 15, 2026):</strong>
                    <ul style="margin: 5px 0; padding-left: 20px;">
                        <li>Students: <strong>$200</strong></li>
                        <li>Academics: <strong>$400</strong></li>
                        <li>Industry: <strong>$550</strong></li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong style="color: #333;">Late Registration (after Feb 15, 2026):</strong>
                    <ul style="margin: 5px 0; padding-left: 20px;">
                        <li>Students: <strong>$250</strong></li>
                        <li>Academics: <strong>$500</strong></li>
                        <li>Industry: <strong>$650</strong></li>
                    </ul>
                </div>
                
                <p style="margin-top: 15px; color: #666; font-size: 0.9em;">
                    📝 <strong>Registration Deadline:</strong> February 15, 2026
                </p>
            </div>`;
        }
        
        // Speakers and keynotes
        if (msg.includes('speaker') || msg.includes('keynote') || msg.includes('presenter')) {
            return `
            <div class="response-content">
                <h6 style="color: #ff6b35; margin-bottom: 15px;">🎤 Keynote Speakers at ICEIMS 2026</h6>
                
                <div style="margin-bottom: 12px;">
                    <strong style="color: #333;">🔬 Dr. Sarah Chen</strong>
                    <br><span style="color: #666; font-size: 0.9em;">AI & Robotics Expert</span>
                    <br><span style="font-size: 0.85em;">Leading researcher in artificial intelligence and autonomous systems</span>
                </div>
                
                <div style="margin-bottom: 12px;">
                    <strong style="color: #333;">🌱 Prof. Michael Rodriguez</strong>
                    <br><span style="color: #666; font-size: 0.9em;">Sustainability Researcher</span>
                    <br><span style="font-size: 0.85em;">Pioneering work in sustainable technology and green innovation</span>
                </div>
                
                <div style="margin-bottom: 12px;">
                    <strong style="color: #333;">💡 Dr. Aisha Patel</strong>
                    <br><span style="color: #666; font-size: 0.9em;">Innovation Management</span>
                    <br><span style="font-size: 0.85em;">Expert in technology transfer and startup ecosystems</span>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong style="color: #333;">🚀 Prof. James Wilson</strong>
                    <br><span style="color: #666; font-size: 0.9em;">Digital Transformation</span>
                    <br><span style="font-size: 0.85em;">Specialist in Industry 4.0 and digital business models</span>
                </div>
            </div>`;
        }
        
        // Conference details and about
        if (msg.includes('about') || msg.includes('conference') || msg.includes('iceims') || msg.includes('detail')) {
            return `
            <div class="response-content">
                <h6 style="color: #ff6b35; margin-bottom: 15px;">🎓 ICEIMS 2026</h6>
                <h6 style="color: #333; font-size: 0.95em; margin-bottom: 15px;">International Conference on Engineering, Innovation, Management, and Sciences</h6>
                
                <div style="margin-bottom: 12px;">
                    <strong style="color: #333;">📅 Date:</strong> March 15-17, 2026
                </div>
                
                <div style="margin-bottom: 12px;">
                    <strong style="color: #333;">🏢 Venue:</strong> Grand Convention Center, Tech City
                </div>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">🎯 Theme:</strong> "Advancing Technology for Sustainable Innovation"
                </div>
                
                <p style="color: #666; font-size: 0.9em; line-height: 1.4;">
                    This premier conference brings together researchers, academics, and industry professionals to share cutting-edge insights in technology and innovation.
                </p>
                
                <div style="margin-top: 15px;">
                    <strong style="color: #333;">Conference Tracks:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li>Engineering & Technology</li>
                        <li>Innovation & Research</li>
                        <li>Management & Business</li>
                        <li>Applied Sciences</li>
                        <li>Sustainability & Environment</li>
                        <li>Digital Transformation</li>
                    </ul>
                </div>
            </div>`;
        }
        
        // Attractions and tourism
        if (msg.includes('attraction') || msg.includes('tourist') || msg.includes('visit') || msg.includes('place') || msg.includes('nearby')) {
            return `
            <div class="response-content">
                <h6 style="color: #ff6b35; margin-bottom: 15px;">🏛️ Venue Attractions & Nearby Places</h6>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">At the Conference Venue:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li><strong>🔬 Tech Museum</strong> - Interactive technology exhibits</li>
                        <li><strong>🚀 Innovation Hub</strong> - Startup showcases and demos</li>
                        <li><strong>🌿 Rooftop Gardens</strong> - Beautiful networking spaces</li>
                        <li><strong>⚙️ Smart Labs</strong> - Hands-on workshop facilities</li>
                        <li><strong>📚 Conference Library</strong> - Research resources</li>
                        <li><strong>☕ Networking Lounges</strong> - Professional meetup areas</li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong style="color: #333;">Nearby Attractions:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li><strong>🏙️ Tech City Downtown</strong> - Shopping and dining</li>
                        <li><strong>🎨 Digital Arts Center</strong> - Interactive exhibitions</li>
                        <li><strong>🏞️ Innovation Park</strong> - Outdoor tech installations</li>
                    </ul>
                </div>
            </div>`;
        }
        
        // Schedule and timing
        if (msg.includes('schedule') || msg.includes('time') || msg.includes('program') || msg.includes('agenda') || msg.includes('when')) {
            return `
            <div class="response-content">
                <h6 style="color: #ff6b35; margin-bottom: 15px;">📅 Conference Schedule - ICEIMS 2026</h6>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">📅 Day 1 - March 15, 2026 (Saturday):</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li><strong>9:00 AM</strong> - Registration & Welcome Coffee</li>
                        <li><strong>10:00 AM</strong> - Opening Ceremony</li>
                        <li><strong>11:00 AM</strong> - Keynote: Dr. Sarah Chen (AI & Robotics)</li>
                        <li><strong>2:00 PM</strong> - Technical Sessions (Engineering & Technology)</li>
                        <li><strong>6:00 PM</strong> - Welcome Reception</li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">📅 Day 2 - March 16, 2026 (Sunday):</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li><strong>9:00 AM</strong> - Keynote: Prof. Michael Rodriguez (Sustainability)</li>
                        <li><strong>10:30 AM</strong> - Workshop Sessions</li>
                        <li><strong>2:00 PM</strong> - Panel Discussions</li>
                        <li><strong>4:00 PM</strong> - Poster Sessions</li>
                        <li><strong>7:00 PM</strong> - Gala Dinner</li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong style="color: #333;">📅 Day 3 - March 17, 2026 (Monday):</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li><strong>9:00 AM</strong> - Keynote: Dr. Aisha Patel (Innovation)</li>
                        <li><strong>11:00 AM</strong> - Final Technical Sessions</li>
                        <li><strong>3:00 PM</strong> - Awards Ceremony</li>
                        <li><strong>4:30 PM</strong> - Closing Ceremony</li>
                    </ul>
                </div>
            </div>`;
        }
        
        // Submission guidelines
        if (msg.includes('submit') || msg.includes('paper') || msg.includes('abstract') || msg.includes('guideline') || msg.includes('deadline')) {
            return `
            <div class="response-content">
                <h6 style="color: #ff6b35; margin-bottom: 15px;">📝 Submission Guidelines</h6>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">Important Dates:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li><strong>Dec 20, 2025</strong> - Abstract Submission Deadline</li>
                        <li><strong>Jan 25, 2026</strong> - Full Paper Submission Deadline</li>
                        <li><strong>Feb 15, 2026</strong> - Registration Deadline</li>
                        <li><strong>Feb 28, 2026</strong> - Final Paper Submission</li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">Presentation Guidelines:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li>Presentation Time: <strong>15 minutes + 5 minutes Q&A</strong></li>
                        <li>Poster sessions available for selected papers</li>
                        <li>All accepted papers published in conference proceedings</li>
                        <li>Best paper awards available in each track</li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong style="color: #333;">Paper Requirements:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li>Maximum 6-8 pages (including references)</li>
                        <li>IEEE conference format required</li>
                        <li>Original research work only</li>
                        <li>Plagiarism check mandatory</li>
                    </ul>
                </div>
            </div>`;
        }
        
        // Awards and recognition
        if (msg.includes('award') || msg.includes('prize') || msg.includes('recognition') || msg.includes('best paper')) {
            return `
            <div class="response-content">
                <h6 style="color: #ff6b35; margin-bottom: 15px;">🏆 Awards & Recognition</h6>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">Conference Awards:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li><strong>🥇 Best Paper Award</strong> - $1000 + Certificate</li>
                        <li><strong>🌟 Young Researcher Award</strong> - $500 + Certificate</li>
                        <li><strong>💡 Innovation Award</strong> - $750 + Certificate</li>
                        <li><strong>🎖️ Lifetime Achievement Award</strong> - Special Recognition</li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">Track-wise Awards:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li>Best Paper in Engineering & Technology</li>
                        <li>Best Paper in Innovation & Research</li>
                        <li>Best Paper in Management & Business</li>
                        <li>Best Paper in Applied Sciences</li>
                        <li>Best Paper in Sustainability</li>
                        <li>Best Paper in Digital Transformation</li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong style="color: #333;">Selection Criteria:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li>Novelty and originality of research</li>
                        <li>Technical quality and rigor</li>
                        <li>Practical impact and applications</li>
                        <li>Presentation quality</li>
                    </ul>
                </div>
            </div>`;
        }
        
        // Workshops and events
        if (msg.includes('workshop') || msg.includes('panel') || msg.includes('event') || msg.includes('session')) {
            return `
            <div class="response-content">
                <h6 style="color: #ff6b35; margin-bottom: 15px;">🔧 Workshops & Special Events</h6>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">Technical Workshops:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li><strong>AI & Machine Learning Workshop</strong> - Hands-on coding session</li>
                        <li><strong>Sustainable Technology Lab</strong> - Green innovation practices</li>
                        <li><strong>Digital Transformation Bootcamp</strong> - Industry 4.0 tools</li>
                        <li><strong>Research Methodology Workshop</strong> - For early-career researchers</li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">Panel Discussions:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li><strong>"Future of AI in Engineering"</strong> - Industry experts panel</li>
                        <li><strong>"Sustainable Innovation Strategies"</strong> - Academic-industry collaboration</li>
                        <li><strong>"Digital Transformation Challenges"</strong> - Implementation strategies</li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong style="color: #333;">Networking Events:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li><strong>Welcome Reception</strong> - March 15, 6:00 PM</li>
                        <li><strong>Gala Dinner</strong> - March 16, 7:00 PM</li>
                        <li><strong>Coffee Breaks & Poster Sessions</strong> - Daily networking</li>
                        <li><strong>Industry Meetups</strong> - Sector-specific networking</li>
                    </ul>
                </div>
            </div>`;
        }
        
        // Location and venue
        if (msg.includes('location') || msg.includes('venue') || msg.includes('address') || msg.includes('where') || msg.includes('direction')) {
            return `
            <div class="response-content">
                <h6 style="color: #ff6b35; margin-bottom: 15px;">📍 Venue Information</h6>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">🏢 Conference Venue:</strong>
                    <p style="margin: 8px 0; color: #666; font-size: 0.9em;">
                        <strong>Grand Convention Center</strong><br>
                        Tech City, Innovation District<br>
                        123 Technology Boulevard<br>
                        Tech City, TC 12345
                    </p>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">🚗 Transportation:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li><strong>Airport:</strong> Tech City International (15 minutes by car)</li>
                        <li><strong>Metro:</strong> Convention Center Station (direct connection)</li>
                        <li><strong>Parking:</strong> Free parking for attendees (500+ spaces)</li>
                        <li><strong>Shuttle:</strong> Free shuttle from major hotels</li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong style="color: #333;">🏨 Recommended Hotels:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li><strong>Tech Grand Hotel</strong> - 5 minutes walk (Special conference rates)</li>
                        <li><strong>Innovation Suites</strong> - 10 minutes walk</li>
                        <li><strong>Convention Plaza Hotel</strong> - Connected to venue</li>
                    </ul>
                </div>
            </div>`;
        }
        
        // Contact and support
        if (msg.includes('contact') || msg.includes('help') || msg.includes('support') || msg.includes('email') || msg.includes('phone')) {
            return `
            <div class="response-content">
                <h6 style="color: #ff6b35; margin-bottom: 15px;">📞 Contact & Support</h6>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">📧 Conference Secretariat:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li><strong>Email:</strong> info@iceims2026.org</li>
                        <li><strong>Phone:</strong> +1-555-ICEIMS (423-467)</li>
                        <li><strong>Website:</strong> www.iceims2026.org</li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #333;">🎫 Registration Support:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li><strong>Email:</strong> registration@iceims2026.org</li>
                        <li><strong>Phone:</strong> +1-555-REG-HELP</li>
                        <li><strong>Hours:</strong> Mon-Fri, 9 AM - 6 PM EST</li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong style="color: #333;">📝 Paper Submission Help:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                        <li><strong>Email:</strong> papers@iceims2026.org</li>
                        <li><strong>Technical Support:</strong> +1-555-PAPER-HELP</li>
                        <li><strong>Submission Portal:</strong> Available 24/7</li>
                    </ul>
                </div>
            </div>`;
        }
        
        // Tracks and topics
        if (msg.includes('track') || msg.includes('topic') || msg.includes('theme') || msg.includes('subject') || msg.includes('area')) {
            return `
            <div class="response-content">
                <h6 style="color: #ff6b35; margin-bottom: 15px;">🎯 Conference Tracks & Topics</h6>
                
                <div style="margin-bottom: 12px;">
                    <strong style="color: #333;">⚙️ Engineering & Technology:</strong>
                    <ul style="margin: 5px 0; padding-left: 20px; color: #666; font-size: 0.85em;">
                        <li>Advanced Manufacturing & Automation</li>
                        <li>Robotics & Mechatronics</li>
                        <li>Materials Science & Engineering</li>
                        <li>Civil & Environmental Engineering</li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 12px;">
                    <strong style="color: #333;">🔬 Innovation & Research:</strong>
                    <ul style="margin: 5px 0; padding-left: 20px; color: #666; font-size: 0.85em;">
                        <li>Emerging Technologies</li>
                        <li>Research Methodologies</li>
                        <li>Technology Transfer</li>
                        <li>Intellectual Property</li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 12px;">
                    <strong style="color: #333;">💼 Management & Business:</strong>
                    <ul style="margin: 5px 0; padding-left: 20px; color: #666; font-size: 0.85em;">
                        <li>Innovation Management</li>
                        <li>Technology Entrepreneurship</li>
                        <li>Project Management</li>
                        <li>Strategic Planning</li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 12px;">
                    <strong style="color: #333;">🧪 Applied Sciences:</strong>
                    <ul style="margin: 5px 0; padding-left: 20px; color: #666; font-size: 0.85em;">
                        <li>Data Science & Analytics</li>
                        <li>Computational Methods</li>
                        <li>Mathematical Modeling</li>
                        <li>Statistical Analysis</li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 12px;">
                    <strong style="color: #333;">🌱 Sustainability & Environment:</strong>
                    <ul style="margin: 5px 0; padding-left: 20px; color: #666; font-size: 0.85em;">
                        <li>Green Technology</li>
                        <li>Renewable Energy Systems</li>
                        <li>Environmental Impact Assessment</li>
                        <li>Sustainable Development</li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <strong style="color: #333;">💻 Digital Transformation:</strong>
                    <ul style="margin: 5px 0; padding-left: 20px; color: #666; font-size: 0.85em;">
                        <li>Artificial Intelligence & Machine Learning</li>
                        <li>Internet of Things (IoT)</li>
                        <li>Blockchain Technology</li>
                        <li>Cybersecurity</li>
                    </ul>
                </div>
            </div>`;
        }
        
        // Thanks and greetings
        if (msg.includes('thank') || msg.includes('great') || msg.includes('good') || msg.includes('excellent')) {
            return `
            <div class="response-content">
                <h6 style="color: #ff6b35; margin-bottom: 15px;">😊 Thank You!</h6>
                
                <p style="color: #333; margin-bottom: 15px;">
                    I'm glad I could help you with information about ICEIMS 2026! 
                </p>
                
                <p style="color: #666; font-size: 0.9em; margin-bottom: 15px;">
                    Is there anything else you'd like to know about the conference? I can provide more details about:
                </p>
                
                <ul style="margin: 10px 0; padding-left: 20px; color: #666; font-size: 0.9em;">
                    <li>Registration process and deadlines</li>
                    <li>Paper submission guidelines</li>
                    <li>Accommodation recommendations</li>
                    <li>Travel and transportation</li>
                    <li>Networking opportunities</li>
                    <li>Technical program details</li>
                </ul>
                
                <p style="color: #ff6b35; font-weight: 600; margin-top: 15px;">
                    Feel free to ask me anything about ICEIMS 2026! 🎓
                </p>
            </div>`;
        }
        
        // Default welcome response for any other questions
        return `
        <div class="response-content">
            <h6 style="color: #ff6b35; margin-bottom: 15px;">Hello! I'm Galgotias AI, your ICEIMS 2026 assistant! 🤖</h6>
            
            <p style="margin-bottom: 15px; color: #333;">I can help you with comprehensive information about:</p>
            
            <div style="margin-bottom: 12px;">
                <strong style="color: #333;">📋 Conference Information:</strong>
                <ul style="margin: 5px 0; padding-left: 20px; color: #666; font-size: 0.85em;">
                    <li>Conference details, dates, and venue</li>
                    <li>Registration rates and deadlines</li>
                    <li>Schedule and program information</li>
                </ul>
            </div>
            
            <div style="margin-bottom: 12px;">
                <strong style="color: #333;">🎤 Speakers & Events:</strong>
                <ul style="margin: 5px 0; padding-left: 20px; color: #666; font-size: 0.85em;">
                    <li>Keynote speakers and presentations</li>
                    <li>Workshops and panel discussions</li>
                    <li>Networking events and social activities</li>
                </ul>
            </div>
            
            <div style="margin-bottom: 12px;">
                <strong style="color: #333;">📝 Submissions & Awards:</strong>
                <ul style="margin: 5px 0; padding-left: 20px; color: #666; font-size: 0.85em;">
                    <li>Paper submission guidelines</li>
                    <li>Conference tracks and topics</li>
                    <li>Awards and recognition programs</li>
                </ul>
            </div>
            
            <div style="margin-bottom: 15px;">
                <strong style="color: #333;">🏛️ Travel & Venues:</strong>
                <ul style="margin: 5px 0; padding-left: 20px; color: #666; font-size: 0.85em;">
                    <li>Venue location and directions</li>
                    <li>Tourist attractions and activities</li>
                    <li>Hotels and accommodation</li>
                </ul>
            </div>
            
            <p style="margin-top: 15px; color: #ff6b35; font-weight: 600;">
                What would you like to know about ICEIMS 2026? Just ask me anything! 🎓
            </p>
        </div>`;
    }
    
    // Send button click
    if (sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
    }
    
    // Enter key press
    if (input) {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
    
    // Quick buttons
    const quickBtns = document.querySelectorAll('.quick-btn');
    quickBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const question = btn.getAttribute('data-question') || btn.textContent;
            if (input) {
                input.value = question;
                sendMessage();
            }
        });
    });
    
    console.log('Test chatbot initialized successfully!');
});
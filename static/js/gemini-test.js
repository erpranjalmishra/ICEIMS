// Test Gemini API directly
async function testGeminiAPI() {
    const apiKey = 'AIzaSyCvkXKq0NHwajkJd7u_4V2C2itq3nQpvyI';
    const apiUrl = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent';
    
    console.log('Testing Gemini API...');
    
    const requestBody = {
        contents: [{
            parts: [{
                text: "Hello, please respond with information about ICEIMS 2026 conference."
            }]
        }],
        generationConfig: {
            temperature: 0.7,
            topK: 40,
            topP: 0.95,
            maxOutputTokens: 200,
        }
    };

    try {
        const response = await fetch(`${apiUrl}?key=${apiKey}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });

        console.log('API Response Status:', response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('API Error:', errorText);
            return false;
        }

        const data = await response.json();
        console.log('API Success! Response:', data);
        return true;
    } catch (error) {
        console.error('Fetch Error:', error);
        return false;
    }
}

// Test when page loads
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        testGeminiAPI().then(success => {
            if (success) {
                console.log('✅ Gemini API is working!');
            } else {
                console.log('❌ Gemini API test failed');
            }
        });
    }, 1000);
});
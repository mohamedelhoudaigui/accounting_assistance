document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    const addMessage = (content, sender) => {
        const messageWrapper = document.createElement('div');
        messageWrapper.classList.add('message', `${sender}-message`);

        if (sender === 'agent') {
            // Use marked.js to parse and render markdown
            messageWrapper.innerHTML = marked.parse(content);
        } else {
            const p = document.createElement('p');
            p.textContent = content;
            messageWrapper.appendChild(p);
        }
        
        chatBox.appendChild(messageWrapper);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    const handleSend = async () => {
        const query = userInput.value.trim();
        if (!query) return;

        addMessage(query, 'user');
        userInput.value = '';

        try {
            const response = await fetch('/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: query }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Something went wrong');
            }

            const data = await response.json();
            
            let resultText = data.result;
            if (typeof resultText !== 'string') {
                // If the result is JSON, format it as a markdown code block.
                resultText = '```json\n' + JSON.stringify(data.result, null, 2) + '\n```';
            }

            addMessage(resultText, 'agent');

        } catch (error) {
            addMessage(`Error: ${error.message}`, 'agent');
        }
    };

    sendBtn.addEventListener('click', handleSend);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSend();
        }
    });
});
// terminal.js
document.addEventListener('DOMContentLoaded', (event) => {
    const terminal = document.getElementById('terminal');
    const output = document.getElementById('output');
    const input = document.getElementById('input');
    const cursor = document.getElementById('cursor');
    const prompt = document.getElementById('prompt');
    const tabs = document.querySelectorAll('.tab');
    const tabContent = document.querySelector('.tab-content');

    let typingTimer;

    // function updateCursorPosition() {
    //     const promptRect = prompt.getBoundingClientRect();
    //     const cursorPosition = input.value.length * 8; // Assuming 8px char width
    //     cursor.style.left = `${promptRect.width + cursorPosition}px`;
    //     cursor.style.bottom = '0px';
    //     cursor.classList.remove('blink');
    //     clearTimeout(typingTimer);
    //     typingTimer = setTimeout(() => cursor.classList.add('blink'), 500);
    // }

    function updateCursorPosition() {
        const promptRect = prompt.getBoundingClientRect();
        const cursorPosition = input.value.length * 8; // Assuming 8px char width
        cursor.style.left = `${promptRect.width + cursorPosition - 8}px`; // Subtract 8px (one character width)
        cursor.style.bottom = '0px';
        cursor.classList.remove('blink');
        clearTimeout(typingTimer);
        typingTimer = setTimeout(() => cursor.classList.add('blink'), 500);
    }

    function moveCursorToNewLine() {
        cursor.style.left = `${prompt.getBoundingClientRect().width}px`;
        cursor.style.bottom = '0px';
    }

    async function sendCommand(command) {
        try {
            const response = await fetch('/api/terminal', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt: command })
            });
            const data = await response.json();
            return data.response;
        } catch (error) {
            console.error('Error sending command:', error);
            return 'Error: Unable to process command';
        }
    }

    input.addEventListener('input', updateCursorPosition);
    input.addEventListener('keyup', updateCursorPosition);
    input.addEventListener('click', updateCursorPosition);
    input.addEventListener('keydown', async (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            const command = input.value;
            output.textContent += `$ ${command}\n`;
            input.value = '';
            moveCursorToNewLine();
            
            const response = await sendCommand(command);
            handleResponse(response);
        }
    });

    function handleResponse(response) {
        // output.textContent += `${response}\n\n`;
        output.textContent += `${response}\n`;
        terminal.scrollTop = terminal.scrollHeight;
        moveCursorToNewLine();
        
        const match = response.match(/switch to (Clients|Switches|Access Points)/i);
        if (match) {
            const tabName = match[1].trim();
            switchTab(tabName);
        }
    }

    function switchTab(tabName) {
        tabs.forEach(tab => {
            tab.classList.remove('active');
            if (tab.textContent.trim().toLowerCase() === tabName.toLowerCase()) {
                tab.classList.add('active');
                loadTabContent(tab.href);
            }
        });
    }

    function loadTabContent(url) {
        fetch(url)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newContent = doc.querySelector('.tab-content').innerHTML;
                tabContent.innerHTML = newContent;
            });
    }

    tabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            loadTabContent(tab.href);
        });
    });

    terminal.addEventListener('click', () => {
        input.focus();
        updateCursorPosition();
    });

    // Initialize cursor position and focus input
    updateCursorPosition();
    input.focus();
});
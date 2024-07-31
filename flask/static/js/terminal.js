document.addEventListener('DOMContentLoaded', (event) => {
    const terminal = document.getElementById('terminal');
    const output = document.getElementById('output');
    const input = document.getElementById('input');
    const cursor = document.getElementById('cursor');

    let typingTimer;

    function updateCursorPosition() {
        const cursorPosition = input.selectionStart * 8; // Assuming 8px char width
        cursor.style.left = `${cursorPosition}px`;
        cursor.classList.remove('blink');
        clearTimeout(typingTimer);
        typingTimer = setTimeout(() => cursor.classList.add('blink'), 500);
    }

    async function sendCommand(command) {
        const response = await fetch('/api/terminal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: command })
        });
        const data = await response.json();
        return data.response;
    }

  
    input.addEventListener('input', updateCursorPosition);
    input.addEventListener('keydown', async (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            const command = input.value;
            input.value = '';
            cursor.style.left = '0px';
            cursor.classList.add('blink');
            output.textContent += `$ ${command}\n`;
    
            // Move cursor to new line without $
            //output.textContent += ' \n';
    
            const response = await sendCommand(command);
            
            // Print response and move cursor to new line
            output.textContent += `${response}\n`;
            
            // Add a new line with the blinking cursor
            //output.textContent += '\n';
            
            terminal.scrollTop = terminal.scrollHeight;
        } else {
            updateCursorPosition();
        }
    });



    terminal.addEventListener('click', () => input.focus());
    updateCursorPosition(); // Initialize cursor position
});
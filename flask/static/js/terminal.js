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

    input.addEventListener('input', updateCursorPosition);
    input.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            const command = input.value;
            output.textContent += `$ ${command}\n`;
            
            switch(command.toLowerCase()) {
                case 'hello': output.textContent += 'Hello there!\n'; break;
                case 'date': output.textContent += `${new Date().toString()}\n`; break;
                case 'clear': output.textContent = ''; break;
                default: output.textContent += `Command not recognized: ${command}\n`;
            }
            
            input.value = '';
            cursor.style.left = '0px';
            cursor.classList.add('blink');
            terminal.scrollTop = terminal.scrollHeight;
        } else {
            updateCursorPosition();
        }
    });

    terminal.addEventListener('click', () => input.focus());
    updateCursorPosition(); // Initialize cursor position
});
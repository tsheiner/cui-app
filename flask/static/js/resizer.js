document.addEventListener('DOMContentLoaded', function() {
    const resizer = document.getElementById('resizer');
    const terminal = document.querySelector('.terminal');

    let isResizing = false;

    console.log('Resizer script loaded');

    resizer.addEventListener('mousedown', function(e) {
        console.log('Mousedown on resizer');
        isResizing = true;
        document.addEventListener('mousemove', resize);
        document.addEventListener('mouseup', stopResize);
    });

    function resize(e) {
        if (isResizing) {
            console.log('Resizing', e.clientX);
            const containerWidth = document.querySelector('.container').offsetWidth;
            let newWidth = e.clientX;
            
            // Enforce min and max widths
            newWidth = Math.max(300, Math.min(newWidth, containerWidth * 0.8));
            
            terminal.style.width = newWidth + 'px';
        }
    }

    function stopResize() {
        console.log('Stop resizing');
        isResizing = false;
        document.removeEventListener('mousemove', resize);
        document.removeEventListener('mouseup', stopResize);
    }
});
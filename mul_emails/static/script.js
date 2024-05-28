document.addEventListener('DOMContentLoaded', function() {
    const editor = document.getElementById('editor');

    function updateHighlight() {
        const text = editor.value;
        const highlightedText = text.replace(/\{([^{}]*)\}/g, function(match, p1) {
            return `{${p1}}`;
        });
        editor.innerHTML = highlightedText;
    }

    editor.addEventListener('input', function(event) {
        const input = event.inputType;
        const value = editor.value;
        const start = editor.selectionStart;

        if (input === 'insertText' && event.data === '{') {
            const textBefore = value.slice(0, start);
            const textAfter = value.slice(start);

            editor.value = `${textBefore}{}${textAfter}`;
            editor.selectionStart = editor.selectionEnd = start;

            updateHighlight();
            return;
        }

        updateHighlight();
    });

    editor.addEventListener('keydown', function(event) {
        const start = editor.selectionStart;
        const value = editor.value;

        if (event.key === '{') {
            event.preventDefault();
            const textBefore = value.slice(0, start);
            const textAfter = value.slice(start);

            editor.value = `${textBefore}{}${textAfter}`;
            editor.selectionStart = editor.selectionEnd = start + 1;
            updateHighlight();
        } else if (event.key === 'Tab') {
            event.preventDefault();
            const textBefore = value.slice(0, start);
            const textAfter = value.slice(start);

            editor.value = `${textBefore}\t${textAfter}`;
            editor.selectionStart = editor.selectionEnd = start + 1;
            updateHighlight();
        }
    });

    updateHighlight();
});

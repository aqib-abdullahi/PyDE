var editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
    theme: 'monokai',
    mode: {
        name: "python",
        version: 3,
        singleLineStringErrors: false
    },
    lineNumbers: true,
    gutters: ["CodeMirror-linenumbers"],
    indentUnit: 4,
    showCursorWhenSelecting: true,
    matchBrackets: true,
    autoCloseBrackets: true,
    autoCloseTags: true,
    styleActiveLine: true,
    indentWithTabs: true,
    extraKeys: {
        "Ctrl-Space": "autocomplete",
        "Ctrl-/": "toggleComment"
    }
});
CodeMirror.commands.autocomplete = function(cm) {
    CodeMirror.simpleHint(cm, CodeMirror.pythonHint);
}
editor.on("change", function(cm) {
    CodeMirror.simpleHint(cm, CodeMirror.pythonHint);
});
editor.setSize('100%', '100%')

const dropDown = document.querySelector('.acc-info')
const profiler = document.getElementById('user-icon')
profiler.addEventListener('click', function() {
    // if (dropDown.classList.contains(block)) {
    //     dropDown.cl
    // }
    dropDown.classList.toggle('block')
})
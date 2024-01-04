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
editor.setSize('100%', '100%');

const dropDown = document.querySelector('.acc-info')
const profiler = document.getElementById('user-icon')
profiler.addEventListener('click', function() {
    dropDown.classList.toggle('block')
});

// function uploads file to container
function uploadFileToContainer(filename, fileContent) {
    const message = `echo "${fileContent}" > ${filename} \n`
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(message);
    } else {
        socket.addEventListener('open', function() {
            socket.send(message);
        });
    }
}

// function uploads file an run on container
function runFileOnContainer(filename, fileContent) {
    const message = `echo '${fileContent}' > ${filename} \n`
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(message);
    } else {
        socket.addEventListener('open', function() {
            socket.send(message);
        });
    }
    socket.send(`chmod 755 ${filename}\n`);
    socket.send(`./${filename}\n`);
}

// exports code
const runBtn = document.querySelector('.run-btn');
runBtn.addEventListener('click', function() {
    codes = editor.getValue();
    console.log(codes);
    runFileOnContainer("a.py", codes);
})
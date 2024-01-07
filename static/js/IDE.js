const containerID = document.getElementById('containerId').value;

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

function UploadFileToContainer(filename, fileContent) {
    const fileInfo = {
        "file_content": fileContent,
        "file_name": filename
    }
    return fetch(`/api/v1/container/${userId}/${containerID}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(fileInfo)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('File uploaded successsfully: ', data);
            return data;
        })
        .catch(error => {
            console.error('Problem uploading file: ', error);
            throw error;
        })

}

function runFileOnContainer(filename, containerID) {
    return fetch(`/api/v1/container/${userId}/${containerID}/${filename}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('File executed successsfully: ', data);
            return data;
        })
        .catch(error => {
            console.error('Problem executing file: ', error);
            throw error;
        })

}


// exports code
const runBtn = document.querySelector('.run-btn');
runBtn.addEventListener('click', function() {
    codes = editor.getValue();
    console.log(codes);
    fileName = "tester.py"
    UploadFileToContainer(fileName, codes);
    runFileOnContainer(fileName, containerID);
    socket.send(`./${fileName}\n`);
})
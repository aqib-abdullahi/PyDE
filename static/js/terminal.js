const term = new Terminal({
    cursorBlink: true,
    cols: 40,
    theme: { background: '#272822' },
    fontSize: 17,
    fontFamily: 'Ubuntu Mono, courier-new, courier, monospace',

});
term.open(document.querySelector('.shell'));

// FIT ADDON
const fitAddon = new FitAddon.FitAddon();
term.loadAddon(fitAddon);
fitAddon.fit();

// WEBSOCKET
const ipAddress = document.getElementById('ipAddress').value;
const containerId = document.getElementById('containerId').value;
const port = document.getElementById('containerPort').value;

const socket = new WebSocket(`ws://${ipAddress}:${port}/containers/${containerId}/attach/ws?stream=1&stdout=1&stdin=1&logs=1`);

// ATTACH ADDON
const attachAddon = new AttachAddon.AttachAddon(socket);
term.loadAddon(attachAddon);


// // function uploads file to container
// function uploadFileToContainer(filename, fileContent) {
//     const message = `echo "${fileContent}" > ${filename} \n`
//     if (socket.readyState === WebSocket.OPEN) {
//         socket.send(message);
//     } else {
//         socket.addEventListener('open', function() {
//             socket.send(message);
//         });
//     }
// }
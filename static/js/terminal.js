const term = new Terminal({
    cursorBlink: true,
    cols: 10,
    theme: { background: '#272822' },
    fontSize: 17,
    fontFamily: 'Ubuntu Mono, courier-new, courier, monospace',

});
term.open(document.querySelector('.shell'));
const fitAddon = new FitAddon.FitAddon();
term.loadAddon(fitAddon);
fitAddon.fit();

// const socket = new WebSocket('ws://localhost:3000');
term.prompt = () => {
    term.write('\r\n$ ');
};

term.prompt();

term.onKey(e => {
    const printable = !e.domEvent.altKey && !e.domEvent.altGraphKey &&
        !e.domEvent.ctrlKey && !e.domEvent.metaKey;

    if (e.domEvent.keyCode === 13) {
        term.prompt();
    } else if (e.domEvent.keyCode === 8) {
        term.write('\b \b');
    } else if (printable) {
        term.write(e.key);
    }
});

// socket.onmessage = event => {
//     term.write(event.data);
// };
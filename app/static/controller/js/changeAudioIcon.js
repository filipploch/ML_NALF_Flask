var socket = io.connect('http://' + document.domain + ':' + location.port);
// Natychmiastowa aktualizacja treści div na podstawie zdarzenia od serwera
socket.on('changeAudioIcon', function(data) {
//    console.log("Received update_div event with data:", data);
    document.getElementById(data['divId']).src = data['imgTag'];
});
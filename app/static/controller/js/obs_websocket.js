var ws = new WebSocket("ws://localhost:4445/ws");

//// Definiujemy funkcję, która jest wywoływana, gdy otrzymujemy wiadomość od serwera
//ws.onmessage = function(event) {
//    // Pobieramy status nagrywania OBS Studio z wiadomości
//    var recording_status = event.data;
//    console.log(recording_status);
//    // Pobieramy element div o id="status"
//    var status = document.getElementById("record-button");
//    // Zmieniamy zawartość elementu div na podstawie statusu nagrywania
//    if (recording_status == "true") {
//        status.innerHTML = '<img src="/static/controller/images/record-on.png">'
//    } else {
//        status.innerHTML = '<img src="/static/controller/images/record-off.png">'
//    }
//};
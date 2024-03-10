var socket = io.connect('http://' + document.domain + ':' + location.port);
// Natychmiastowa aktualizacja treści div na podstawie zdarzenia od serwera
socket.on('changeRecordIcon', function(data) {
    var className = data;
//    console.log(typeof(className));
    var elementId = 'record-button';
    classListRemove(elementId, 'button-active');
    classListRemove(elementId, 'button-inactive');
    classListAdd(elementId, className);
});
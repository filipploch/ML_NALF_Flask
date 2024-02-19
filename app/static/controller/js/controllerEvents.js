function startRecording() {
    fetch('/start-recording')
    .then(response => {
        if (response.ok) {
            changeTagAttributeValue('record-button', 'ondblclick', 'stopRecording()');
        } else {
            console.error('Błąd podczas rozpoczęcia nagrywania:', response.statusText);
        }
    })
    .catch(error => {
        console.error('Błąd podczas rozpoczęcia nagrywania:', error);
    });
}

function stopRecording() {
    fetch('/stop-recording')
    .then(response => {
        if (response.ok) {
            changeTagAttributeValue('record-button', 'ondblclick', 'startRecording()');
        } else {
            console.error('Błąd podczas rozpoczęcia nagrywania:', response.statusText);
        }
    })
    .catch(error => {
        console.error('Błąd podczas rozpoczęcia nagrywania:', error);
    });
}

function checkRecordingStatus() {
    fetch('/check-record-status')
    .then(response => response.json())
    .then(data => {
        // Sprawdzenie wartości outputActive w danych
        var outputActive = data.outputActive;

        // Zmiana wartości ondblclick na podstawie outputActive
        var buttonId = 'record-button';
        var newOnDblClick = outputActive ? 'stopRecording()' : 'startRecording()';
        changeTagAttributeValue(buttonId, 'ondblclick', newOnDblClick);
    })
    .catch(error => {
        console.error('Błąd podczas sprawdzania statusu nagrywania:', error);
    });
}

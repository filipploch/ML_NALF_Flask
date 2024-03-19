function submitFormData(formId, elementToChange) {
    const formElement = document.getElementById(formId);
    const formData = new FormData(formElement);

    // Pobierz endpoint POST z atrybutu action formularza
    const endpoint = formElement.getAttribute('action');

    // Utwórz obiekt konfiguracyjny dla metody fetch
    const fetchOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            // Dodaj inne nagłówki według potrzeb
        },
        body: new URLSearchParams(formData).toString(),
    };

    // Wyślij żądanie POST na endpoint
    fetch(endpoint, fetchOptions, elementToChange)
        .then(response => response.json())
        .then(data => {
            // Obsłuż odpowiedź z serwera (jeśli to konieczne)
            let content = data.content;
            if (typeof elementToChange !== 'undefined') {
                document.getElementById(elementToChange).innerHTML = content;
            }
        })
        .catch(error => console.error('Error:', error));
}

function submitNewFormData(element, formId, elementToChange) {
    console.log(element.dataset.isedited);
    const formElement = document.getElementById(formId);
    const idElement = document.getElementsByClassName('competitions-form-id')[0];
    const checkboxes = formElement.querySelectorAll('.competitions-form-checkbox');
    const button = document.getElementById(`get-${formId}-button`);

    classListRemove('spinner-container', 'invisible');
    // Inicjalizuj obiekt dynamicData
    const formData = {};
    formData[idElement.name] = idElement.value;
    formData['isEdited'] = element.dataset.isedited;
    console.log(formData['isEdited']);

    checkboxes.forEach(checkbox => {
        const key = checkbox.name;
        const value = checkbox.value;
        if(checkbox.checked) {
            formData[key] = value;
        }
        checkbox.disabled = true;
    });

    // Pobierz endpoint POST z atrybutu action formularza
    const endpoint = formElement.getAttribute('action');

    // Utwórz obiekt konfiguracyjny dla metody fetch
    const fetchOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // Dodaj inne nagłówki według potrzeb
        },
        body: JSON.stringify(formData),
    };

    // Wyślij żądanie POST na endpoint
    fetch(endpoint, fetchOptions, elementToChange)
        .then(response => response.json())
        .then(data => {
            // Obsłuż odpowiedź z serwera (jeśli to konieczne)
            let content = data.content;
            if (typeof elementToChange !== 'undefined') {
                document.getElementById(elementToChange).innerHTML = content;
                button.value = 'Odblokuj wybór rozgrywek';
                button.removeAttribute('onclick');
                button.setAttribute('onclick', 'unblockForm("' + formId + '")');
                classListRemove(button.id, 'yellow-bg')
                classListAdd('spinner-container', 'invisible');

            }
        })
        .catch(error => console.error('Error:', error));
}

function unblockForm(formId) {
    const formElement = document.getElementById(formId);
    const idElement = document.getElementsByClassName('competitions-form-id')[0];
    const episodeId = idElement.value;
    const checkboxes = formElement.querySelectorAll('.competitions-form-checkbox');
    let button = document.getElementById(`get-${formId}-button`);
    button.value = 'Pobierz dane dla rozgrywek';
    button.removeAttribute('onclick');
    button.setAttribute('onclick',
                        "submitNewFormData(this, '" + formId + "', 'episode-" + episodeId + "-best-five-block')");
//    button.onclick = submitNewFormData(formId, `episode-${episodeId}-best-five-block`);
    classListAdd(button.id, 'yellow-bg')
    checkboxes.forEach(checkbox => {
        checkbox.disabled = false;
    });
}

function checkCompetitionSelect(episodeId) {
    let formElement = document.getElementById('episode-' + episodeId + '-competitions-form');
    let button = document.getElementById('get-episode-' + episodeId + '-competitions-form-button');
    let checkboxes = formElement.querySelectorAll('.competitions-form-checkbox');
    checkAndDisableElement(button.id);
    checkboxes.forEach(checkbox => {
        if(checkbox.checked) {
            checkAndEnableElement(button.id);
        }
    });
}

function checkAndDisableElement(id) {
    var element = document.getElementById(id);

    if (element && !element.disabled) {
        element.disabled = true;
    }
}

function checkAndEnableElement(id) {
    var element = document.getElementById(id);

    if (element && element.disabled) {
        element.disabled = false;
    }
}

function loadContent(endpoint, elementToChange, optionalArg) {
    if (typeof optionalArg !== 'undefined') {
        endpoint = endpoint + '/' + optionalArg;
    }

    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            let content = data.content;
            document.getElementById(elementToChange).innerHTML = content;
        })
        .catch(error => console.error('Error:', error));
}

function fetchData(endpoint) {
    classListRemove('spinner-container', 'invisible');
    fetch(endpoint)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            classListAdd('spinner-container', 'invisible');
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function getTeamsFromSiteTitle(endpoint, url, inputId, number) {
    let input = document.getElementById(inputId);
    let episodeId = input.dataset.episodeid;
    endpoint = endpoint + '/' + url;
    fetch(endpoint)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            let content = data.content;
            input.value = content;
            input.title = content;
        })
        .catch(error => {
            console.error('Error:', error);
            // Wywołanie funkcji removeHighlightFields w przypadku błędu
            removeHighlightFields(episodeId, 'delete-button-' + number);
        });
}

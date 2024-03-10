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
        console.log('data:', data);
            // Obsłuż odpowiedź z serwera (jeśli to konieczne)
            let content = data.content;
            if (typeof elementToChange !== 'undefined') {
            console.log('content:', content);
                document.getElementById(elementToChange).innerHTML = content;
            }
        })
        .catch(error => console.error('Error:', error));
}


function submitNewFormData(formId, elementToChange) {
    const formElement = document.getElementById(formId);
    const idElement = document.getElementsByClassName('competitions-form-id')[0];
    const checkboxes = document.querySelectorAll('.competitions-form-checkbox:checked');
    classListRemove('spinner-container', 'invisible');
    // Inicjalizuj obiekt dynamicData
    const formData = {};
    formData[idElement.name] = idElement.value;

    checkboxes.forEach(checkbox => {
        const key = checkbox.name;
        const value = checkbox.value;
        formData[key] = value;
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
    console.log(fetchOptions);

    // Wyślij żądanie POST na endpoint
    fetch(endpoint, fetchOptions, elementToChange)
        .then(response => response.json())
        .then(data => {
            // Obsłuż odpowiedź z serwera (jeśli to konieczne)
            let content = data.content;
            if (typeof elementToChange !== 'undefined') {
                document.getElementById(elementToChange).innerHTML = content;
                classListAdd('spinner-container', 'invisible');

            }
        })
        .catch(error => console.error('Error:', error));
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

function getTeamsFromSiteTitle(endpoint, url, inputId) {
    endpoint = endpoint + '/' + url;
    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            let content = data.content;
            let input = document.getElementById(inputId);
            input.value = content;
            input.title = content;
        })
        .catch(error => console.error('Error:', error));
}

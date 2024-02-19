function classListRemove(elementId, className) {
    var element = document.getElementById(elementId);
    if (element && element.classList.contains(className)) {
        element.classList.remove(className);
    }
}

function classListAdd(elementId, className) {
    var element = document.getElementById(elementId);
    if (element && !element.classList.contains(className)) {
        element.classList.add(className);
    }
}

function setDefaultOnClickUrl(elementId) {
    var element = document.getElementById(elementId);
    if (element && element.hasAttribute('data-endpoint-url')) {
        var endpointUrl = element.getAttribute('data-endpoint-url');
        var newOnClickValue = 'showScene("' + element.id + '", "' + endpointUrl + '")';
        element.setAttribute('onclick', newOnClickValue);
    }
}

function setEndHighlightOnClickUrl(elementId) {
    var element = document.getElementById(elementId);
    if (element && element.hasAttribute('data-endpoint-url')) {
        var endpointUrl = 'end-highlight';
        var newOnClickValue = 'showScene("' + element.id + '", "' + endpointUrl + '")';
        element.setAttribute('onclick', newOnClickValue);
    }
}

function changeTagAttributeValue(tagId, attribute, value) {
    var element = document.getElementById(tagId);
    if (element) {
        element.setAttribute(attribute, value);
    } else {
        console.error('Element o identyfikatorze ' + tagId + ' nie został znaleziony.');
    }
}

function showScene(elementId, endpointUrl) {
        fetch(endpointUrl)
            .then(response => {
                if (response.ok) {
                    setThisButtonActive(elementId, 'scene-switcher-button');
                } else {
                    console.error('Błąd podczas pobierania danych:', response.statusText);
                }
            })
            .catch(error => {
                // Obsługa błędu w przypadku problemów z żądaniem
                console.error('Błąd podczas pobierania danych:', error);
            });
    }

function setThisButtonActive(elementId, className) {
    var elements = document.getElementsByClassName(className);
    var button = document.getElementById(elementId);
    for (var i = 0; i < elements.length; i++) {
        var currentElementId = elements[i].id;

        if (currentElementId === elementId && button.classList.contains('button-inactive')) {
            classListRemove(elementId, 'button-inactive');
            classListAdd(elementId, 'button-active');
            setEndHighlightOnClickUrl(elementId);
        } else {
            classListRemove(currentElementId, 'button-active');
            classListAdd(currentElementId, 'button-inactive');
            setDefaultOnClickUrl(currentElementId);
        }
    }

}
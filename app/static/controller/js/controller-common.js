function classListAdd(elementId, className) {
    var element = document.getElementById(elementId);
    if (element && !element.classList.contains(className)) {
        element.classList.add(className);
    }
    else if (!element) {
        console.log(`Element ${elementId} not found`)
    }
}

function classListRemove(elementId, className) {
    var element = document.getElementById(elementId);
    if (element && element.classList.contains(className)) {
        element.classList.remove(className);
    }
    else if (!element) {
        console.log(`Element ${elementId} not found`)
    }
}

function sleep(time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}


function removeClassFromClassElements(elementsClassName, classToRemove) {
    var elements = document.getElementsByClassName(elementsClassName);
        Array.from(elements).forEach(function(element) {
        if (element && element.classList.contains(classToRemove)) {
            element.classList.remove(classToRemove);
        }
    });
}

function addClassToClassElements(elementsClassName, classToAdd) {
    var elements = document.getElementsByClassName(elementsClassName);
        Array.from(elements).forEach(function(element) {
        if (element && !element.classList.contains(classToAdd)) {
            element.classList.add(classToAdd);
        }
    });
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

function generateScene(endpointUrl, optionalArgument = null) {
    const headers = new Headers();

    if (optionalArgument !== null) {
        const element = document.getElementById(optionalArgument);

        // Sprawdzamy, czy istnieje element o podanym id i czy ma atrybut data-optionalarg
        if (element && element.hasAttribute('data-optionalarg')) {
            const dataOptionalArg = element.getAttribute('data-optionalarg');
            headers.append('Optional-Header', dataOptionalArg);
        }
    } else {
        headers.append('Optional-Header', optionalArgument);
    }

    fetch(endpointUrl, { headers: headers })
//        .then(response => {
//            if (response.ok) {
//                setThisButtonActive(elementId, 'main-button');
//            } else {
//                console.error('Błąd podczas pobierania danych:', response.statusText);
//            }
//        })
        .catch(error => {
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

function handleRadioButtonClick(radioButton, i) {
    // Sprawdzenie, czy radio button był wcześniej zaznaczony
    var isChecked = radioButton.dataset.ischecked;
    let dataId = radioButton.dataset.id
    let competitionId = radioButton.dataset.competitionid
    let episodeId = radioButton.dataset.episodeid
    var hiddenForRadio = document.getElementById(`mvp-hidden-${episodeId}-${competitionId}-${i}`)
    var radioButtons = document.querySelectorAll('input[type="radio"][class="mvp-radio"]');
    var hiddenForRadios = document.querySelectorAll('input[type="hidden"][class="mvp-hidden"]');

    // Odznaczenie wszystkich radio buttonów w danej grupie, jeśli naciśnięty był wcześniej zaznaczony
    if (isChecked == 1) {
        radioButtons.forEach(function (otherRadioButton) {
            otherRadioButton.checked = false;
            otherRadioButton.dataset.ischecked = 0;
        });
        hiddenForRadios.forEach(function (otherHiddenForRadios) {
            otherHiddenForRadios.value = 0;
        });
    } else {
        radioButtons.forEach(function (otherRadioButton) {
            otherRadioButton.checked = false;
            otherRadioButton.dataset.ischecked = 0;
        });
        radioButton.dataset.ischecked = 1;
        radioButton.checked = true;
        hiddenForRadios.forEach(function (otherHiddenForRadios) {
            otherHiddenForRadios.value = 0;
        });
            hiddenForRadio.value = 1;
    }
}



//function toggleClassInClassElements(elementsClassName, classes, force=false) {
//    var elements = document.getElementsByClassName(elementsClassName);
//    Array.from(elements).forEach(function(element) {
//        if (element) {
//            var elementClasses = element.classList;
//            var hasClass1 = elementClasses.contains(classes[0]);
//            var hasClass2 = elementClasses.contains(classes[1]);
//            if (force) {
//                if (!hasClass1 && !hasClass2) {
//                    classListAdd(elementsClassName, classes[0]);
//                    classListRemove(elementsClassName, classes[1]);
//                }
//            }
//            if ((!hasClass1 && hasClass2) || (hasClass1 && hasClass2)) {
//                classListAdd(elementsClassName, classes[0]);
//                classListRemove(elementsClassName, classes[1]);
//            } else if hasClass1 && !hasClass2) {
//                classListRemove(classes[0]);
//                classListAdd(classes[1]);
//            }
//        } else {
//            console.log("Element with the provided ID does not exist.");
//        }
//
//    });
//
//}


//  if (element) {
//    // Pobieramy listę klas przypisanych do elementu
//    var elementClasses = element.classList;
//
//    // Sprawdzamy, które klasy są przypisane do elementu
//    var hasClass1 = elementClasses.contains(class1);
//    var hasClass2 = elementClasses.contains(class2);
//
//    // Wykonujemy odpowiednie funkcje w zależności od obecności klas
//    if (hasClass1 && !hasClass2) {
//      funcA();
//    } else if (!hasClass1 && hasClass2) {
//      funcB();
//    } else if (!hasClass1 && !hasClass2) {
//      funcC();
//    } else if (hasClass1 && hasClass2) {
//      funcD();
//    } else {
//      funcE();
//    }
//  } else {
//    console.log("Element with the provided ID does not exist.");
//  }
//}

//    var episodesToEditContainers = document.getElementsByClassName('episode-to-edit-container');
////    var button = document.getElementById('confirm-episode-' + episode.id + '-changes-button');
//    Array.from(episodesToEditContainers).forEach(function(element) {
//      classListAdd(element.id, 'invisible');
//    });

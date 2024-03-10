function setNewEpisodesSettings() {
    var newEpisodesNumber = document.getElementById('how-many-episodes').value;
    var dateRange = [document.getElementById('start-date').value, document.getElementById('end-date').value];
    var data = {
        'newEpisodesNumber': newEpisodesNumber,
        'dateRange': dateRange
    };
    return data;
}

function showEpisodeEditOverlay(episodeId) {
    var episodesToEditContainers = document.getElementsByClassName('episode-to-edit-container');
//    var button = document.getElementById('confirm-episode-' + episode.id + '-changes-button');
    Array.from(episodesToEditContainers).forEach(function(element) {
      classListAdd(element.id, 'invisible');
    });
      classListAdd('show-episode-' + episodeId + '-edit-overlay-button', 'invisible');
      classListRemove('episode-to-edit-container-' + episodeId, 'invisible');
      classListRemove('episode-' + episodeId + '-edit-overlay', 'invisible');
//      button.removeAttribute('onclick');
//      button.setAttribute('onclick', 'hideEpisodeEditOverlay(' + episodeId + ')');
}

function showEpisodeToEditOverlay(episodeId) {
    loadContent('/settings-overlay-edit-episode', 'settings-overlay-content', episodeId);
    sleep(1).then(() => {
                    classListAdd('show-episode-' + episodeId + '-edit-overlay-button', 'invisible');
                    classListRemove('episode-to-edit-container-' + episodeId, 'invisible');
                    classListRemove('episode-' + episodeId + '-edit-overlay', 'invisible');
                });
}

function confirmEpisodeChanges(episodeId) {
    // fetch function
    hideEpisodeEditOverlay(episodeId);
}

function hideEpisodeEditOverlay(episodeId) {
    var episodesToEditContainers = document.getElementsByClassName('episode-to-edit-container');
    classListRemove('show-episode-' + episodeId + '-edit-overlay-button', 'invisible');
    classListAdd('episode-' + episodeId + '-edit-overlay', 'invisible');
    Array.from(episodesToEditContainers).forEach(function(element) {
      classListRemove(element.id, 'invisible');
    });
      classListRemove('show-episode-' + episodeId + '-edit-overlay-button', 'invisible');
//      button.removeAttribute('onclick');
//      button.setAttribute('onclick', 'showEpisodeEditOverlay(episodeId)');
}

function showEpisodeBestFiveBlock(episodeId, competitionId) {
    classListRemove('episode-' + episodeId + '-' + competitionId + '-best-five-container', 'invisible');
}

function showEpisodeHighlightsOverlay(episodeId) {
//    classListAdd('episode-to-edit-container-' + episodeId, 'invisible');
//    classListAdd('episodes-back-button', 'invisible');
    classListRemove('episode-' + episodeId + '-highlights-container', 'invisible');
}

function showEpisodeToEditContainer(episodeId) {
    editBlocks = document.getElementsByClassName('edit-block');
    Array.from(editBlocks).forEach(function(editBlock) {
        classListRemove(editBlock.id, 'invisible');
    });
    classListRemove('episode-to-edit-container-' + episodeId, 'invisible');
    classListRemove('episodes-back-button', 'invisible');
    classListAdd('episode-' + episodeId + '-highlights-container', 'invisible');
    classListAdd('episode-' + episodeId + '-best-five-container', 'invisible');
}

function processYouTubeUrl(episodeId, number) {
    var highlightBeforeRequestDiv = document.getElementById('highlight-before-request-div-' + episodeId + '-' + number);
    var highlightAfterRequestDiv = document.getElementById('highlight-after-request-div-' + episodeId + '-' + number);
    var inputUrl = document.getElementById('highlight-text-input-' + episodeId + '-' + number);
    var inputDescription = document.getElementById('highlight-description-input-' + episodeId + '-' + number);
    var url = getYoutubeVideoId(inputUrl.value)
    classListAdd(highlightBeforeRequestDiv.getAttribute('id'), 'invisible');
    classListRemove(highlightAfterRequestDiv.getAttribute('id'), 'invisible');
    getTeamsFromSiteTitle('/get-teams-from-site-title', url, inputDescription.id)
}

function eraseResponseContent(episodeId, number) {
    var highlightBeforeRequestDiv = document.getElementById('highlight-before-request-div-' + episodeId + '-' + number);
    var highlightAfterRequestDiv = document.getElementById('highlight-after-request-div-' + episodeId + '-' + number);
    classListRemove(highlightBeforeRequestDiv.getAttribute('id'), 'invisible');
    classListAdd(highlightAfterRequestDiv.getAttribute('id'), 'invisible');
}

function addHighlightFields(episodeId) {
    var highlightsContainer = document.getElementById('highlights-container-' + episodeId);
    var numberOfHighlightsDivs = document.getElementsByClassName('highlight-container').length;

    var highlightContainer = document.createElement('div');
    highlightContainer.setAttribute('id', 'highlight-container-' + episodeId + '-' + numberOfHighlightsDivs);
    highlightContainer.classList.add('highlight-container');

    var highlightBeforeRequestDiv = document.createElement('div');
    highlightBeforeRequestDiv.setAttribute('id', 'highlight-before-request-div-' + episodeId + '-' + numberOfHighlightsDivs);
    highlightBeforeRequestDiv.setAttribute('class', 'highlight-before-request-div');
    highlightContainer.appendChild(highlightBeforeRequestDiv);

    var inputUrl = document.createElement('input');
    inputUrl.type = 'text';
    inputUrl.setAttribute('id', 'highlight-text-input-' + episodeId + '-' + numberOfHighlightsDivs);
    inputUrl.setAttribute('value', '');
    inputUrl.setAttribute('title', '');
    inputUrl.setAttribute('name', 'url-' + episodeId + '-' + numberOfHighlightsDivs);
    inputUrl.classList.add('before-request', 'highlight-text-input');
    highlightBeforeRequestDiv.appendChild(inputUrl);

    var processButton = document.createElement('input');
    processButton.type = 'button';
    processButton.value = '>>';
    processButton.setAttribute('id', 'process-button-' + episodeId + '-' + numberOfHighlightsDivs);
    processButton.classList.add('process-button', 'button-small', 'green-bg');
    processButton.setAttribute('onclick', 'processYouTubeUrl(' + episodeId + ', ' + numberOfHighlightsDivs + ')');
    highlightBeforeRequestDiv.appendChild(processButton);

    var highlightAfterRequestDiv = document.createElement('div');
    highlightAfterRequestDiv.setAttribute('id', 'highlight-after-request-div-' + episodeId + '-' + numberOfHighlightsDivs);
    highlightAfterRequestDiv.classList.add('invisible', 'highlight-after-request-div');
    highlightContainer.appendChild(highlightAfterRequestDiv);

    var inputDescription = document.createElement('input');
    inputDescription.type = 'text';
    inputDescription.setAttribute('id', 'highlight-description-input-' + episodeId + '-' + numberOfHighlightsDivs);
    inputDescription.setAttribute('class', 'highlight-description');
    inputDescription.setAttribute('name', 'teams-' + episodeId + '-' + numberOfHighlightsDivs);
    highlightAfterRequestDiv.appendChild(inputDescription);

//    var inputVideoId = document.createElement('input');
//    inputVideoId.type = 'text';
//    inputVideoId.setAttribute('id', 'video-id-input-' + episodeId + '-' + numberOfHighlightsDivs);
//    inputVideoId.setAttribute('class', 'invisible');
//    inputVideoId.setAttribute('name', 'video-id-' + episodeId + '-' + numberOfHighlightsDivs);
//    highlightAfterRequestDiv.appendChild(inputVideoId);

    var eraseButton = document.createElement('input');
    eraseButton.type = 'button';
    eraseButton.value = '<<';
    eraseButton.setAttribute('id', 'erase-button-' + episodeId + '-' + numberOfHighlightsDivs);
    eraseButton.classList.add('erase-button', 'button-small', 'yellow-bg');
    eraseButton.setAttribute('onclick', 'eraseResponseContent(' + episodeId + ', ' + numberOfHighlightsDivs + ')');
    highlightAfterRequestDiv.appendChild(eraseButton);

    var deleteButton = document.createElement('input');
    deleteButton.type = 'button';
    deleteButton.value = 'X';
    deleteButton.setAttribute('id', 'delete-button-' + numberOfHighlightsDivs);
    deleteButton.classList.add('delete-button', 'button-small', 'red-bg');
    deleteButton.setAttribute('ondblclick', 'removeHighlightFields(' + episodeId + ', ' + 'this.id)');
    highlightAfterRequestDiv.appendChild(deleteButton);

    // Dodawanie diva do dynamic-content
    highlightsContainer.appendChild(highlightContainer);
}

function removeHighlightFields(episodeId, buttonId) {
    let splittedButtonId = buttonId.split('-');
    let highlightContainerNumber = splittedButtonId[splittedButtonId.length - 1];
    let highlightsContainer = document.getElementById('highlights-container' + episodeId);
    let highlightContainer = document.getElementById('highlight-container-' + episodeId + '-' + highlightContainerNumber);
    if (highlightContainer && highlightContainer.parentNode) {
        highlightContainer.parentNode.removeChild(highlightContainer);
    }
}

function deleteCompetition(competitionId) {
    let endpoint = '/settings-overlay-delete-competition/' + competitionId;
    fetch(endpoint);
    loadContent('/settings-overlay-edition', 'settings-overlay-content');
}

function updateCheckboxValue(checkbox) {
//    var hiddenCheckbox = document.getElementById('hidden-is-cup-checkbox');
    if (checkbox.checked) {
        checkbox.value = '1';
    } else {
        checkbox.value = '0';
    }
}

function getYoutubeVideoId(url) {
    var videoIdStart = url.indexOf("v=") + 2;
    var videoIdEnd = url.indexOf("&", videoIdStart);

    if (videoIdEnd === -1) {
        return url.slice(videoIdStart);
    } else {
        return url.slice(videoIdStart, videoIdEnd);
    }
}

function passCompetitionType() {
    var radioButtons = document.getElementsByClassName('competition-best-five-radio');
    var hiddenInput = document.getElementById('competition-best-five-hidden');

    radioButtons.forEach(function(radioButton) {
        radioButton.addEventListener('change', function() {
            hiddenInput.value = this.value;
        });
    });
}

function hideEditWrappers() {
    const editWrappers = document.getElementsByClassName('edit-wrapper');
    Array.from(editWrappers).forEach(function(editWrapper) {
        classListAdd(editWrapper.id, 'invisible');
    });
}
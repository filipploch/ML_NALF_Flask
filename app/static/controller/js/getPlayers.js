async function displayOptions(playerInputId, teamInputId, dataListId) {
    const playerInput = document.getElementById(playerInputId);
    const teamInput = document.getElementById(teamInputId);
    const dataList = document.getElementById(dataListId);
    playerInput.addEventListener('focus', function() {
        // Zmiana klasy na visible, gdy input jest aktywowany (ma kursor)
        classListRemove(dataListId, 'invisible');
    });

    playerInput.addEventListener('blur', function() {
        // Zmiana klasy na invisible, gdy input nie jest aktywowany (brak kursora)
        classListAdd(dataListId, 'invisible');
    });
    playerInput.addEventListener('input', async function() {
        var searchInput = playerInput.value.toLowerCase();
        try {
            // Pobieranie danych z serwera za pomocą fetch
            var response = await fetch('/get-players?query=' + searchInput);
            var data = await response.json();

            // Filtrujemy wyniki na podstawie wpisanego tekstu
            var filteredResults = data.filter(function(result) {
                return result;
//                return result.name.toLowerCase().includes(searchInput);
            });

            // Czyścimy poprzednie wyniki
            dataList.innerHTML = '';

            // Dodajemy nowe wyniki do dataList
            filteredResults.forEach(function(result) {
                var option = document.createElement('option');
                option.value = result.team;
                option.text = result.name;
                option.setAttribute('data-bestfive', result.best_five);
                option.addEventListener('mousedown', function(event) {
                    playerInput.value = option.text + ' (' + option.dataset.bestfive + ')';
                    playerInput.title = option.text + ' (' + option.dataset.bestfive + ')';
                    playerInput.focus();
                    teamInput.value = option.value;
                    teamInput.title = option.value;
//                    teamInput.title = 'to jest przykładowy tekst title';
                    teamInput.focus();
            classListAdd('dataList', 'invisible');
                });
                dataList.appendChild(option);
            });
        } catch (error) {
            console.error('Błąd fetch:', error);
        }
    });
}
    function addDynamicFunction() {
        var script = document.createElement('script');
        script.textContent = `
            function mojaDynamicznaFunkcja() {
                console.log('To jest dynamiczna funkcja!');
            }
        `;
        document.body.appendChild(script);
    }

    function callDynamicFunction() {
        if (typeof mojaDynamicznaFunkcja === 'function') {
            mojaDynamicznaFunkcja();
        } else {
            console.log('Funkcja jeszcze nie została dodana.');
        }
    }
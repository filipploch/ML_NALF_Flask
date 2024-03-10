//  function checkDatepickerExistence(className) {
//    // Pobierz listę elementów o danej klasie
//    const datepickerElements = document.getElementsByClassName(className);
//
//    // Iteruj przez listę i wywołaj funkcję checkAndInitDatepicker dla każdego elementu
//    Array.from(datepickerElements).forEach(function(element) {
//      checkAndInitDatepicker(element);
//    });
//  }

  function initDatepicker(elementId) {
    const inputElement = document.getElementById(elementId);
    if (inputElement) {
      const existingDatepicker = inputElement.datepicker;
      if (!existingDatepicker) {
        inputElement.datepicker = new DateRangePicker(inputElement, {'format': 'yyyy-mm-dd'});
      }
    } else {
      console.log('Element input nie istnieje.');
    }
  }
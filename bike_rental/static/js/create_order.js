document.addEventListener("DOMContentLoaded", function() {
  // Funkcja aktualizująca dostępność opcji w polach sprzętu
  function updateEquipmentOptions() {
    const equipmentFields = document.querySelectorAll('.equipment-field');
    let selectedOptions = [];

    // Zbieramy wszystkie wybrane wartości
    equipmentFields.forEach(function(field) {
      if (field.value) {
        selectedOptions.push(field.value);
      }
    });

    console.log("Wybrane opcje:", selectedOptions);

    // Aktualizujemy dostępność opcji w każdym polu
    equipmentFields.forEach(function(field) {
      const options = field.querySelectorAll('option');
      options.forEach(function(option) {
        if (selectedOptions.includes(option.value) && option.value !== field.value) {
          option.disabled = true;
          console.log(`Wyłączam opcję ${option.value} w polu ${field.id}`);
        } else {
          option.disabled = false;
        }
      });
    });
  }

  // Funkcja aktualizująca dostępność opcji w polach akcesoriów
  function updateAccessoryOptions() {
    const accessoryFields = document.querySelectorAll('.accessory-field');
    let AccselectedOptions = [];

    // Zbieramy wszystkie wybrane wartości
    accessoryFields.forEach(function(field) {
      if (field.value) {
        AccselectedOptions.push(field.value);
      }
    });

    console.log("Wybrane opcje:", AccselectedOptions);

    // Aktualizujemy dostępność opcji w każdym polu
    accessoryFields.forEach(function(field) {
      const options = field.querySelectorAll('option');
      options.forEach(function(option) {
        if (AccselectedOptions.includes(option.value) && option.value !== field.value) {
          option.disabled = true;
          console.log(`Wyłączam opcję ${option.value} w polu ${field.id}`);
        } else {
          option.disabled = false;
        }
      });
    });
  }

  // Inicjalizacja formularzy
  const equipmentFields = document.querySelectorAll('.equipment-field');
  equipmentFields.forEach(function(field) {
    field.addEventListener('change', updateEquipmentOptions);
  });

  const accessoryFields = document.querySelectorAll('.accessory-field');
  accessoryFields.forEach(function(field) {
    field.addEventListener('change', updateAccessoryOptions);
  });

  // Wywołujemy funkcję na starcie
  updateEquipmentOptions();
  updateAccessoryOptions();

  // Funkcja ustawiająca min i max dla end_date
  function updateEndDateLimits() {
    const startDateField = document.querySelector("input[name='start_date']");
    const endDateField = document.querySelector("input[name='end_date']");

    if (startDateField && endDateField) {
      const startDate = startDateField.value;
      if (startDate) {
        // Ustawienie min daty dla end_date
        endDateField.setAttribute("min", startDate);
        // Ustawienie max daty dla end_date (start_date + 14 dni)
        const maxDate = new Date(startDate);
        maxDate.setDate(maxDate.getDate() + 14);  // Dodajemy 14 dni
        endDateField.setAttribute("max", maxDate.toISOString().split("T")[0]);
      }
    }
  }

  // Wywołujemy funkcję przy każdej zmianie start_date
  const startDateField = document.querySelector("input[name='start_date']");
  if (startDateField) {
    startDateField.addEventListener('change', updateEndDateLimits);
  }

  // Wywołujemy funkcję na starcie, aby ustawić wartości domyślne
  updateEndDateLimits();
});
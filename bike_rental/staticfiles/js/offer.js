function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.style.display = 'none');
    document.querySelectorAll('#tabs li').forEach(tab => tab.classList.remove('active-tab'));
    document.getElementById(tabId).style.display = 'block';
    document.getElementById(`${tabId}-link`).classList.add('active-tab');
  }

  // Funkcja do utrzymywania aktywnej zakładki po załadowaniu strony
  function maintainActiveTab() {
    const activeTab = localStorage.getItem('activeTab');
    if (activeTab) {
      showTab(activeTab);
    } else {
      // Domyślnie ustawia tablicę na "bikes-tab"
      showTab('bikes-tab');
    }
  }

  // Funkcja wywołana przy zmianie zakładki
  window.onload = function () {
    maintainActiveTab();
    updatePriceOutput();
  };

  // Przechowywanie aktywnej zakładki w localStorage
  document.querySelectorAll('#tabs li').forEach(tab => {
    tab.addEventListener('click', function () {
      const tabId = this.id.replace('-link', '');
      localStorage.setItem('activeTab', tabId);
    });
  });
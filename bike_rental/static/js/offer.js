function showTab(tabId) {
  // Ukryj wszystkie zakładki i usuń klasę aktywną
  document.querySelectorAll('.tab-content').forEach(tab => tab.style.display = 'none');
  document.querySelectorAll('#tabs li').forEach(tab => tab.classList.remove('active-tab'));

  // Wyświetl wybraną zakładkę i ustaw ją jako aktywną
  const selectedTab = document.getElementById(tabId);
  const selectedTabLink = document.getElementById(`${tabId}-link`);
  if (selectedTab && selectedTabLink) {
      selectedTab.style.display = 'block';
      selectedTabLink.classList.add('active-tab');
  }
}

function maintainActiveTab() {
  const activeTab = localStorage.getItem('activeTab');
  console.log('Restoring active tab:', activeTab); // Debugowanie
  if (activeTab) {
    showTab(activeTab);
  } else {
    showTab('bikes-tab'); // Domyślnie bikes-tab
  }
}

window.onload = function () {
  maintainActiveTab();
};

document.querySelectorAll('#tabs li').forEach(tab => {
  tab.addEventListener('click', function () {
      const tabId = this.id.replace('-link', '');
      localStorage.setItem('activeTab', tabId);
      console.log('Active tab saved:', tabId); // Debugowanie
  });
});





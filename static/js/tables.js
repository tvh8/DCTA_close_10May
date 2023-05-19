// Fetch data and populate tables
async function loadDataAndPopulateTables() {
  // Fetch all bills
  const responseBills = await fetch('/get_bills');
  const allBills = await responseBills.json();

  // Filter recently introduced bills
  const recentlyIntroduced = allBills.sort((a, b) => new Date(b.introduced) - new Date(a.introduced)).slice(0, 10);
  // Populate 'Recently Introduced' table
  populateTable(recentlyIntroduced, document.getElementById('recently-introduced-table-body'), true);

  // Filter recent actions
  const recentActions = allBills.sort((a, b) => new Date(b.latest_action_date) - new Date(a.latest_action_date)).slice(0, 10);
  // Populate 'Recent Actions' table
  populateTable(recentActions, document.getElementById('recent-actions-table-body'), false);
}

// Removed window.onload = loadDataAndPopulateTables;

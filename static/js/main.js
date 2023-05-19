var fullData = []
function loadRecentData() {
    $.get('/get_bills', function (data) {
        var recentData = data;
        recentData.sort(function (a, b) {
            return new Date(b['Introduced']) - new Date(a['Introduced']);
        });
        recentData = recentData.slice(0, 100);
        var table = $('#recently-introduced-table-body');
        table.empty();
        recentData.forEach(function (row) {
            var tr = $('<tr>');
            tr.append($('<td>').text(row['bill_number']));
            tr.append($('<td>').text(row['st']));
            tr.append($('<td>').text(row['short_subject']));
            tr.append($('<td>').text(row['introduced']));
            tr.click(function () {
                populateSelectedBillCard(row);
            });
            table.append(tr);
        });
    });
}

function loadRecentActionsData() {
    $.get('/get_bills', function (data) {
        var recentData = data;
        recentData.sort(function (a, b) {
            return new Date(b['Latest Action Date']) - new Date(a['Latest Action Date']);
        });
        recentData = recentData.slice(0, 100);
        var table = $('#recent-actions-table-body');
        table.empty();
        recentData.forEach(function (row) {
            var tr = $('<tr>');
            tr.append($('<td>').text(row['bill_number']));
            tr.append($('<td>').text(row['st']));
            tr.append($('<td>').text(row['short_subject']));
            tr.append($('<td>').text(row['latest_action_date']));
            tr.click(function () {
                populateSelectedBillCard(row);
            });
            table.append(tr);
        });
    });
}

function loadAllData() {
    $.get('/get_bills', function (data) {
        fullData = data;
        fullData.sort(function (a, b) {
            return a['St'].localeCompare(b['St']);
        });
        populateTable(fullData);
    });
}
function populateSelectedBillCard(bill) {
    console.log(bill);

    // Set the new data
    $('#selectedBillNumber').text(bill['bill_number'] || '');
    $('#selectedBillState').text(bill['state'] || '');
    $('#selectedBillSession').text(bill['session'] || '');
    $('#selectedBillIntroduced').text(bill['introduced'] || '');
    $('#selectedBillLatestAction').text(bill['latest_action'] || '');
    $('#selectedBillLatestActionDate').text(bill['latest_action_date'] || '');
    $('#selectedBillPrimarySponsor').text(bill['primary_sponsor'] || '');
    $('#selectedBillSubject').text(bill['subject'] || '');
    $('#selectedBillSummary').text(bill['summary'] || '');
    $('#selectedBillCryptoImpact').text(bill['crypto_impact'] || '');
    $('#selectedBillDCTAAnalysis').text(bill['dcta_analysis'] || '');
    $('#selectedBilltimestamp').text(bill['timestamp'] || '');
    $('#latestBillBtn').data('latestBillTextUrl', bill['latest_bill_text_url'] || '');
    $('#openStatesBtn').data('openStatesUrl', bill['link'] || '');

    populateSelectedBillAnalysis(bill['bill_number'] || '');
}

function previewBill(billId) {
    $.get('/preview/' + billId, function (data) {
        var bill = data[0];
        var previewContainer = $('.preview-container');
        previewContainer.empty();
        // Add the bill's details to the preview container
        previewContainer.append($('<h4>').text('bill_number' + bill['bill_number']));
        previewContainer.append($('<p>').text('state: ' + bill['state']));
        previewContainer.append($('<p>').text('subject: ' + bill['subject']));
        previewContainer.append($('<p>').text('introduced: ' + bill['introduced']));
        previewContainer.append($('<p>').text('latest_action: ' + bill['latest_action']));
        previewContainer.append($('<p>').text('position: ' + bill['position']));
        previewContainer.append($('<p>').text('primary_sponsor: ' + bill['primary_sponsor']));
    });
}

$(document).ready(function () {
    $("table tbody tr").on("click", function () {
        // Remove 'highlighted' class from all rows
        $("table tbody tr").removeClass("highlighted");

        // Add 'highlighted' class to the clicked row
        $(this).addClass("highlighted");

        // Get the index of the clicked row
        const rowIndex = $(this).index();

        // Synchronize the highlighting in other tables
        $("table.recently-introduced tbody tr").eq(rowIndex).addClass("highlighted");
        $("table.recent-actions tbody tr").eq(rowIndex).addClass("highlighted");
        $("table.search-results tbody tr").eq(rowIndex).addClass("highlighted");
    });
    loadRecentData();
    loadRecentActionsData();
    loadAllData()
    $('#latestBillBtn').click(function() {
        var url = $(this).data('latestBillTextUrl');
        if(url && url !== '') {
            window.open(url, '_blank');
        } else {
            console.log("No URL found for Latest Bill Text");
        }
    });

    $('#openStatesBtn').click(function () {
        const openStatesUrl = $(this).data('openStatesUrl');
        if (openStatesUrl) {
            window.open(openStatesUrl, '_blank');
        }
    });

    $('#analyzeBtn').click(function () {
        // Get the actual values from the selected bill
        var latest_bill_text = $('#latestBillBtn').data('latestBillTextUrl');
        var bill_number = $('#selectedBillNumber').text();
        var bill_state = $('#selectedBillState').text();
        var bill_session = $('#selectedBillSession').text();

        // Call the backend route to execute the OpenAI_analysis.py script
        $.get('/analyze', {
            latest_bill_text: latest_bill_text,
            bill_number: bill_number,
            bill_state: bill_state,
            bill_session: bill_session
        }, function (data) {
            // Update the displayed data with the new analysis results
            $('#selectedBillSummary').text(data['summary']);
            $('#selectedBillCryptoImpact').text(data['crypto_impact']);
            $('#selectedBillDCTAAnalysis').text(data['dcta_analysis']);
            $('#selectedBilltimestamp').text(data['timestamp']);

            // Set a timeout to refresh the page 10 seconds after the data is received
            setTimeout(function () {
                location.reload();
            }, 10000);  // 10000 milliseconds = 10 second
        });
    });

    $('#createLetterbtn').click(function () {
        const billId = $('#selectedBillNumber').text();  // Get the selected bill number
        $.get('/create_letter/' + billId, function (data) {
            console.log(data);
        });
    });

    // Trigger the default tab to open after everything else has been initialized
    $('#defaultOpen').click();

    $('#search-button').click(function() {
        const searchTerm = $('#search-input').val();
        if(searchTerm) {
            const filteredData = filterData(searchTerm, fullData);
            populateTable(filteredData);
        } else {
            populateTable(fullData);
        }
    });


});

function populateSelectedBillAnalysis(billNumber) {
    // Clear the old data
    $('#selectedBillSummary').text('');
    $('#selectedBillCryptoImpact').text('');
    $('#selectedBillDCTAAnalysis').text('');
    $('#selectedBilltimestamp').text('');

    $.get('/get_analysis/' + billNumber, function (data) {
        if (data) {
            // Set the new data
            $('#selectedBillSummary').text(data['summary'] || '');
            $('#selectedBillCryptoImpact').text(data['crypto_impact'] || '');
            $('#selectedBillDCTAAnalysis').text(data['dcta_analysis'] || '');
            $('#selectedBilltimestamp').text(data['timestamp'] || '');
        }
        console.log(data)
    });
}

function openTab(evt, tabName) {
  console.log(evt);
  console.log(evt.currentTarget);

  // Hide all tabcontent elements
  var tabcontent = document.getElementsByClassName("tabcontent");
  for (var i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Remove the active class from all tablinks/buttons
  var tablinks = document.getElementsByClassName("tablinks");
  for (var i = 0; i < tablinks.length; i++) {
    var className = tablinks[i].className.replace(" active", "");
    tablinks[i].className = className;
  }

  // Show the specific tab content and add an "active" class to the button that opened the tab
  document.getElementById(tabName).style.display = "block";

  // Add the "active" class to the button that triggered the event
  evt.currentTarget.className += " active";
}

function filterData(searchTerm, data) {
    return data.filter(function(row) {
        return Object.values(row).some(val => String(val).toLowerCase().includes(searchTerm.toLowerCase()));
    });
}

function populateTable(data) {
    var table = $('#search-results-table tbody');
    table.empty();
    data.forEach(function (row) {
        var tr = $('<tr>');
        tr.append($('<td>').text(row['bill_number']));
        tr.append($('<td>').text(row['st']));
        tr.append($('<td>').text(row['subject']));
        tr.click(function () {
            populateSelectedBillCard(row);
        });
        table.append(tr);
    });
}
//Line placed at end of script//
window.onload = function() {
    document.getElementById("defaultOpen").click();
};

window.addEventListener('load', function() {
  document.getElementById("defaultOpen").click();
  loadDataAndPopulateTables();  // Call the function from tables.js
});
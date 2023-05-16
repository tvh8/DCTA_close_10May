var fullData = []
var dateField = 'event_date';

function loadAllData() {
    $.get('/get_bills', function (data) {
        fullData = data.filter(function (item) {
            return item['St'] !== 'DE' && item['St'] !== 'DC' && item['St'] !== 'RMI';
        });
        console.log('fullData:', fullData);
        loadRecentData(fullData, $('#recently-introduced-table-body'), 'Introduced');
        loadRecentActionsData(fullData, $('#recent-actions-table-body'), 'Latest Action Date');
        populateTable(fullData, $('#search-results-table tbody'), 'Subject');
    });
}

function loadRecentData(data, tableBody, key) {
    console.log('loadRecentData - data:', data);
    var recentData = [...data]; // create a copy of data
    recentData.sort(function (a, b) {
        return new Date(b[key]) - new Date(a[key]);
    });
    recentData = recentData.slice(0, 100);
    populateTable(recentData, tableBody, dateField);
}

function loadRecentActionsData(data, tableBody, key) {
    console.log('loadRecentActionsData - data:', data);
    loadRecentData(data, tableBody, dateField);
}
$(document).ready(function () {
    loadAllData()
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

    loadRecentActionsData();

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
            $('#selectedBillSummary').text(data['Summary']);
            $('#selectedBillCryptoImpact').text(data['Crypto Impact']);
            $('#selectedBillDCTAAnalysis').text(data['DCTA Analysis']);
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

function populateTable(data, tableElement, dateField) {
    tableElement.empty();
    data.forEach(function (row) {
        var tr = $('<tr>');
        tr.append($('<td>').text(row['Bill #']));
        tr.append($('<td>').text(row['St']));
        tr.append($('<td>').text(row['Short Subject']));
        tr.append($('<td>').text(row[dateField]));
        tr.click(function () {
            // Unhighlight all other rows
            $('tr').css('background-color', '');
            // Highlight the clicked row
            $(this).css('background-color', 'yellow');
            populateSelectedBillCard(row);
        });
        tableElement.append(tr);
    });
}
function populateSelectedBillCard(bill) {
    console.log(bill);
    // Set the new data
    $('#selectedBillNumber').text(bill['Bill #'] || '');
    $('#selectedBillState').text(bill['State'] || '');
    $('#selectedBillSession').text(bill['Session'] || '');
    $('#selectedBillIntroduced').text(bill['Introduced'] || '');
    $('#selectedBillLatestAction').text(bill['Latest Action'] || '');
    $('#selectedBillLatestActionDate').text(bill['Latest Action Date'] || '');
    $('#selectedBillPrimarySponsor').text(bill['Primary Sponsor'] || '');
    $('#selectedBillSubject').text(bill['Subject'] || '');
    $('#selectedBillSummary').text(bill['Summary'] || '');
    $('#selectedBillCryptoImpact').text(bill['Crypto Impact'] || '');
    $('#selectedBillDCTAAnalysis').text(bill['DCTA Analysis'] || '');
    $('#selectedBilltimestamp').text(bill['timestamp'] || '');
    $('#latestBillBtn').data('latestBillTextUrl', bill['Latest Bill Text'] || '');
    $('#openStatesBtn').data('openStatesUrl', bill['Link'] || '');

    populateSelectedBillAnalysis(bill['Bill #'] || '');
}

function previewBill(billId) {
    $.get('/preview/' + billId, function (data) {
        var bill = data[0];
        var previewContainer = $('.preview-container');
        previewContainer.empty();
        // Add the bill's details to the preview container
        previewContainer.append($('<h4>').text('Bill #' + bill['Bill #']));
        previewContainer.append($('<p>').text('State: ' + bill['State']));
        previewContainer.append($('<p>').text('Subject: ' + bill['Subject']));
        previewContainer.append($('<p>').text('Introduced: ' + bill['Introduced']));
        previewContainer.append($('<p>').text('Latest Action: ' + bill['Latest Action']));
        previewContainer.append($('<p>').text('Position: ' + bill['Position']));
        previewContainer.append($('<p>').text('Primary Sponsor: ' + bill['Primary Sponsor']));
    });
}

function populateSelectedBillAnalysis(billNumber) {
    // Clear the old data
    $('#selectedBillSummary').text('');
    $('#selectedBillCryptoImpact').text('');
    $('#selectedBillDCTAAnalysis').text('');
    $('#selectedBilltimestamp').text('');

    $.get('/get_analysis/' + billNumber, function (data) {
        if (data) {
            // Set the new data
            $('#selectedBillSummary').text(data['Summary'] || '');
            $('#selectedBillCryptoImpact').text(data['Crypto Impact'] || '');
            $('#selectedBillDCTAAnalysis').text(data['DCTA Analysis'] || '');
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
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the specific tab content and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

function filterData(searchTerm, data) {
    return data.filter(function(row) {
        return Object.values(row).some(val => String(val).toLowerCase().includes(searchTerm.toLowerCase()));
    });
}

function changeColor() {
  var dropdown = document.getElementById('dropdown');
  var selectedValue = dropdown.options[dropdown.selectedIndex].value;

  if (selectedValue === 'support') {
    dropdown.style.backgroundColor = 'green';
  } else if (selectedValue === 'oppose') {
    dropdown.style.backgroundColor = 'red';
  } else if (selectedValue === 'watch') {
    dropdown.style.backgroundColor = 'grey';
  } else {
    dropdown.style.backgroundColor = 'white';
  }
}

function populateSearchTable(data) {
    var table = $('#search-results-table tbody');
    table.empty();
    data.forEach(function (row) {
        var tr = $('<tr>');
        tr.append($('<td>').text(row['Bill #']));
        tr.append($('<td>').text(row['St']));
        tr.append($('<td>').text(row['Subject']));
        tr.click(function () {
            // Unhighlight all other rows
            $('tr').css('background-color', '');
            // Highlight the clicked row
            $(this).css('background-color', 'yellow');
            populateSelectedBillCard(row);
        });
        table.append(tr);
    });
}
//Line placed at end of script//
window.onload = function() {
    document.getElementById("defaultOpen").click();
};

document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    events: '/get_events',
    // Other FullCalendar options...
  });

  calendar.render();
});

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
            tr.append($('<td>').text(row['Bill #']));
            tr.append($('<td>').text(row['St']));
            tr.append($('<td>').text(row['Short Subject']));
            tr.append($('<td>').text(row['Introduced']));
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
            tr.append($('<td>').text(row['Bill #']));
            tr.append($('<td>').text(row['St']));
            tr.append($('<td>').text(row['Short Subject']));
            tr.append($('<td>').text(row['Latest Action Date']));
            tr.click(function () {
                populateSelectedBillCard(row);
            });
            table.append(tr);
        });
    });
}

function populateSelectedBillCard(bill) {
    $('#selectedBillNumber').text(bill['Bill #']);
    $('#selectedBillState').text(bill['State']);
    $('#selectedBillSession').text(bill['Session']);
    $('#selectedBillIntroduced').text(bill['Introduced']);
    $('#selectedBillLatestAction').text(bill['Latest Action']);
    $('#selectedBillLatestActionDate').text(bill['Latest Action Date']);
    $('#selectedBillPrimarySponsor').text(bill['Primary Sponsor']);
    $('#selectedBillSubject').text(bill['Subject']);
    $('#latestBillBtn').data('latestBillTextUrl', bill['Latest Bill Text']);
    $('#openStatesBtn').data('openStatesUrl', bill['Link']);
    updateSummaryContent(bill['Bill #']);
}

function updateSummaryContent(billNumber) {
  $.get(`/get_summary_data?bill_number=${billNumber}`, function (data) {
    const summaryElement = document.getElementById("summary");
    const cryptoImpactElement = document.getElementById("crypto-impact");
    const dctaAnalysisElement = document.getElementById("dcta-analysis");

    const summaryLastUpdated = summaryElement.querySelector("h6");
    const cryptoImpactLastUpdated = cryptoImpactElement.querySelector("h6");
    const dctaAnalysisLastUpdated = dctaAnalysisElement.querySelector("h6");

    const summaryContent = summaryElement.querySelector("p");
    const cryptoImpactContent = cryptoImpactElement.querySelector("p");
    const dctaAnalysisContent = dctaAnalysisElement.querySelector("p");

    if (data) {
      summaryLastUpdated.innerHTML = `Last Updated: ${data.timestamp}`;
      cryptoImpactLastUpdated.innerHTML = `Last Updated: ${data.timestamp}`;
      dctaAnalysisLastUpdated.innerHTML = `Last Updated: ${data.timestamp}`;

      summaryContent.innerHTML = data.summary;
      cryptoImpactContent.innerHTML = data.crypto_impact;
      dctaAnalysisContent.innerHTML = data.dcta_analysis;
    } else {
      summaryLastUpdated.innerHTML = "Last Updated:";
      cryptoImpactLastUpdated.innerHTML = "Last Updated:";
      dctaAnalysisLastUpdated.innerHTML = "Last Updated:";

      summaryContent.innerHTML = "No summary data available for the selected bill.";
      cryptoImpactContent.innerHTML = "No crypto impact data available for the selected bill.";
      dctaAnalysisContent.innerHTML = "No DCTA analysis data available for the selected bill.";
    }
  });
}

function analyzeAndUpdateContent(billNumber) {
  // Simulate the analysis process
  setTimeout(() => {
    // After the analysis is done, update the content
    updateSummaryContent(billNumber);
  }, 1000); // Adjust this value to simulate the time it takes for the analysis process
}

function search() {
    var query = $('#search-input').val();
    $.post('/search', { query: query }, function (data) {
        var searchResults = data;
        var table = $('#search-results-table');
        table.empty();
        searchResults.forEach(function (row) {
            var tr = $('<tr>');
            tr.append($('<td>').text(row['Bill #']));
            tr.append($('<td>').text(row['State']));
            tr.append($('<td>').text(row['Subject']));
            tr.append($('<td>').text(row['Introduced']));
            tr.append($('<td>').text(row['Latest Action']));
            tr.append($('<td>').text(row['Position']));
            tr.append($('<td>').text(row['Primary Sponsor']));
            tr.click(function () {
                previewBill(row['Bill #']);
            });
            table.append(tr);
        });
    });
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

$(document).ready(function () {
    $("#analyzeBtn").on("click", function () {
    const billNumber = $("#selectedBillNumber").text();
    analyzeAndUpdateContent(billNumber);
  });
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
    $('#latestBillBtn').click(function () {
        const latestBillTextUrl = $(this).data('latestBillTextUrl');
        if (latestBillTextUrl) {
            window.open(latestBillTextUrl, '_blank');
        }
    });

    $('#openStatesBtn').click(function () {
        const openStatesUrl = $(this).data('openStatesUrl');
        if (openStatesUrl) {
            window.open(openStatesUrl, '_blank');
        }
    });

    $('#analyzeBtn').click(function () {
    const billNumber = $('#selectedBillNumber').text();
    const billState = $('#selectedBillState').text();
    const billSession = $('#selectedBillSession').text();

    // Show the spinner
    $('#analyzeSpinner').css('display', 'inline-block');
    console.log('Spinner should be visible now.');

    // Call the backend route to execute the OpenAI_analysis.py script
    $.get('/analyze', { bill_number: billNumber, bill_state: billState, bill_session: billSession }, function (data, textStatus, jqXHR) {
        // Process the response data as needed
        console.log(data);
        if (jqXHR.status === 408) {
            alert("The analysis process took too long and has timed out. Please try again later.");
        } else {
            setTimeout(function() {
                updateSummaryContent(billNumber);
            }, 1000);
        }
    });
});

    loadRecentData();
});

function openTab(evt, tabName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("defaultOpen").click();
});
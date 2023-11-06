// BO columns
/*
   { data: "Nr" },
   { data: "Titel" },
   { data: "Beschrieb" },
   { data: "Ort" },
   { data: "OrtLink" },
   { data: "Jahr" },
   { data: "Akteurinnen" },
   { data: "Themenfelder" },
   { data: "FinanzielleUnterstuetzung" },
   { data: "Laufend" },
   { data: "Link1" },
   { data: "Link2" }
*/
columns: [
    { data: "Nr",
        render: function (data, type, row) {
            
            // Workaround for Microsoft Edge 44.18362.449.0
            if (row.Nr !== undefined) {
                return row.Nr.toString();
            }
            else {
                return '';
            }
        }
    },
    { data: "Titel",
        render: function (data, type, row) {
            return '<span style="color: #0074c4; text-decoration: none; border-bottom: 1px solid #bfdcf0;">' +
                row.Titel + '</span>';
        }
    },
    { data: "Beschrieb",
        render: function (data, type, row) {
            if (row['Beschrieb'].toString().length > 100) {
                return row['Beschrieb'].toString().substring(0, 100) + '...';
            }
            return row['Beschrieb'].toString();
        }
    },
    { data: "Jahr" },
    { data: "Ort",
        render: function (data, type, row) {
            return '<a href="' + row['OrtLink'] + '" target="_blank">' +
                data.toString() + '</a>';
        }
    },
    { data: "Themenfelder", width: "15%" },
    { data: "Akteurinnen", width:"15%" }
]
// EO columns

// BO columnDefs
columnDefs: [
    { width: "15%", targets: 5,6 }
]
// EO columnDefs

// BO processCustomJS
function processCustomJS(table) {
    $('#e937688 tbody').on('click', 'td', function () {
        var tr = this.closest('tr');
        var row = table.row(tr);
        if (this.cellIndex == 1 || this.cellIndex == 2) {
            title = row.data()['Titel'];
            body = row.data()['Beschrieb'] + '<br /><br />';
            support = '<strong>Finanzielle Unterstützung:</strong> ' + row.data()['FinanzielleUnterstuetzung'] + '<br />';
            support = row.data()['FinanzielleUnterstuetzung'].trim() != '' ? support : '';
            ongoing = '<strong>Laufend:</strong> ' + row.data()['Laufend'] + '<br /><br />';
            href1 = row.data()['Link1'];
            link1 = href1.substring(0, 50);
            link1 = link1.length==50 ? link1 + '...' : link1;
            href2 = row.data()['Link2'];
            link2 = href2.substring(0, 50);
            link2 = link2.length==50 ? link2 + '...' : link2;
            $('#datatableModalTitle').text(title);
            $('#datatableModalBody').html(body + support + ongoing +
                '<a href="' +
                href1 + '" target="_blank">' + link1 + '</a><br /><a href="' +
                href2 + '" target="_blank">' + link2 + '</a>');
            $('#datatableModal').modal('toggle');
        }
    });
    $('#e937688 tbody').on('mouseover', 'td', function () {
        var tr = this.closest('tr');
        var row = table.row(tr);
        if (this.cellIndex == 1 || this.cellIndex == 2) {
            $(this).css('cursor', 'pointer');
        }
    });
}
// EO processCustomJS
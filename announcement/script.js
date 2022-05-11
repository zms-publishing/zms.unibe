"use strict";

const TimeSpan = Object.freeze({
    NOW: 1,
    FUTURE: 2,
    PAST: 3
});

let unknownDateText = "";

let timeSpanDict = {};
timeSpanDict[TimeSpan.NOW] = "Aktuell";
timeSpanDict[TimeSpan.FUTURE] = "Anstehend";
timeSpanDict[TimeSpan.PAST] = "Vergangen";

let typeDict = {
    "WARTUNG": "Wartung",
    "DRINGENDE WARTUNG": "Wartung",
    "STOERUNG": "Störung",
    "SICHERHEITSMELDUNG": "Sicherheit",
    "HINWEIS": "Hinweis"
};

let repeatingValueClass = "repeating";

function mapType(type) {
    return typeDict[type];
}

function renderTimeSpan(timeSpan, role) {
    if (role === "display") {
        return timeSpanDict[timeSpan];
    }
    return timeSpan;
}

function renderDate(date, role) {
    if (date) {
        if (role === "display") {
            let dateString = date.toLocaleString('de-CH', {day: '2-digit', month: '2-digit', year: 'numeric'});
            let timeString = date.toLocaleString('de-CH', {hour: 'numeric', minute: 'numeric'});
            if (timeString !== '00:00') {
                return dateString + '<br />' + timeString;
            }
            return dateString;
        }
        return date.getTime();
    } else {
        if (role === "display") {
            return unknownDateText;
        }
        return Number.MAX_VALUE;
    }
}

function dateOrNull(text) {
    if (text) {
        return new Date(text);
    }
    return null;
}

function getTimeSpan(begin, end, now) {
    if (end !== null && now > end) {
        return TimeSpan.PAST;
    } else if (begin !== null && now >= begin && begin >= dateOrNull('2021/01/01')) {
        return TimeSpan.NOW;
    } else if (begin > now) {
        return TimeSpan.FUTURE;
    }
    else {
        return TimeSpan.PAST;
    }
}

function convert(data) {
    let announcements = data;
    let now = new Date();

    announcements.forEach((announcement) => {
        announcement.begin = dateOrNull(announcement.begin);
        announcement.end = dateOrNull(announcement.end);
        announcement.timeSpan = getTimeSpan(announcement.begin, announcement.end, now);
    });

    return announcements;
}

function draw() {
    let column = this.api().column("timeSpan:name", {page: 'current'});

    let cells = column.nodes();
    let data = column.data().toArray();

    let lastTimeSpan = null;

    for (let i = 0; i < data.length; i++) {
        let cell = cells[i];
        let timeSpan = data[i];

        if (timeSpan === lastTimeSpan) {
            cell.classList.add(repeatingValueClass);
        } else {
            cell.classList.remove(repeatingValueClass);
        }
        lastTimeSpan = timeSpan;
    }
}

function linkify(inputText) {
    var replacedText, replacePattern1, replacePattern2, replacePattern3;

    // URLs starting with http://, https://, or ftp://
    replacePattern1 = /(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim;
    replacedText = inputText.replace(replacePattern1, '<a href="$1" target="_blank">$1</a>');

    // URLs starting with "www." (without // before it, or it'd re-link the ones done above).
    replacePattern2 = /(^|[^\/])(www\.[\S]+(\b|$))/gim;
    replacedText = replacedText.replace(replacePattern2, '$1<a href="http://$2" target="_blank">$2</a>');

    // Change email addresses to mailto:: links.
    replacePattern3 = /(([a-zA-Z0-9\-\_\.])+@[a-zA-Z\_]+?(\.[a-zA-Z]{2,6})+)/gim;
    replacedText = replacedText.replace(replacePattern3, '<a href="mailto:$1">$1</a>');

    return replacedText;
}

// This class should be modified/replaced for CMS.
class PopUp {
    constructor() {
        this._subject = document.getElementById("detailSubject");
        this._description = document.getElementById("detailDescription");
        this._type = document.getElementById("detailType");
        this._begin = document.getElementById("detailBegin");
        this._end = document.getElementById("detailEnd");
        this._service = document.getElementById("detailService");
    }

    set announcement(announcement) {
        this._subject.innerHTML = announcement.subject;
        let announcement_table = '<table>';
        announcement_table += '<tr><th>Typ</th><td>' + mapType(announcement.type).toUpperCase() + '</td></tr>';
        announcement_table += '<tr><th>Beginn</th><td>' + renderDate(announcement.begin, "display").replace('<br />', ' ') + '</td></tr>';
        announcement_table += '<tr><th>Ende</th><td>' + renderDate(announcement.end, "display").replace('<br />', ' ') + '</td></tr>';
        announcement_table += '<tr><th>Service</th><td>' + announcement.service + '</td></tr>';
        announcement_table += '<tr><th>Info</th><td>' + linkify(announcement.info) + '</td></tr>';
        announcement_table += '<tr><th>Beschreibung</th><td><p style="white-space: pre-line">' + linkify(announcement.description) + '</p></td></tr>';
        this._description.innerHTML = announcement_table;
    }
}

$(document).ready(() => {
    let popup = new PopUp();

    // Replace with actual popup function.
    let assignClickListener = (row, announcement) => {
        row.addEventListener("click", () => {
            popup.announcement = announcement;
        });
    };

    let table = $("#table").DataTable({
        processing: true,
        ajax: {url: "data.json", dataSrc: convert},
        columns: [
            {data: "timeSpan", name: "timeSpan", width: "10%"},
            {data: "begin", width: "15%"},
            {data: "end", width: "15%"},
            {data: "description", width: "50%",
                render: function (data, type, row) {
                    if (data.toString().length>100) {
                        return '<strong>' + row['subject'] + '</strong><br />' + data.toString().substring(0, 100) + '...';
                    }
                    else {
                        return '<strong>' + row['subject'] + '</strong><br />' + data.toString();
                    }

                }
            },
            {data: "type", width: "10%"}
        ],
        columnDefs: [
            {render: renderTimeSpan, targets: 0},
            {render: mapType, targets: 4},
            {render: renderDate, targets: [1, 2]}
        ],
        order: [[0, "asc"], [1, "asc"]],
        drawCallback: draw,
        createdRow: assignClickListener,
        asStripeClasses: [], // disable zebra coloring of rows
        bSortClasses: false, // disable coloring of sorted column
        oLanguage: {
            "sSearch": ""
        },
        dom: "frtipl",
    });

    let checkboxes = $("#form input[type=checkbox]");

    checkboxes.change(function () {
        let changedBox = this;
        let term = "";

        if (changedBox.checked) {
            term = changedBox.value;

            // Uncheck other boxes
            checkboxes.each(function () {
                if (changedBox !== this) {
                    this.checked = false;
                }
            });
        }

        table
            .column("timeSpan:name")
            .search(term, false, false, false)
            .draw();
    });
});
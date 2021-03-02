"use strict";

const TimeSpan = Object.freeze({
    NOW: 1,
    FUTURE: 2,
    PAST: 3
});

let unknownDateText = "Unbekannt";

let timeSpanDict = {};
timeSpanDict[TimeSpan.NOW] = "Jetzt";
timeSpanDict[TimeSpan.FUTURE] = "Anstehend";
timeSpanDict[TimeSpan.PAST] = "Vergangenheit";

let typeDict = {
    "WARTUNG": "Wartung",
    "DRINGENDE WARTUNG": "Dringende Wartung",
    "STOERUNG": "St&ouml;rung",
    "SICHERHEITSMELDUNG": "Sicherheitsmeldung",
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
            return date.toLocaleString();
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
    } else if (begin !== null && now > begin) {
        return TimeSpan.NOW;
    } else {
        return TimeSpan.FUTURE;
    }
}

function convert(data) {
    let announcements = data.status_announcements;
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

/// This class should be modified/replaced for CMS.
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
        this._description.innerHTML = announcement.description;
        this._type.innerHTML = mapType(announcement.type);
        this._begin.innerHTML = announcement.begin.toLocaleString();
        this._end.innerHTML = announcement.end.toLocaleString();
        this._service.innerHTML = announcement.service;
    }
}

$(document).ready(() => {
    let popup = new PopUp();

    // Replace with actual popup function.
    let assignClickListener = (row, announcement) => {
        row.addEventListener("click", () => popup.announcement = announcement);
    };

    let table = $("#table").DataTable({
        processing: true,
        ajax: {url: "data.json", dataSrc: convert},
        columns: [
            {data: "timeSpan", name: "timeSpan"},
            {data: "subject"},
            {data: "description"},
            {data: "type"},
            {data: "begin"},
            {data: "end"}
        ],
        columnDefs: [
            {render: renderTimeSpan, targets: 0},
            {render: mapType, targets: 3},
            {render: renderDate, targets: [4, 5]}
        ],
        order: [[0, "asc"], [4, "asc"]],
        drawCallback: draw,
        createdRow: assignClickListener,
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
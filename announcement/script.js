"use strict";

const TimeSpan = Object.freeze({NOW: 1, FUTURE: 2, PAST: 3});

let unknownDateText = "Unbekannt";
let timeSpanDict = {1: "Jetzt", 2: "Anstehend", 3: "Vergangenheit"};
let typeDict = {WARTUNG: "Wartung", STOERUNG: "St&ouml;rung"};

function mapTimeSpan(timeSpan) {
    return timeSpanDict[timeSpan];
}

function mapType(type) {
    return typeDict[type];
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

function dateOrNull(text) {
    if (text) {
        return new Date(text);
    }
    return null;
}

function getTimeSpan(begin, end, now) {
    // [some date] greater than [null] returns false.
    if (now > end) {
        return TimeSpan.PAST;
    } else if (now > begin) {
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
    let api = this.api();
    let rows = api.rows({page: "current"});

    let lastTimeSpan = null;

    rows.data().each((announcement, index) => {
        let timeSpan = announcement.timeSpan;

        if (timeSpan !== lastTimeSpan) {
            $(rows.nodes()).eq(index).before(
                "<tr class=\"group\"><td colspan=\"5\">" + mapTimeSpan(timeSpan) + "</td></tr>"
            );
        }
        lastTimeSpan = timeSpan;
    });
}

$(document).ready(() => {
    let popup = new PopUp();

    let assignClickListener = (row, announcement) => {
        row.addEventListener("click", () => popup.announcement = announcement);
    };

    let table = $("#table").DataTable({
        processing: true,
        ajax: {url: "data.json", dataSrc: convert},
        columns: [
            {data: "subject"},
            {data: "description"},
            {data: "type"},
            {data: "begin"},
            {data: "end"},
            {data: "timeSpan", visible: false, searchable: false}
        ],
        columnDefs: [
            {render: mapType, targets: 2},
            {render: renderDate, targets: [3, 4]}
        ],
        order: [[5, "asc"], [3, "asc"]],
        drawCallback: draw,
        createdRow: assignClickListener,
    });
});
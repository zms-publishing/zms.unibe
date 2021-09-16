"use strict";

let unknownText = "Unbekannt";

let cssHiddenClass = "hidden";

function csvToObjects(text) {
    let rows = text.split("\n");

    let header = rows[0].split(";");

    let list = [];

    for (let rowI = 1; rowI < rows.length; rowI++) {
        // Ignore new line at end of file
        if (rows[rowI].length > 0) {
            let object = {};
            let row = rows[rowI].split(";");

            for (let colI = 0; colI < row.length; colI++) {
                let data = row[colI];

                object[header[colI]] = data.length === 0 ? null : data;
            }

            list.push(object);
        }
    }

    return list;
}

function convertData(data) {
    let objects = csvToObjects(data);

    let lastRow = null;
    let groupId = 0;

    objects.forEach(row => {
        if (row.title) {
            groupId++;

            row.date = new Date(row.date);
        } else {
            row.date = lastRow.date;
            row.title = lastRow.title;
            row.type = lastRow.type;
            row.link = lastRow.link;
            // row.affiliation
            // row.speaker
            // row.speakerLink
        }
        // Use to keep track which rows belong together
        row.group = groupId;

        lastRow = row;
    });

    return objects;
}

function makeLink(url, text) {
    if (url !== null) {
        return `<a href="${url}" target="_blank">${text}</a>`;
    }
    return `<span>${text}</span>`
}

function renderDate(data, type, row) {
    if (row.date == null) {
        if (type === "display") {
            return unknownText;
        }
        return Number.MAX_VALUE;
    }
    if (type === "display") {
        return row.date.toLocaleDateString('de-CH', { day: "2-digit", month: "2-digit", year: "numeric" });
    }
    return row.date.getTime();
}

function renderTime(data, type, row) {
    if (row.date == null) {
        if (type === "display") {
            return unknownText;
        }
        return Number.MAX_VALUE;
    }
    if (type === "display") {
        return row.date.toLocaleTimeString('de-CH', { hour: "2-digit", minute: "2-digit" });
    }
    return row.date.getTime();
}

function renderLink(data, type, row) {
    if (type === "display") {
        return makeLink(row.link, row.type);
    }
    return row.type;
}

function renderSpeaker(data, type, row) {
    if (type === "display") {
        return makeLink(row.speakerLink, row.speaker);
    }
    return row.speaker;
}

function mergeCellsOfSameGroup(api, column) {
    let groups = api.column("group:name", {page: "current"}).data().toArray();
    let nodes = api.column(column, {page: "current"}).nodes();

    let lastGroup = null;
    let fistNodeOfGroup = null;
    let repetitions = 1;

    for (let i = 0; i < groups.length; i++) {
        if (groups[i] === lastGroup) {
            repetitions++;
            nodes[i].classList.toggle(cssHiddenClass, true);
            nodes[i].rowSpan = 1;
        } else {
            // No longer row of same group, expand row of last group.
            if (fistNodeOfGroup) {
                fistNodeOfGroup.rowSpan = repetitions;
            }
            repetitions = 1;

            nodes[i].classList.toggle(cssHiddenClass, false);

            fistNodeOfGroup = nodes[i];
            lastGroup = groups[i];
        }
    }
}

function draw() {
    mergeCellsOfSameGroup(this.api(), "date:name");
    mergeCellsOfSameGroup(this.api(), "time:name");
    mergeCellsOfSameGroup(this.api(), "title:name");
}

$(document).ready(() => {
    $("#table").DataTable({
        processing: true,
        ajax: {url: "data.csv", dataType: "text", dataSrc: convertData},
        columns: [
            {data: "date", name: "date", render: renderDate},
            {data: "time", name: "time", render: renderTime},
            {data: "title", name: "title"},
            {data: "affiliation", name: "affiliation"},
            {data: "link", name: "speaker", render: renderLink},
            {data: "speaker", render: renderSpeaker},
            {data: "group", name: "group", visible: false},
        ],
        autoWidth: false,
        order: [[ 0, 'asc' ], [ 1, 'asc' ]],
        drawCallback: draw
    });
});
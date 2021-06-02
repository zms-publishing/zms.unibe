"use strict";

let unknownText = "Unbekannt";

let cssHiddenClass = "hidden";

function csvToObjects(text) {
    let rows = text.split("\n");

    let header = rows[0].split(";");

    let list = [];

    for (let rowI = 1; rowI < rows.length; rowI++) {
        let object = {};
        let row = rows[rowI].split(";");

        for (let colI = 0; colI < row.length; colI++) {
            let data = row[colI];

            object[header[colI]] = data.length === 0 ? null : data;
        }

        list.push(object);
    }

    return list;
}

function parseTime(data) {
    let parts = [0, 0, 0, 0, 0, 0, 0];
    let splits = data.split(":");

    for (let i = 0; i < splits.length; i++) {
        parts[4 + i] = parseInt(splits[i]);
    }

    return new Date(...parts);
}

function parseDate(data) {
    let parts = [0, 0, 0];
    let splits = data.split("-");

    for (let i = 0; i < splits.length; i++) {
        parts[i] = parseInt(splits[i]);
    }

    return new Date(...parts);
}

function convertData(data) {
    let objects = csvToObjects(data);

    let lastRow = null;
    let groupId = 0;

    objects.forEach(row => {
        if (row.title) {
            groupId++;
        }
        // Use to keep track which rows belong together
        row.group = groupId;

        // If value empty, copy from row before
        row.time = row.time ? parseTime(row.time) : lastRow.time;
        row.date = row.date ? parseDate(row.date) : lastRow.date;
        row.title = row.title ? row.title : lastRow.title;
        row.speaker = row.speaker ? row.speaker : lastRow.speaker;
        row.speakerLink = row.speakerLink ? row.speakerLink : lastRow.speakerLink;
        row.type = row.type ? row.type : lastRow.type;
        row.link = row.link ? row.link : lastRow.link;

        lastRow = row;
    });

    return objects;
}

function renderDate(data, type) {
    if (data == null) {
        if (type === "display") {
            return unknownText;
        }
        return Number.MAX_VALUE;
    }
    if (type === "display") {
        return data.toLocaleDateString();
    }
    return data.getTime();
}

function renderTime(data, type) {
    if (data == null) {
        if (type === "display") {
            return unknownText;
        }
        return Number.MAX_VALUE;
    }
    if (type === "display") {
        return data.toLocaleTimeString();
    }
    return data.getTime();
}

function renderLink(data, type, row) {
    if (type === "display") {
        return '<a href="' + row.link + '">' + row.type + '</a>'
    }
    return row.type;
}

function renderSpeaker(data, type, row) {
    if (type === "display") {
        return '<a href="' + row.speakerLink + '">' + row.speaker + '</a>'
    }
    return row.speaker;
}

function expandDuplicates(api, column) {
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
            nodes[i].classList.toggle(cssHiddenClass, false);

            if (fistNodeOfGroup) {
                fistNodeOfGroup.rowSpan = repetitions;
                repetitions = 1;
            }

            fistNodeOfGroup = nodes[i];
            lastGroup = groups[i];
        }
    }
}

function draw() {
    expandDuplicates(this.api(), "date:name");
    expandDuplicates(this.api(), "time:name");
    expandDuplicates(this.api(), "title:name");
    expandDuplicates(this.api(), "speaker:name");
}

$(document).ready(() => {
    $("#table").DataTable({
        processing: true,
        ajax: {url: "data.csv", dataType: "text", dataSrc: convertData},
        columns: [
            {data: "date", name: "date", render: renderDate},
            {data: "time", name: "time", render: renderTime},
            {data: "title", name: "title"},
            {data: "link", name: "speaker", render: renderLink},
            {data: "speaker", render: renderSpeaker},
            {data: "group", name: "group", visible: false},
        ],
        drawCallback: draw
    });
});
"use strict";

let cssHiddenClass = "hidden";

let roleNames = {
    "TV": "Technik",
    "S0": "Software",
    "KV": "Konto"
};

function dataToRows(array) {
    let entities = [];

    array.forEach(institute => {
        institute.members.forEach(member => {
            entities.push({
                department: `${institute.name}`,
                member: {
                    firstname: member.firstname,
                    lastname: member.lastname,
                    email: member.email,
                    tel: member.tel
                },
                roles: member.roles.map(role => roleNames[role]).join(", ")
            });
        })
    });

    return entities;
}

function renderMember(data, role) {
    let name = data.firstname + " " + data.lastname;
    let tel = data.tel ? data.tel : "";

    if (role === "display") {
        if (data.email) {
            return `<a href='mailto:${data.email}'>${name}</a><br>${tel}`;
        }
        return `${name}<br>${tel}`;
    }
    return name;
}

function draw() {
    let nodes = this.api().column(0, {page: 'current'}).nodes().toArray();

    let groupText = null;
    let groupNode = null;
    let repetition = 1;

    nodes.forEach(node => {
        if (node.innerHTML === groupText) {
            // Hide
            node.classList.toggle(cssHiddenClass, true);
            repetition++;
        } else {
            // Show
            node.classList.toggle(cssHiddenClass, false);
            groupText = node.innerHTML;
            groupNode = node;
            repetition = 1;
        }
        if (groupNode) {
            // Expand
            groupNode.rowSpan = repetition;
        }
    });
}

function dataReady() {
    let api = this.api();

    // Add all institutions to set to ensure every element is unique.
    let set = new Set();
    api.column(0).data().each((value) => set.add(value));

    // Add all institutions to an array and sort. (Set doesn't sort alphabetically.)
    let array = [...set].sort((l, r) => l.localeCompare(r, undefined, {sensitivity: 'base'}));

    $("#institution-filter").each(function () {
        this.addEventListener("change", function () {
            api.column(0).search(this.value, false, false, false).draw();
        });

        array.forEach((institution) => {
            let option = document.createElement("option");
            option.innerHTML = institution;
            option.value = institution;
            this.appendChild(option);
        });
    });
}

$(document).ready(() => {
    let table = $("#table").DataTable({
        processing: true,
        ajax: {url: "http://localhost:7000/institutions.json", dataSrc: dataToRows},
        columns: [
            {data: "department"},
            {data: "member"},
            {data: "roles", searchable: false}
        ],
        columnDefs: [
            {targets: 1, render: renderMember},
        ],
        initComplete: dataReady,
        drawCallback: draw
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
            .column(2)
            .search(term, false, false, false)
            .draw();
    });
});
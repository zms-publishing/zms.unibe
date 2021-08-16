"use strict";

let cssHiddenClass = "hidden";

let roleNames = {
    "TV": "Technik",
    "S0": "Software",
    "KV": "Konto"
};

function prepare(array) {
    let entities = [];

    array.forEach(institute => {
        institute.members.forEach(member => {
            entities.push({
                department: `${institute.name} (${institute.externId})`,
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
            return `<a href='mailto:${data.mail}'>${name}</a><br>${tel}`;
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

function fillDepartmentDropdown() {
    // TODO
}

$(document).ready(() => {
    let table = $("#table").DataTable({
        processing: true,
        ajax: {url: "data.json", dataSrc: prepare},
        columns: [
            {data: "department"},
            {data: "member"},
            {data: "roles"}
        ],
        columnDefs: [
            {targets: 1, render: renderMember},
        ],
        initComplete: fillDepartmentDropdown,
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
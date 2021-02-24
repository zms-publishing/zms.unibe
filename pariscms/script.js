"use strict";

let repeatingValueClass = "repeating";

class Row {
    constructor(person, responsibility) {
        this.organizationalUnit = responsibility.type;
        this.department = responsibility.nameGerman + " (" + responsibility.externId + ")";
        this.name = person.firstname + " " + person.lastname;
        this.phone = person.phone;
        this.email = person.email;
    }
}

function flatten(array) {
    let flatArray = [];

    array.forEach((person) => {
        person.responsibilities.forEach((responsibility) => {
            flatArray.push(new Row(person, responsibility));
        });
    });
    return flatArray;
}

function draw() {
    let column = this.api().column("department:name", {page: 'current'});

    let cells = column.nodes();
    let data = column.data().toArray();

    let lastDepartment = "";

    for (let i = 0; i < data.length; i++) {
        let cell = cells[i];
        let department = data[i];

        if (department === lastDepartment) {
            cell.classList.add(repeatingValueClass);
        } else {
            cell.classList.remove(repeatingValueClass);
        }
        lastDepartment = department;
    }
}

function tableReady() {
    let api = this.api();

    // Add all departments to set to ensure every element is unique
    let departmentSet = new Set();
    api.column("department:name").data().each((value) => departmentSet.add(value));
    // Add all departments to an array and sort. (Set doesn't sort alphabetically.)
    let departmentArray = [...departmentSet].sort((a, b) => a.localeCompare(b, undefined, {sensitivity: 'base'}));

    $("#select-department").each(function () {
        this.addEventListener("change", function () {
            api.column("department:name").search(this.value, false, false, false).draw();
        });

        departmentArray.forEach((department) => {
            let option = document.createElement("option");
            option.innerHTML = department;
            option.value = department;
            this.appendChild(option);
        });
    });
}

$(document).ready(() => {
    let table = $("#table").DataTable({
        processing: true,
        ajax: {url: "data.json", dataSrc: flatten},
        columns: [
            {data: "organizationalUnit", name: "organizationalUnit", visible: false},
            {data: "department", name: "department"},
            {data: "name"},
            {data: "phone"},
            {data: "email"}
        ],
        drawCallback: draw,
        initComplete: tableReady
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
            .column("organizationalUnit:name")
            .search(term, false, false, false)
            .draw();
    });
});
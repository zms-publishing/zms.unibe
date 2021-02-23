"use strict";

let repeatingValueClass = "repeating";

class Row {
    constructor(person, responsibility) {
        this.organizationalUnit = responsibility.type;
        this.externId = responsibility.externId;
        this.department = responsibility.nameGerman;
        this.name = person.firstname + " " + person.lastname;
        this.phone = person.phone;
        this.email = person.email;
    }
}

function flatten(array) {
    let flatArray = [];

    array.forEach(function (person) {
        person.responsibilities.forEach(function (responsibility) {
            flatArray.push(new Row(person, responsibility));
        });
    });
    return flatArray;
}

function draw(settings) {
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

function tableReady(settings) {
    let departmentSet = new Set();
    this.api().column("department:name").data().each(function (value) {
        departmentSet.add(value);
    });
    $("#select-department").each(function() {
        let select = this;
        // select.addEventListener("change", filterByDepartment);

        departmentSet.forEach(function(department) {
            let option = document.createElement("option");
            option.innerHTML = department;
            option.value = department;
            select.appendChild(option);
        });
    });
}

$(document).ready(function () {
    let table = $("#table").DataTable({
        processing: true,
        ajax: {url: "test.json", dataSrc: flatten},
        columns: [
            {data: "organizationalUnit", name: "organizationalUnit", visible: false},
            {data: "externId"},
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
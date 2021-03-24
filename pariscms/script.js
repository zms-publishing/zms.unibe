"use strict";

let repeatingValueClass = "repeating";

let responsibilityTypeOrder = ["TV", "S0", "KV"];
let responsibilityTypeMap = {
    "TV": "Technik",
    "S0": "Software",
    "KV": "Konto"
};

class Department {
    constructor(name, externId, responsibilities) {
        this.name = name;
        this.externId = externId;
        this.responsibilities = responsibilities;
    }
}

class Row {
    constructor(person, department) {
        this.responsibilities = department.responsibilities;
        this.department = department.name + " (" + department.externId + ")";
        this.name = person.firstname + " " + person.lastname;
        this.phone = person.phone;
        this.email = person.email;
    }
}

function responsibilityComparer(left, right) {
    return responsibilityTypeOrder.indexOf(left) - responsibilityTypeOrder.indexOf(right);
}

function departmentNameComparer(left, right) {
    return left.localeCompare(right, undefined, {sensitivity: 'base'});
}

function flatten(array) {
    let flatArray = [];

    array.forEach((person) => {
        // We make a map of each department, then we add each responsibility type to the corresponding department.
        let departmentMap = {};

        person.responsibilities.forEach((responsibility) => {
            // This value is not visible and should an id or the shortest string possible.
            let key = responsibility.shortNameGerman;

            let department = departmentMap[key];

            if (department === undefined) {
                department = new Department(responsibility.nameGerman, responsibility.externId, []);
                departmentMap[key] = department;
            }

            department.responsibilities.push(responsibility.type);
        });

        Object.values(departmentMap).forEach((department) => {
            department.responsibilities.sort(responsibilityComparer);

            flatArray.push(new Row(person, department));
        });
    });
    return flatArray;
}

function responsibilitiesRenderer(array, role) {
    if (role === "display") {
        return array.map(type => responsibilityTypeMap[type]).join(", ");
    }
    return array.join(";");
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
    let departmentArray = [...departmentSet].sort(departmentNameComparer);

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
            {data: "department", name: "department"},
            {data: "name"},
            {data: "phone"},
            {data: "email"},
            {data: "responsibilities", name: "responsibilities"}
        ],
        columnDefs: [
            {render: responsibilitiesRenderer, targets: 4},
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
            .column("responsibilities:name")
            .search(term, false, false, false)
            .draw();
    });
});
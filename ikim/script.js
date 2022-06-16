class Popup {
    constructor() {
        this._popup = document.getElementById("popup");
        this._title = document.getElementById("popupTitle");
        this._author = document.getElementById("popupAuthor");
        this._icd = document.getElementById("popupICD10");
        this._trialDesign = document.getElementById("popupTrialDesign");
        this._comparator = document.getElementById("popupComparator");
        this._sampleSize = document.getElementById("popupSampleSize");
        this._peerReview = document.getElementById("popupPeerReview");

        this._journal = document.getElementById("popupJournal");
        this._volume = document.getElementById("popupVolume");
        this._issue = document.getElementById("popupIssue");
        this._pages = document.getElementById("popupPages");

        this._expander = document.getElementById("popupExpander");

        document.getElementById("popupClose").addEventListener("click", () => {
            this._popup.classList.toggle("visible", false);
        });
        document.getElementById("popupMore").addEventListener("click", () => {
            this._expander.classList.toggle("expanded");
        });
    }

    show(data) {
        this._title.innerHTML = data.Title;
        this._author.innerHTML = data.Author;
        this._icd.innerHTML = data.ICD10;
        this._trialDesign.innerHTML = data.TrialDesign;
        this._comparator.innerHTML = data.Comparator;
        this._sampleSize.innerHTML = data.SampleSize;
        this._peerReview.innerHTML = data.PeerReview;

        this._journal.innerHTML = data.JournalLong;
        this._volume.innerHTML = data.Volume;
        this._issue.innerHTML = data.Issue;
        this._pages.innerHTML = data.Pages;

        this._expander.classList.toggle("expanded", false);
        this._popup.classList.toggle("visible", true);
    }
}

$(() => {
    $.csv.defaults.separator = ";";
    $.csv.defaults.delimiter = "\"";

    let popup = new Popup();

    $("#table").DataTable({
        ajax: {url: "http://localhost:7000/data.csv", dataType: "text", dataSrc: $.csv.toObjects},
        columns: [
            {data: "ICD10"},
            {data: "Author"},
            {data: "Year"},
            {data: "Title"},
            {data: "TrialDesign"},
            {data: "Comparator"},
            {data: "SampleSize"},
        ],
        createdRow: (row, data) => row.addEventListener("click", () => popup.show(data)),
    });
});
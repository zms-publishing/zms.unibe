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
        this._prev = document.getElementById("popupPrev");
        this._next = document.getElementById("popupNext");

        // This index DOES NOT refer to the visual index.
        this._index = null;
        this._api = null;

        document.getElementById("popupClose").addEventListener("click", () => this.close());
        document.getElementById("popupMore").addEventListener("click", () => {
            this._expander.classList.toggle("expanded");
        });
        this._prev.addEventListener("click", () => {
            let indexes = this.indexes();
            let current = indexes.indexOf(this._index);

            this.show(current - 1, indexes);
        });
        this._next.addEventListener("click", () => {
            let indexes = this.indexes();
            let current = indexes.indexOf(this._index);

            this.show(current + 1, indexes);
        });
    }

    show(pos, indexes) {
        let index = indexes[pos];
        let data = this._api.row(index).data();

        this._index = index;
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

        this.updateNavButtons(pos, indexes);
        this._expander.classList.toggle("expanded", false);
        this._popup.classList.toggle("visible", true);
    }

    indexes() {
        return this._api.rows(null, {pages: 'all', search: 'applied', order: 'current'}).indexes();
    }

    updateNavButtons(pos, indexes) {
        this._prev.disabled = pos === 0;
        this._next.disabled = pos === indexes.length - 1;
    }

    setApi(api) {
        this._api = api;
    }

    handleClick(index) {
        let indexes = this.indexes();
        let selected = indexes.indexOf(index);

        this.show(selected, indexes);
    }

    handleDraw() {
        if (this._index !== null) {
            let indexes = this.indexes();
            let pos = indexes.indexOf(this._index);

            this.updateNavButtons(pos, indexes);
        }
    }

    close() {
        this._popup.classList.toggle("visible", false);
        this._index = null;
    }
}

$(() => {
    $.csv.defaults.separator = ";";
    $.csv.defaults.delimiter = "\"";

    let popup = new Popup();

    let api = $("#table")
        .on('search.dt', () => popup.close())
        .DataTable({
            ajax: {url: "http://localhost:8081/2022-06-24T1053380200_ger.csv", dataType: "text", dataSrc: $.csv.toObjects},
            columns: [
                {data: "ICD10"},
                {data: "Author"},
                {data: "Year"},
                {data: "Title"},
                {data: "TrialDesign"},
                {data: "Comparator"},
                {data: "SampleSize"},
            ],
            createdRow: (row, data, index) => row.addEventListener("click", () => popup.handleClick(index)),
            drawCallback: () => popup.handleDraw()
    });
    popup.setApi(api);

    document.getElementById("export").addEventListener("click", () => {
        let data = api.rows(null, {pages: 'all', search: 'applied', order: 'current'}).data();
        let csv = $.csv.fromObjects(data);
        let blob = new Blob([csv], {type: "text/csv"});
        let url = window.URL.createObjectURL(blob);

        window.open(url);
    });
});
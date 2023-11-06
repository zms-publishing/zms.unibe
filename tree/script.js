// BO columns
columns: [
    {
        data: null,
        render: function (data, type, row) {
            let cit = row.citation.text;
            let uri = row.uri;
            let str = cit.toString();
            try {
                let reg = new RegExp('<(http[s]?:\/\/)?([^\/\s]+\/)(?<doi>.*)>', 'g');
                let res = str.matchAll(reg);
                for (let r of res) {
                    let grp = r.groups;
                    let url = r[0];
                    str = str.replace(url, '');
                    str = str.replace(grp.doi, '[<a href="' + url.slice(1, -1) + '" target="_blank">doi/' + grp.doi + '</a>]');
                }
            }
            catch(err) {
                console.log('RegExp Lookbehind Assertions are only supported in latest versions of Chrome and Safari - but not Firefox (see https://stackoverflow.com/a/49816860).')
            }
            str = str + ' [<a href="' + uri + '" target="_blank">boris/' + row.eprintid + '</a>]';
            return str;
        }
    },
    {
        data: "date",
        render: function (data, type, row) {
            return data.toString().substring(0, 4);
        }
    },
    {
        data: "citation.lang",
    },
    {
        data: "type",
        render: function (data, type, row) {
            return '<span style="text-transform: capitalize;">' + data.toString().replace('_', ' ') + '</span>';
        }
    }

],
order: [[ 1, "desc" ]], // order by year descending
asStripeClasses: [] // disable zebra coloring of rows
//bSortClasses: false // disable coloring of sorted column
// EO columns

// BO processCustomJS
function processCustomJS(table) {
    
}
// EO processCustomJS
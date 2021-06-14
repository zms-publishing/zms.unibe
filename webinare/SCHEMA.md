# CSV Schema

### CSV Format
* Columns are separated with a semicolon ( ; )
* Rows are separated with a new lines
* No quotes around values
* A header with the exact names has to be present

### Multiple speakers
If a row has no title, it's considered to be part of the last row with a title.

### Schema
| Column | Value | Example |
|:---|:---|:---|
| date | An ISO Date/Time (YYYY-MM-DDTHH:mm) | 2020-06-14T12:30 |
| title | The title of the webinar | ... |
| speaker | The name of the speaker | ... |
| speakerLink | A link to the website of the speaker | https://... |
| type | The text to display as link text | "Webinar" or "Recording" |
| link | A link to the webinar | https://... |
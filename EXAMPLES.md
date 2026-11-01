# zms.unibe / Helper Functions

### Code Examples

- [Date/Time handling](#datetime-handling)
- [Date/Time formatting](#datetime-formatting)
- [Output sanitization](#output-sanitization)
- [String splitting](#string-splitting)

The code snippets below are `Python Scripts` – but the examples can be used in `Page Templates` as well.

<details>
<summary>Prerequisite for use in <a href="https://github.com/zopefoundation/RestrictedPython" target="_blank"><code>RestrictedPython</code></a> code as <code>py, zpt, dtml</code></summary>

```html
# Add this config to ./etc/site.zcml:

<configure xmlns:zcml="http://namespaces.zope.org/zcml">
  <include zcml:condition="installed zms.unibe.patches" package="zms.unibe.patches" />
</configure>
```
</details>

```html
<tal:block tal:define="
    datetime modules/zms.unibe.helpers/datetime;
    tomorrow python:datetime.local_timezone(context.ZopeTime()+1);">
    <p tal:content="python:datetime.get_when(tomorrow)">2026-10-10T20:33:00+02:00</p>
    <p tal:content="python:datetime.get_when(tomorrow, mode='date', locale='en_GB')">10 October 2026</p>
    <p tal:content="python:datetime.get_when(tomorrow, mode='date', locale='en_US')">October 10, 2026</p>
    <p tal:content="python:datetime.get_when(tomorrow, mode='weekday', locale='de_DE')">Sa</p>
    <p tal:content="python:datetime.get_when(tomorrow, mode='EEEE', locale='ru')">суббота</p>
    
    <tal:block tal:define="
        newyear_bermuda python:datetime.local_timezone('2027-01-01', tz='Atlantic/Bermuda');">
        <p tal:content="python:newyear_bermuda">2026-12-31 19:00:00-04:00</p>
        <p tal:content="python:datetime.get_when(newyear_bermuda)">2027-01-01T00:00:00+01:00</p>
    </tal:block>
</tal:block>
```

> [!TIP]
> In `Python Console` you can use the following shorthand to import all helper functions at once and start using them straight away:
> ```python
> Python 3.14.9 (main, Oct 21 2026, 17:47:42) [Clang 23.1.3 ] on darwin
> 
> >>> from zms.unibe.helpers import *
> 
> Helper: zms.unibe.helpers.datetime.local_timezone
> Helper: zms.unibe.helpers.datetime.get_when
> Helper: zms.unibe.helpers.string.sanitize_html
> Helper: zms.unibe.helpers.string.flatten_to_str_list
> Helper: zms.unibe.helpers.string.normalize_split_by
> 
> >>> get_when()
> '2026-10-24T13:40:47+02:00'
> ```

## Date/Time handling

- Normalize arbitrary representations of dates and times to a standard Python timezone-aware [`datetime`](https://docs.python.org/3/library/datetime.html#aware-and-naive-objects) object.
- You can put in as any `ISO strings`, `struct_time`, or UNIX timestamps and convert them to the specified timezone.
- If no timezone is provided, it defaults to `Europe/Zurich` – see [list of timezones](https://github.com/zms-publishing/zms.unibe/blob/main/TIMEZONES.md).
- You can also adjust the datetime by a number of days given as delta.

<details>
<summary><code>zms.unibe.helpers.datetime.local_timezone</code></summary>

```python
def local_timezone(dt: Any = None,
                   tz: str | tzinfo | None = None,
                   days_delta: int = 0) -> datetime:
    """
    Convert a date/time value to a timezone-aware datetime.

    Naive calendar values are interpreted as wall times in the target timezone.
    Aware values are converted without changing their represented instant. An
    aware ISO8601 string retains its offset when no timezone is explicitly given.
    Unix timestamps represent instants; ``struct_time`` is interpreted in the
    system timezone. Invalid ISO8601 strings fall back to the Unix epoch.

    :param dt: A datetime, date, time, ISO8601 string, ``struct_time``,
        Unix timestamp, legacy Zope ``DateTime``, or ``None`` for the current time.
    :param tz: Target IANA timezone name or tzinfo object. Defaults to
        ``Europe/Zurich``; an aware ISO8601 string supplies its timezone if omitted.
    :param days_delta: Number of days to add before converting to the target timezone.
    :return: A timezone-aware datetime in the resolved timezone.
    """
```
</details>

```python
from zms.unibe.helpers.datetime import local_timezone

now = local_timezone()

local_timezone(now)
# datetime.datetime(2026, 11, 1, 14, 0, 43, 597064, tzinfo=zoneinfo.ZoneInfo(key='Europe/Zurich'))

local_timezone(now, days_delta=7, tz='Asia/Tokyo')
# datetime.datetime(2026, 11, 8, 22, 0, 43, 597064, tzinfo=zoneinfo.ZoneInfo(key='Asia/Tokyo'))

local_timezone('2027-01-01', tz='Atlantic/Bermuda')
# datetime.datetime(2027, 1, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='Atlantic/Bermuda'))
```

## Date/Time formatting

- Format dates, times, weekdays, and time deltas in a localized manner, defaults to `de_CH`.
- It supports various modes for formatting and can handle different locales and time zones.
- You can adjust the direction and granularity for delta formats.
- It is basically a wrapper for the [`Babel`](https://babel.pocoo.org/en/latest/dates.html) library.

<details>
<summary><code>zms.unibe.helpers.datetime.get_when</code></summary>

```python
def get_when(dt: Any = None,
             mode: str | None = None,
             locale: str = 'de_CH',
             tz: str | tzinfo | None = None,
             granularity: str = 'second',
             threshold: float | int = 0.85,
             format: str = 'long',
             add_direction: bool = True) -> str | float:
    """
    Format a date/time value or relative duration using Babel.

    ``date``, ``time``, ``day``, and ``weekday`` select localized calendar
    representations; ``utcoffset`` returns the offset in hours. ``delta``
    formats a timedelta or a number interpreted as days. A timedelta always
    selects ``delta`` mode. Other string modes are Babel datetime patterns;
    ``None``, ``iso``, and ``iso8601`` use the default ISO8601 pattern.

    :param dt: A datetime, date, time, ISO8601 string, timedelta, or numeric
        value interpreted as days in ``delta`` mode. ``None`` means the current time.
    :param mode: Formatting mode, Babel datetime pattern, or ``None`` for ISO8601.
    :param locale: Babel locale identifier.
    :param tz: Target IANA timezone or tzinfo. If omitted, an aware input
        supplies its timezone; otherwise ``Europe/Zurich`` is used.
    :param granularity: Smallest unit used by Babel for ``delta`` mode.
    :param threshold: Babel's threshold for stepping to the next duration unit.
    :param format: Babel duration format, such as ``long`` or ``short``.
    :param add_direction: Whether delta output includes relative direction.
    :return: Formatted text, or the UTC offset in hours for ``utcoffset`` mode.
    """
```
</details>

```python
from zms.unibe.helpers.datetime import get_when, local_timezone

now = local_timezone()

get_when(now, mode='date')
# '9. Oktober 2026'

get_when(now, mode='date', locale='en_GB')
# '9 October 2026'

get_when(now, mode='date', locale='en_US')
# 'October 9, 2026'

get_when(now, mode='date', locale='fr')
# '9 octobre 2026'

get_when(now, mode='date', locale='ja')
# '2026年10月9日'

get_when(now, mode='EEEE', locale='de')
# 'Freitag'

get_when(now, mode='EEEE', locale='ru')
# 'пятница'
```
```python
from zms.unibe.helpers.datetime import get_when, local_timezone

now = local_timezone()
diff = local_timezone('2026-12-31') - now

get_when(diff)
# 'in 3 Monaten'

get_when(-diff)
# 'vor 3 Monaten'

get_when(diff, locale='en')
# 'in 3 months'

get_when(-diff, locale='en')
# '3 months ago'

get_when(diff, threshold=10)
# 'in 12 Wochen'

get_when(diff, threshold=20)
# 'in 82 Tagen'

get_when(diff, threshold=100)
# 'in 1976 Stunden'

get_when(diff, threshold=10000)
# 'in 118573 Minuten'

get_when(diff, threshold=1000000)
# 'in 7114406 Sekunden'

get_when(mode='utcoffset')
# 1.0

get_when(tz='Asia/Tokyo', mode='utcoffset')
# 9.0

get_when(tz='Atlantic/Bermuda', mode='utcoffset')
# -4.0
```

## Output sanitization

<details>
<summary>Example HTML content produced by Outlook WYSIWYG editor</summary>

```html
<html xmlns:v="urn:schemas-microsoft-com:vml"
xmlns:o="urn:schemas-microsoft-com:office:office"
xmlns:w="urn:schemas-microsoft-com:office:word"
xmlns:m="http://microsoft.com"
xmlns="http://w3.org">

<head>
<meta http-equiv=Content-Type content="text/html; charset=utf-8">
<meta name=Generator content="Microsoft Word 15 (filtered medium)">
<!--[if gte mso 9]><xml>
<o:OfficeDocumentSettings>
 <o:AllowPNG/>
 <o:PixelsPerInch>96</o:PixelsPerInch>
</o:OfficeDocumentSettings>
</xml><![endif]-->
<style>
<!--
 /* Font Definitions */
 @font-face
	{font-family:"Cambria Math";
	panose-1:2 4 5 3 5 4 6 3 2 4;}
@font-face
	{font-family:Calibri;
	panose-1:2 15 5 2 2 2 4 3 2 4;}
 /* Style Definitions */
 p.MsoNormal, li.MsoNormal, div.MsoNormal
	{margin:0cm;
	font-size:11.0pt;
	font-family:"Calibri",sans-serif;
	mso-fareast-language:EN-US;}
span.E-MailFormatvorlage17
	{mso-style-type:personal-compose;
	font-family:"Calibri",sans-serif;
	color:windowtext;}
.MsoChpDefault
	{mso-type:normal-trid;}
@page WordSection1
	{size:595.3pt 841.9pt;
	margin:70.85pt 70.85pt 2cm 70.85pt;}
div.WordSection1
	{page:WordSection1;}
-->
</style>
</head>

<body lang=DE link="#0563C1" vlink="#954F72" style='word-wrap:break-word'>

<div class=WordSection1>

<p class=MsoNormal><b><span style='font-size:14.0pt;color:#1F4E78'>Hallo Team</span></b><o:p></o:p></p>

<p class=MsoNormal><o:p>&nbsp;</o:p></p>

<p class=MsoNormal>Das ist ein typischer Inhalt, der mit dem <a href="https://microsoft.com"><span style='color:#0563C1'>Outlook WYSIWYG-Editor</span></a> erstellt wurde. Er enthält eine Liste und Textformatierungen.<o:p></o:p></p>

<p class=MsoNormal><o:p>&nbsp;</o:p></p>

<ul style='margin-top:0cm' type=disc>
 <li class=MsoNormal style='mso-list:l0 level1 lfo1'>Wichtiger Punkt 1</li>
 <li class=MsoNormal style='mso-list:l0 level1 lfo1'>Wichtiger Punkt 2</li>
</ul>

<p class=MsoNormal><o:p>&nbsp;</o:p></p>

<p class=MsoNormal>Mit freundlichen Grüßen,<br>
<b>Max Mustermann</b><br>
<span style='font-size:9.0pt;color:#595959'>Abteilung für digitale Kommunikation</span><o:p></o:p></p>

</div>

<p><a href="link2.html">Link 2</a></p>

<div><img src="screenshot.png" alt="Screenshot" /></div>

</body>
</html>
```
</details>

- Uses the [`MarkItDown`](https://github.com/microsoft/markitdown) library to sanitize and convert given HTML content to Markdown, if the content starts with `<html>`.
- Alternatively, the Markdown can be converted back to HTML, performing additional cleaning such as removing images, empty paragraphs, and unwanted newline characters.
- As a fallback the [`BeautifulSoup`](https://beautiful-soup-4.readthedocs.io/en/latest/) library is used to extract text content.
- Can also extract and return the last hyperlink `<a href="...">` present in the HTML to create 'more...' links easily.

<details>
<summary><code>zms.unibe.helpers.string.sanitize_html</code></summary>

```python
def sanitize_html(content: Any = None,
                  return_type: str ='html') -> str:
    """
    Sanitizes HTML content by converting it into either plain Markdown or sanitized HTML.
    It uses the ``MarkItDown`` library to sanitize and convert it to Markdown.
    By default, the Markdown is converted back to HTML, performing additional cleaning
    such as removing images, empty paragraphs, and unwanted newline characters.

    If errors occur, it uses ``BeautifulSoup`` to extract text content.

    Parameters:
    content (str): The input HTML content to be sanitized or processed.

    return_type (str, optional): Specifies the type of value to return:
        - ``markdown``: Converts the HTML to Markdown and returns it.
        - ``html``: Sanitizes the HTML, removing unwanted elements, and returns cleaned HTML.
        - ``href``: Extracts and returns the last hyperlink ('<a href="...">') present in the HTML.
        Default is ``html``.

    Returns:
    str: The output in the format specified by ``return_type``.

    Raises:
    Does not explicitly raise errors but logs any exceptions that occur during processing.
    """
```
</details>

```python
from zms.unibe.helpers.string import sanitize_html

content = '...'   # see the example HTML content above

sanitize_html(content)
# <p><strong>Hallo Team</strong></p>
# <p>Das ist ein typischer Inhalt, der mit dem <a href="https://microsoft.com">Outlook WYSIWYG-Editor</a> erstellt wurde. 
# Er enthält eine Liste und Textformatierungen.</p> 
# <ul> <li>Wichtiger Punkt 1</li> <li>Wichtiger Punkt 2</li> </ul>
# <p>Mit freundlichen Grüßen, <strong>Max Mustermann</strong> Abteilung für digitale Kommunikation</p> 
# <p><a href="link2.html">Link 2</a></p>

sanitize_html(content, 'markdown')
# **Hallo Team**
#
# Das ist ein typischer Inhalt, der mit dem [Outlook WYSIWYG-Editor](https://microsoft.com) erstellt wurde.
# Er enthält eine Liste und Textformatierungen.
#
# * Wichtiger Punkt 1
# * Wichtiger Punkt 2
#
# Mit freundlichen Grüßen,
# **Max Mustermann**
# Abteilung für digitale Kommunikation
#
# [Link 2](link2.html)
#
# ![Screenshot](screenshot.png)

sanitize_html(content, 'href')
# link2.html
```


## String splitting

- Split any values, first by line if text and then using multiple delimiters (by default `,` `;` or `|`)
- Convert the specified values into a sorted list of strings with duplicates removed

<details>
<summary><code>zms.unibe.helpers.string</code></summary>

```python
def flatten_to_str_list(*values) -> list[str]:
    """Flatten the given values (scalars or lists) into a sorted, deduplicated
    list of strings, dropping non-string values like None or numbers."""

def normalize_split_by(values: Any = None,
                       delimiters: str = ',;|',
                       splitlines: bool = True,
                       keepends: bool = False,
                       maxsplit: int = 0) -> list[str]:
    """Split arbitrary values based on multiple delimiters,
    split lines of text first, with or without keeping the line endings,
    and limiting the maximum number of splits. Returns a list of strings."""
```
</details>

```python
from zms.unibe.helpers.string import flatten_to_str_list, normalize_split_by


splitted = normalize_split_by("""Line 1
                              Line 2    , Word B     | Word C
                              Word A; Line 3""")
# ['Line 1', 'Line 2', 'Word B', 'Word C', 'Word A', 'Line 3']

flatten_to_str_list(splitted, 'Word A', 'Line 4', 'Word A', ['1', '2', '3'], '3', '2')
# ['1', '2', '3', 'Line 1', 'Line 2', 'Line 3', 'Line 4', 'Word A', 'Word B', 'Word C']

normalize_split_by('0 1 2 3')
# ['0 1 2 3']

normalize_split_by('0 1 2 3', delimiters=' ')
# ['0', '1', '2', '3']

normalize_split_by((3,4,1,2,1,1,2,3))
# ['3', '4', '1', '2', '1', '1', '2', '3']

flatten_to_str_list(normalize_split_by((3,4,1,2,1,1,2,3)))
# ['1', '2', '3', '4']
```
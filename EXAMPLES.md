# zms.unibe / Helper Functions

### Code Examples

- [Date/Time handling](#datetime-handling)
- [Date/Time formatting](#datetime-formatting)
- [Output sanitization](#output-sanitization)

These helper functions can be used in any ZMS/Zope-based system with the `zms.unibe` [add-on package installed](https://github.com/zms-publishing/zms.unibe/blob/main/README.md#installation).

The code snippets below are `Python Scripts` – but the examples can be used in `Page Templates` as well.

<details>
<summary>Prerequisite for use in <a href="https://github.com/zopefoundation/RestrictedPython" target="_blank"><code>RestrictedPython</code></a> code as <code>py, zpt, dtml</code></summary>

Add the following config to `./.venv/etc/site.zcml`:
```xml
<configure xmlns:zcml="http://namespaces.zope.org/zcml">
  <include zcml:condition="installed zms.unibe.patches" package="zms.unibe.patches" />
</configure>
```
</details>

```html
<tal:block tal:define="
    helpers modules/zms.unibe.utils/helpers;
    tomorrow python:helpers.local_timezone(context.ZopeTime()+1);">
    <p tal:content="python:helpers.get_when(tomorrow)">2026-10-10T20:33:00+02:00</p>
    <p tal:content="python:helpers.get_when(tomorrow, mode='date', locale='en_GB')">10 October 2026</p>
    <p tal:content="python:helpers.get_when(tomorrow, mode='date', locale='en_US')">October 10, 2026</p>
    <p tal:content="python:helpers.get_when(tomorrow, mode='weekday', locale='de_DE')">Sa</p>
    <p tal:content="python:helpers.get_when(tomorrow, mode='EEEE', locale='ru')">суббота</p>
    
    <tal:block tal:define="
        newyear_bermuda python:helpers.local_timezone('2027-01-01', tz='Atlantic/Bermuda');">
        <p tal:content="python:newyear_bermuda">2026-12-31 19:00:00-04:00</p>
        <p tal:content="python:helpers.get_when(newyear_bermuda)">2027-01-01T00:00:00+01:00</p>
    </tal:block>
</tal:block>
```

## Date/Time handling

- Normalize arbitrary representations of dates and times to a standard Python timezone-aware [`datetime`](https://docs.python.org/3/library/datetime.html#aware-and-naive-objects) object.
- You can put in as any `ISO strings`, `struct_time`, or UNIX timestamps and convert them to the specified timezone.
- If no timezone is provided, it defaults to `Europe/Zurich` – see [list of timezones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).
- You can also adjust the datetime by a number of days given as delta.

<details>
<summary><code>zms.unibe.utils.helpers.local_timezone</code></summary>

```python
def local_timezone(dt=None, tz='Europe/Zurich', days_delta=0):
    """
    Convert a datetime, timestamp, or ISO8601 string to the specified local timezone.

    This function takes a datetime object or other datetime representations such 
    as ISO8601 strings, struct_time objects, or UNIX timestamps and converts them 
    to the specified timezone. If no timezone is provided, it defaults to 'Europe/Zurich'. 
    The function optionally adjusts the datetime by a specified number of days before 
    performing the timezone conversion.

    :param dt: The datetime input, which can be a datetime or date object, ISO8601 string, 
        struct_time object, or a UNIX timestamp (int or float). If no value 
        is provided, the current datetime will be used.
    :type dt: Optional[Union[datetime, date, str, time.struct_time, int, float, DateTime]]

    :param tz: The timezone to convert the datetime to. If it is not provided, the 
        timezone 'Europe/Zurich' will be used.
    :type tz: Optional[str]

    :param days_delta: Number of days to adjust the datetime before converting it 
        to the specified timezone.
    :type days_delta: int

    :return: A timezone-aware datetime object in the specified timezone.
    :rtype: datetime
    """
```
</details>

```python
from zms.unibe.utils.helpers import local_timezone

now = local_timezone()

local_timezone(now)
# datetime.datetime(2026, 10, 9, 16, 46, 33, 741677, tzinfo=<DstTzInfo 'Europe/Zurich' CEST+2:00:00 DST>)

local_timezone(now, days_delta=7, tz='Asia/Tokyo')
# datetime.datetime(2026, 10, 16, 23, 46, 33, 741677, tzinfo=<DstTzInfo 'Asia/Tokyo' JST+9:00:00 STD>)

local_timezone('2027-01-01', tz='Atlantic/Bermuda')
# datetime.datetime(2026, 12, 31, 19, 0, tzinfo=<DstTzInfo 'Atlantic/Bermuda' AST-1 day, 20:00:00 STD>)
```

## Date/Time formatting

- Format dates, times, weekdays, and time deltas in a localized manner, defaults to `de_CH`.
- It supports various modes for formatting and can handle different locales and time zones.
- You can adjust the direction and granularity for delta formats.
- It is basically a wrapper for the [`Babel`](https://babel.pocoo.org/en/latest/dates.html) library.

<details>
<summary><code>zms.unibe.utils.helpers.get_when</code></summary>

```python
def get_when(dt, mode=None,
             locale='de_CH', tz='Europe/Zurich', 
             granularity='second', threshold=0.85,
             format='long', add_direction=True):
    """
    Determines and returns a formatted representation of the input date, time, or timedelta 
    based on the specified `mode` and formatting criteria. Handles localization, time zone 
    adjustments, and granularity for delta formats.
    
    It is basically a wrapper for https://babel.pocoo.org/en/latest/dates.html

    :param dt: Input date, time, or timedelta. Can be a `datetime`, `date`, or a number 
               (interpreted as days). This parameter determines the entity to be formatted 
               based on the given `mode`.
    :type dt: datetime | date | timedelta | int | float
    :param mode: Specifies the formatting operation to perform. Options include:
                 - 'date': Formats only the date.
                 - 'time': Formats only the time.
                 - 'day': Formats the day of the month.
                 - 'weekday': Formats the name of the weekday.
                 - 'delta': Formats timedelta with varying granularity and threshold.
                 - Other values are interpreted as explicit format strings or defaulted
                   to ISO8601 if not recognized.
    :type mode: str | None
    :param locale: Locale string for localized formatting. Defaults to 'de_CH'.
    :type locale: str
    :param tz: Timezone information for adjusting the datetime. Defaults to 'Europe/Zurich' 
               if the provided timezone is unrecognized or `None`.
    :type tz: str | None
    :param granularity: Defines the smallest time unit (e.g., 'second', 'minute', 'day') 
                        for timedelta formatting when the mode is 'delta'. Defaults to 'second'.
    :type granularity: str
    :param threshold: Threshold value determining when to step into the next higher 
                      granularity for timedelta formatting. Defaults to 0.85.
    :type threshold: float
    :param format: Specifies the verbosity of the output in timedelta formatting (e.g., 'short', 
                   'long'). Defaults to 'long'.
    :type format: str
    :param add_direction: When `True`, includes direction indicators (e.g., 'in', 'ago') 
                          in timedelta formatting. Defaults to `True`.
    :type add_direction: bool
    :return: Returns a string representing the formatted input based on the specified mode 
             and locale. The format varies depending on the mode. Examples include formatted 
             dates, times, weekdays, and timedelta durations.
    :rtype: str
    """
```
</details>

```python
from zms.unibe.utils.helpers import local_timezone, get_when

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
from zms.unibe.utils.helpers import local_timezone, get_when

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
<summary><code>zms.unibe.utils.helpers.sanitize_html</code></summary>

```python
def sanitize_html(content, return_type='html'):
    """
    Sanitizes HTML content by converting it into either plain markdown or sanitized HTML.
    If the content starts with <html>, it uses the MarkItDown library to sanitize and
    convert it to markdown. Alternatively, the markdown is converted back to HTML,
    performing additional cleaning such as removing images, empty paragraphs, and
    unwanted newline characters.

    If errors occur, it uses BeautifulSoup to extract text content.

    Parameters:
    content (str): The input HTML content to be sanitized or processed.

    return_type (str, optional): Specifies the type of value to return:
        - 'markdown': Converts the HTML to Markdown and returns it.
        - 'html': Sanitizes the HTML, removing unwanted elements, and returns cleaned HTML.
        - 'href': Extracts and returns the last hyperlink ('<a href="...">') present in the HTML.
        Default is 'html'.

    Returns:
    str: The output in the format specified by `return_type`.

    Raises:
    Does not explicitly raise errors but logs any exceptions that occur during processing.
    """
```
</details>

```python
from zms.unibe.utils.helpers import sanitize_html

content = '...'   # see the example HTML content above

sanitize_html('<html>'+content)
# <p><strong>Hallo Team</strong></p>
# <p>Das ist ein typischer Inhalt, der mit dem <a href="https://microsoft.com">Outlook WYSIWYG-Editor</a> erstellt wurde. 
# Er enthält eine Liste und Textformatierungen.</p> 
# <ul> <li>Wichtiger Punkt 1</li> <li>Wichtiger Punkt 2</li> </ul>
# <p>Mit freundlichen Grüßen, <strong>Max Mustermann</strong> Abteilung für digitale Kommunikation</p> 
# <p><a href="link2.html">Link 2</a></p>

sanitize_html('<html>'+content, 'markdown')
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

sanitize_html('<html>'+content, 'href')
# link2.html
```

## License

Copyright (c) 2020-2026 [UniBE, University of Bern, IT Services Department](https://id.unibe.ch). All rights reserved.

Licensed under the [MIT license](https://github.com/zms-publishing/zms.unibe/blob/main/LICENSE).
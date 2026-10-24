import logging
import re
from io import BytesIO
from typing import Any
from unittest.mock import MagicMock

from bs4 import BeautifulSoup
from markdown import markdown as render_as_html
from markitdown import MarkItDown

from .MockDecorator import MockDecorator

try:
    import zExceptions
    from AccessControl import ModuleSecurityInfo

    security = ModuleSecurityInfo('zms.unibe.helpers.string')  # allow module import in RestrictedPython
except:
    security = MagicMock()  # fallback if no Zope/ZMS context available
    security.public = MagicMock(wraps=MockDecorator())

LOGGER = logging.getLogger('zms.unibe.helpers.string')


print('Helper: zms.unibe.helpers.string.sanitize_html')
@security.public
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
    if content is None:
        return ''
    content = str(content).strip()
    
    if not content:
        return ''
    elif not content.startswith('<html'):
        content = f'<html><body>{content}</body></html>'
    
    try:
        if return_type in ('markdown', 'html'):
            md = MarkItDown()
            stream = BytesIO(content.encode(encoding="utf-8"))
            markdown = md.convert_stream(stream).text_content
            markdown = markdown.replace('\xa0', ' ')  # non-breaking space in Latin1 (ISO 8859-1)
            if return_type == 'markdown':
                return markdown
            elif return_type == 'html':
                html = render_as_html(markdown)
                html = re.compile(r'<img.*?/>').sub('', html)
                html = html.replace('<p></p>', '')
                html = html.replace('\n', ' ')
                return html.strip()

    except Exception as e:
        LOGGER.error(f'Error on sanitize_html: {e}')

    soup = BeautifulSoup(content, "html.parser")

    if return_type == 'href':
        links = soup.find_all('a')
        if len(links) > 0:
            # last hyperlink in given HTML
            return links[-1].get('href')

    # extract at least plain text if conversion to markdown or html failed above
    text = soup.get_text()
    text = text.replace('\r\n', ' ')
    text = text.replace('\n', '')
    text = text.replace('  ', ' ')
    return text.strip()


print('Helper: zms.unibe.helpers.string.flatten_to_str_list')
@security.public
def flatten_to_str_list(*values) -> list[str]:
    """Flatten the given values (scalars or lists) into a sorted, deduplicated
    list of strings, dropping non-string values like None or numbers."""

    flattened = set()
    for value in values:
        flattened.update(value if isinstance(value, list) else [value])
    return sorted(x for x in flattened if isinstance(x, str))


print('Helper: zms.unibe.helpers.string.normalize_split_by')
@security.public
def normalize_split_by(values: Any = None,
                       delimiters: str = ',;|',
                       splitlines: bool = True,
                       keepends: bool = False,
                       maxsplit: int = 0) -> list[str]:
    """Split arbitrary values based on multiple delimiters,
    split lines of text first, with or without keeping the line endings,
    and limiting the maximum number of splits. Returns a list of strings."""

    if values is None:
        return []

    if isinstance(values, str) and splitlines:
        values = values.splitlines(keepends=keepends)

    strings = values if isinstance(values, list) or isinstance(values, tuple) else [str(values)]
    pattern = '|'.join(map(re.escape, delimiters))
    splitup = []

    for string in strings:
        splitup.extend(re.split(pattern, str(string), maxsplit=maxsplit))

    return [s.strip() for s in splitup if s.strip()]


# Apply security assertions by ModuleSecurityInfo()
# https://zope.readthedocs.io/en/latest/zdgbook/Security.html#external-modulesecurityinfo-declarations
security.apply(globals())

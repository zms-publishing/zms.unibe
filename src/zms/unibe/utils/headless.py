from io import BytesIO
from zope.globalrequest import setRequest
from ZPublisher.HTTPRequest import HTTPRequest
from ZPublisher.HTTPResponse import HTTPResponse


def create_headless_http_request():
    """
    Returns a ZPublisher.HTTPRequest object to be used in headless mode.
    """
    env = {}
    env.setdefault('SERVER_NAME', 'nohost')
    env.setdefault('SERVER_PORT', '80')
    resp = HTTPResponse(stdout=BytesIO)

    return HTTPRequest(stdin=BytesIO, environ=env, response=resp)


headless_http_request = create_headless_http_request()
# Set defaults
headless_http_request.set('ZMS_CONTEXT_URL', True)
# Set headless_http_request via zope.globalrequest.setRequest.
# The ZMS uses the zope.globalrequest.getRequest as a fallback.
setRequest(headless_http_request)

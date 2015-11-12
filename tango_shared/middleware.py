import re

RE_MULTISPACE = re.compile(r"\s{4,}")
RE_NEWLINE = re.compile(r"\n\n")


class StripEmptyLines(object):
    """ Remove extra newlines from HTML output """
    def process_response(self, request, response):
        if 'text/html' in response['Content-Type']:
            response.content = RE_NEWLINE.sub("\n", response.content)
            # do it again to catch leftovers
            response.content = RE_NEWLINE.sub("\n", response.content)
        return response


class CompactHTMLMiddleware(object):
    """
    Remove extra newlines and extraneous spaces from HTML output,
    creating compact layout.
     """
    def process_response(self, request, response):
        if 'text/html' in response['Content-Type']:
            response.content = RE_MULTISPACE.sub(" ", response.content)
            response.content = RE_NEWLINE.sub("\n", response.content)
        return response

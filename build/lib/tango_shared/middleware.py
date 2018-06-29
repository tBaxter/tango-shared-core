import re

# Big thanks to Kenneth Love (@kennethlove) for helping with the regexes.
# This is still not 100% safe with `pre` tags, but you'll *probably* be OK.


# SAFE_PRE skips anything it finds in a `pre` tag
SAFE_PRE = r'(?<!(\<pre\>))(?P<catch>(?:{})+)(?!(\<\/pre\>))'
RE_MULTISPACE = re.compile(SAFE_PRE.format(r" {4,}"))
RE_NEWLINE = re.compile(SAFE_PRE.format(r"\n\n"))


class StripEmptyLines(object):
    """
    Remove extra newlines from HTML output, except inside `pre` tags.
    It's run twice to hopefully catch more multi-line empty spaces.
    """
    def process_response(self, request, response):
        if 'text/html' in response['Content-Type']:
            response.content = RE_NEWLINE.sub("\n", response.content)
            # do it again to catch leftovers
            response.content = RE_NEWLINE.sub("\n", response.content)
        return response


class CompactHTMLMiddleware(object):
    """
    Remove extra newlines and extraneous spaces from HTML output,
    except inside `pre` tags, to create a compact, semi-minified HTML source.
     """
    def process_response(self, request, response):
        if 'text/html' in response['Content-Type']:
            response.content = RE_MULTISPACE.sub(" ", response.content)
            response.content = RE_NEWLINE.sub("\n", response.content)
        return response

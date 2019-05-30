'''Contains a dictionary that maps MIME types to parsers.'''

from .parser import HTMLParser

mimetype = {
	'text/html': HTMLParser
}

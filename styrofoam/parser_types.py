'''Contains a dictionary that maps MIME types to parsers.'''

from .parser import *

mimetype = {
	'text/html': HTMLParser
}
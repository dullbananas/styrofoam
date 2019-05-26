'''Contains a dictionary that maps MIME types to parsers.'''

mime = {}

from .html_parser import HTMLParser
mime['text/html'] = HTMLParser
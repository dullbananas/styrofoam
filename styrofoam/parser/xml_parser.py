import xml.parsers.expat as xml
import logging
import time
from styrofoam.utils import modify_url


class XMLParser:
	'''Parser for XML files.
	
	:param data: The original XML data.
	:param url_prefix: The URL prefix used to modify URLs.
	:param parse: Specifies whether or not to parse the data right away. Default
	              value is ``False``.
	'''
	
	__slots__ = ('data', 'parsed_data', 'url_prefix')
	
	replacements = {}
	
	def __init__(self, data, url_prefix, parse=False):
		self.data = data
		self.url_prefix = url_prefix
		if parse:
			self.parse()
	
	def parse(self):
		'''Parses ``self.data`` and modifies URLs.'''
		# Set parsed_data to empty string
		self.parsed_data = ''
		# Initialize XML parser
		p = xml.ParserCreate()
		p.StartElementHandler = self.handle_start_element
		p.DefaultHandler = self.handle_default
		# Parse data and log execution time
		start_time = time.time()
		p.Parse(self.data, True)
		elapsed_time = time.time() - start_time
		logging.debug('Parsed {} bytes in {} seconds'.format(len(self.data), elapsed_time))
		# Return the resulting data
		return self.data
	
	def a(self, text):
		'''Appends data to ``self.parsed_data``.'''
		self.parsed_data += text
	
	def handle_start_element(self, name, attributes):
		'''Handles beginning element tags (e.g. ``<element attr="value">``) when parsing.'''
		# Define variable that holds the resulting key="value" stuff
		a = ''
		# Iterate through the existing XML tag's attributes
		for key, value in attributes.items():
			# See if the tag has a replaceable attribute (one with a URL)
			if name in self.replacements.keys():
				replacement = self.replacements[name]
				if type(replacement) is str and replacement == key:
					value = modify_url(value, self.url_prefix)
				elif key in replacement:
					value = modify_url(value, self.url_prefix)
			a += '{}="{}" '.format(key, value)
		self.a('<{} {}>'.format(name, a))
	
	def handle_default(self, data):
		'''Handles data when parsing where no other handler is specified.'''
		self.a(data)

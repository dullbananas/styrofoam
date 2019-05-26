import xml.parsers.expat as xml
import logging
import time
from .utils import modify_url


class XMLParser:
	
	__slots__ = ('data', 'parsed_data', 'url_prefix')
	
	replacements = {}
	
	def __init__(self, data, url_prefix, parse=False):
		self.data = data
		self.url_prefix = url_prefix
		if parse:
			self.parse()
	
	def parse(self):
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
		self.parsed_data += text
	
	def handle_start_element(self, name, attributes):
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
		self.a(data)
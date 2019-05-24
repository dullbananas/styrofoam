import xml.parsers.expat as xml
import logging
import time
from .utils import modify_url


class XMLParser:
	
	__slots__ = ('data', 'replacements', 'parsed_data')
	
	replacements = {}
	
	def __init__(self, data, parse=False):
		self.data = data
		if parse:
			self.parse()
	
	def parse(self):
		# Initialize XML parser
		p = xml.ParserCreate()
		p.StartElementHandler = self.handle_start_element
		p.DefaultHandler = self.handle_default
		# Parse data and log execution time
		start_time = time.time()
		p.parse(self.data, True)
		elapsed_time = time.time() - start_time
		logging.debug('Parsed {} bytes in {} seconds'.format(len(self.data), elapsed_time))
		# Return the resulting data
		return self.data
	
	def a(self, text):
		self.parsed_data += text
	
	def handle_start_element(self, name, attributes):
		a = ''
		for key, value in attributes.items():
			if name in self.replacements.keys() and self.replacements[name] == key:
				value = modify_url(value)
			a += '{}="{}"'.format(key, value)
		self.a('<{} {}>'.format(name, a))
	
	def handle_default(self, data):
		self.a(data)
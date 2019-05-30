from . import XMLParser

class HTMLParser(XMLParser):
	'''Parser for HTML files'''
	
	replacements = {
		'a': 'href',
		'applet': 'code',
		'area': 'href',
		'base': 'href',
		'blockquote': 'cite',
		'body': 'background',
		'button': 'formaction',
		'embed': 'src',
		'form': 'action',
		'frame': ('longdesc', 'src'),
		'head': 'profile',
		'iframe': ('longdesc', 'src'),
		'img': 'src',
	}

from styrofoam.parser import XMLParser
import pytest

def rm_whitespace(text):
	result = text.replace(' ', '')
	result = result.replace('\n', '')
	return result


class MyParser(XMLParser):
	
	replacements = {
		'thing': 'url',
		'oof': ('url1', 'url2'),
	}


def test_xml_relative_urls():
	xml = '''<element >
<thing url="path/to/thing" ></thing>
<oof url1="path/to/garbage" url2="nooo/ooo/ooo/oo" ></oof>
</element>'''
	parser = MyParser(xml, '/prefix/of/urls', parse=True)
	assert rm_whitespace(parser.parsed_data) == rm_whitespace(xml)

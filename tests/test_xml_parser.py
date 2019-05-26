from styrofoam.xml_parser import XMLParser


class TestParser(XMLParser):
	
	replacements = {
		'thing': 'url',
		'oof': ('url1', 'url2'),
	}


def test_xml_relative_urls():
	xml = '''<element>
<thing url="path/to/thing"></thing>
<oof url1="path/to/garbage" url2="nooo/ooo/ooo/oo" ></oof>
</element>'''
	parser = TestParser(xml, '/prefix/of/urls')
	assert parser.parse() == xml
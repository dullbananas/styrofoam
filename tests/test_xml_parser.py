from styrofoam.parser import XMLParser
import pytest


class MyParser(XMLParser):
	
	replacements = {
		'thing': 'url',
		'oof': ('url1', 'url2'),
	}


@pytest.mark.filterwarnings('ignore::pytest.PytestCollectionWarning')
def test_xml_relative_urls():
	xml = '''<element >
<thing url="path/to/thing" ></thing>
<oof url1="path/to/garbage" url2="nooo/ooo/ooo/oo" ></oof>
</element>'''
	parser = MyParser(xml, '/prefix/of/urls', parse=True)
	assert parser.parsed_data == xml

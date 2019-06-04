import pytest
from styrofoam.utils import modify_url, unnest_list

def test_modify_url():
	assert modify_url(url='relative/path', prefix='/prefix') == 'relative/path'
	assert modify_url(url='/absolute/path', prefix='/prefix') == '/prefix/absolute/path'
	assert modify_url('/prefix/path/to/thing', '/prefix', remove_prefix=True) == '/path/to/thing'
	assert modify_url('/prefix', '/prefix', remove_prefix=True) == '/'

def test_unnest_list_lists():
	assert unnest_list([['hi']]) == [b'hi']
	assert unnest_list(['hi']) == [b'hi']
	assert unnest_list('hi') == [b'hi']

def test_unnest_list_generators():
	def gen():
		for i in range(3):
			yield('hi')
	
	assert unnest_list([gen()]) == [b'hi']

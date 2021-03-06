import pytest
from styrofoam.utils import modify_url

def test_modify_url():
	assert modify_url(url='relative/path', prefix='/prefix') == 'relative/path'
	assert modify_url(url='/absolute/path', prefix='/prefix') == '/prefix/absolute/path'
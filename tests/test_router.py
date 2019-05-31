import pytest
from styrofoam import Router, Application

sample_environ = {
	'PATH_INFO': '/hi',
	'QUERY_STRING': '',
	'REQUEST_URI': '/hi'
}

def f(*args):
	pass

def app(*args):
	return 'hi'

def test_router_init():
	r = Router(f, [
		Application(f, '/url/a'),
		Application(f, '/url/b'),
	])
	assert r.default.func is f
	assert len(r.apps) == 2
	r.add_app(f, '/url/c')
	assert len(r.apps) == 3

def test_default_app_call():
	r = Router(app)
	assert r(sample_environ, f) == app()
	

def test_application_modify_url():
	a = Application(f, '/prefix')
	assert a._modify_url('/hi') == '/prefix/hi'

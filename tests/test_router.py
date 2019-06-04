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

def app1(environ, start_response):
	start_response('200 OK', [('Content-Type', 'text/plain')])
	env_list = (environ['PATH_INFO'], environ['QUERY_STRING'], environ['REQUEST_URI'])
	for i in env_list:
		yield '{};'.format(i).encode('utf-8')

def test_router_init():
	r = Router(f, [
		Application(f, '/url/a'),
		Application(f, '/url/b'),
	])
	assert r.default.func is f
	assert len(r.apps) == 2
	r.add_app(f, '/url/c')
	assert len(r.apps) == 3

def test_router_environ():
	r = Router(f, [
		Application(app1, '/hi', modify_urls=True)
	])
	assert r(sample_environ, f) == '/;;/;'

def test_router_default_app_call():
	r = Router(app)
	assert r(sample_environ, f) == app()
	

def test_application_modify_url():
	a = Application(f, '/prefix')
	assert a._modify_url('/hi') == '/prefix/hi'

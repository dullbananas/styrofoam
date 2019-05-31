import pytest
from styrofoam import Router, Application

def f():
	pass

def test_router_init():
	r = Router(f, [
		Application(f, '/url/a'),
		Application(f, '/url/b'),
	])
	assert r.default.func is f
	assert len(r.apps) == 2
	r.add_app(f, '/url/c')
	assert len(r.apps) == 3

def test_application_modify_url():
	a = Application(f, '/prefix')
	assert a._modify_url('/hi') == '/prefix/hi'

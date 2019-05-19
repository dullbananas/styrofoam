'''Contains the main Router class that functions as the main WSGI app, and an
Application object that represents a WSGI app
'''

import logging


class Application:
	'''This class represents a WSGI application. It holds the WSGI handler
	function of the app, the url prefix that the app is mounted at, and some
	other configuration options. A ``Router`` object holds an array of
	``Application`` objects, along with the default WSGI application.
	
	:param func: The WSGI handler function (the one with the ``environ`` and the
	             ``start_request`` arguments)
	:param url: The url to mount the application at. It must have a beginning
	            forward slash, but must not have one at the end
	            (e.g. ``/path/to/app``).
	:param modify_urls: Whether or not to parse the app's output and correct
	                    urls in it (e.g. in an ``<a>`` tag) to go to urls within
	                    the one the app is mounted at. For example, an
	                    application that is mounted at ``/oof`` will have
	                    ``<a href="/no">`` replaced to ``<a href="/oof/no">``. It
	                    currently has not been implemented yet. When this
	                    parameter is set to ``True`` (the default), the app's
	                    output will be minified regardless of the ``minify``
	                    attribute.
	'''
	
	def __init__(self, func, url, modify_urls=True, minify=False):
		self.func = func
		self.url = url
		self.modify_urls = modify_urls
		self.minify = minify
		logging.info('Initialized Application with url "{}" and handler {}'.format(url, func))
	
	def __call__(self, *args):
		'''Calls the application's ``func`` attribute'''
		self.func(*args)


class Router:
	
	__slots__ = ('default', 'apps')

	def __init__(self, default_app=None, apps=[]):
		if default_app:
			self.default = Application(func=default_app, url='/')
		self.apps=apps
		logging.info('Initialized styrofoam.Router')
	
	def add_app(self, *args):
		'''Adds a WSGI application to the router. The attributes passed to this
		method are passed to ``Application.__init__``, so these two are the same:
		::
			
			my_router.apps.append(Application(func=f, url='/hi'))
		
		::
			
			my_router.add_app(func=f, url='/hi')
		'''
		self.apps.append(Application(*args))
	
	def __call__(self, environ, start_response):
		logging.info('Router has been called')
		logging.debug('Values in environ dictionary:')
		for key, value in environ.items():
			logging.debug('    {} = "{}"'.format(key, value))
		selected_app = None
		for app in self.apps:
			logging.debug('Checking if "{}" starts with "{}"'.format(environ['SCRIPT_NAME'], app.url))
			if environ['PATH_INFO'].startswith(app.url):
				logging.debug('App {} has been selected'.format(app))
				selected_app = app
				break
			else:
				logging.debug('Default app has been selected')
		if selected_app is not None:
			return selected_app.func(environ, start_response)
		else:
			return self.default.func(environ, start_response)
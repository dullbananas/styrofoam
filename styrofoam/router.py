'''Contains the main Router class that functions as the main WSGI app, and an
Application object that represents a WSGI app
'''

import logging
from .parser_types import mimetype as mime
from .utils import modify_url
from xml.parsers.expat.errors import messages as expat_messages
from xml.parsers.expat import ExpatError


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
	                    currently supports HTTP headers and HTML.
	'''
	
	def __init__(self, func, url, modify_urls=True):
		self.func = func
		self.url = url
		self.modify_urls = modify_urls
		logging.debug('Initialized Application with url "{}" and handler {}'.format(url, func))
	
	def _modify_url(self, url):
		'''Calls ``styrofoam.utils.modify_url`` and automatically fills in the
		``prefix`` argument. It is used by ``__call__`` and is only for internal
		use. It also calls ``logging.debug()``.
		'''
		modified_url = modify_url(url, self.url)
		logging.debug('Changed {} to {}'.format(url, modified_url))
		return modified_url
	
	def __call__(self, environ, start_response):
		'''Calls the application's ``func`` attribute and modifies URLs in the output
		if the object is configured to do so.
		'''
		_status = ''
		_headers = []
		_content = ''
		_environ = {}
		def _start_response(status, headers):
			nonlocal _status, _headers
			_status = status
			_headers = headers
		# Code to run if object is configured to modyify urls
		if self.modify_urls:
			logging.debug('Modifying environ URLs')
			# Modify CGI env variables that contain URLs
			_environ = environ
			_environ['PATH_INFO'] = self._modify_url(_environ['PATH_INFO'])
			_environ['REQUEST_URI'] = _environ['PATH_INFO'] + '?' + _environ['QUERY_STRING']
			# Get self.func's output
			_content = self.func(_environ, _start_response)
			# Modify urls in headers
			_headers_dict = dict((x, y) for x, y in _headers) # Convert headers to a dictionary
			for header_name in ('Content-Location', 'Location'):
				if header_name in  _headers_dict:
					_headers_dict[header_name] = self._modify_url(_headers_dict[header_name])
			_headers = []
			for key, value in _headers_dict.items(): # Convert dict back to list of tuples
				a_farting_tuple = (key, value)
				_headers.append(a_farting_tuple)
			# Modify urls in output's body
			if 'Content-Type' in _headers_dict and _headers_dict['Content-Type'] in mime:
				try:
					parser = mime[_headers_dict['Content-Type']](_content, self.url)
					_content = parser.parse()
				except ExpatError as e:
					logging.warn('XML parsing error: line {e.lineno}, column {e.offset}: {msg} ({e.code})').format(e=e, msg=expat_messages[e.code])
			# Make the response
			start_response(_status, _headers)
			return [_content]
		# If URLs don't need modification, self.func can simply be called
		else:
			return self.func(environ, start_response)


class Router:
	'''This implements the main WSGI app and is the central object. It holds ``Application``
	objects and can be called as a WSGI app.
	
	:param default_app: The default app that is mounted at ``'/'`` (technically it's mounted
	                    at ``''``). This must be a function, not an ``Application`` object.
	:param apps: A list of ``Application`` objects that will be used as the initial
	             value of the ``apps`` property. A tuple should not be used. Default
	             value is an empty list.
	'''
	
	__slots__ = ('default', 'apps')

	def __init__(self, default_app=None, apps=None):
		if default_app:
			self.default = Application(func=default_app, url='')
		self.apps = [] if apps is None else apps
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
		logging.info('-'*40)
		logging.info('Router has been called')
		logging.debug('Values in environ dictionary:')
		for key, value in environ.items():
			logging.debug('    {} = "{}"'.format(key, value))
		selected_app = self.default
		for app in self.apps:
			logging.debug('Checking if "{}" starts with "{}"'.format(environ['SCRIPT_NAME'], app.url))
			if environ['PATH_INFO'].startswith(app.url):
				logging.debug('App {} has been selected'.format(app))
				selected_app = app
				break
			else:
				logging.debug('Default app has been selected')
		logging.debug('Now calling {}'.format(selected_app))
		return selected_app(environ, start_response)

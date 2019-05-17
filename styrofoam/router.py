'''Contains the main Router class that functions as the main WSGI app, and an
Application object that represents a WSGI app'''


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
	
	def __init__(
		self,
		func,
		url,
		modify_urls=True,
		minify=False,
	):
		self.func = func
		self.url = url
		self.modify_urls = modify_urls
		self.minify = minify


class Router:

	def __init__(self, default_app=None, apps=None):
		if default_app:
			self.default = Application(func=default_app, url='/')
		if apps:
			self.apps=apps
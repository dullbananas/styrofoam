def modify_url(url, prefix, remove_prefix=False):
	'''Modifies a URL to go to a location withing ``prefix`` instead of ``/``.
	Here are some examples:
	
	::
	   >>> modify_url('/path/to/thing', '/prefix')
	   '/prefix/path/to/thing'
	   >>> modify_url('/prefix/path/to/thing', '/prefix', remove_prefix=True)
	   '/path/to/thing'
	   >>> modify_url('../relative/path', '/prefix')
	   '../relative/path'
	
	:param url: The original URL
	:param prefix: The URL prefix to modify the URL with. Must start with a slash
	               but not end with one.
	:param remove_prefix: If set to ``True``, this function will remove a prefix
	                      instead of adding one. This assumes that the URL starts
	                      with the prefix and is an absolute URL. Default value is
	                      ``False``.
	'''
	
	if not remove_prefix:
		# See if the path is relative and do nothing
		if not url.startswith('/'):
			return url
		# Modify the url if it is absolute
		else:
			return prefix + url
	else:
		return url[len(prefix):] if url != prefix else '/'


def unnest_list(obj):
	'''Changes ``[['hi']]`` to ``['hi']`` and ``[[['hi', 'bye']]]`` to
	``['hi', 'bye']``, etc., then coverts the list items to ``bytes`` objects.
	This is used by the router to prevent the ``chardet`` library from raising
	a ``TypeError``.
	'''
	if type(obj) in (bytearray, bytes):
		return [obj]
	elif type(obj) == str:
		return [bytes(obj, 'utf-8')]
	else:
		return unnest_list(list(obj)[0])

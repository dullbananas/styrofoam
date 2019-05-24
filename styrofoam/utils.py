def modify_url(url, prefix):
	# See if the path is relative and do nothing
	if not url.startswith('/'):
		return url
	# Modify the url if it is absolute
	else:
		return prefix + url
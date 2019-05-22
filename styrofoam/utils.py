def modify_url(url, prefix):
	if not url.startswith('/'):
		return url
	else:
		return prefix + url
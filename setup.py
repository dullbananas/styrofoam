from setuptools import setup, find_packages
from styrofoam import __version__

with open('README.md') as f:
	readme = f.read()

setup(
	name='styrofoam',
	version=__version__,
	packages=find_packages(),
	python_requires='>=3',
	
	author='Dull Bananas',
	author_email='dull.bananas0@gmail.com',
	license='Unlicense',
	description='Smart and lightweight WSGI router for running multiple separate WSGI apps',
	long_description=readme,
	long_description_content_type='text/markdown',
	keywords='wsgi router',
	url='https://github.com/dullbananas/styrofoam',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'License :: Public Domain',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3 :: Only',
		'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
	],
)
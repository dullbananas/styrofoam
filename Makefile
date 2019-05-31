.PHONY: test

test:
	coverage run --source styrofoam -m pytest
	coverage html
	coverage xml
	python-codacy-coverage -r coverage.xml

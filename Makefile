PHONY: cov, test, travisbuild

travisbuild:
	coverage run --source styrofoam -m pytest -v
	coverage xml
	python-codacy-coverage -r coverage.xml

test:
	python3 -m pytest

cov:
	coverage run --source styrofoam -m pytest
	coverage html

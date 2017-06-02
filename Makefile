
.PHONY: clean-pyc clean-build


tests: clean-pyc
	PYTHONPATH=. py.test tests --verbose

test: clean-pyc
	PYTHONPATH=. py.test $(file) --verbose

deploy:
	git push origin master
	python setup.py sdist upload -r pypi

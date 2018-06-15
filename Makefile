.PHONY: generate setup


generate:
	@pipenv run main manifest.yml dist


setup:
	pip install pipenv --upgrade
	pipenv install --dev
	pipenv run pre-commit install

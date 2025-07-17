.PHONY: build
build:
	python -m build

.PHONY: publish
publish:
	python -m twine upload dist/*
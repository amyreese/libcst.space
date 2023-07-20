install:
	python -m pip install -Ue .[dev]

.venv:
	python -m venv .venv
	source .venv/bin/activate && make install
	echo 'run `source .venv/bin/activate` to activate virtualenv'

venv: .venv

test:
	python -m unittest -v libcstdotspace
	python -m mypy -p libcstdotspace

lint:
	python -m flake8 libcstdotspace
	python -m ufmt check libcstdotspace

format:
	python -m ufmt format libcstdotspace

release: lint test clean
	flit publish

clean:
	rm -rf .mypy_cache build dist html *.egg-info

distclean: clean
	rm -rf .venv

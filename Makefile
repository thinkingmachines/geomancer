.PHONY: build
build: venv requirements.txt
	venv/bin/pip-sync
dev: venv requirements-dev.txt
	venv/bin/pip-sync requirements-dev.txt
venv:
	python3 -m venv venv
	venv/bin/pip3 install pip-tools
requirements.txt: requirements.in
	venv/bin/pip-compile -o requirements.txt --no-header --no-annotate requirements.in 
requirements-dev.txt: requirements-dev.in
	venv/bin/pip-compile -o requirements-dev.txt --no-header --no-annotate requirements-dev.in 

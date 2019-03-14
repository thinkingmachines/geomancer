## Setup

1. Clone and enter the repository.
2. Make a virtual environment, install pip-tools, and activate the virtual environment.
3. Install the dependencies.


### For Mac/Linux
```
$ git clone https://github.com/thinkingmachines/geomancer.git
$ cd geomancer
$ make venv
$ make build
$ make dev
```

### For Windows
```
$ git clone https://github.com/thinkingmachines/geomancer.git
$ cd geomancer
$ python -m venv venv
$ venv\Scripts\activate
$ pip install pip-tools
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
```

Now you're all set! Go out make a few of your own spells. :sparkles: :sparkles: :sparkles:

## Updating the list of dependencies

1. Open up `requirements.in` or `requirements-dev.in` on a text editor and add/remove the package.

2. Use pip-compile in order to update `requirements.txt` or `requirements-dev.txt` based on the contents of the `.in` file.

### For Mac/Linux
```
$ make requirements.txt
$ make requirements-dev.txt
```

### For Windows
```
$ venv\Scripts\pip-compile -o requirements.txt --no-header --no-annotate --no-index --no-emit-trusted-host requirements.in
$ venv\Scripts\pip-compile -o requirements-dev.txt --no-header --no-annotate --no-index --no-emit-trusted-host requirements-dev.in
```

## Running the tests

We use [pytest](https://docs.pytest.org/en/latest/) for testing.

If you don't want to run BigQuery test:
```
$ pytest -m "not bqtest" -v
```

To run all tests:
```
# In project root
$ pytest -v
```
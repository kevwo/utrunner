# utrunner
A simple test runner that wraps unittest and Coverage

### Command line args
```
python -m utrunner -h
```

### Run the unit tests and view a web coverage report
```
python -m utrunner -w
```

### Run the unit tests against a custom source and test location
```
python -m utrunner -s "D:/dev/myproject/mymodule" -t "D:/dev/myproject/tests/unittests
```

### Defaults
The defaults assume the following:
* Currently executing in the directory above both source modules and unit test modules
* The root source module directory name has the same name as it's parent directory
* The unit tests are in a "unittests" subfolder

Example:
```
D:/dev/myproject/requirements.txt
D:/dev/myproject/.gitignore

D:/dev/myproject/myproject/__init__.py
D:/dev/myproject/myproject/samplesourcefile.py

D:/dev/myproject/unittests/__init__.py
D:/dev/myproject/unittests/sampletestfile.py
```

### Considerations
You will likely want to add the following to your projects .gitignore as they are used to story the most recent coverage results
```
htmlcov/
.coverage
```

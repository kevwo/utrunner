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

### Automatically attach debugger when a test case fails
```
python -m utrunner -d
```

### Compare the test execution time of unit tests to catch slow tests or missing mocks
```
python -m utrunner --timer
```

Sample output:

```
Ran 230 tests in 0.451s
OK

Timings (in milliseconds):

test_slow_test_1 68.0549144744873
test_medium_test_1 22.018909454345703
test_medium_test_2 15.012025833129883
test_another_medium_test_2 15.01011848449707
test_medium_test_3 14.014005661010742
test_medium_test_5 14.01209831237793
test_another_medium_test_3 14.011859893798828
test_another_medium_test_1 14.011144638061523
test_medium_test_4 14.010906219482422
test_fast_test_2 5.010128021240234
test_fast_test_1 5.004167556762695
...
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

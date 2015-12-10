import unittest
import sys
import datetime


class JSONTestRunner:

    def __init__(self, stream=sys.stderr):
        self.stream = stream

    def writeUpdate(self, message):
        self.stream.write(message)

    def writeError(self, message, stream=sys.stderr):
        stream.write(message)

    def run(self, test):
        """Run the given test case or test suite."""
        result = _JSONTestResult(self)
        start_time = datetime.datetime.now()
        test(result)
        stop_time = datetime.datetime.now()
        result.printResults(start_time, stop_time)
        result.printErrors()
        run = result.testsRun
        return result


class _JSONTestResult(unittest.TestResult):
    """A test result class that can print test results to JSON"""

    def __init__(self, runner):
        unittest.TestResult.__init__(self)
        self.runner = runner
        self.tests_run = []

    def startTest(self, test):
        unittest.TestResult.startTest(self, test)

    def addSuccess(self, test):
        unittest.TestResult.addSuccess(self, test)
        self.tests_run.append([test.id(), "Passed"])

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        self.tests_run.append([test.id(), "Error"])

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        self.tests_run.append([test.id(), "Failed"])

    def printResults(self, start_time, end_time):
        failed = len(self.failures) + len(self.errors)
        passed = len(self.tests_run) - (len(self.skipped) + failed)
        total_time = end_time - start_time
        passed_percent = (passed / len(self.tests_run)) * 100
        # Print Result Summary
        self.runner.writeUpdate('{\n\t"resultSummary": {\n\t\t')
        self.runner.writeUpdate('"startTime": "%s",\n\t\t' % start_time.isoformat())
        self.runner.writeUpdate('"excludedTests": "%s",\n\t\t' % len(self.skipped))
        self.runner.writeUpdate('"failedTests": "%s",\n\t\t' % failed)
        self.runner.writeUpdate('"passedTests": "%s",\n\t\t' % passed)
        self.runner.writeUpdate('"totalTime": "%s",\n\t\t' % (total_time.seconds + (total_time.microseconds / 1000000)))
        self.runner.writeUpdate('"endTime": "%s",\n\t\t' % end_time.isoformat())
        self.runner.writeUpdate('"passedPercent": "%s",\n\t\t' % round(passed_percent, 2))
        self.runner.writeUpdate('"totalTests": "%s"\n\t' % len(self.tests_run))
        self.runner.writeUpdate('},\n\t')

        # Print detailed results
        self.runner.writeUpdate('"detailedResults": [\n\t\t')
        for test in self.tests_run:
            if self.tests_run.index(test) == (len(self.tests_run) - 1):
                self.runner.writeUpdate('{\n\t\t\t"testDuration": "N/A",\n\t\t\t"testOutcome": "%s",\n\t\t\t"testName": "%s"\n\t\t}\n\t' % (test[1], test[0]))
            else:
                self.runner.writeUpdate('{\n\t\t\t"testDuration": "N/A",\n\t\t\t"testOutcome": "%s",\n\t\t\t"testName": "%s"\n\t\t},\n\t\t' % (test[1], test[0]))

        self.runner.writeUpdate(']\n}\n')

    def printErrors(self):
        self.printErrorList('Error', self.errors)
        self.printErrorList('Failure', self.failures)

    def printErrorList(self, flavor, errors):
        for test, err in errors:
            self.runner.writeError('%s!\n' % flavor)
            self.runner.writeError('Test Name: %s\n' % test.id())
            self.runner.writeError('%s\n' % err)

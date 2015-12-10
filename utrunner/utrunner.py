import sys
import os
import unittest
import pkgutil
import webbrowser
import coverage
import optparse
from utrunner import jsontestrunner


def discover_and_run_tests(test_dir, json_file_path=None):
    # Separate output from the invoking command
    print("=" * 70)

    # use the default shared TestLoader instance
    test_loader = unittest.defaultTestLoader
    # create a TestSuite
    test_suite = unittest.TestSuite()

    #  discover all tests in .\tests directory
    for imp, modname, _ in pkgutil.walk_packages([test_dir]):
        mod = imp.find_module(modname).load_module(modname)
        for test in test_loader.loadTestsFromModule(mod):
            test_suite.addTests(test)

    if json_file_path is not None:
        # open file
        with open(json_file_path, 'w') as f:
            # use the custom JSON test runner
            test_runner = jsontestrunner.JSONTestRunner(f)
            results = test_runner.run(test_suite)
    else:
        # use the basic test runner that outputs to sys.stderr
        test_runner = unittest.TextTestRunner()
        results = test_runner.run(test_suite)
    return results


def test_with_coverage(source_directory=None, test_directory=None, html=False, report=False, json_file_path=None, force=False):
    current_dir = os.getcwd()
    if source_directory is None:
        source_directory = os.path.split(current_dir)[1]
    if test_directory is None:
        test_directory = "unittests"
    source_directory = os.path.join(current_dir, source_directory)
    test_directory = os.path.join(current_dir, test_directory)

    if report or html:
        cov = coverage.Coverage(source=[source_directory])
        cov.start()
        result = discover_and_run_tests(test_directory, json_file_path)
        cov.stop()
        cov.save()
        if result.wasSuccessful() or force:
            if html:
                cov.html_report()
                webbrowser.open(os.path.join(current_dir, 'htmlcov', 'index.html'))
            if report:
                cov.report()
    else:
        results = discover_and_run_tests(test_directory, json_file_path)


def main():
    parser = optparse.OptionParser("usage: %prog [options]")
    parser.add_option("-s", "--source", dest="source_directory", default=None, type="string",
                      help="Location of source files (for determining code coverage)")
    parser.add_option("-t", "--tests", dest="test_directory", default=None, type="string",
                      help="Location of unit test files")
    parser.add_option("-w", '--web', action="store_true", default=False, dest="html",
                      help="Generate an HTML report and opens the report in the default web browser")
    parser.add_option("-r", '--report', action="store_true", default=False, dest="report",
                      help="Generate an text report and displays to the console")
    parser.add_option("-f", '--force', action="store_true", default=False, dest="force",
                      help="Continue with specified reporting even if unit tests fail")
    parser.add_option("-j", "--json", dest="json_file_path", default=None, type="string",
                      help="Output via JSON test results format to FILE", metavar="FILE")
    (options, args) = parser.parse_args()
    input_args = options.__dict__

    # Validate json file input
    file_path = input_args.get('json_file_path', None)
    if file_path is not None:
        # default to local directory if just a filename
        directory = os.path.dirname(file_path[0]) or '.'
        os.makedirs(directory, exist_ok=True)
    test_with_coverage(**input_args)
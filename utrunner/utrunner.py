import sys
import os
import unittest
import pkgutil
import webbrowser
import coverage
import optparse
from utrunner import jsontestrunner, wrappers


def discover_and_run_tests(test_dir, timer=False, debug=False, json_file_path=None):
    # Separate output from the invoking command
    print("=" * 70)

    # use the default shared TestLoader instance
    test_loader = unittest.defaultTestLoader
    # create a TestSuite
    test_suite = unittest.TestSuite()

    #  discover all tests in .\tests directory
    timings = []
    for imp, modname, _ in pkgutil.walk_packages([test_dir]):
        mod = imp.find_module(modname).load_module(modname)
        for test in test_loader.loadTestsFromModule(mod):
            if timer:
                for item in test._tests:
                    item.run = wrappers.timing(item.run, item._testMethodName, timings)
            if debug:
                for item in test._tests:
                    wrappers.debug_testcase(item)
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
    if timer:
        sorted_timings = sorted(timings, key=lambda x: x[1], reverse=True)
        print()
        print("Timings (in milliseconds):")
        print()
        for item in sorted_timings:
            print("{} {}".format(item[0], item[1]))
    return results


def test_with_coverage(source_directory=None, test_directory=None, xml=False, html=False, html_and_launch=False, timer=False, debug=False, report=False, json_file_path=None, force=False):
    current_dir = os.getcwd()
    if source_directory is None:
        source_directory = os.path.split(current_dir)[1]
    if test_directory is None:
        test_directory = "unittests"
    source_directory = os.path.join(current_dir, source_directory)
    test_directory = os.path.join(current_dir, test_directory)

    if report or html or html_and_launch:
        cov = coverage.Coverage(source=[source_directory])
        cov.start()
        results = discover_and_run_tests(test_directory, timer, debug, json_file_path)
        cov.stop()
        cov.save()
        if results.wasSuccessful() or force:
            if html:
                cov.html_report()
                if html_and_launch:
                    webbrowser.open(os.path.join(current_dir, 'htmlcov', 'index.html'))
            if report:
                cov.report()
            if xml:
                cov.xml_report()
    else:
        results = discover_and_run_tests(test_directory, timer, debug, json_file_path)
    return results


def main():
    parser = optparse.OptionParser("usage: %prog [options]")
    parser.add_option("-s", "--source", dest="source_directory", default=None, type="string",
                      help="Location of source files (for determining code coverage)")
    parser.add_option("-t", "--tests", dest="test_directory", default=None, type="string",
                      help="Location of unit test files")
    parser.add_option('--timer', action="store_true", default=False, dest="timer",
                      help="Times the individual unittest execution times")
    parser.add_option('-d', '--debug', action="store_true", default=False, dest="debug",
                      help="Attach debugger when a test case fails")
    parser.add_option("-c", '--coverage', action="store_true", default=False, dest="html",
                      help="Generate an HTML report")
    parser.add_option("-w", '--web', action="store_true", default=False, dest="html_and_launch",
                      help="Generate an HTML report and opens the report in the default web browser")
    parser.add_option("-x", '--xml', action="store_true", default=False, dest="xml",
                      help="Generate an XML report")
    parser.add_option("-r", '--report', action="store_true", default=False, dest="report",
                      help="Generate a text report and displays to the console")
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
    results = test_with_coverage(**input_args)
    sys.exit(not results.wasSuccessful() * 1)

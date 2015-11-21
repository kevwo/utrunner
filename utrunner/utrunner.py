import os
import unittest
import pkgutil
import webbrowser
import coverage
import optparse


def discover_and_run_tests(test_dir):

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

    # use the basic test runner that outputs to sys.stderr
    test_runner = unittest.TextTestRunner()
    return test_runner.run(test_suite)


def test_with_coverage(source_directory=None, test_directory=None, html=False, report=False, force=False):
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
        result = discover_and_run_tests(test_directory)
        cov.stop()
        cov.save()
        if result.wasSuccessful() or force:
            if html:
                cov.html_report()
                webbrowser.open(os.path.join(current_dir, 'htmlcov', 'index.html'))
            if report:
                cov.report()

    else:
        result = discover_and_run_tests(test_directory)

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
    (options, args) = parser.parse_args()
    test_with_coverage(**options.__dict__)
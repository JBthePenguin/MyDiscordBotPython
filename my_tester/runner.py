import os
from unittest import TestLoader, TestSuite
from HtmlTestRunner import HTMLTestRunner
from datetime import datetime
from fnmatch import fnmatchcase
from colorama import Fore, Style
from .result import HtmlTestCaseResult


class MyTestLoader(TestLoader):
    """Override TestLoader to get a non alphabetical order for test methods."""

    def getTestCaseNames(self, testCaseClass):
        """Return a sequence of method names found within TestCaseClass,
        ordered by declaration."""
        def shouldIncludeMethod(attrname):
            if not attrname.startswith(self.testMethodPrefix):
                return False
            testFunc = getattr(testCaseClass, attrname)
            if not callable(testFunc):
                return False
            fullName = f'%s.%s.%s' % (
                testCaseClass.__module__, testCaseClass.__qualname__, attrname
            )
            return self.testNamePatterns is None or \
                any(fnmatchcase(
                    fullName, pattern) for pattern in self.testNamePatterns)
        return list(filter(
            shouldIncludeMethod, vars(testCaseClass).keys()))


class TestCaseRunner(HTMLTestRunner):
    """A HTMLTestRunner for TestCase."""

    def __init__(self, test_cases, add_timestamp, open_in_browser):
        """Set property suites a dict for all tests docs.
        For each tests cases list
        Init ArgumentParser with formatter class and description.
        Set help message's title for help command. Make argument groups.
        Check args and run the corresponding tests.
        ***arg_groups -> [('group_name', [TestCase1, ...]), (..)].***"""
        self.suites = []
        self.tests_docs = {}
        for test_case in test_cases:
            self.update_suites_docs(test_case)
        template_args = {'tests_docs': self.tests_docs}
        super().__init__(
            output='html_test_reports', combine_reports=True,
            report_name='result', add_timestamp=add_timestamp,
            resultclass=HtmlTestCaseResult, template_args=template_args,
            template=os.path.join(
                os.path.dirname(__file__), 'template', 'base_temp.html'),
            report_title=f"{os.path.basename(os.getcwd())} Unittest Results",
            open_in_browser=open_in_browser)

    def update_suites_docs(self, test_case):
        """Init a TestSuite for test_case (or methods) and corresponding docs.
        Update suites property and tests_docs."""
        if isinstance(test_case, tuple):  # suite with methods
            test_case, m_names = test_case
            suite = TestSuite([test_case(m_name) for m_name in m_names])
        else:  # suite with TestCase
            suite = MyTestLoader().loadTestsFromTestCase(test_case)
        if suite._tests:
            self.suites.append((test_case, suite))  # update suites
            tests_docs = {}  # corresponding docs
            for test in suite._tests:
                tests_docs[test._testMethodName] = test._testMethodDoc
            self.tests_docs[test_case.__name__] = tests_docs  # update docs

    def run_suites(self, result):
        """Run all TestCases suites and display result in console."""
        self.start_time = datetime.now()
        for test_case, suite in self.suites:
            self.stream.writeln(  # test case title
                f"\n {Style.BRIGHT}--- {test_case.__name__} ---")
            self.stream.writeln(
                f" {Style.DIM}{test_case.__module__}.py{Style.NORMAL}\n")
            suite(result)  # run tests
            t_case_time = 0  # calculate  and display time for TestCase
            for t_result in result.successes + result.failures + (
                    result.errors + result.skipped):
                if t_result.test_name.split('.')[-1] == test_case.__name__:
                    t_case_time += t_result.elapsed_time
            self.stream.writeln(
                f"\n {Fore.MAGENTA}{result._format_duration(t_case_time)}")
            self.stream.writeln(f"{Fore.RESET}\n{result.separator2}")

    def run(self):
        """ Runs the given testcase or testsuite. """
        result = self._make_result()
        result.failfast = self.failfast
        self.stream.writeln("\nRunning tests... ")
        self.stream.writeln(result.separator2)
        self.run_suites(result)
        result.printErrors()
        self.stream.writeln(result.separator2)
        result.printTotal()
        self.stream.writeln()
        result.printInfos()
        self.stream.writeln(f"Generating HTML reports...{Style.DIM}")
        result.generate_reports(self)
        self.stream.writeln(f"{Style.RESET_ALL}")
        if self.open_in_browser:
            import webbrowser
            for report in result.report_files:
                webbrowser.open_new_tab('file://' + report)
        return result

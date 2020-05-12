import os
from unittest import TestLoader, TestSuite
from HtmlTestRunner import HTMLTestRunner
from HtmlTestRunner.result import HtmlTestResult
from datetime import datetime
from fnmatch import fnmatchcase


class HtmlTestCaseResult(HtmlTestResult):
    """Override HtmlTestResult to change desription and format duration,
    and get a non alphabetical order for test methods."""

    def getDescription(self, test):
        """Return the test description with the test method name."""
        return test._testMethodName

    def _get_info_by_testcase(self):
        """Organize test results by TestCase module,
        without alphabetical order for metohds."""
        tests_by_testcase = {}
        for tests in (
                self.successes, self.failures, self.errors, self.skipped):
            for test_info in tests:
                testcase_name = ".".join(test_info.test_id.split(".")[:-1])
                if testcase_name not in tests_by_testcase:
                    tests_by_testcase[testcase_name] = []
                tests_by_testcase[testcase_name].append(test_info)
        return tests_by_testcase

    @staticmethod
    def _format_duration(elapsed_time):
        """Format the elapsed time in seconds,
        or milliseconds if the duration is less than 1 second."""
        if elapsed_time >= 1:
            duration = f"{str(round(elapsed_time, 3))} s"
        else:
            duration = f"{str(round(elapsed_time * 1000, 2))} ms"
        return duration

    def _prepare_callback(self, t_info, target_list, v_str, short_str):
        """Appends a 'info class' to the given target list,
         and sets a callback method to be called by stopTest method."""
        target_list.append(t_info)

        def callback():
            """ Print test method outcome to the stream and elapsed time."""
            t_info.test_finished()
            if self.showAll:
                self.stream.writeln(  # change original here: format duration
                    f"{v_str} ({self._format_duration(t_info.elapsed_time)})")
            elif self.dots:
                self.stream.write(short_str)
        self.callback = callback


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

    def __init__(self, test_cases):
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
        template_args = {
            'tests_docs': self.tests_docs
        }
        super().__init__(
            output='html_test_reports', combine_reports=True,
            report_name='result', add_timestamp=False,
            resultclass=HtmlTestCaseResult, template_args=template_args,
            template=os.path.join(
                os.path.dirname(__file__), 'template', 'base_temp.html'),
            report_title=f"{os.path.basename(os.getcwd())} Unittest Results")

    def update_suites_docs(self, test_case):
        """Init a TestSuite for test_case (or methods) and corresponding docs.
        Update suites property and tests_docs."""
        if isinstance(test_case, tuple):  # suite with methods
            test_case, m_names = test_case
            suite = TestSuite([test_case(m_name) for m_name in m_names])
        else:  # suite with TestCase
            suite = MyTestLoader().loadTestsFromTestCase(test_case)
        if suite._tests:
            self.suites.append((test_case.__name__, suite))  # update suites
            tests_docs = {}  # corresponding docs
            for test in suite._tests:
                tests_docs[test._testMethodName] = test._testMethodDoc
            self.tests_docs[test_case.__name__] = tests_docs  # update docs

    def run(self):
        """ Runs the given testcase or testsuite. """
        try:
            result = self._make_result()
            result.failfast = self.failfast
            self.stream.writeln()
            self.stream.writeln("Running tests... ")
            self.stream.writeln(result.separator2)
            self.start_time = datetime.now()
            for test_case_name, suite in self.suites:
                self.stream.writeln(f"\n{test_case_name}\n")
                suite(result)
                self.stream.writeln(f"\n{result.separator2}")
            result.printErrors()
            self.stream.writeln(result.separator2)
            full_time = 0
            for t_result in result.successes + result.failures + (
                    result.errors + result.skipped):
                full_time += t_result.elapsed_time
            run = result.testsRun
            self.stream.writeln("Ran {} test{} in {}".format(
                run, run != 1 and "s" or "",
                result._format_duration(full_time)))
            self.stream.writeln()
            expectedFails = len(result.expectedFailures)
            unexpectedSuccesses = len(result.unexpectedSuccesses)
            skipped = len(result.skipped)

            infos = []
            if not result.wasSuccessful():
                self.stream.writeln("FAILED")
                failed, errors = map(len, (result.failures, result.errors))
                if failed:
                    infos.append("Failures={0}".format(failed))
                if errors:
                    infos.append("Errors={0}".format(errors))
            else:
                self.stream.writeln("OK")

            if skipped:
                infos.append("Skipped={}".format(skipped))
            if expectedFails:
                infos.append("Expected Failures={}".format(expectedFails))
            if unexpectedSuccesses:
                infos.append("Unexpected Successes={}".format(unexpectedSuccesses))

            if infos:
                self.stream.writeln(" ({})".format(", ".join(infos)))
            else:
                self.stream.writeln("\n")

            self.stream.writeln()
            self.stream.writeln('Generating HTML reports... ')
            result.generate_reports(self)
            self.stream.writeln()
            if self.open_in_browser:
                import webbrowser
                for report in result.report_files:
                    webbrowser.open_new_tab('file://' + report)
        finally:
            pass
        return result

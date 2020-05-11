from unittest import TestLoader, TestSuite
from HtmlTestRunner import HTMLTestRunner
from HtmlTestRunner.result import HtmlTestResult
from datetime import datetime


class HtmlTestCaseResult(HtmlTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)

    def getDescription(self, test):
        """ Return the test description if not have test name. """
        return test._testMethodName


    def _prepare_callback(self, test_info, target_list, verbose_str,
                          short_str):
        """ Appends a 'info class' to the given target list and sets a
            callback method to be called by stopTest method."""
        target_list.append(test_info)

        def callback():
            """ Print test method outcome to the stream and elapsed time too."""
            test_info.test_finished()

            if self.showAll:
                self.stream.writeln(
                    f"{verbose_str} {str(round(test_info.elapsed_time * 1000, 3))}ms")
            elif self.dots:
                self.stream.write(short_str)

        self.callback = callback


    def addSuccess(self, test):
        """ Called when a test executes successfully. """
        self._save_output_data()
        # print(self)
        self._prepare_callback(self.infoclass(self, test), self.successes, "OK", ".")


class TestCaseRunner(HTMLTestRunner):
    """Override HTMLTestRunner..."""

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
            "report_title": "MyDiscordBotPython Unittest Results",
            'tests_docs': self.tests_docs
        }
        super().__init__(
            output='html_test_reports', combine_reports=True,
            report_name='result', add_timestamp=False,
            resultclass=HtmlTestCaseResult,
            template='html_test_reports/base_temp.html',
            template_args=template_args)

    def update_suites_docs(self, test_case):
        """Return the corresponding tests suite and dict with all tests's docs."""
        if isinstance(test_case, tuple):
            t_case, m_names = test_case
            methods = []
            for m_name in m_names:
                test_method = t_case(m_name)
                methods.append(test_method)
            suite = TestSuite(methods)
            test_case = t_case
        else:
            suite = TestLoader().loadTestsFromTestCase(test_case)
        self.suites.append(suite)
        tests_docs = {}
        for test_method in suite._tests:
            tests_docs[
                test_method._testMethodName] = test_method._testMethodDoc
        self.tests_docs[test_case.__name__] = tests_docs

    def run(self):
        """ Runs the given testcase or testsuite. """
        try:
            result = self._make_result()
            result.failfast = self.failfast
            self.stream.writeln()
            self.stream.writeln("Running tests... ")
            self.stream.writeln(result.separator2)
            t_names = []
            for suite in self.suites:
                if suite._tests:
                    t_name = str(suite._tests[0]).split(" ")
                    t_name = t_name[-1].split('.')[-1][:-1]
                    t_names.append(t_name)
            i = 0
            self.start_time = datetime.now()
            for suite in self.suites:
                if suite._tests:
                    self.stream.writeln(f"\n{t_names[i]}\n")
                    suite(result)
                    self.stream.writeln(f"\n{result.separator2}")
                    i += 1
            stop_time = datetime.now()
            self.time_taken = stop_time - self.start_time
            # print(round(self.time_taken.total_seconds() * 1000, 3))
            result.printErrors()
            self.stream.writeln(result.separator2)
            run = result.testsRun
            self.stream.writeln("Ran {} test{} in {} ms".format(
                run, run != 1 and "s" or "",
                str(round(self.time_taken.total_seconds() * 1000, 3))))
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

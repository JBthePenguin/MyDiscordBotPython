from HtmlTestRunner import HTMLTestRunner
from unittest import TestProgram, TestSuite, TestLoader
from my_bot.info.test import ALL_TESTS_CASE as INFO_TESTS
from sys import argv


class MyTestProgram(TestProgram):
    """A variation of the unittest.TestProgram ."""

    def runTests(self):
        # Pick HTMLTestRunner as the default test runner.
        if self.testRunner is None:
            self.testRunner = HTMLTestRunner(
                output='html_test_reports', combine_reports=True,
                report_name="unittest", add_timestamp=False)
        print(self.tests)
        TestProgram.runTests(self)


main = MyTestProgram



print(argv)
suite_list = []
print(INFO_TESTS[2].__name__)
for test_case in INFO_TESTS:
    suite_list.append(TestLoader().loadTestsFromTestCase(test_case))
suite = TestSuite(suite_list)
runner = HTMLTestRunner(
    output='html_test_reports', combine_reports=True,
    report_name="unittest", add_timestamp=False)
runner.run(suite)

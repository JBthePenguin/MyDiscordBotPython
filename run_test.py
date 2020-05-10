from unittest import TestSuite, TestLoader
from my_tester.com_parser import ArgumentParserTestCase
from my_tester.runner import TestCaseRunner
from my_bot.info.test import INFO_TESTS
import sys

EVENT_TESTS = []
ALL_TESTS = EVENT_TESTS + INFO_TESTS


def get_suite_docs(tests, options=None):
    """Return the corresponding tests suite and dict with all tests's docs."""
    suite_list = []
    all_docs = {}
    if options is None:
        for test_case in tests:
            tests_suite = TestLoader().loadTestsFromTestCase(test_case)
            suite_list.append(tests_suite)
            tests_docs = {}
            for test_method in tests_suite._tests:
                tests_docs[
                    test_method._testMethodName] = test_method._testMethodDoc
            all_docs[test_case.__name__] = tests_docs
    else:
        test_case = tests[0]
        methods = []
        tests_docs = {}
        for option in options:
            test_method = test_case(option)
            methods.append(test_method)
            # suite_list.append(test_method)
            tests_docs[
                test_method._testMethodName] = test_method._testMethodDoc
        all_docs[test_case.__name__] = tests_docs
        suite_list.append(TestSuite(methods))
    suite = TestSuite(suite_list)
    return suite, all_docs


if __name__ == "__main__":
    if len(sys.argv) == 1:  # no argument passed
        suite, all_docs = get_suite_docs(ALL_TESTS)
        TestCaseRunner('full_test', all_docs).run(suite)
    else:  # parse args
        groups = [('info', INFO_TESTS), ('event', EVENT_TESTS)]
        parser = ArgumentParserTestCase(groups)
        args = parser.parse_args()
        # check args
        args_dict = vars(args)
        for name_tests in groups:
            if args_dict[name_tests[0]]:  # all group test
                suite, all_docs = get_suite_docs(name_tests[1])
                TestCaseRunner(f"{name_tests[0]}_test", all_docs).run(suite)
        for test_case in ALL_TESTS:
            test_name = test_case.__name__
            options = args_dict[test_name]
            if isinstance(options, list):
                if not options:  # all test case tests
                    suite, all_docs = get_suite_docs([test_case])
                    TestCaseRunner(test_name, all_docs).run(suite)
                else:  # tests case methods
                    suite, all_docs = get_suite_docs([test_case], options)
                    TestCaseRunner(f"{test_name}_methods", all_docs).run(suite)

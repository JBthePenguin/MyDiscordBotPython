from HtmlTestRunner import HTMLTestRunner
from unittest import TestSuite, TestLoader
from my_bot.info.test import INFO_TESTS
from sys import argv
from argparse import ArgumentParser

I_TEST_NAMES = [t.__name__ for t in INFO_TESTS]
EVENT_TESTS = []
E_TEST_NAMES = [t.__name__ for t in EVENT_TESTS]


class MyTestRunner(HTMLTestRunner):

    pass


def get_suite(tests):
    suite_list = []
    for test_case in tests:
        suite_list.append(
            TestLoader().loadTestsFromTestCase(test_case))
    return TestSuite(suite_list)


if __name__ == "__main__":
    if len(argv) == 1:  # no argument passed
        MyTestRunner(
            output='html_test_reports', combine_reports=True,
            report_name='full_test', add_timestamp=False).run(
                get_suite(INFO_TESTS + EVENT_TESTS))
    else:
        # check if all argv exist
        parser = ArgumentParser(
            description='\n'.join([
                'Run without argument for all tests, ',
                'or with optionnal one(s) for all tests for a specific app',
                '', ]))
        parser.add_argument(
            '-i', '--info', nargs='*', choices=I_TEST_NAMES,
            help='Run without parameter for all InfoTeam test or name')
        parser.add_argument(
            '-e', '--event', nargs='*', choices=E_TEST_NAMES,
            help='Run without parameter for all Event tests or name')
        args = parser.parse_args()
        if args.info is not None:
            if args.info == []:  # all info tests
                MyTestRunner(
                    output='html_test_reports', combine_reports=True,
                    report_name='info_test', add_timestamp=False).run(
                        get_suite(INFO_TESTS))
            else:
                print("run test ", args.info)
        if args.event is not None:
            if args.event == []:  # all event tests
                MyTestRunner(
                    output='html_test_reports', combine_reports=True,
                    report_name='event_test', add_timestamp=False).run(
                        get_suite(EVENT_TESTS))
            else:
                print("run test ", args.event)

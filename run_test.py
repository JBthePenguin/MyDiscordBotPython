from HtmlTestRunner import HTMLTestRunner
from unittest import TestSuite, TestLoader
from my_bot.info.test import INFO_TESTS
from sys import argv
from argparse import (
    ArgumentParser, HelpFormatter, SUPPRESS, OPTIONAL, ZERO_OR_MORE,
    ONE_OR_MORE, REMAINDER, PARSER)

I_TEST_NAMES = [t.__name__ for t in INFO_TESTS]
EVENT_TESTS = []
E_TEST_NAMES = [t.__name__ for t in EVENT_TESTS]
TESTS = {
    'info': INFO_TESTS,
    'event': EVENT_TESTS}
TEST_NAMES = {
    'info': I_TEST_NAMES,
    'event': E_TEST_NAMES}


class MyHelpFormatter(HelpFormatter):

    def _format_args(self, action, default_metavar):
        get_metavar = self._metavar_formatter(action, default_metavar)
        if action.nargs is None:
            result = '%s' % get_metavar(1)
        elif action.nargs == OPTIONAL:
            result = '[%s]' % get_metavar(1)
        elif action.nargs == ZERO_OR_MORE:
            metavar = get_metavar(1)
            if len(metavar) == 2:
                result = '[%s [%s ...]]' % metavar
            else:
                result = "[Optionnal: method's names]"
                # result = '%s' % metavar
        elif action.nargs == ONE_OR_MORE:
            result = '%s [%s ...]' % get_metavar(2)
        elif action.nargs == REMAINDER:
            result = '...'
        elif action.nargs == PARSER:
            result = '%s ...' % get_metavar(1)
        elif action.nargs == SUPPRESS:
            result = ''
        else:
            try:
                formats = ['%s' for _ in range(action.nargs)]
            except TypeError:
                raise ValueError("invalid nargs value") from None
            result = ' '.join(formats) % get_metavar(action.nargs)
        return result

    def _format_action_invocation(self, action):
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            metavar, = self._metavar_formatter(action, default)(1)
            return metavar
        else:
            parts = []
            if action.nargs == 0:
                parts.extend(action.option_strings)
            else:
                default = self._get_default_metavar_for_optional(action)
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    parts.append('%s %s' % (option_string, args_string))

            return '\n' + ', '.join(parts)


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
            formatter_class=MyHelpFormatter, description='\n'.join([
                'Without argument to run all tests, ',
                'or with optionnal one(s) without option to run all ',
                "specific app or TestCase tests, or with test's names",
                " in option for a TestCase arg to run specific tests.", ]))
        parser._optionals.title = 'Help'
        # argument groups
        for arg_name in ['info', 'event']:
            group = parser.add_argument_group(f"{arg_name.title()} Tests")
            # app arg
            group.add_argument(
                f"--{arg_name}", action='store_true',
                help=f"Run all {arg_name.title()} tests.")
            for test_case in TESTS[arg_name]:
                # test case arg
                for test_name in TEST_NAMES[arg_name]:
                    if test_name == test_case.__name__:
                        break
                # optionnal choise -> tests case methods
                methods = TestLoader().loadTestsFromTestCase(test_case)._tests
                methods_names = [m._testMethodName for m in methods]
                group.add_argument(
                    f"--{test_name}", choices=methods_names, nargs='*',
                    help="".join([
                        f"Without option to run all {test_name} tests,",
                        " or pass method's names to run specific tests. ",
                        "Allowed values are: ", " - ".join(methods_names)]))
        args = parser.parse_args()
        if args.info:  # all info tests
            MyTestRunner(
                output='html_test_reports', combine_reports=True,
                report_name='info_test', add_timestamp=False).run(
                    get_suite(INFO_TESTS))
        if args.event:  # all event test
            MyTestRunner(
                output='html_test_reports', combine_reports=True,
                report_name='event_test', add_timestamp=False).run(
                    get_suite(EVENT_TESTS))
        args_dict = vars(args)
        for test_name in (I_TEST_NAMES + E_TEST_NAMES):
            options = args_dict[test_name]
            if isinstance(options, list):
                if not options:  # all test case tests
                    for test_case in (INFO_TESTS + EVENT_TESTS):
                        if test_name == test_case.__name__:
                            break
                    MyTestRunner(
                        output='html_test_reports', combine_reports=True,
                        report_name=test_name, add_timestamp=False).run(
                            get_suite([test_case]))

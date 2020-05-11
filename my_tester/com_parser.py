import sys
from unittest import TestLoader
from argparse import (
    ArgumentParser, HelpFormatter, SUPPRESS, OPTIONAL, ZERO_OR_MORE,
    ONE_OR_MORE, REMAINDER, PARSER)
from .runner import TestCaseRunner


class HelpFormatterTestCase(HelpFormatter):
    """Overide HelpFormatter to customize help message."""

    def _format_args(self, action, default_metavar):
        """Just change result for args."""
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
        """Just add a \n between args."""
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
            # return ', '.join(parts)


class ArgumentParserTestCase(ArgumentParser):
    """Override ArgumentParser..."""

    def __init__(self, arg_groups):
        """Set a all tests list and run them if no argument passed.
        Else, init ArgumentParser with formatter - description,
        set help message's title for help command, make argument groups.
        ***arg_groups -> [('group_name', [TestCase1, ...]), (..)].***"""
        all_tests = []
        for name_tests in arg_groups:
            all_tests += name_tests[1]
        if len(sys.argv) == 1:  # no arg -> all tests
            TestCaseRunner('full_test', all_tests).run()
        else:  # parse args
            super().__init__(  # init ArgumentParser
                formatter_class=HelpFormatterTestCase, description='\n'.join([
                    'Without argument to run all tests, ',
                    'or with optionnal one(s) without option to run ',
                    "specific app or TestCase tests, or with method's names",
                    " in options for TestCase arg to run specific tests."]))
            self._optionals.title = 'Help'  # help msg's title for help command
            self.make_arg_groups(arg_groups)  # groups
            args = self.parse_args()  # parse
            args_dict = vars(args)  # check args and run associated tests
            for name_tests in arg_groups:
                if args_dict[name_tests[0]]:  # group's name arg -> group's tests
                    TestCaseRunner(f"{name_tests[0]}_test", name_tests[1]).run()
            for test_case in all_tests:
                test_name = test_case.__name__
                options = args_dict[test_name]
                if isinstance(options, list):  # test case's name arg
                    if not options:  # no param -> test case's tests
                        TestCaseRunner(test_name, [test_case]).run()
                    else:  # method name(s) param -> methods's tests
                        TestCaseRunner(
                            f"{test_name}_methods", [test_case], options).run()

    def make_arg_groups(self, arg_groups):
        """ For each group, set help message's title with his name,
        add argument with his name, for each of his TestCases,
        add argument with his name, for each of his methods,
        add optionnal parameter with his name."""
        for group_name, tests_cases in arg_groups:  # groups
            group = self.add_argument_group(f"{group_name.title()} Tests")
            group.add_argument(  # arg with group name to run all tests
                f"--{group_name}", action='store_true',
                help=f"Run all {group_name.title()} tests.")
            for test_case in tests_cases:
                methods = TestLoader().loadTestsFromTestCase(test_case)._tests
                methods_names = [m._testMethodName for m in methods]
                # arg with testcase name and methods names for optionnal params
                group.add_argument(  # arg with testcase name
                    f"--{test_case.__name__}", choices=methods_names,
                    nargs='*', help="".join([  # optionnal params with methods
                        f"Without option to run {test_case.__name__}'s tests,",
                        " or pass method's names to run specific tests. ",
                        "Allowed values are: ", " - ".join(methods_names)]))

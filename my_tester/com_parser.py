import sys
from argparse import ArgumentParser, HelpFormatter
from unittest import TestLoader
from .runner import TestCaseRunner


class HelpFormatterTestCase(HelpFormatter):
    """Override HelpFormatter to customize help message."""

    def _format_args(self, action, default_metavar):
        """Return the result to display nargs(ZERO_OR_MORE)."""
        return "options"

    def _format_action_invocation(self, action):
        """Add \n a the end of original method to add a space between args."""
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


class ArgumentParserTestCase(ArgumentParser):
    """An Argument Parser for groups of TestCase."""

    def __init__(self, tests_groups):
        """Set properties arg_groups and all tests list.
        Init ArgumentParser with formatter class and description.
        Set help message's title for help command. Make argument groups.
        Check args and run the corresponding tests.
        ***arg_groups -> [('group_name', [TestCase1, ...]), (..)].***"""
        self.tests_groups = tests_groups
        self.all_tests = []
        super().__init__(  # init ArgumentParser
            formatter_class=HelpFormatterTestCase, allow_abbrev=False,
            description=''.join([
                'Without argument to run all tests, or with optionnal ',
                'one(s) without option to run group or TestCase tests, or ',
                'with method names in options to a TestCase arg to run',
                'specific test methods.']))
        self._optionals.title = 'Optionnal'  # help msg title for help command
        self.add_argument(  # arg to open report diretly in browser
            "-t", "--timestamp", action='store_true',
            help="Add timestamp in report file name.")
        self.add_argument(  # arg to open report diretly in browser
            "-o", "--open", action='store_true',
            help="Open report in browser directly after tests.")
        self.make_arg_groups()  # groups
        self.check_and_run()  # check args and run the corresponding tests

    def make_arg_groups(self):
        """ For each tests group, set help message's title with his name,
        add argument with his name, for each of his TestCases,
        add argument with his name, for each of his methods,
        add optionnal parameter with his name.
        ***construct all tests list by adding each tests cases list"""
        for group_name, tests_cases in self.tests_groups:  # groups
            self.all_tests += tests_cases
            group = self.add_argument_group(f"{group_name.title()} TestCases")
            group.add_argument(  # arg with group name to run all tests
                f"-{group_name}", action='store_true',
                help=f"Run all {group_name.title()} tests.")
            for t_case in tests_cases:
                methods = TestLoader().loadTestsFromTestCase(t_case)._tests
                m_names = [m._testMethodName for m in methods]
                group.add_argument(  # arg with testcase name
                    f"-{t_case.__name__}", help=' - '.join(m_names),
                    nargs='*', choices=m_names)  # methods names for params

    def check_and_run(self):
        """Check args, set a list and append to it corresponding tests cases,
        before run it."""
        all_test_cases = []
        args = self.parse_args()
        if (len(sys.argv) == 1) or (
                (len(sys.argv) == 2) and (args.open or args.timestamp)) or (
                    (len(sys.argv) == 3) and args.open and args.timestamp):
            all_test_cases += self.all_tests  # no arg or open -> all tests
        else:
            args_dict = vars(args)
            for group_name, test_cases in self.tests_groups:
                if args_dict[group_name]:  # group's name arg -> group tests
                    all_test_cases += test_cases
            for test_case in self.all_tests:
                # t_case_name = test_case.__name__
                options = args_dict[test_case.__name__]
                if isinstance(options, list):  # test case's name arg
                    if not options:  # no param -> test case's tests
                        all_test_cases.append(test_case)
                    else:  # method name(s) param -> methods's tests
                        all_test_cases.append((test_case, options))
        TestCaseRunner(all_test_cases, args.timestamp, args.open).run()

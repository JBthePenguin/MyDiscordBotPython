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
        """Set properties arg_groups and all tests list.
        Init ArgumentParser with formatter class and description.
        Set help message's title for help command. Make argument groups.
        Check args and run the corresponding tests.
        ***arg_groups -> [('group_name', [TestCase1, ...]), (..)].***"""
        self.arg_groups = arg_groups
        self.all_tests = []
        super().__init__(  # init ArgumentParser
            formatter_class=HelpFormatterTestCase, description='\n'.join([
                'Without argument to run all tests, ',
                'or with optionnal one(s) without option to run ',
                "specific app or TestCase tests, or with method's names",
                " in options for TestCase arg to run specific tests."]))
        self._optionals.title = 'Help'  # help msg's title for help command
        self.make_arg_groups()  # groups
        self.check_and_run()

    def make_arg_groups(self):
        """ For each group, set help message's title with his name,
        add argument with his name, for each of his TestCases,
        add argument with his name, for each of his methods,
        add optionnal parameter with his name.
        ***construct all tests list by adding each tests cases list"""
        for group_name, tests_cases in self.arg_groups:  # groups
            self.all_tests += tests_cases
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

    def check_and_run(self):
        """Check args and set the corresponding tests cases list and run it."""
        tests_cases = []
        if len(sys.argv) == 1:  # no arg -> all tests
            tests_cases.append(self.all_tests)
        else:
            args_dict = vars(self.parse_args())
            for name_tests in self.arg_groups:
                if args_dict[name_tests[0]]:  # group's name arg -> group tests
                    tests_cases.append(name_tests[1])
            for test_case in self.all_tests:
                test_name = test_case.__name__
                options = args_dict[test_name]
                if isinstance(options, list):  # test case's name arg
                    if not options:  # no param -> test case's tests
                        tests_cases.append([test_case])
                    else:  # method name(s) param -> methods's tests
                        tests_cases.append(([test_case], options))
        TestCaseRunner(tests_cases).run()

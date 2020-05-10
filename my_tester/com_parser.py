from unittest import TestLoader
from argparse import (
    ArgumentParser, HelpFormatter, SUPPRESS, OPTIONAL, ZERO_OR_MORE,
    ONE_OR_MORE, REMAINDER, PARSER)


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

    def __init__(self, groups):
        """Init ArgumentParser with MyHelpFormatter and description.
        groups -> [(name, [TestCase, ...]), (..)].
        Name is used for arg's name to run all tests."""
        super().__init__(
            formatter_class=HelpFormatterTestCase, description='\n'.join([
                'Without argument to run all tests, ',
                'or with optionnal one(s) without option to run all ',
                "specific app or TestCase tests, or with test's names",
                " in option for a TestCase arg to run specific tests."]))
        # groups
        self._optionals.title = 'Help'
        for name_tests in groups:
            group = self.add_argument_group(f"{name_tests[0].title()} Tests")
            # all tests arg
            group.add_argument(
                f"--{name_tests[0]}", action='store_true',
                help=f"Run all {name_tests[0].title()} tests.")
            for test_case in name_tests[1]:
                test_name = test_case.__name__
                # optionnal choise -> tests case methods
                methods = TestLoader().loadTestsFromTestCase(test_case)._tests
                methods_names = [m._testMethodName for m in methods]
                # test ase tests
                group.add_argument(
                    f"--{test_name}", choices=methods_names, nargs='*',
                    help="".join([
                        f"Without option to run all {test_name} tests,",
                        " or pass method's names to run specific tests. ",
                        "Allowed values are: ", " - ".join(methods_names)]))

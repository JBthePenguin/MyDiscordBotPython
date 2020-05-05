from HtmlTestRunner import HTMLTestRunner
import unittest

# if __name__ == '__main__':
#     unittest.main(testRunner=HTMLTestRunner(output='example_suite'))


class TestProgram(unittest.TestProgram):
    """
    A variation of the unittest.TestProgram. Please refer to the base
    class for command line parameters.
    """
    def runTests(self):
        # Pick TestRunner as the default test runner.
        # base class's testRunner parameter is not useful because it means
        # we have to instantiate TestRunner before we know self.verbosity.
        if self.testRunner is None:
            self.testRunner = HTMLTestRunner(output='example_suite')
        unittest.TestProgram.runTests(self)

main = TestProgram

##############################################################################
# Executing this module from the command line
##############################################################################

if __name__ == "__main__":
    main(module=None)

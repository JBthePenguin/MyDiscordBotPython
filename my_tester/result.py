from HtmlTestRunner.result import HtmlTestResult
from colorama import Fore


class HtmlTestCaseResult(HtmlTestResult):
    """Override HtmlTestResult to change desription and format duration,
    and get a non alphabetical order for test methods."""

    def getDescription(self, test):
        """Return the test description with the test method name."""
        return test._testMethodName

    def _get_info_by_testcase(self):
        """Organize test results by TestCase module,
        without alphabetical order for metohds."""
        tests_by_testcase = {}
        for tests in (
                self.successes, self.failures, self.errors, self.skipped):
            for test_info in tests:
                testcase_name = ".".join(test_info.test_id.split(".")[:-1])
                if testcase_name not in tests_by_testcase:
                    tests_by_testcase[testcase_name] = []
                tests_by_testcase[testcase_name].append(test_info)
        return tests_by_testcase

    @staticmethod
    def _format_duration(elapsed_time):
        """Format the elapsed time in seconds,
        or milliseconds if the duration is less than 1 second."""
        if elapsed_time >= 1:
            duration = f"{str(round(elapsed_time, 3))}s"
        else:
            duration = f"{str(round(elapsed_time * 1000, 2))}ms"
        return duration

    def _prepare_callback(self, t_info, target_list, v_str, short_str):
        """Appends a 'info class' to the given target list,
         and sets a callback method to be called by stopTest method."""
        target_list.append(t_info)

        def callback():
            """ Print test method outcome to the stream and elapsed time."""
            t_info.test_finished()
            if self.showAll:
                if v_str == "OK":
                    t_color = Fore.GREEN
                else:
                    t_color = ''
                self.stream.writeln(  # change original here: format duration
                    f"{t_color}{v_str}{Fore.RESET} ... {Fore.MAGENTA}{self._format_duration(t_info.elapsed_time)}{Fore.RESET}")
            elif self.dots:
                self.stream.write(short_str)
        self.callback = callback

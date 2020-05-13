from HtmlTestRunner.result import HtmlTestResult
from colorama import Fore, Style


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
            if self.showAll:  # add colors
                if v_str == "OK":
                    t_color = Fore.GREEN
                elif v_str == "FAIL":
                    t_color = Fore.YELLOW
                elif v_str == "ERROR":
                    t_color = Fore.RED
                elif v_str == "SKIP":
                    t_color = Fore.CYAN
                else:
                    t_color = ''
                status = f"{t_color}{v_str}{Fore.RESET}"
                time_str = f"{self._format_duration(t_info.elapsed_time)}"
                self.stream.writeln(
                    f"{status} ... {Fore.MAGENTA}{time_str}{Fore.RESET}")
            elif self.dots:
                self.stream.write(short_str)
        self.callback = callback

    def printErrorList(self, flavour, errors):
        for test_info in errors:
            if flavour == "ERROR":
                t_color = Fore.RED
            else:
                t_color = Fore.YELLOW
            self.stream.writeln(self.separator1)
            c_flavour = f"{t_color}{flavour}"
            test_name = f"{test_info.test_id}".split('.')[-2:]
            test_str = f"{Style.BRIGHT}{test_name[0]}{Style.NORMAL}"
            test_str += f".{test_name[1]}"
            time_str = f"{Fore.MAGENTA}"
            time_str += f"{self._format_duration(test_info.elapsed_time)}"
            error_name = f"{t_color}{test_info.err[0].__name__}"
            traceback = test_info.get_error_info()
            self.stream.writeln(
                f"{c_flavour} {time_str}{Fore.RESET}: {test_str}")
            self.stream.writeln(self.separator2)
            self.stream.writeln(
                f"{error_name}: {str(test_info.err[1])}{Fore.RESET}")
            self.stream.writeln(self.separator2)
            self.stream.writeln(f"{Style.DIM}{traceback}{Style.NORMAL}")

    def printTotal(self):
        full_time = 0
        for t_result in self.successes + self.failures + (
                self.errors + self.skipped):
            full_time += t_result.elapsed_time
        run = self.testsRun
        s_test = "test"
        if run > 1:
            s_test += "s"
        ran_text = f"{Style.BRIGHT}Ran {run} {s_test}{Style.NORMAL}"
        full_time_str = self._format_duration(full_time)
        self.stream.writeln(
            f"{ran_text} in {Fore.MAGENTA}{full_time_str}{Fore.RESET}")

    def printInfos(self):
        """Print infos at the end of all tests."""
        expectedFails = len(self.expectedFailures)
        unexpectedSuccesses = len(self.unexpectedSuccesses)
        skipped = len(self.skipped)
        infos = []
        if not self.wasSuccessful():
            self.stream.writeln(f"{Fore.RED}FAILED{Fore.RESET}")
            failed, errors = map(len, (self.failures, self.errors))
            if failed:
                infos.append(f"{Fore.YELLOW}Failures={failed}{Fore.RESET}")
            if errors:
                infos.append(f"{Fore.RED}Errors={errors}{Fore.RESET}")
        else:
            self.stream.writeln(f"{Fore.GREEN}OK{Fore.RESET}")
        if skipped:
            infos.append(f"{Fore.CYAN}Skipped={skipped}{Fore.RESET}")
        if expectedFails:
            e_fail = "Expected Failures="
            infos.append(
                f"{Fore.YELLOW}{e_fail}{expectedFails}{Fore.RESET}")
        if unexpectedSuccesses:
            u_suc = "Unexpected Successes="
            infos.append(
                f"{Fore.GREEN}{u_suc}{unexpectedSuccesses}{Fore.RESET}")
        if infos:
            self.stream.writeln(" ({})".format(", ".join(infos)))
        else:
            self.stream.writeln("\n")

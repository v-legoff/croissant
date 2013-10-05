# Copyright (c) 2013 LE GOFF Vincent
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Module containing the console output."""

import sys

from croissant.output.base import BaseOutput

class ConsoleOutput(BaseOutput):

    """Console output.

    This class defines a console output, an output that is used in console.

    """

    def __init__(self):
        BaseOutput.__init__(self)
        self.file = sys.stdout
        self.error_file = sys.stderr

    def get_trace(self, scenario):
        """Try to retrieve the traceback from the scenario.

        The trace, if found, is formatted.

        """
        trace = self.traces.get(scenario.identifier)
        if trace is None:
            return "[can't be found]"

        lines = trace.split("\n")
        del lines[0]
        return "\n  " + "\n  ".join(lines)

    def handle_syntax_error(self, error):
        """Handle a syntax error in one of the user stories."""
        self.error_file.write(str(error) + "\n")

    def handle_step_not_found(self, error):
        """Handle the error if a step cannot be found."""
        self.file.write("U")

    def handle_assertion(self, error):
        """Handle the error when an assertion fails."""
        self.file.write("F")

    def handle_exception(self, exception):
        """Handle the exception when an error occures while executing."""
        self.file.write("E")

    def handle_success(self, story_name):
        """Handle a success."""
        self.file.write(".")

    def display_main_report(self):
        """Display the main report (statistics)."""
        file = self.file
        print("\n\n" + "-" * 79, file=file)
        nb_passed = len(self.stories) - len(self.failures) - len(self.errors)
        print("\n  {} stories found (passed={}, failed={}, " \
                "errors={}".format(len(self.stories), nb_passed,
                len(self.failures), len(self.errors)), file=file)

    def display_report_failures(self):
        """Display the report on failures."""
        file = self.file
        failures = self.failures
        if failures:
            print("\nFailures:", file=file)

        for failure in failures:
            scenario = failure.scenario
            story = scenario.father
            story_title = story.title
            path = scenario.path
            title = scenario.title
            no_line = scenario.start_at
            message = failure.message
            print("\n  Story {} ({})".format(story_title, path), file=file)
            print("  Scenario: {} (line {})".format(title, no_line), file=file)
            print("  Failure: {}".format(message), file=file)
            print("  Traceback: {}".format(self.get_trace(scenario)),
                    file=file)

    def display_report_errors(self):
        """Display the report on errors."""
        file = self.file
        errors = self.errors
        if errors:
            print("\nErrors:", file=file)

        for scenario, error in errors:
            story = scenario.father
            story_title = story.title
            path = scenario.path
            title = scenario.title
            no_line = scenario.start_at
            message = str(error)
            print("\n  Story {} ({})".format(story_title, path), file=file)
            print("  Scenario: {} (line {})".format(title, no_line), file=file)
            print("  Failed assertion: {}".format(message), file=file)
            print("  Traceback: {}".format(self.get_trace(scenario)),
                    file=file)

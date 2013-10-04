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


"""Module containing the base class of outputs."""

from abc import *
import traceback

from language.exceptions.syntax import LanguageSyntaxError
from project.definition import Definition
from step.exceptions import *

class BaseOutput(metaclass=ABCMeta):

    """Base class for ouput.

    Ideally, all outputs should inherit from this class.  It contains
    methods to help control how the reports are displayed.

    """

    def __init__(self):
        self.definition = Definition()
        self.stories = self.definition.stories
        self.failures = []
        self.errors = []
        self.traces = {}

    def load(self, root):
        """Load the steps and stories of a given directory."""
        try:
            self.definition.load(root)
        except LanguageSyntaxError as err:
            self.handle_syntax_error(err)
            sys.exit(1)

    def run(self):
        """Run the different stories."""
        for story_name in self.stories:
            self.run_story(story_name)

    def run_story(self, story_name):
        """Run a specific story.

        In this method, the different assert_* errors are being tested
        to produce a report.

        """
        story = self.definition.stories[story_name]
        for scenario in story.scenarios:
            self.run_scenario(story_name, scenario)

    def run_scenario(self, story_name, scenario):
        """Run a specific scenario."""
        try:
            self.definition.run_scenario(story_name, scenario)
        except StepNotFound as err:
            self.failures.append(err)
            self.traces[scenario.identifier] = traceback.format_exc()
            self.handle_step_not_found(err)
        except StepAssertionError as err:
            self.failures.append(err)
            self.traces[scenario.identifier] = traceback.format_exc()
            self.handle_assertion(err)
        except Exception as err:
            self.errors.append((scenario, err))
            self.traces[scenario.identifier] = traceback.format_exc()
            self.handle_exception(err)
        else:
            self.handle_success(story_name)

        self.display_report()

    @abstractmethod
    def handle_syntax_error(self, error):
        """Handle a syntax error in one of the user stories."""
        pass

    @abstractmethod
    def handle_step_not_found(self, error):
        """Handle the error if a step cannot be found."""
        pass

    @abstractmethod
    def handle_assertion(self, error):
        """Handle the error when an assertion fails."""
        pass

    @abstractmethod
    def handle_exception(self, exception):
        """Handle the exception when an error occures while executing."""
        pass

    @abstractmethod
    def handle_success(self, story_name):
        """Handle when a user story passes without errors."""
        pass

    def display_report(self):
        """Display a report."""
        self.display_main_report()
        self.display_report_failures()
        self.display_report_errors()

    @abstractmethod
    def display_main_report(self):
        """Display the main report (statistics)."""
        pass

    @abstractmethod
    def display_report_failures(self):
        """Display the report on failures."""
        pass

    @abstractmethod
    def display_report_errors(self):
        """Display the report on errors."""
        pass

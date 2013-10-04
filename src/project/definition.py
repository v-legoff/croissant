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


import importlib
import os

from step.exceptions import *
from story.story import Story

"""Module containing the class Definition described Below."""

class Definition:

    """Class containing a user's definition.

    It contains:
        steps -- the user's steps
        stories -- the user's stories
        ...

    """

    def __init__(self):
        self.stories = {}
        self.classes = {}

    def load(self, root):
        """Load the steps and stories in a directory.

        The stories are supposed to be stored in files with the '.feature'
        extension.  The steps, on the other hand, are stored in '.py'
        files.  The given directory could have two different structures:
        * Either it contains only sub-directories: in this case, each
          sub-directory is recursively browsed, but the root of
          the project is considered to be the sub-directory (see the
          example below).
        * Or the root directory contains files.  In this context,
          the root directory remains the root of the project.

        For instance:
          If you have the following directory structure:
            example/
                features/
                    fist.feature
                    second.feature
                steps/
                    first.py
                    second.py
          Then the step in 'example/steps/first.py' will be stored in
          the 'first' module (example and steps are not included).
          But if you have the following directory structure:
            example/
                fist.feature
                second.feature
                first.py
                second.py
          Then the root directory will be 'example'.

        """
        # If the root directory only contains sub-directory
        if all(os.path.isdir(os.path.join(root, name)) for name in \
                os.listdir(root)):
            min_depth = 2
        else:
            min_depth = 1

        self.load_directory(root, min_depth)

    def load_directory(self, directory, min_depth):
        """Recursively load a directory and its content.

        This method is automatically called by the 'load' method and
        should not be called directly by the user.  Its role is to be
        consistent with the structure of the root directory (which is
        analyzed in the 'load' method).

        """
        for file in os.listdir(directory):
            path = os.path.join(directory, file)
            if file.endswith(".py"):
                self.load_steps(path, min_depth)
            elif file.endswith(".feature"):
                self.load_stories(path, min_depth)
            elif os.path.isdir(path):
                self.load_directory(path, min_depth)

    def load_stories(self, path, min_depth):
        with open(path, "r") as file:
            content = file.read()

        story = Story.parse(path, content)
        name = os.path.basename(path)[:-8]
        basename = self.get_base_name(path, min_depth)
        id_name = basename and basename + "." + name or name
        self.stories[id_name] = story

    def load_steps(self, path, min_depth):
        dir_name = os.path.dirname(path)
        basename = self.get_base_name(path, min_depth)
        name = os.path.basename(path)[:-3]
        package = dir_name.replace(os.path.sep, ".")
        module_name = package and package + "." + name or name
        id_name = basename and basename + "." + name or name
        module = importlib.import_module(module_name)
        classes = [value for value in module.__dict__.values() if \
                getattr(value, "croissant_path", None) == "unknown"]
        if len(classes) == 0:
            print("Not found")
            return
        elif len(classes) > 1:
            raise ValueError("multiple steps defined in the same file, it seems")
        else:
            class_object = classes[0]

        class_object.croissant_path = id_name
        self.classes[id_name] = class_object

    def run_story(self, name):
        """Run the specified story."""
        story = self.stories[name]
        for scenario in story.scenarios:
            self.run_scenario(name, scenario)

    def run_scenario(self, story_name, scenario):
        """Run the specified scenario."""
        # Create the step for this scenario
        class_object = self.classes[story_name]
        step = class_object(scenario)

        # Call the contexts
        for context in scenario.contexts:
            method_name = self.find_expression(class_object.contexts,
                    scenario, context)
            getattr(step, method_name)(context)

        # Call the event
        method_name = self.find_expression(class_object.events,
                scenario, scenario.event)
        getattr(step, method_name)(scenario.event)

        # Call the postconditions
        for postcondition in scenario.postconditions:
            method_name = self.find_expression(class_object.postconditions,
                    scenario, postcondition)
            getattr(step, method_name)(postcondition)

    @staticmethod
    def find_expression(expressions, scenario, message):
        for expression, method_name in expressions.items():
            if expression.search(message):
                return method_name

        raise StepNotFound(scenario, message)

    @staticmethod
    def get_base_name(path, min_depth):
        """Return the path's name without the root directory."""
        dirs = path.split(os.path.sep)
        if len(dirs) < min_depth + 1:
            raise ValueError("Invalid directory")

        del dirs[-1]
        for i in range(min_depth):
            del dirs[0]

        return ".".join(dirs)

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


"""Module containing the Scenario class, described below."""

from language.keyword import keywords
from organization.block import Block

class Scenario:

    """Class representing a simple scenarios contained in a story.

    A scenario has:
        title -- a simple title
        contexts -- lines of context
        event -- the event triggering the test
        postconditions -- lines of postcondition.

    """

    def __init__(self, title, father=None):
        self.title = title
        self.father = father
        self.contexts = []
        self.event = ""
        self.postconditions = []

    def __repr__(self):
        path = self.father and self.father.path or "[undefined]"
        return "<Scenario (title={} from path={})>".format(
                repr(self.title), path)

    @property
    def path(self):
        """Return the father's path, if found."""
        return self.father and self.father.path or "[undefined]"

    @classmethod
    def parse(cls, block, father=None):
        """Parse a block and create the corresponding scenario.

        This method expects a block as a first argument.  Therefore,
        some content (like a file) was parsed before.

        """
        scenario = cls("unknown", father)
        if not block:
            raise ValueError("the block is empty")

        # The title is the first line off the scenario
        scenario.extract_title(block)

        # We work inside the sub-block
        try:
            block = block[1]
        except IndexError:
            raise ValueError("the scenario doesn't have a proper definition")

        # The first line of this block should be a context
        # 'given something...'
        scenario.extract_contexts(block)
        scenario.extract_event(block)
        scenario.extract_postconditions(block)
        return scenario

    def extract_title(self, block):
        """Extract the title from a block."""
        title = block[0].display(indentation=False)
        keyword = keywords["scenario.title"]
        symbol = "en"
        title = keyword.parse(symbol, title)
        if title is None:
            raise MissingKeyword("the {} keyword should be the " \
                    "first line of the scenario ({}:{})".format(
                    repr(keyword.languages[symbol]),
                    repr(scenario.path), block.start_at))

        self.title = title

    def extract_contexts(self, block, symbol="en"):
        """Extract the contexts from a block."""
        given = keywords["scenario.given"]
        context = given.parse(symbol, block[0].display(indentation=False))
        if context is None:
            raise MissingKeyword("the {} keyword should be the " \
                    "first line of the scenario ({}:{})".format(
                    repr(keyword.languages[symbol]),
                    repr(scenario.path), block.start_at))

        contexts = [context]
        still = True
        i = 1
        while still:
            try:
                line = block[i].display(indentation=False)
            except IndexError:
                break

            keyword = keywords["scenario.and"]
            context = keyword.parse(symbol, line)
            if context:
                contexts.append(context)
                i += 1
            else:
                break


        self.contexts = contexts

    def extract_event(self, block, symbol="en"):
        """Extract the contexts from a block."""
        block = block[len(self.contexts)]
        keyword = keywords["scenario.when"]
        event = keyword.parse(symbol, block[0].display(indentation=False))
        if event is None:
            raise MissingKeyword("the {} keyword should be the " \
                    "first line of the scenario ({}:{})".format(
                    repr(keyword.languages[symbol]),
                    repr(scenario.path), block.start_at))

        self.event = event

    def extract_postconditions(self, block, symbol="en"):
        """Extract the postconditions of a block."""
        block = block[len(self.contexts) + 1]
        keyword = keywords["scenario.then"]
        condition = keyword.parse(symbol, block[0].display(indentation=False))
        if condition is None:
            raise MissingKeyword("the {} keyword should be the " \
                    "first line of the scenario ({}:{})".format(
                    repr(keyword.languages[symbol]),
                    repr(scenario.path), block.start_at))

        conditions = [condition]
        still = True
        i = 1
        while still:
            try:
                line = block[i].display(indentation=False)
            except IndexError:
                break

            keyword = keywords["scenario.and"]
            condition = keyword.parse(symbol, line)
            if condition:
                conditions.append(condition)
                i += 1
            else:
                break

        self.postconditions = conditions

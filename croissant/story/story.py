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


"""Module containing the Story class, described below."""

from language.exceptions.syntax import *
from language.keyword import keywords
from organization.block import Block
from story.scenario import Scenario

class Story:

    """Class representing a simple story containing scenarios.

    A story is most likely a file with a specific structure.  It has:
        title -- the story's title
        description -- the story's description
        scenarios -- a list of scenarios defined in this story

    The definition of this structure is explained in more details
    in the 'language.story' module.

    """

    def __init__(self, path="[undefined]", father=None):
        self.path = path
        self.father = father
        self.title = "not set"
        self.description = "not set"
        self.scenarios = []

    def __repr__(self):
        return "<Story (path={})>".format(self.path)

    @property
    def name(self):
        """Return the file part of the path."""
        return os.path.basename(self.path)

    def add_scenario(self, scenario):
        """Add a new scenario to the story."""
        self.scenarios.append(scenario)
        scenario.father = self

    def remove_scenario(self, scenario):
        """Remove the scenario from the story."""
        self.scenarios.remove(scenario)
        scenario.father = None

    @classmethod
    def parse(cls, path, content, father=None):
        """Parse a file and create the corresponding story.

        The path should be the path leading to the story file.
        If mentioned, the father argument should be the story set
        that will add this story when it will be parsed.

        """
        story = cls(path=path, father=father)
        block = Block.build(content)

        # The first line should contain the title
        if len(block) == 0:
            # The file is empty
            raise EmptyFile("the story file {} is empty".format(
                    repr(path)))

        try:
            block_title = block[0]
        except IndexError:
            raise MissingKeyword("the {} keyword should be the " \
                    "first line of your {} file".format(
                    repr(keyword.languages[symbol]), repr(file)))

        symbol = "en"
        title = block_title.display(indentation=False)
        keyword = keywords["story.title"]
        story.title = keyword.parse(symbol, title)
        if story.title is None:
            raise MissingKeyword(path, block.start_at + 1, symbol, keyword)

        # The description should be slightly indented then (2nd block)
        try:
            description_block = block[1]
        except IndexError:
            raise StructureError("the descrption couldn't be read " \
                    "from {}".format(repr(path)))

        story.description = description_block.display(indentation=False)
        scenario_blocks = block[2:]
        title = None
        for sub_block in scenario_blocks:
            if title:
                title._children.append(sub_block)
                scenario = Scenario.parse(title, story)
                story.add_scenario(scenario)
                title = None
            else:
                title = sub_block

        return story

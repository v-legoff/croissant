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


"""Module containing the tests for the block object."""

import unittest

from croissant.organization.block import Block
from croissant.tests.organization.contents import *

class BlockTest(unittest.TestCase):

    """Class to test (with unittest) the behavior of the Block object.

    The following checks are done:
        nb_lines -- given a content, is the number of lines valid?

    """

    def test_nb_lines(self):
        """Test that the number of lines of a given content is consistent."""
        content = CONTENT_WITHOUT_INDENTATION
        block = Block.build(content)
        self.assertEqual(block.nb_lines, len(content.splitlines()))

    def test_sub_blocks(self):
        """Test that an indented content creates sub-blocks."""
        content = CONTENT_WITH_INDENTATION
        block = Block.build(content)
        self.assertEqual(len(block), 5)
        self.assertEqual(block[0], "We now try a different content")
        self.assertEqual(block[3][2], "Let's try it")

    def test_hierarchy(self):
        """Test the hierarchy consistence, parent, children and siblings."""
        content = CONTENT_WITH_INDENTATION
        block = Block.build(content)
        self.assertIs(block[0].parent, block)
        self.assertIs(block[1], block[0].next)
        self.assertIs(block[1].previous, block[0])
        self.assertIs(block[3][0].next, block[3][1])
        self.assertIs(block[3][0], block[3][1].previous)

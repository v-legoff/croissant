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


"""Module containing the Block class, described below."""

class Block:

    """A block of text built by indentation level.

    A block object is a block of text.  It could contain only one line of text, a few lines of text or even sub-blocks.  If a block is a container, it contains other blocks that may contain only one line of text.

    The block structure is recursively created based on content indentation.  Take for instance this content:
        <beginning of text>
        Here is a line,
        That is not indented
          But this one is slightly indented
          That one too
            And this one is more indented than ever
        The first block continues on...
        <end of text>

    This little example would create:
    *   A block object that will contain:
        *   A block of one line ('Here is a line,')
        *   Another one ('That is not indented')
        *   A sub-block that will contain:
            *   A block with one line of text ('But this one...')
            *   ...
        *   And finally the last block with one line.

    The indentation marker is not important:  spaces or tabulations
    could be used (not in the same content, though) and a number of
    each is the user's choice.

    To build a hierarchy of blocks based on a content (string), use
    the 'build' class method.

    Once the hierarchy is created, you can manipulate each contained
    blocks using the standard methods:
        __getitem__ to select a sub-block (always a Block object)
        __iter__ to browse a block
        __len__ to know how long is the block

    Additional properties are provided:
        start_at -- the line number where the block starts
        end_at -- the line number at which the block ends.

    """

    @staticmethod
    def get_indentation_from_line(line, indentation):
        """Return the found indentation."""
        if not indentation:
            if line.startswith("\t"):
                symbole = "\t"
            elif line.startswith(" "):
                symbole = " "
            else:
                return ""
        else:
            symbole = indentation[0]

        i = 0
        while i < len(line) and line[i] == symbole:
            i += 1

        return symbole * i

    @classmethod
    def build(cls, content, start_at=0, indentation=""):
        """Build a hierarchy of blocks based on the specified content.

        The content must be a string, for instance extracted from
        a file.  Each line is:
        *   Of the same indentation as the previous one.  In this case,
            a new block with this line is simply added to the current
            block.
        *   Of a sub-level of indentation.  In this case, a new block is
            built based on this level of indentation.

        """
        block = cls()
        block.start_at = start_at
        block.indentation = indentation
        i = 0
        lines = content.splitlines()
        while i < len(lines):
            try:
                line = lines[i]
            except IndexError:
                break

            line_indentation = Block.get_indentation_from_line(line,
                    indentation)
            if line.strip() == "":
                i += 1
            elif line_indentation == indentation:
                sub_block = Block()
                line = line[len(indentation):]
                sub_block._children.append(line)
                sub_block.start_at = start_at + i
                sub_block.indentation = line_indentation
                block._children.append(sub_block)
                i += 1
            elif len(line_indentation) > len(indentation):
                sub_content = "\n".join(lines[i:])
                sub_block = Block.build(sub_content, start_at=start_at + i,
                        indentation=line_indentation)
                block._children.append(sub_block)
                i += sub_block.nb_lines
            else:
                break

        previous = None
        for child in block._children:
            child.parent = block
            child.previous = previous
            if previous is not None:
                previous.next = child
            previous = child

        return block

    def __init__(self):
        self._children = []
        self.start_at = -1
        self.indentation = ""
        self.parent = None
        self.previous = None
        self.next = None

    def __len__(self):
        return len(self._children)

    def __getitem__(self, item):
        lines = list(self._children)
        line = None
        try:
            line = lines[item]
        except IndexError:
            pass

        if line and isinstance(line, str):
            block = Block()
            block.start_at = self.start_at
            block.parent = self
            block._children = [line]
            return block

        return self._children[item]

    def __iter__(self):
        for child in self._children:
            yield child

    def __repr__(self):
        if len(self._children) == 1:
            return "<Block with 1 child>"
        else:
            return "<Block with {} children>".format(len(self._children))

    def __str__(self):
        return self.display(show_lines=True)

    def __eq__(self, compared_to):
        """Compare the block to some content.

        This content can be:
            A string
            Another block

        """
        if isinstance(compared_to, Block):
            compared_to = compared_to.display(indentation=False)
        elif isinstance(compared_to, str):
            pass
        else:
            raise TypeError("cannot compare {} to {}".format(
                    self, compared_to))

        return self.display(indentation=False) == compared_to

    @property
    def nb_lines(self):
        """Return the number of lines contained in this block.

        This property is recusrive:  each block can contain sub-blocks that can contain sub-sub-blocks ans so on.

        """
        nb = 0
        for line in self._children:
            if isinstance(line, str):
                nb += 1
            else:
                nb += line.nb_lines

        return nb

    @property
    def end_at(self):
        """Return the line where the block should end."""
        return self.start_at + self.nb_lines

    def display(self, show_lines=False, indentation=True):
        """Display this block and its children."""
        res = ""
        i = 0
        nb_lines = self.nb_lines
        for line in self:
            if i != 0 and nb_lines > 1:
                res += "\n"

            if isinstance(line, str):
                if show_lines:
                    res += str(self.start_at + i + 1).rjust(2) + " "

                if indentation:
                    res += self.indentation

                res += line
            else:
                res += line.display(show_lines=show_lines, indentation=indentation)

            i += 1

        return res

    def insert(self, child):
        """Insert the child at the beginnning of the block.

        If the child is a block itself, the 'start_at' attribute is
        set to the new child.  If not, the start_at is simply decreased.

        """
        if isinstance(child, Block):
            start_at = child.start_at
        else:
            start_at = self.start_at - 1

        self._children.insert(0, child)
        self.start_at = start_at

    def append(self, child):
        """Append a child."""
        self._children.append(child)

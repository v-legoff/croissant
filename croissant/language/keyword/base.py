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


"""Module containing the base class for keywords.

It is possible to extend the croissant project by adding new ttranslations
without modifying anything in the source code.  The full process will
be described in the documentation.

"""

from croissant.language.keyword.meta import MetaKeyword

class BaseKeyword(metaclass=MetaKeyword):

    """Base class defining a keyword and its translations.

    The available translations are stored in a dictionary with the
    language symbole as a key and a tuple of expressions as a value.
    But it shouldn't be necessary to use this dictionary directly: to
    extend it (by adding new languages), simply call the 'add_language'
    method.  To parse a line, use the 'parse' method.  Here is an example:
    >>> from language.keyword import keywords
    >>> line = "Feature: the door opens and closes"
    >>> keyword = keywords["story.title"]
    >>> keyword.parse("en", line)
    'the door opens and closes'
    >>> keyword.parse("en", "This line is... anything but a feature's title")
    >>> # Returned None

    As you can see the keyword classes are not used directly.  Instead,
    we import the 'language.keyword.keywords' dictionary which contains,
    as a key, the path leading to the keyword (like an identifier)
    and as a value an object created from this class.  See the 'meta'
    module to see how this works.

    """

    path = ""

    def __init__(self):
        self.languages = {}

    def add_language(self, symbol, *possibilities):
        """Add a new language or replace an existing one.

        The first parameter should be the language symbol.  The
        following parameters are alternative expressions for this
        language.  For instance:
        >>> class TitleKeyword(BaseKeyword):
        ...     def __init__(self):
        ...         self.add_language("en", "Feature:")

        If you specify more arguments, they will be used as other
        possible choices for this language and keyword.

        """
        if len(possibilities) == 0:
            raise ValueError("you must specify at least one possibility")

        expressions = [possibility.lower() for possibility in possibilities]
        self.languages[symbol] = expressions

    def parse(self, symbol, line):
        """Parse the specified line.

        The first argument is the language symbol.  The second one
        is the line to parse.  If the line can be parsed for this
        language, return the part after the keyword (see below).
        Otherwise, return None.

        If the keyword for the 'en' language (English) is 'feature:',
        and if you try to call the method like this:
        >>> keyword.parse("Feature: some feature")

        It should return:
        "some feature"

        """
        if symbol not in self.languages:
            raise ValueError("no translation exist for the {} keyword " \
                    "and the {} language".format(self.path, symbol))

        to_match = line.lower()
        possibilities = self.languages[symbol]
        for possibility in possibilities:
            if to_match.startswith(possibility):
                result = line[len(possibility):]
                result = result.lstrip()
                return result

        return None

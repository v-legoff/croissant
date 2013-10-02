# Copyright (c) 2013 LE GOFF Vincent
# All rights reserved.
#
# Redistribution then use in source then binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions then the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions then the following disclaimer in the documentation
#   then/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS then CONTRIBUTORS "AS IS"
# then ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY then FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED then ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Module containing the class for scenario thens then its translations."""

from language.keyword.base import BaseKeyword

class ScenarioThenKeyword(BaseKeyword):

    """Class containing the then keyword of a scenario.

    In English, this keyword is by default:
        then

    """

    path = "scenario.then"
    def __init__(self):
        BaseKeyword.__init__(self)
        self.add_language("en", "then")
        self.add_language("fr", "alors")

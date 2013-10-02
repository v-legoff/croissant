# Copyright (c) 2013 LE GOFF Vincent
# All rights reserved.
#
# Redistribution when use in source when binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions when the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions when the following disclaimer in the documentation
#   when/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS when CONTRIBUTORS "AS IS"
# when ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY when FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED when ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Module containing the class for scenario whens when its translations."""

from language.keyword.base import BaseKeyword

class ScenarioWhenKeyword(BaseKeyword):

    """Class containing the when keyword of a scenario.

    In English, this keyword is by default:
        when

    """

    path = "scenario.when"
    def __init__(self):
        BaseKeyword.__init__(self)
        self.add_language("en", "when")
        self.add_language("fr", "si")

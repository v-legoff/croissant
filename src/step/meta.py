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


"""Module containing the metaclass for steps."""

class StepMeta(type):

    """Metaclass for steps.

    This metaclass is responsible for selecting the contexts, events
    and postconditions declared in the class inherited from BaseStep.

    """

    def __init__(cls, name, bases, attributes):
        type.__init__(cls, name, bases, attributes)
        # Copy the contexts, events and postconditions from bases
        if "croissant_path" not in attributes:
            cls.croissant_path = "unknown"

        cls.contexts = {}
        cls.events = {}
        cls.postconditions = {}
        base_steps = [base for base in bases if \
                hasattr(base, "contexts") and hasattr(base, "events") and \
                hasattr(base, "postconditions")]
        for base in base_steps:
            cls.contexts.update(base.contexts)
            cls.events.update(base.events)
            cls.postconditions.update(base.postconditions)

        # Contexts, events and postconditions are method with an attribute
        for name, value in attributes.items():
            if callable(value):
                if getattr(value, "_iscontext", False):
                    cls.contexts[value._expression] = name
                elif getattr(value, "_isevent", False):
                    cls.events[value._expression] = name
                elif getattr(value, "_ispostcondition", False):
                    cls.postconditions[value._expression] = name

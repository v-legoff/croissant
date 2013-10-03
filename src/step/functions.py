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


"""Module containing step functions (and decorators).

This module contains different decorators that are useful to
specify class methods as step contexts, events and postconditions.

"""

import re

def context(expression):
    """Decorator to mark a method as a context.

    Usage example:
        class Step(BaseStep):
            @context("a precondition")
            def method(self):
                ...

    """
    expression = re.compile(expression)
    def decorator(method):
        def call_context(self, context):
            res = expression.search(context)
            if res:
                args = res.groups()
            else:
                raise ValueError("Invalid expression: {}".format(
                        repr(context)))

            return method(self, *args)
        call_context._iscontext = True
        call_context._expression = expression
        return call_context
    return decorator

def event(expression):
    """Decorator to mark a method as an event.

    Usage example:
        class Step(BaseStep):
            @event("something happens")
            def method(self):
                ...

    """
    expression = re.compile(expression)
    def decorator(method):
        def call_event(self, event):
            res = expression.search(event)
            if res:
                args = res.groups()
            else:
                raise ValueError("Invalid expression: {}".format(
                        repr(event)))

            return method(self, *args)
        call_event._isevent = True
        call_event._expression = expression
        return call_event
    return decorator

def postcondition(expression):
    """Decorator to mark a method as a postcondition.

    Usage example:
        class Step(BaseStep):
            @postcondition("a postcondition")
            def method(self):
                ...

    """
    expression = re.compile(expression)
    def decorator(method):
        def call_postcondition(self, postcondition):
            res = expression.search(postcondition)
            if res:
                args = res.groups()
            else:
                raise ValueError("Invalid expression: {}".format(
                        repr(postcondition)))

            return method(self, *args)
        call_postcondition._ispostcondition = True
        call_postcondition._expression = expression
        return call_postcondition
    return decorator

"""
Copyright (c) 2016 Keith Sterling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging

from programy.parser.exceptions import ParserException
from programy.parser.pattern.nodes.base import PatternNode
from programy.parser.pattern.nodes.root import PatternRootNode


class PatternWordNode(PatternNode):

    def __init__(self, word):
        PatternNode.__init__(self)
        self._word = word

    def is_word(self):
        return True

    @property
    def word(self):
        return self._word

    def can_add(self, new_node):
        if new_node.is_root():
            raise ParserException("Cannot add root node to child node")

    def equivalent(self, other):
        if other.is_word():
            if self._word == other.word:
                return True
        return False

    def equals(self, bot, clientid, word):
        return self.equals_ignore_case(bot, clientid, self._word, word)
        #if self.word == word:
        #    return True
        #return False

    def to_string(self, verbose=True):
        if verbose is True:
            return "WORD [%s] word=[%s]" % (self._child_count(verbose), self.word)
        else:
            return "WORD [%s]" % (self.word)


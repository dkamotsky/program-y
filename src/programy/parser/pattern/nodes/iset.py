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

from programy.parser.pattern.nodes.word import PatternWordNode


class PatternISetNode(PatternWordNode):

    def __init__(self, words):
        PatternWordNode.__init__(self, 'iset')
        self._words = []
        self._parse_words(words)

    def _parse_words(self, words):
        splits = words.split(",")
        for word in splits:
            self._words.append(word.strip().upper())

    @property
    def words(self):
        return self._words

    def is_set(self):
        return True

    def equivalent(self, other):
        # All isets are never equivalent, as they are inline and are unique regardless of set content
        return False

    def equals(self, bot, client, word):
        for set_word in self._words:
            if word == set_word:
                return True
        return False

    def to_string(self, verbose=True):
        words_str = ",".join(self._words)
        if verbose is True:
            return "ISET [%s] words=[%s]" % (self._child_count(verbose), words_str)
        else:
            return "ISET words=[%s]" % words_str


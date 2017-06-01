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

from programy.utils.text.text import TextUtils

from programy.parser.pattern.nodes.wildcard import PatternWildCardNode
from programy.parser.pattern.matcher import Match
from programy.parser.pattern.nodes.topic import PatternTopicNode
from programy.parser.pattern.nodes.that import PatternThatNode

class PatternZeroOrMoreWildCardNode(PatternWildCardNode):

    MATCH_CHARS = ['^', '#']

    def __init__(self, wildcard):
        PatternWildCardNode.__init__(self, wildcard)

    def is_zero_or_more(self):
        return True

    def matching_wildcards(self):
        return PatternZeroOrMoreWildCardNode.MATCH_CHARS

    @staticmethod
    def is_wild_card(text):
        return bool(text in PatternZeroOrMoreWildCardNode.MATCH_CHARS)

    def equivalent(self, other):
        if isinstance(other, PatternZeroOrMoreWildCardNode):
            if self._wildcard == other.wildcard:
                return True
        return False

    def to_string(self, verbose=True):
        if verbose is True:
            return "ZEROORMORE [%s] wildcard=[%s]" % (self._child_count(verbose), self.wildcard)
        else:
            return "ZEROORMORE [%s]" % (self.wildcard)

    def consume(self, bot, clientid, context, words, word_no, type, depth):

        tabs = TextUtils.get_tabs(word_no)

        if depth > context.max_search_depth:
            logging.error("%sMax search depth [%d]exceeded" % (tabs, context.max_search_depth))
            return None

        context_match = Match(type, self, None)
        context.add_match(context_match)
        matches_added = 1

        if self._0ormore_hash is not None:
            logging.debug("%sWildcard is next node, moving on!"%(tabs))
            match = self._0ormore_hash.consume(bot, clientid, context, words, word_no+1, type, depth+1)
            if match is not None:
                return match

        if self._1ormore_underline is not None:
            logging.debug("%sWildcard is next node, moving on!"%(tabs))
            match = self._1ormore_underline.consume(bot, clientid, context, words, word_no+1, type, depth+1)
            if match is not None:
                return match

        if self._0ormore_arrow is not None:
            logging.debug("%sWildcard is next node, moving on!"%(tabs))
            match = self._0ormore_arrow.consume(bot, clientid, context, words, word_no+1, type, depth+1)
            if match is not None:
                return match

        if self._1ormore_star is not None:
            logging.debug("%sWildcard is next node, moving on!"%(tabs))
            match = self._1ormore_star.consume(bot, clientid, context, words, word_no+1, type, depth+1)
            if match is not None:
                return match

        # TODO Add priority words first

        word = words.word(word_no)

        if len(self._children) > 0:
            for child in self._children:
                if child.equals(bot, clientid, word):
                    logging.debug ("%sWildcard child %s matched %s"%(tabs, child._word, word))

                    logging.debug("%s*MATCH -> %s" % (tabs, word))
                    context_match2 = Match(Match.WORD, child, word)
                    context.add_match(context_match2)
                    matches_added += 1

                    skip_to=self.consume_set_phrase(bot, clientid, context, child, context_match2, words, word_no)                
                    if skip_to is None:
                        continue
                    else:
                        word_no=skip_to

                    match = child.consume(bot, clientid, context, words, word_no+1, type, depth+1)
                    if match is not None:
                        return match

                    if word == PatternTopicNode.TOPIC :
                        logging.debug ("1 Found a topic at the wrong place....")
                        context.pop_matches(matches_added)
                        return None

                    if word == PatternThatNode.THAT:
                        logging.debug("Found a that at the wrong place....")
                        context.pop_matches(matches_added)
                        return None

            logging.debug("%sWildcard %s consumed %s" % (tabs, self._wildcard, word))

            logging.debug("%s*MATCH -> %s" % (tabs, word))
            context_match.add_word(word)

            match = super(PatternZeroOrMoreWildCardNode, self).consume(bot, clientid, context, words, word_no + 1, type, depth+1)
            if match is not None:
                return match

            word_no += 1
            word = words.word(word_no)

            if word == PatternTopicNode.TOPIC:
                logging.debug("2 Found a topic at the wrong place....")
                context.pop_matches(matches_added)
                return None

            if word == PatternThatNode.THAT:
                logging.debug("Found a that at the wrong place....")
                context.pop_matches(matches_added)
                return None

            logging.debug("%sWildcard %s consumed %s" % (tabs, self._wildcard, word))
            logging.debug("%s*MATCH -> %s" % (tabs, word))
            context_match.add_word(word)

            match = super(PatternZeroOrMoreWildCardNode, self).consume(bot, clientid, context, words, word_no + 1, type, depth+1)
            if match is not None:
                return match

            word_no += 1
            if word_no >= words.num_words():
                context.pop_matches(matches_added)
                return None
            word = words.word(word_no)

        logging.debug("%sNo children, consume words until next break point" % (tabs))
        while word_no < words.num_words() - 1:
            match = super(PatternZeroOrMoreWildCardNode, self).consume(bot, clientid, context, words, word_no, type, depth+1)
            if match is not None:
                return match

            if word == PatternTopicNode.TOPIC:
                logging.debug("3 Found a topic at the wrong place....")
                context.pop_matches(matches_added)
                return None

            if word == PatternThatNode.THAT:
                logging.debug("Found a that at the wrong place....")
                context.pop_matches(matches_added)
                return None

            logging.debug("%s*MATCH -> %s" % (tabs, word))
            context_match.add_word(word)

            word_no += 1
            word = words.word(word_no)
            logging.debug("%sWildcard %s consumed %s" % (tabs, self._wildcard, word))

        logging.debug("%sWildcard %s consumed %s" % (tabs, self._wildcard, word))

        match = super(PatternZeroOrMoreWildCardNode, self).consume(bot, clientid, context, words, word_no, type, depth+1)

        if match is not None:
            return match
        else:
            context.pop_matches(matches_added)
            return None

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
from programy.parser.exceptions import ParserException, DuplicateGrammarException
from programy.parser.pattern.factory import PatternNodeFactory
from programy.parser.pattern.nodes.root import PatternRootNode
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programy.parser.pattern.nodes.zeroormore import PatternZeroOrMoreWildCardNode

# TODO better handling of <html> type tags

#######################################################################################################################
#
class PatternGraph(object):

    def __init__(self, root_node=None, pattern_factory=None):
        if root_node is None:
            logging.debug("Defaulting root to PatternRootNode")
            self._root_node = PatternRootNode()
        else:
            if root_node.is_root() is False:
                raise ParserException("Root node needs to be of base type PatternRootNode")
            self._root_node = root_node

        if pattern_factory is None:
            logging.debug("Defaulting node factory to PatternNodeFactory")
            self._pattern_factory = PatternNodeFactory()
            self._pattern_factory.load_nodes_config_from_file("dummy_config.conf")
        else:
            if isinstance(pattern_factory, PatternNodeFactory) is False:
                raise ParserException("Pattern factory needs to be base class of PatternNodeFactory" )
            self._pattern_factory = pattern_factory

    @property
    def root(self):
        return self._root_node

    def node_from_text(self, word):
        if word.startswith("$"):
            node_class = self._pattern_factory.new_node_class('priority')
            return node_class(word[1:])
        elif PatternZeroOrMoreWildCardNode.is_wild_card(word):
            node_class = self._pattern_factory.new_node_class('zeroormore')
            return node_class(word)
        elif PatternOneOrMoreWildCardNode.is_wild_card(word):
            node_class = self._pattern_factory.new_node_class('oneormore')
            return node_class(word)
        else:
            node_class = self._pattern_factory.new_node_class('word')
            return node_class(word)

    def node_from_element(self, element):

        node_name = element.tag
        if self._pattern_factory.exists(node_name) is False:
            raise ParserException ("Unknown node name [%s]"%node_name)

        node_instance = self._pattern_factory.new_node_class(node_name)
        if 'name' in element.attrib:
            return node_instance(element.attrib['name'])
        else:
            return node_instance(TextUtils.strip_whitespace(element.text))

    def _parse_text(self, pattern_text, current_node):

        stripped = pattern_text.strip()
        words = stripped.split(" ")
        for word in words:
            if word != '': # Blank nodes add no value, ignore them
                word = TextUtils.strip_whitespace(word)

                new_node = self.node_from_text(word)

                current_node = current_node.add_child(new_node)

        return current_node

    def get_text_from_element(self, element):
        text = element.text
        if text is not None:
            text = TextUtils.strip_whitespace(text)
            if text == "":
                return None
            return text
        return None

    def get_tail_from_element(self, element):
        text = element.tail
        if text is not None:
            text = TextUtils.strip_whitespace(text)
            if text == "":
                return None
            return text
        return None

    def add_pattern_to_node(self, pattern_element):
        try:

            head_text = self.get_text_from_element(pattern_element)
            if head_text is not None:
                current_node = self._parse_text(head_text, self._root_node)
            else:
                current_node = self._root_node

            for sub_element in pattern_element:
                new_node = self.node_from_element(sub_element)
                current_node = current_node.add_child(new_node)

                tail_text = self.get_tail_from_element(sub_element)
                if tail_text is not None:
                    current_node = self._parse_text(tail_text, current_node)

            return current_node

        except ParserException as parser_excep:
            parser_excep._xml_element = pattern_element
            raise parser_excep

    def add_topic_to_node(self, topic_element, base_node):
        try:

            current_node = self._pattern_factory.new_node_class('topic')()
            current_node = base_node.add_topic(current_node)

            head_text = self.get_text_from_element(topic_element)
            if head_text is not None:
                current_node = self._parse_text(head_text, current_node)

            added_child = False
            for sub_element in topic_element:
                new_node = self.node_from_element(sub_element)
                current_node = current_node.add_child(new_node)

                tail_text = self.get_tail_from_element(sub_element)
                if tail_text is not None:
                    current_node = self._parse_text(tail_text, current_node)
                added_child = True

            if head_text is None:
                if added_child is False:
                    raise ParserException("Topic node text is empty", xml_element=topic_element)

            return current_node

        except ParserException as parser_excep:
            parser_excep._xml_element = topic_element
            raise parser_excep

    def add_that_to_node(self, that_element, base_node):
        try:

            current_node = self._pattern_factory.new_node_class('that')()
            current_node = base_node.add_that(current_node)

            head_text = self.get_text_from_element(that_element)
            if head_text is not None:
                current_node = self._parse_text(TextUtils.strip_whitespace(head_text), current_node)

            added_child = False
            for sub_element in that_element:
                new_node = self.node_from_element(sub_element)
                current_node = current_node.add_child(new_node)

                tail_text = self.get_tail_from_element(sub_element)
                if tail_text is not None:
                    current_node = self._parse_text(tail_text, current_node)
                added_child = True

            if head_text is None:
                if added_child is False:
                    raise ParserException("That node text is empty", xml_element=that_element)

            return current_node

        except ParserException as parser_excep:
            parser_excep._xml_element = that_element
            raise parser_excep

    def add_template_to_node(self, template_graph_root, current_node):
        template_node = self._pattern_factory.new_node_class('template')(template_graph_root)
        current_node = current_node.add_child(template_node)
        return current_node

    def add_pattern_to_graph(self, pattern_element, topic_element, that_element, template_graph_root):

        current_node = self.add_pattern_to_node(pattern_element)

        current_node = self.add_topic_to_node(topic_element, current_node)

        current_node = self.add_that_to_node(that_element, current_node)

        if current_node.has_template():
            raise DuplicateGrammarException("Dupicate grammar tree found [%s]"%(pattern_element.text))
        else:
            self.add_template_to_node(template_graph_root, current_node)

    def count_words_in_patterns(self):
        counter = [0]
        self._count_words_in_children(self._root_node, counter)
        return counter[0]

    def _count_words_in_children(self, node, counter):
        for child in node.children:
            counter[0] += 1
            self._count_words_in_children(child, counter)

    def dump(self, output_func=logging.debug, eol="", verbose=True):
        self.root.dump("", output_func, eol, verbose)
        output_func("")

    def dump_to_file(self, filename):
        with open(filename, "w+") as dump_file:
            self.dump(output_func=dump_file.write, eol="\n")
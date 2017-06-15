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
import os
from abc import ABCMeta, abstractmethod

from programy.utils.classes.loader import ClassLoader

class NodeFactory(object):
    __metaclass__ = ABCMeta

    def __init__(self, type):
        self._nodes_config = {}
        self._type = type

    @abstractmethod
    def default_config_file(self):
        raise NotImplementedError()

    def process_config_line(self, line):
        if self.valid_config_line(line):
            splits = line.split("=")
            node_name = splits[0].strip()
            if node_name in self._nodes_config:
                logging.error("Node already exists in config [%s]"%line)
                return
            class_name = splits[1].strip()
            logging.debug("Pre-instantiating %s Node [%s]"%(self._type, class_name))
            self._nodes_config[node_name] =  ClassLoader.instantiate_class(class_name)

    def valid_config_line(self, line):

        if len(line) == 0:
            logging.error ("Config line empty")
            return False

        if line.startswith('#'):
            logging.error ("Config line is comment")
            return False

        if "=" not in line:
            logging.error ("Config line missing '=' [%s]"%line)
            return False

        return True

    def load_nodes_config_from_file(self, filename):
        try:
            if os.path.exists(filename) is False:
                filename = self.default_config_file()

            with open(filename, "r+") as node_file:
                for line in node_file:
                    line = line.strip()
                    self.process_config_line(line)

        except Exception as e:
            logging.error("Failed to load %s Node Factory config file [%s]"%(self._type, filename))
            logging.exception(e)

    def load_nodes_config_from_text(self, text):
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            self.process_config_line(line)

    def exists(self, node_name):
        return node_name in self._nodes_config

    def new_node_class(self, name):
        if name not in self._nodes_config:
            raise Exception("Invalid node name [%s]"% name)
        return self._nodes_config[name]


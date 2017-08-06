"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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

from programy.config.base import BaseConfigurationData


class BrainNodesConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, "nodes")
        self._pattern_nodes = None
        self._template_nodes = None

    @property
    def pattern_nodes(self):
        return self._pattern_nodes

    @property
    def template_nodes(self):
        return self._template_nodes

    def load_config_section(self, file_config, bot_config, bot_root):
        nodes = file_config.get_section("nodes", bot_config)
        if nodes is not None:
            pattern_nodes = file_config.get_option(nodes, "pattern_nodes", missing_value=None)
            if pattern_nodes is not None:
                self._pattern_nodes = self.sub_bot_root(pattern_nodes, bot_root)
            template_nodes = file_config.get_option(nodes, "template_nodes", missing_value=None)
            if template_nodes is not None:
                self._template_nodes = self.sub_bot_root(template_nodes, bot_root)
        else:
            logging.warning("'nodes' section missing from bot config, using to defaults")
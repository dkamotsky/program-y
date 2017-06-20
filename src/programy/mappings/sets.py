"""
Copyright(c) 2016 Keith Sterling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files(the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging
import json
from programy.utils.files.filefinder import FileFinder

def add_prefixes(set_dict):
    prefix_dict={}
    for k in set_dict.keys():
        if isinstance(k, tuple):
            for i in range(1, len(k)):
                r=k[0:-i]
                r=r[0] if len(r)==1 else r
                if not r in set_dict:
                    prefix_dict[r]=False
    set_dict.update(prefix_dict)         

class SetLoader(FileFinder):
    def __init__(self):
        FileFinder.__init__(self)

    def load_file_contents(self, filename):
        logging.debug("Loading set [%s]", filename)
        the_set = {}
        try:
            with open(filename, 'r', encoding='utf8') as my_file:
                tuple_list=json.load(my_file)
            for tup in tuple_list:
                self.process_line(" ".join(tup), the_set)
        except Exception as excep:        
            logging.warn("Failed to load set [%s] as JSON, will retry in the old style. %s", filename, excep)
            try:
                with open(filename, 'r', encoding='utf8') as my_file:
                    for line in my_file:
                        self.process_line(line, the_set)
            except Exception as excep:
                logging.error("Failed to load set [%s] - %s", filename, excep)
        add_prefixes(the_set)
        logging.debug("Loaded set [%s]. Full contents: \n%s", filename, the_set)
        return the_set

    def load_from_text(self, text):
        the_set = {}
        lines = text.split("\n")
        for line in lines:
            self.process_line(line, the_set)
        return the_set

    def process_line(self, line, the_set):
        text = line.strip()
        if text is not None and len(text) > 0:
            key=tuple(text.upper().split())
            the_set[key[0] if len(key)==1 else key] = True


class SetCollection(object):

    def __init__(self):
        self._sets = {}

    def add_list_to_set(self, name, set_contents):
        # Set names always stored in upper case to handle ambiquity
        set_name = name.upper()
        if set_name in self._sets:
            raise Exception("Set %s already exists" % set_name)
        logging.debug("Adding set [%s[ to set group", set_name)
        new_set = {}
        for word in set_contents:
            new_set[word.upper()] = word
        self._sets[set_name] = new_set

    def set(self, name):
        # Set names always stored in upper case to handle ambiquity
        set_name = name.upper()
        return self._sets[set_name]

    def contains(self, name):
        # Set names always stored in upper case to handle ambiquity
        set_name = name.upper()
        return bool(set_name in self._sets)

    def count_words_in_sets(self):
        count = 0
        for aset in self._sets.values():
            count += len(aset)
        return count

    def load(self, configuration):
        loader = SetLoader()
        self._sets = loader.load_dir_contents(configuration.files, configuration.directories, configuration.extension)
        return len(self._sets)

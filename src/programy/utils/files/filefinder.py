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

class FileFinder(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def load_file_contents(self, filename):
        """
        Never Implemented
        """

    def find_files(self, path, subdir=False, extension=None):
        found_files = []
        if subdir is False:
            paths = os.listdir(path)
            for filename in paths:
                if filename.endswith(extension):
                    found_files.append((filename, os.path.join(path, filename)))
        else:
            for dirpath, _, filenames in os.walk(path):
                for filename in [f for f in filenames if f.endswith(extension)]:
                    found_files.append((filename, os.path.join(dirpath, filename)))

        return found_files

    def get_just_filename_file(self, file):
        if "." in file[0]:
            filename = file[0].split(".")[0]
        else:
            filename = file[0]
        return filename.upper()

    def load_dir_contents(self, path_to_sets, subdir=False, extension=".txt"):

        files = self.find_files(path_to_sets, subdir, extension)

        collection = {}
        for file in files:
            just_filename = self.get_just_filename_file(file)

            try:
                collection[just_filename] = self.load_file_contents(file[1])
            except Exception as e:
                logging.error ("Failed to load file contents for file [%s]. Exception %s.", file[1], e)

        return collection

    def get_just_filename_from_filename(self, filename):

        sections = filename.split(os.sep)
        last_section = sections[-1]
        if "." in last_section:
            filename = last_section.split(".")[0]
        else:
            filename = last_section
        return filename

    def load_single_file_contents(self, filename):

        just_filename = self.get_just_filename_from_filename(filename)

        collection = {}
        try:
            collection[just_filename] = self.load_file_contents(filename)
        except Exception as e:
            logging.error ("Failed to load file contents for file [%s]. Exception %s.", filename, e)

        return collection

#! /usr/local/bin/python

#
# noweb.py
# By Jonathan Aquino (jonathan.aquino@gmail.com)
#
# This program extracts code from a literate programming document in "noweb" format.
# It was generated from noweb.py.txt, itself a literate programming document.
# For more information, including the original source code and documentation,
# see http://jonaquino.blogspot.com/2010/04/nowebpy-or-worlds-first-executable-blog.html
#

import re

OPEN = "<<"
CLOSE = ">>"

class Document(object):
    def __init__(self, document):
        self.chunks = self._parse_chunks(document)

    def _parse_chunks(self, document):
        chunk_name = None
        chunks = {}
        for line in document.split('\n'):
            match = re.match(OPEN + "([^>]+)" + CLOSE + "=", line)
            if match:
                chunk_name = match.group(1)
                # If chunk_name exists in chunks, then we'll just add to the existing chunk.
                if not chunk_name in chunks:
                    chunks[chunk_name] = []
            else:
                match = re.match("@", line)
                if match:
                    chunk_name = None
                elif chunk_name:
                    chunks[chunk_name].append(line)

        return chunks

    def _expand(self, chunks, chunkName, indent=""):
        indent = ""
        chunkLines = chunks[chunkName]
        expanded_chunk_lines = []
        for line in chunkLines:
            match = re.match("(\s*)" + OPEN + "([^>]+)" + CLOSE + "\s*$", line)
            if match:
                expanded_chunk_lines.extend(self._expand(chunks, match.group(2), indent + match.group(1)))
            else:
                expanded_chunk_lines.append(indent + line)
        return expanded_chunk_lines

    def get_chunk(self, chunkName):
        return self._expand(self.chunks, chunkName)
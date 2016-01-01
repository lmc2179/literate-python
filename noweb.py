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

import sys, re

OPEN = "<<"
CLOSE = ">>"

def parse_chunks(document):
    chunkName = None
    chunks = {}
    for line in document.split('\n'):
        match = re.match(OPEN + "([^>]+)" + CLOSE + "=", line)
        if match:
            chunkName = match.group(1)
            # If chunkName exists in chunks, then we'll just add to the existing chunk.
            if not chunkName in chunks:
                chunks[chunkName] = []
        else:
            match = re.match("@", line)
            if match:
                chunkName = None
            elif chunkName:
                chunks[chunkName].append(line)

    return chunks

def expand(chunks, chunkName, indent=""):
    chunkLines = chunks[chunkName]
    expandedChunkLines = []
    for line in chunkLines:
        match = re.match("(\s*)" + OPEN + "([^>]+)" + CLOSE + "\s*$", line)
        if match:
            expandedChunkLines.extend(expand(match.group(2), indent + match.group(1)))
        else:
            expandedChunkLines.append(indent + line)
    return expandedChunkLines
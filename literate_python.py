from collections import defaultdict
import re

OPEN = "<<"
CLOSE = ">>"

class Document(object):
    def __init__(self, document):
        self.chunks = self._parse_chunks(document)

    def _parse_chunks(self, document):
        current_chunk_name = None
        chunks = defaultdict(list)
        for line in document.split('\n'):
            section_open_match = self._match_code_section_open(line)
            if section_open_match:
                current_chunk_name = section_open_match.group(1)
            else:
                section_end_match = self._match_code_section_end(line)
                if section_end_match:
                    current_chunk_name = None
                elif current_chunk_name:
                    chunks[current_chunk_name].append(line)
        return chunks

    def _match_code_section_open(self, line):
        return re.match(OPEN + "([^>]+)" + CLOSE + "=", line)

    def _match_code_section_end(self, line):
        return re.match("@", line)

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

    def get_chunk_recursive(self, section_name):
        return self._expand(self.chunks, section_name)

class Tangler(object):
    def tangle_module(self, lp_filename, main_chunk_name, target_filename):
        f = open(lp_filename)
        file_contents = f.read()
        d = Document(file_contents)
        tangled_file = '\n'.join(d.get_chunk_recursive(main_chunk_name))
        f_out = open(target_filename, 'w')
        f_out.write(tangled_file)
        f_out.close()

class Weaver(object):
    def weave_module(self, lp_filename, target_filename):
        f = open(lp_filename)
        file_contents = f.read()
        f_out = open(target_filename, 'w')
        f_out.write(file_contents)
        f_out.close()
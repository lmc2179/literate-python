from collections import defaultdict
import re

OPEN = "<<"
CLOSE = ">>"

class Document(object):
    LATEX = 'L'
    PYTHON = 'P'
    def __init__(self, document):
        self.python_sections, self.map = self._parse_doc(document)

    def _parse_doc(self, document):
        current_section_name = None
        sections = defaultdict(list)
        map = []
        for line in document.split('\n'):
            section_open_match = self._match_code_section_open(line)
            if section_open_match:
                current_section_name = section_open_match.group(1)
            else:
                section_end_match = self._match_code_section_end(line)
                if section_end_match:
                    map.append((self.PYTHON, current_section_name))
                    current_section_name = None
                elif current_section_name:
                    sections[current_section_name].append(line)
                else:
                    map.append((self.LATEX, line))
        return sections, map

    def _match_code_section_open(self, line):
        return re.match(OPEN + "([^>]+)" + CLOSE + "=", line)

    def _match_code_section_end(self, line):
        return re.match("@", line)

    def _expand(self, sections_dict, section_name, indent=""):
        indent = ""
        section_lines = sections_dict[section_name]
        expanded_section_lines = []
        for line in section_lines:
            match = re.match("(\s*)" + OPEN + "([^>]+)" + CLOSE + "\s*$", line)
            if match:
                expanded_section_lines.extend(self._expand(sections_dict, match.group(2), indent + match.group(1)))
            else:
                expanded_section_lines.append(indent + line)
        return expanded_section_lines

    def get_section(self, section_name):
        return self._expand(self.python_sections, section_name)

    def get_map(self):
        return self.map

    def weave(self):
        woven_doc = ''
        for line_type, line in self.map:
            if line_type == self.PYTHON:
                section_code = '\n'.join(self.get_section(line))
                woven_doc += "\\begin{lstlisting}" #TODO: Colors and stuff in doc?
                woven_doc += '<<{0}>>=\n{1}\n'.format(line, section_code)
                woven_doc += "\end{lstlisting}"
            elif line_type == self.LATEX:
                woven_doc += line + '\n'
        woven_doc = self._add_document_level_info(woven_doc)
        return woven_doc

    def _add_document_level_info(self, doc):
        PACKAGE_DECLARATION = """\documentclass{article}
\\usepackage{color}
\\usepackage[procnames]{listings}"""
        COLOR_AND_LIST_INFO = """\\begin{document}
\definecolor{keywords}{RGB}{255,0,90}
\definecolor{comments}{RGB}{0,0,113}
\definecolor{red}{RGB}{160,0,0}
\definecolor{green}{RGB}{0,150,0}
\lstset{language=Python,
        basicstyle=\\ttfamily\small,
        keywordstyle=\color{keywords},
        commentstyle=\color{comments},
        stringstyle=\color{red},
        showstringspaces=false,
        identifierstyle=\color{green},
        procnamekeys={def,class}}"""
        doc = doc.replace('\documentclass{article}', PACKAGE_DECLARATION)
        doc = doc.replace('\\begin{document}', COLOR_AND_LIST_INFO)
        return doc

class Tangler(object):
    def tangle_module(self, lp_filename, main_chunk_name, target_filename):
        f = open(lp_filename)
        file_contents = f.read()
        d = Document(file_contents)
        tangled_file = '\n'.join(d.get_section(main_chunk_name))
        f_out = open(target_filename, 'w')
        f_out.write(tangled_file)
        f_out.close()

class Weaver(object):
    def weave_module(self, lp_filename, target_filename):
        f = open(lp_filename)
        file_contents = f.read()
        d = Document(file_contents)
        f_out = open(target_filename, 'w')
        f_out.write(d.weave())
        f_out.close()
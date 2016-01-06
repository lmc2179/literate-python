import unittest
import tempfile
import os
from literate_python import Document, Tangler, Weaver

class ParserTest(unittest.TestCase):
    def test_parse_flat(self):
        d = Document(TEST_DOC_FLAT)
        target = d.get_section("test_flat.py")
        self.assertEqual(target, ['print("Hello, world!")'])

    def test_parse_nested(self):
        d = Document(TEST_DOC_NESTED)
        target = d.get_section("test_nested.py")
        self.assertEqual(target, ['print("Hello, world!")'])
        target = d.get_section("test code inner")
        self.assertEqual(target, ['print("Hello, world!")'])

class TangleTest(unittest.TestCase):
    def test_tangle_flat(self):
        temp_dir = tempfile.mkdtemp()
        target = os.path.join(temp_dir, 'test_flat.py')
        Tangler().tangle_module('test_flat.pyl', 'test_flat.py', target)
        output = open(target).read()
        self.assertEqual(output, """print("Hello, world!")""")

    def test_tangle_nested(self):
        temp_dir = tempfile.mkdtemp()
        target = os.path.join(temp_dir, 'test_nested.py')
        Tangler().tangle_module('test_nested.pyl', 'test_nested.py', target)
        output = open(target).read()
        self.assertEqual(output, """print("Hello, world!")""")

class WeaveTest(unittest.TestCase):
    maxDiff = None
    def test_weave_flat(self):
        temp_dir = tempfile.mkdtemp()
        target = os.path.join(temp_dir, 'test_flat.py')
        Weaver().weave_module('test_flat.pyl', target)
        output = open(target).read()
        self.assertEqual(output, TEST_DOC_FLAT_WOVEN)

    def test_weave_nested(self):
        temp_dir = tempfile.mkdtemp()
        target = os.path.join(temp_dir, 'test_nested.py')
        Weaver().weave_module('test_nested.pyl', target)
        output = open(target).read()
        self.assertEqual(output, TEST_DOC_NESTED_WOVEN)

TEST_DOC_FLAT = """\documentclass{article}
\\begin{document}
This is a test document.
$
<<test_flat.py>>=
print("Hello, world!")
@
$
This concludes the test
\\end{document}
"""

TEST_DOC_FLAT_WOVEN = """\documentclass{article}
\\usepackage{color}
\\usepackage[procnames]{listings}
\\usepackage{algorithm}
\\begin{document}
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
        procnamekeys={def,class}}
This is a test document.
\\begin{algorithm}\caption{test\_flat.py}\\begin{lstlisting}
print("Hello, world!")
\end{lstlisting}\end{algorithm}This concludes the test
\end{document}
"""

TEST_DOC_NESTED = """\documentclass{article}
\\begin{document}
This is a test document.
$
<<test code inner>>=
print("Hello, world!")
@
$
$
<<test_nested.py>>=
<<test code inner>>
@
$
This concludes the test
\\end{document}
"""

TEST_DOC_NESTED_WOVEN = """\documentclass{article}
\\usepackage{color}
\\usepackage[procnames]{listings}
\\usepackage{algorithm}
\\begin{document}
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
        procnamekeys={def,class}}
This is a test document.
\\begin{algorithm}\caption{test code inner}\\begin{lstlisting}
print("Hello, world!")
\end{lstlisting}\end{algorithm}\\begin{algorithm}\caption{test\_nested.py}\\begin{lstlisting}
print("Hello, world!")
\end{lstlisting}\end{algorithm}This concludes the test
\end{document}
"""

if __name__ == '__main__':
    unittest.main()
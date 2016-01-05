import unittest
import tempfile
import os
from literate_python import Document, Tangler, Weaver

class ParserTest(unittest.TestCase):
    def test_parse_flat(self):
        d = Document(TEST_DOC_FLAT)
        target = d.get_chunk_recursive("test_flat.py")
        self.assertEqual(target, ['print("Hello, world!")'])

    def test_parse_nested(self):
        d = Document(TEST_DOC_NESTED)
        target = d.get_chunk_recursive("test_nested.py")
        self.assertEqual(target, ['print("Hello, world!")'])
        target = d.get_chunk_recursive("test code inner")
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
    def test_weave_flat(self):
        temp_dir = tempfile.mkdtemp()
        target = os.path.join(temp_dir, 'test_flat.py')
        Weaver().weave_module('test_flat.pyl', target)
        output = open(target).read()
        self.assertEqual(output, TEST_DOC_FLAT)

    def test_weave_nested(self):
        temp_dir = tempfile.mkdtemp()
        target = os.path.join(temp_dir, 'test_nested.py')
        Weaver().weave_module('test_nested.pyl', target)
        output = open(target).read()
        self.assertEqual(output, TEST_DOC_NESTED)

TEST_DOC_FLAT = """\documentclass{article}
\\begin{document}
This is a test document.
$
<<test_flat.py>>=
print("Hello, world!")
@
$
This concludes the test
\\end{document}"""

TEST_DOC_NESTED = """\documentclass{article}
\\begin{document}
This is a test document.
$
<<test code inner>>=
print("Hello, world!")
@
<<test_nested.py>>=
<<test code inner>>
@
$
This concludes the test
\end{document}"""

if __name__ == '__main__':
    unittest.main()
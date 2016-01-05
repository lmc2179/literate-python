import unittest
import tempfile
import os
from literate_python import Document, Tangler

class ParserTest(unittest.TestCase):
    def test_parse_flat(self):
        d = Document(TEST_DOC_FLAT)
        target = d.get_chunk_recursive("test code")
        self.assertEqual(target, ['print("Hello, world!")'])

    def test_parse_nested(self):
        d = Document(TEST_DOC_NESTED)
        target = d.get_chunk_recursive("test code")
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

TEST_DOC_FLAT = """This is a test document.
<<test code>>=
print("Hello, world!")
@
This concludes the test
"""

TEST_DOC_NESTED = """This is a test document.
<<test code inner>>=
print("Hello, world!")
@
<<test code>>=
<<test code inner>>
@
This concludes the test
"""

if __name__ == '__main__':
    unittest.main()
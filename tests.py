import unittest
from noweb import Document

class ParserTest(unittest.TestCase):
    def test_parse_flat(self):
        d = Document(TEST_DOC_FLAT)
        target = d.get_chunk("test code")
        self.assertEqual(target, ['print("Hello, world!")'])

    def test_parse_nested(self):
        d = Document(TEST_DOC_NESTED)
        target = d.get_chunk("test code")
        self.assertEqual(target, ['print("Hello, world!")'])

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
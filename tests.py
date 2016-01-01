import unittest
from noweb import parse_chunks, expand

class ParserTest(unittest.TestCase):
    def test_parse(self):
        test_doc = TEST_DOC
        chunks = parse_chunks(test_doc)
        print(chunks)
        target = expand(chunks, "test code")
        self.assertEqual(target, ['print("Hello, world!")'])

TEST_DOC = """This is a test document.
<<test code>>=
print("Hello, world!")
@
This concludes the test
"""

if __name__ == '__main__':
    unittest.main()
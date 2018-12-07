import unittest
import datasetviewer.viewer.StringReverser as sr

class BasicTestCase(unittest.TestCase):

    def test_reverse(self):
        self.assertTrue("olleh" == sr.reverse_string("hello"))

if __name__ == '__main__':
    unittest.main()

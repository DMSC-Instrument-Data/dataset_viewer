import unittest

def reverse_string(word):
    return word[::-1] 

class BasicTestCase(unittest.TestCase):

    def test_reverse(self):
        self.assertTrue("olleh" == reverse_string("hello"))

if __name__ == '__main__':
    unittest.main()

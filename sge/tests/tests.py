import unittest

import sys
sys.path.append("../")

import sge


class SimpleTest(unittest.TestCase):
    def equal(self):
        self.assertTrue('test', 'test')


if __name__ == '__main__':
    unittest.main()

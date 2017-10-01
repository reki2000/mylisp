#!/usr/bin/env pt\ython
# encoding:utf-8

import core as c

import unittest

class Test(unittest.TestCase):
    def test_symbol(self):
        s1 = c.symbol('a')
        s2 = c.symbol('a')
        s3 = c.symbol('b')
        self.assertEqual(s1,s2)
        self.assertNotEqual(s1,s3)

if __name__ == '__main__':
    unittest.main()

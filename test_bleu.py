#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from bleu import SmoothedBleuReference

class TestSmoothedBleuReference(unittest.TestCase):
    """
    Regression tests for SmoothedBleuReference
    """
    @staticmethod
    def tokenize(sentence):
        return sentence.split(" ")
    def test_identical_segments(self):
        segment = self.tokenize("Consistency is the last refuge of the unimaginative")
        ref = SmoothedBleuReference(segment)
        self.assertEqual(ref.score(segment), -1.0)
    def test_completely_different_segments(self):
        segment_a = self.tokenize("A A A")
        segment_b = self.tokenize("B B B")
        ref = SmoothedBleuReference(segment_a)
        self.assertEqual(ref.score(segment_b), -0.0)


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from bleu import SmoothedBleuScorer

class TestSmoothedBleuReference(unittest.TestCase):
    """
    Regression tests for SmoothedBleuReference
    """
    @staticmethod
    def tokenize(sentence):
        return sentence.split(" ")
    def test_identical_segments(self):
        segment = self.tokenize("Consistency is the last refuge of the unimaginative")
        scorer = SmoothedBleuScorer('n=4')
        scorer.set_reference(segment)
        self.assertEqual(scorer.score(segment), -1.0)
    def test_completely_different_segments(self):
        segment_a = self.tokenize("A A A")
        segment_b = self.tokenize("B B B")
        scorer = SmoothedBleuScorer('n=4')
        scorer.set_reference(segment_a)
        self.assertEqual(scorer.score(segment_b), -0.0)


if __name__ == '__main__':
    unittest.main()

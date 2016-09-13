#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from bleu import SmoothedBleuReference

class TestSmoothedBleuReference(unittest.TestCase):
    """
    Regression tests for SmoothedBleuReference
    """
    def test_identical_segments(self):
        segment = "Consistency is the last refuge of the unimaginative."
        ref = SmoothedBleuReference(segment)
        self.assertEqual(ref.score(segment), 100.0)
    def test_completely_different_segments(self):
        segment_a = "A A A"
        segment_b = "B B B"
        ref = SmoothedBleuReference(segment_a)
        self.assertEqual(ref.score(segment_b), 0.00)


if __name__ == '__main__':
    unittest.main()

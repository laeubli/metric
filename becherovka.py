#!/usr/bin/env python
# -*- coding: utf-8 -*-

from reference import Reference

class BecherovkaReference(Reference):
    """
    A sample metric that returns 100.0 if the hypothesis equals the reference
    and 0.0 otherwise.
    """

    def __init__(self, reference_tokens):
        Reference.__init__(self, reference_tokens)

    def score(self, hypothesis_tokens):
        return 100.0 if self._reference_tokens == hypothesis_tokens else 0.0


if __name__ == "__main__":
    ref = BecherovkaReference(["This", "is", "a", "small", "drink", "."])
    print ref.score(["This", "is", "a", "small", "drink", "."])
    print ref.score_matrix([
        ["This", "is", "a", "big", "drink", "."],
        ["This", "is", "a", "small", "drink", "."]
    ])

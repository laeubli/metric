#!/usr/bin/env python
# -*- coding: utf-8 -*-

from reference import Reference

class BecherovkaReference(Reference):
    """
    A sample metric that returns 100.0 if the hypothesis equals the reference
    and 0.0 otherwise.
    """

    def __init__(self, reference):
        Reference.__init__(self, reference)

    def score(self, hypothesis):
        return 100.0 if self.reference == hypothesis else 0.0


if __name__ == "__main__":
    ref = BecherovkaReference("This is a small drink.")
    print ref.score("This is a big drink.")
    print ref.score_many(["This is a small drink.", "This is a big drink."])

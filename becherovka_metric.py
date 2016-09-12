#!/usr/bin/env python
# -*- coding: utf-8 -*-

from metric import Metric, Reference

class BecherovkaMetric(Metric):
    """
    A sample metric that returns 100.0 if the hypothesis equals the reference
    and 0.0 otherwise.
    """

    def score(self, reference, hypothesis):
        return 100.0 if reference == hypothesis else 0.0

class BecherovkaReference(Reference):
    """
    A reference translation against which hypotheses can be scored through
    BecherovkaMetric.
    """

    def __init__(self, reference):
        metric = BecherovkaMetric()
        Reference.__init__(self, reference, metric)


if __name__ == "__main__":
    ref = BecherovkaReference("This is a small drink.")
    print ref.score("This is a big drink.")
    print ref.score_many(["This is a small drink.", "This is a big drink."])

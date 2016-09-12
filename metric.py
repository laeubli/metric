#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

class Metric(object):
    """
    An automatic translation metric that scores a hypothesis against a
    reference translation.
    """

    def init(self):
        """
        Initialises the metric, probably with metric-specific parameters.
        """
        pass

    def score(self, reference, hypothesis):
        """
        Scores @param hypothesis against @param reference.
        @return score as a percentage; usually a number between 0.0 and 100.0.
        """
        pass

    def _tokenize(self, sentence):
        """
        Splits @param sentence into a list of tokens.
        """
        return sentence.split(" ") #todo: adjust to Nematus

class Reference(object):
    """
    A re-usable reference agains which translation hypotheses can be compared.
    """

    def __init__(self, reference, metric):
        """
        @param reference: The reference againt which hypotheses shall be
                          scored.
        @param metric:    The metric to be used for the scoring.
        """
        self.metric = metric
        self.reference = reference

    def score(self, hypothesis):
        """
        Scores @param hypothesis against this reference.
        """
        return self.metric.score(self.reference, hypothesis)

    def score_many(self, hypotheses):
        """
        Scores every hypothesis in @param hypotheses against this reference.
        """
        return [self.score(hypothesis) for hypothesis in hypotheses]

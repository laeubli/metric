#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class Reference:
    """
    Abstract base class for re-usable translation reference. Hypotheses can be
    scored against this reference through the evaluation metric implemented in
    its `score` function.
    """

    __metaclass__ = ABCMeta #abstract base class

    def __init__(self, reference):
        """
        @param reference the reference translation that hypotheses shall be
                         scored against.
        """
        self.reference = reference
        #additional (metric-specific) parameters to be defined in subclass

    @abstractmethod
    def score(self, hypothesis):
        """
        Scores @param hypothesis against this reference.
        """
        pass #to be implemented in sublcass

    def score_many(self, hypotheses):
        """
        Scores every hypothesis in @param hypotheses against this reference.
        """
        return [self.score(hypothesis) for hypothesis in hypotheses]

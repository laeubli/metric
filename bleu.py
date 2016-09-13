#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

from math import exp
from operator import mul

from reference import Reference

class SmoothedBleuReference(Reference):
    """
    Implements smoothed sentence-level BLEU as as proposed by Lin and Och (2004).
    """

    def __init__(self, reference, n=4):
        """
        @param reference the reference translation that hypotheses shall be
                         scored against.
        @param n         maximum n-gram order to consider.
        """
        Reference.__init__(self, reference)
        self.n = n
        # preprocess reference
        self._reference_tokens = self._get_tokens(self.reference)
        self._reference_length = len(self._reference_tokens)
        self._reference_ngrams = self._get_ngrams(self._reference_tokens, self.n)

    def _get_tokens(self, sentence):
        """
        Splits @param sentence into a list of tokens.
        """
        return sentence.split(" ") #todo: adjust to Nematus

    def _get_ngrams(self, tokens, max_n):
        """
        Extracts all n-grams of order 1 up to (and including) @param max_n from
        a list of @param tokens.
        """
        def ngrams(tokens, n):
            return zip(*[tokens[i:] for i in range(n)])
        return {n: ngrams(tokens, n) for n in range(1, max_n+1)}

    def score(self, hypothesis):
        """
        Scores @param hypothesis against this reference.
        @return the smoothed sentence-level BLEU score.
        """
        def product(iterable):
            return reduce(mul, iterable, 1)
        def ngram_precisions(ref_ngrams, hyp_ngrams):
            precisions = []
            for n in range(1, self.n+1):
                overlap = len([ngram for ngram in hyp_ngrams[n] if ngram in ref_ngrams[n]])
                hyp_length = len(hyp_ngrams[n])
                if n >= 2:
                    # smoothing as proposed by Lin and Och (2004),
                    # implemented as described in (Chen and Cherry, 2014)
                    overlap += 1
                    hyp_length += 1
                precisions.append(overlap/hyp_length)
            return precisions
        def brevity_penalty(ref_length, hyp_length):
            return min(1.0, exp(1-(ref_length/hyp_length)))
        # preprocess hypothesis
        hypothesis_tokens = self._get_tokens(hypothesis)
        hypothesis_length = len(hypothesis_tokens)
        hypothesis_ngrams = self._get_ngrams(hypothesis_tokens, self.n)
        # calculate n-gram precision for all orders
        np = ngram_precisions(self._reference_ngrams, hypothesis_ngrams)
        # calculate brevity penalty
        bp = brevity_penalty(self._reference_length, hypothesis_length)
        # compose final BLEU score
        return product(np)**(1/self.n) * bp * 100.0

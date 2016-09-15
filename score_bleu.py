#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Scores two line-delimited files (references, translations) using
SmoothedBleuReference.
"""

import argparse
from itertools import izip

from bleu import SmoothedBleuReference

def get_parser():
    parser = argparse.ArgumentParser(description='Sentence-level BLEU scorer')
    parser.add_argument('references', help='file with one referene per line')
    parser.add_argument('hypotheses', help='file with one hypothesis per line')
    parser.add_argument('-o', '--output', help='file to write BLEU scores to; scores are written to STDOUT by default')
    return parser

def tokenize(segment):
    return segment.split(" ")

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    if args.output:
        output = open(args.output, 'w')
    # walk through files
    with open(args.references, 'r') as refs, open(args.hypotheses, 'r') as hyps:
        for ref, hyp in izip(refs, hyps):
            ref_tokens = tokenize(ref)
            hyp_tokens = tokenize(hyp)
            r = SmoothedBleuReference(ref_tokens)
            score = r.score(hyp_tokens)
            if args.output:
                output.write('%.4f\n' % score)
            else:
                print score
    if args.output:
        output.close()

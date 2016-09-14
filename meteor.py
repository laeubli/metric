#!/usr/bin/env python
# -*- coding: utf-8 -*-

METEOR_PATH="/home/juli/data/programming/meteor-1.5"

import subprocess, shlex
from reference import Reference

class MeteorReference(Reference):
    """
    Python wrapper for the METEOR metric.
    """

    def __init__(self, reference_tokens, meteor_language="en", meteor_path="~/meteor/"):
        #print "building reference"
        Reference.__init__(self, reference_tokens)
        self.meteor_language = meteor_language
        self.meteor_path = meteor_path + "/"
        self.reference_string = " ".join(reference_tokens)
        command = "java -Xmx2G -jar "+self.meteor_path+"meteor-*.jar - - -l "+self.meteor_language+" -stdio"
        #print command
        #command = shlex.split(command)
        #print command
        self.meteor_process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    def score(self, hypothesis_tokens):
        #return 100.0 if self._reference_tokens == hypothesis_tokens else 0.0
        #print "scoring"
        reference_string = " ".join(hypothesis_tokens)
        #std_out, std_err = self.meteor_process.communicate(input="SCORE ||| reference 1 words ||| reference n words ||| hypothesis words")
        self.meteor_process.stdin.write("SCORE ||| "+self.reference_string+" ||| "+reference_string+"\n")
        std_out = self.meteor_process.stdout.readline()
        self.meteor_process.stdin.write("EVAL ||| "+std_out)
        std_out = self.meteor_process.stdout.readline()
        return float(std_out)
        #print std_err
        #self.meteor_process.close()
        #return 66.0

if __name__ == "__main__":
    ref = MeteorReference(["This", "is", "a", "small", "drink", "."], meteor_path=METEOR_PATH)
    print ref.score(["This", "is", "a", "small", "drink", "."])
    print ref.score_matrix([
        ["This", "is", "a", "big", "drink", "."],
        ["This", "is", "a", "small", "drink", "."]
    ])
    print ref.score_matrix([
        ["This", "is", "a", "big", "drink", "."],
        ["This", "is", "a", "small", "drink", "."]
    ])

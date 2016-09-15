#!/usr/bin/env python
# -*- coding: utf-8 -*-

METEOR_PATH="/home/juli/data/programming/meteor-1.5"

import subprocess
from reference import Reference

class MeteorScorer():
    """
    Starts a METEOR process and keeps it alive, so that the model can be kept in memeory.
    """
    def __init__(self, meteor_language="en", meteor_path="~/meteor"):
        self.meteor_language = meteor_language
        self.meteor_path = meteor_path + "/"
        command = "java -Xmx2G -jar "+self.meteor_path+"meteor-*.jar - - -l "+self.meteor_language+" -stdio"
        self.meteor_process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        
    def terminate_process(self):
        self.meteor_process.terminate()
        
class MeteorReference(Reference):
    """
    Python wrapper for the METEOR metric.
    """

    def __init__(self, reference_tokens, meteor_language="en", meteor_path="~/meteor/", meteor_scorer=None):
        Reference.__init__(self, reference_tokens)
        self.meteor_language = meteor_language
        self.meteor_path = meteor_path + "/"
        self.reference_string = " ".join(reference_tokens)
        if meteor_scorer is None:
            self.meteor_scorer = MeteorScorer(meteor_language=meteor_language, meteor_path=meteor_path)
        else:
            self.meteor_scorer = meteor_scorer
        #command = "java -Xmx2G -jar "+self.meteor_path+"meteor-*.jar - - -l "+self.meteor_language+" -stdio"
        #self.meteor_process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    def score(self, hypothesis_tokens):
        reference_string = " ".join(hypothesis_tokens)
        self.meteor_scorer.meteor_process.stdin.write("SCORE ||| "+self.reference_string+" ||| "+reference_string+"\n")
        std_out = self.meteor_scorer.meteor_process.stdout.readline()
        self.meteor_scorer.meteor_process.stdin.write("EVAL ||| "+std_out)
        std_out = self.meteor_scorer.meteor_process.stdout.readline()
        return float(std_out)
    
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

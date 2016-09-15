#!/usr/bin/env python
# -*- coding: utf-8 -*-

METEOR_PATH="/home/juli/data/programming/meteor-1.5"

import subprocess, threading
from reference import Reference

class MeteorScorer():
    """
    Starts a METEOR process and keeps it alive, so that the model can be kept in memeory.
    
    Arguments are the meteor language abbreviation and the path to the METEOR installation. They need to be specified as follows:"meteor_language=lg,meteor_path=path"
    """
    def __init__(self, argument_string):
        
        arguments = {}
        argument_strings = argument_string.split(",")
        for a in argument_strings:
            argument, value = a.split("=")
            argument = argument.strip()
            value = value.strip()
            arguments[argument] = value
        
        self.lock = threading.Lock()
        self.meteor_language = arguments["meteor_language"]
        self.meteor_path = arguments["meteor_path"] + "/"
        command = "java -Xmx2G -jar "+self.meteor_path+"meteor-*.jar - - -l "+self.meteor_language+" -stdio"
        self.meteor_process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        
    def set_reference(self, reference_tokens):
        self.reference = MeteorReference(reference_tokens, self)
        
    def score(self, hypothesis_tokens):
        return self.reference.score(hypothesis_tokens)
    
    def score_matrix(self, hypothesis_matrix):
        return self.reference.score_matrix(hypothesis_matrix)
    
    def terminate_process(self):
        self.meteor_process.terminate()
        
class MeteorReference(Reference):
    """
    Python wrapper for the METEOR metric.
    """

    def __init__(self, reference_tokens, meteor_scorer):
        Reference.__init__(self, reference_tokens)
        self.reference_string = " ".join(reference_tokens)
        self.meteor_scorer = meteor_scorer

    def score(self, hypothesis_tokens):
        reference_string = " ".join(hypothesis_tokens)
        self.meteor_scorer.lock.acquire()
        self.meteor_scorer.meteor_process.stdin.write("SCORE ||| "+self.reference_string+" ||| "+reference_string+"\n")
        std_out = self.meteor_scorer.meteor_process.stdout.readline()
        self.meteor_scorer.meteor_process.stdin.write("EVAL ||| "+std_out)
        std_out = self.meteor_scorer.meteor_process.stdout.readline()
        self.meteor_scorer.lock.release()
        return float(std_out)
    
if __name__ == "__main__":
    scorer = MeteorScorer("meteor_language=en,meteor_path="+METEOR_PATH)
    scorer.set_reference(["This", "is", "a", "small", "drink", "."])
    print scorer.score(["This", "is", "a", "small", "drink", "."])
    print scorer.score_matrix([
        ["This", "is", "a", "big", "drink", "."],
        ["This", "is", "a", "small", "drink", "."]
    ])
    print scorer.score_matrix([
        ["This", "is", "a", "big", "drink", "."],
        ["This", "is", "a", "small", "drink", "."]
    ])

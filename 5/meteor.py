#!/usr/bin/env python
import sys, os
baseline_path = os.path.join(os.getcwd()[:-1], "en600.468/reranker/")
if baseline_path not in sys.path:
    sys.path.insert(0, baseline_path)

src = [line.strip().split() for line in open(baseline_path+"data/dev+test.src")]

a = 0.16

def word_matches(h, ref):
    return sum(1 for w in h if w in ref)

def precision(h, ref):
    len_h = float(len(h))
    word_m = word_matches(h, ref)
    return (word_m / len_h)

def recall(h, ref):
    len_ref = float(len(ref))
    word_m = word_matches(h, ref)
    return (word_m / len_ref)

def meteor(h, s):
    r = recall(h, src[s])
    p = precision(h, src[s])
    if (r == 0 or p == 0 ):
        return 0
    return ( p * r ) / ( ( (1 - a) * r ) + (a * p) )

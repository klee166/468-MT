#!/usr/bin/env python

## This program is built on the decode program written for CS468 MT @ JHU.
## It implements the METOR metric and uses WordNet to generate synonyms,
## though only for the reference sentences.

import argparse # optparse is deprecated
from itertools import islice # slicing for iterators
import sys, os
baseline_path = os.path.join(os.getcwd()[:-7], "en600.468/evaluator/")
if baseline_path not in sys.path:
    sys.path.insert(0, baseline_path)
from nltk.corpus import wordnet as wn

a = 0.16

def word_matches(h, ref):
    synonyms = set()
    for w in ref:
        synonyms.add(w)
        for syn in wn.synsets(w):
            for l in syn.lemmas():
                synonyms.add(l.name())
    return sum(1 for w in h if w in synonyms)

def percision(h, ref):
    len_h = float(len(h))
    word_m = word_matches(h, ref)
    return (word_m / len_h)

def recall(h, ref):
    len_ref = float(len(ref))
    word_m = word_matches(h, ref)
    return (word_m / len_ref)

def meteor(h, ref):
    r = recall(h, ref)
    p = percision(h, ref)
    if (r == 0 or p == 0 ):
        return 0
    return ( p * r ) / ( ( (1 - a) * r ) + (a * p) )

def main():
    parser = argparse.ArgumentParser(description='Evaluate translation hypotheses.')
    parser.add_argument('-i', '--input', default=baseline_path+'data/hyp1-hyp2-ref',
            help='input file (default data/hyp1-hyp2-ref)')
    parser.add_argument('-n', '--num_sentences', default=None, type=int,
            help='Number of hypothesis pairs to evaluate')
    # note that if x == [1, 2, 3], then x[:None] == x[:] == x (copy); no need for sys.maxint
    opts = parser.parse_args()

    # we create a generator and avoid loading all sentences into a list
    def sentences():
        with open(opts.input) as f:
            for pair in f:
                yield [sentence.strip().split() for sentence in pair.split(' ||| ')]

    # note: the -n option does not work in the original code
    for h1, h2, ref in islice(sentences(), opts.num_sentences):
        rset = set(ref)
        h1_match = meteor(h1, rset)
        # print "meteor is h1_match ", h1_match
        h2_match = meteor(h2, rset)
        # print "meteor is h2_match ", h2_match
        print(1 if h1_match > h2_match else # \begin{cases}
                (0 if h1_match == h2_match
                    else -1)) # \end{cases}

# convention to allow import of this file as a module
if __name__ == '__main__':
    main()

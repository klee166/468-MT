#!/usr/bin/env python

## This program is built on the align program written for CS468 MT @ JHU.
## The program implements the IBM Model 1 for French-English word alignments
## using transition probabilities t(e|f) and most probable alignment.

import optparse
import sys
from collections import defaultdict

optparser = optparse.OptionParser()
optparser.add_option("-d", "--data", dest="train", default="en600.468/aligner/data/hansards", help="Data filename prefix (default=data)")
optparser.add_option("-e", "--english", dest="english", default="e", help="Suffix of English filename (default=e)")
optparser.add_option("-f", "--french", dest="french", default="f", help="Suffix of French filename (default=f)")
optparser.add_option("-t", "--threshold", dest="threshold", default=0.5, type="float", help="Threshold for aligning with Dice's coefficient (default=0.5)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to use for training and alignment")
(opts, _) = optparser.parse_args()
f_data = "%s.%s" % (opts.train, opts.french)
e_data = "%s.%s" % (opts.train, opts.english)

bitext = [[sentence.strip().split() for sentence in pair] for pair in zip(open(f_data), open(e_data))[:opts.num_sents]]
f_count = defaultdict(float) # Maps an English word to expected count
fe_count = defaultdict(float) # Maps all (f,e) word pairs to expected count
t_probability = defaultdict(float) # Transition probability

sys.stderr.write("Initializing theta...")
for (n, (f, e)) in enumerate(bitext):
    for f_i in set(f):
        for e_j in set(e):
            t_probability[(f_i,e_j)] = 1.0/(len(e)+1) # Uniform distribution
        if n % 500 == 0:
            sys.stderr.write(".") # To give user rough-estimate of execution progress
sys.stderr.write("\n")

sys.stderr.write("Expectation Maximization...")
k = 0 # Number of iterations for EM loop

while k < 5:
    k += 1

    # Set count(e|f) = 0 for all (f,e) and set total(f) = 0 for all f
    for (n, (f, e)) in enumerate(bitext):
        for f_i in set(f):
            f_count[f_i] = 0
            for e_j in set(e):
                fe_count[(f_i,e_j)] = 0
        if n % 500 == 0:
            sys.stderr.write(".")

    # Expectation or E-step
    for (n, (f, e)) in enumerate(bitext):
        for (j, e_j) in enumerate(e):
            Z = 0 # Normalization term
            for (i, f_i) in enumerate(f):
                Z += t_probability[(f_i, e_j)]
            for (i, f_i) in enumerate(f):
                c = t_probability[(f_i, e_j)] / Z # Expected count
                fe_count[(f_i, e_j)] += c # Increment count(e|f) by expected count
                f_count[f_i] += c # Increment count(f) by expected count
            if n % 5000 == 0:
                sys.stderr.write(".")

    # Maximation or M-step
    for (f_i, e_j) in fe_count.keys():
        t_probability[(f_i,e_j)] = fe_count[(f_i, e_j)] / f_count[f_i]

sys.stderr.write("\n")

# Align by most probable alignment method
for (n, (f, e)) in enumerate(bitext):
    for (i, f_i) in enumerate(f):
        best_p = 0
        best_j = 0
        for (j, e_j) in enumerate(e):
            if t_probability[(f_i,e_j)] > best_p:
                best_p = t_probability[(f_i,e_j)]
                best_j = j
        sys.stdout.write("%i-%i " % (i,best_j))
    sys.stdout.write("\n")

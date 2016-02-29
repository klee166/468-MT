#!/usr/bin/env python

## This program is built on the align program written for CS468 MT @ JHU.
## The program implements the IBM Model 2, which lexical translation model with
## word ordering, for French to English word alignments.

import optparse
import sys
from collections import defaultdict
from nltk.stem import SnowballStemmer
import ibm1_f2e

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

# Stem words before model training
french_stemmer = SnowballStemmer("french")
english_stemmer = SnowballStemmer("english")
bitext_stemmed = []
for (n, (f, e)) in enumerate(bitext):
    f_stemmed = [french_stemmer.stem(word.decode("utf-8")) for word in f]
    e_stemmed = [english_stemmer.stem(word) for word in e]
    bitext_stemmed.append([f_stemmed, e_stemmed])

bitext = bitext_stemmed

f_count = defaultdict(float) # Expected count of each French word
fe_count = defaultdict(float) # Expected count of each (f,e) word pair
a_probability = defaultdict(float) # Alignment probability
a_count = defaultdict(float) # Count of i given j, len(e) and len(f)
a_count_for_any_i = defaultdict(float)
t_probability = ibm1_f2e.IBM1(opts.train, opts.num_sents).t_probability # Translation probabilites carried over from Model 1

# Initializing alignment probability distribution
for (n, (f, e)) in enumerate(bitext):
    for (j, e_j) in enumerate(e):
        for (i, f_i) in enumerate(f):
            a_probability[(j, i, len(e), len(f))] = 1.0/(len(f)+1) # Uniform distribution

Z = dict() # Normalization term for counts
k = 0 # Iteration count

# Expectation maximization until iteration count met
while k < 5:
    k += 1

    # Set counts to 0
    for (n, (f, e)) in enumerate(bitext):
        l = len(f)
        m = len(e)
        for (i, f_i) in enumerate(f):
            f_count[f_i] = 0
            for (j, e_j) in enumerate(e):
                fe_count[(f_i, e_j)] = 0
        for (j, e_j) in enumerate(e):
            a_count_for_any_i[(j, m, l)] = 0
            for (i, f_i) in enumerate(f):
                a_count[(j, i, m, l)] = 0

    for (n, (f, e)) in enumerate(bitext):
        l = len(f)
        m = len(e)
        # E-step (a): Compute normalization
        for (j, e_j) in enumerate(e):
            Z[e_j] = 0
            for (i, f_i) in enumerate(f):
                Z[e_j] += t_probability[(f_i, e_j)] * a_probability[(j, i, m, l)]
        # E-step (b): Calculate expected counts
        for (j, e_j) in enumerate(e):
            for (i, f_i) in enumerate(f):
                c = (t_probability[(f_i, e_j)] * a_probability[(j, i, m, l)]) / Z[e_j] # Expected count
                fe_count[(f_i, e_j)] += c # Increment count(e|f) by expected count
                f_count[f_i] += c # Increment count(f) by expected count
                a_count[(j, i, m, l)] += c
                a_count_for_any_i[(j, m, l)] += c

    # M-step (a): Estimate lexical translation probabilities
    for (f_i, e_j) in fe_count.keys():
        t_probability[(f_i,e_j)] = fe_count[(f_i, e_j)] / f_count[f_i]

    # M-step(b): Estimate alignment probabilities
    for (j, i, len_e, len_f) in a_count.keys():
        a_probability[(j, i, len_e, len_f)] = a_count[(j, i, len_e, len_f)] / a_count_for_any_i[(j, len_e, len_f)]

# Alignment
for (n, (f, e)) in enumerate(bitext):
    for (i, f_i) in enumerate(f):
        best_p = t_probability[(f_i,e[0])] * a_probability[(0, i, len(e), len(f))]
        best_j = 0
        for (j, e_j) in enumerate(e):
            p = t_probability[(f_i,e_j)] * a_probability[(j, i, len(e), len(f))]
            if p > best_p:
                best_p = p
                best_j = j
        sys.stdout.write("%i-%i " % (i,best_j))
    sys.stdout.write("\n")

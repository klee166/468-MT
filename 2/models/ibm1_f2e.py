#!/usr/bin/env python

## This program is built on the align program written for CS468 MT @ JHU.
## The program implements the IBM Model 1, a lexical translation model,
## for French to English word alignments.

import sys
from collections import defaultdict
from nltk.stem import SnowballStemmer

reload(sys)
sys.setdefaultencoding("latin-1") # required for stemming

class IBM1:

    f_count = defaultdict(float) # Expected count of each French word
    fe_count = defaultdict(float) # Expected count of each (f,e) word pair
    t_probability = defaultdict(float) # Lexical translation probability

    def __init__(self, data="en600.468/aligner/data/hansards", num_sents=sys.maxint):
        f_data = "%s.%s" % (data, "f")
        e_data = "%s.%s" % (data, "e")

        bitext = [[sentence.strip().split() for sentence in pair] for pair in zip(open(f_data), open(e_data))[:num_sents]]

        # Stem words before model training
        french_stemmer = SnowballStemmer("french")
        english_stemmer = SnowballStemmer("english")
        bitext_stemmed = []
        for (n, (f, e)) in enumerate(bitext):
            f_stemmed = [french_stemmer.stem(word.decode("utf-8")) for word in f]
            e_stemmed = [english_stemmer.stem(word) for word in e]
            bitext_stemmed.append([f_stemmed, e_stemmed])

        bitext = bitext_stemmed

        self._train(bitext)
        self._align(bitext)


    def _train(self, bitext):
        ''' Training IBM Model 1.
        '''
        # Initializing lexical translation probability distribution t(e|f) with uniform distribution
        for (n, (f, e)) in enumerate(bitext):
            for f_i in set(f):
                for e_j in set(e):
                    self.t_probability[(f_i,e_j)] = 1.0 / len(e)

        Z = dict() # Normalization term for counts
        k = 0

        # Expectation maximization until iteration count met
        while k < 5:
            k += 1

            # Set count(e|f) = 0 for all (f,e) and set total(f) = 0 for all f
            for (n, (f, e)) in enumerate(bitext):
                for f_i in set(f):
                    self.f_count[f_i] = 0
                    for e_j in set(e):
                        self.fe_count[(f_i,e_j)] = 0

            for (n, (f, e)) in enumerate(bitext):
                # E-step (a): Compute normalization
                for (j, e_j) in enumerate(e):
                    Z[e_j] = 0.0
                    for (i, f_i) in enumerate(f):
                        Z[e_j] += self.t_probability[(f_i, e_j)]
                # E-step (b): Calculate expected counts
                for (j, e_j) in enumerate(e):
                    for (i, f_i) in enumerate(f):
                        c = self.t_probability[(f_i, e_j)] / Z[e_j] # Expected count
                        self.fe_count[(f_i, e_j)] += c # Increment count(e|f) by expected count
                        self.f_count[f_i] += c # Increment count(f) by expected count

            # M-step
            for (f_i, e_j) in self.fe_count.keys():
                self.t_probability[(f_i,e_j)] = self.fe_count[(f_i, e_j)] / self.f_count[f_i]

        return


    def _align(self, bitext):
        '''Align by most probable alignment method.
        '''
        for (n, (f, e)) in enumerate(bitext):
            alignment = []
            for (i, f_i) in enumerate(f):
                best_p = 0
                best_j = 0
                for (j, e_j) in enumerate(e):
                    if self.t_probability[(f_i,e_j)] > best_p:
                        best_p = self.t_probability[(f_i,e_j)]
                        best_j = j
                sys.stdout.write("%i-%i " % (i,best_j))
            sys.stdout.write("\n")
        return

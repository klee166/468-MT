#!/usr/bin/env python

## This program is built on the align program written for CS468 MT @ JHU.
## The program implements the IBM Model 1, a lexical translation model,
## for English to French word alignments.

import sys
from collections import defaultdict
from nltk.stem import SnowballStemmer

reload(sys)
sys.setdefaultencoding("latin-1") # required for stemming

class IBM1:

    e_count = defaultdict(float) # Expected count of each English word
    fe_count = defaultdict(float) # Expected count of each (e,f) word pair
    t_probability = defaultdict(float) # Lexical translation probability

    def __init__(self, data="en600.468/aligner/data/hansards", num_sents=sys.maxint):
        f_data = "%s.%s" % (data, "f")
        e_data = "%s.%s" % (data, "e")

        bitext = [[sentence.strip().split() for sentence in pair] for pair in zip(open(e_data), open(f_data))[:num_sents]]

        # Stem words before model training
        french_stemmer = SnowballStemmer("french")
        english_stemmer = SnowballStemmer("english")
        bitext_stemmed = []
        for (n, (e, f)) in enumerate(bitext):
            f_stemmed = [french_stemmer.stem(word.decode("utf-8")) for word in f]
            e_stemmed = [english_stemmer.stem(word) for word in e]
            bitext_stemmed.append([e_stemmed, f_stemmed])

        bitext = bitext_stemmed

        self._train(bitext)
        self._align(bitext)


    def _train(self, bitext):
        ''' Training IBM Model 1.
        '''
        # Initializing lexical translation probability distribution t(f|e) with uniform distribution
        for (n, (e, f)) in enumerate(bitext):
            for e_j in set(e):
                for f_i in set(f):
                    self.t_probability[(e_j,f_i)] = 1.0 / len(f)

        Z = dict() # Normalization term for counts
        k = 0

        # Expectation maximization until iteration count met
        while k < 5:
            k += 1

            # Set count(f|e) = 0 for all (e,f) and set total(e) = 0 for all e
            for (n, (e, f)) in enumerate(bitext):
                for e_j in set(e):
                    self.e_count[e_j] = 0
                    for f_i in set(f):
                        self.fe_count[(e_j,f_i)] = 0

            for (n, (e, f)) in enumerate(bitext):
                # E-step (a): Compute normalization
                for (i, f_i) in enumerate(f):
                    Z[f_i] = 0.0
                    for (j, e_j) in enumerate(e):
                        Z[f_i] += self.t_probability[(e_j, f_i)]
                # E-step (b): Calculate expected counts
                for (i, f_i) in enumerate(f):
                    for (j, e_j) in enumerate(e):
                        c = self.t_probability[(e_j, f_i)] / Z[f_i] # Expected count
                        self.fe_count[(e_j, f_i)] += c # Increment count(e|f) by expected count
                        self.e_count[e_j] += c # Increment count(f) by expected count

            # M-step
            for (e_j, f_i) in self.fe_count.keys():
                self.t_probability[(e_j,f_i)] = self.fe_count[(e_j, f_i)] / self.e_count[e_j]

        return


    def _align(self, bitext):
        '''Align by most probable alignment method.
        '''
        for (n, (e, f)) in enumerate(bitext):
            alignment = []
            for (j, e_j) in enumerate(e):
                best_p = 0
                best_i = 0
                for (i, f_i) in enumerate(f):
                    if self.t_probability[(e_j,f_i)] > best_p:
                        best_p = self.t_probability[(e_j,f_i)]
                        best_i = i
                sys.stdout.write("%i-%i " % (best_i,j))
            sys.stdout.write("\n")
        return

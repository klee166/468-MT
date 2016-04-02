#!/usr/bin/env python

## This program is built on the reranker program written for CS468 MT @ JHU.

import optparse
import sys, os
from random import randint
from math import fabs
from collections import defaultdict
from numpy import array, zeros, sign, linalg
from sklearn import svm
baseline_path = os.path.join(os.getcwd()[:-1], "en600.468/reranker/")
if baseline_path not in sys.path:
    sys.path.insert(0, baseline_path)
import bleu

optparser = optparse.OptionParser()
optparser.add_option("-k", "--kbest-list", dest="input", default=baseline_path+"data/dev+test.100best", help="100-best translation lists")
optparser.add_option("-l", "--lm", dest="lm", default=-1.0, type="float", help="Language model weight")
optparser.add_option("-t", "--tm1", dest="tm1", default=-0.5, type="float", help="Translation model p(e|f) weight")
optparser.add_option("-s", "--tm2", dest="tm2", default=-0.5, type="float", help="Lexical translation model p_lex(f|e) weight")
optparser.add_option("-r", "--reference", dest="reference", default=baseline_path+"data/dev.ref", help="Target language reference sentences")

(opts, _) = optparser.parse_args()
weights = {'p(e)'       : float(opts.lm) ,
           'p(e|f)'     : float(opts.tm1),
           'p_lex(f|e)' : float(opts.tm2)}

ref = [line.strip().split() for line in open(opts.reference)]
all_hyps = [pair.split(' ||| ') for pair in open(opts.input)]
num_sents = len(zip(ref, all_hyps))

# Calculate the "gold" scoring function G
# which is just the local BLEU score here.
all_scores = defaultdict(list)
for s in xrange(0, num_sents):
    hyps_for_one_sent = all_hyps[s * 100:s * 100 + 100]
    for (num, hyp, feats) in hyps_for_one_sent:
        stats = [0 for i in xrange(10)]
        stats = [sum(scores) for scores in zip(stats, bleu.bleu_stats(hyp.split(" "), ref[s]))]
        score = bleu.bleu(stats)
        all_scores[s].append( (score, hyp, feats) )

def tune():
    ''' Finds best weight w '''
    w = array([[float(opts.lm), float(opts.tm1), float(opts.tm2)]])
    binary_classifier = svm.SVC(kernel="linear")

    for _ in range(0,5): # for desired number of iterations
        X, y = [], []
        for s in xrange(0, num_sents):
            samples = sampler(s, 5000, 50, 0.05)
            for (feats, sign) in samples:
                X.append(feats)
                y.append(sign)

        # Optimize
        binary_classifier.fit(X,y)
        coef = binary_classifier.coef_.ravel() / linalg.norm(binary_classifier.coef_)

    return coef

def sampler(s, tau=5000, xi=50, alpha=0.05):
    ''' @params
    tau: number of samples in n-best list per source sentence
    alpha: sample acceptance cut-off
    xi: training data generated from tau
    '''
    v = list() # sample list
    for _ in xrange(0, tau):
        # Choose (j, j') uniformly at random
        index_1 = randint(0, len(all_scores[s])-1)
        index_2 = randint(0, len(all_scores[s])-1)
        (score_1, hyp_1, feats_1) = all_scores[s][index_1]
        (score_2, hyp_2, feats_2) = all_scores[s][index_2]
        # Add to v with probability alpha*|g(i,j) - g(i,j')|
        if fabs(score_1 - score_2) > alpha:
            v.append((fabs(score_1 - score_2), score_1, score_2, feats_1, feats_2))

    V = list()
    for (g, g_1, g_2, feats_1, feats_2) in sorted(v, reverse=True)[:xi]:
        features_1, features_2 = zeros(3), zeros(3)
        for i, feat in enumerate(feats_1.split(" ")):
            (k, v) = feat.split("=")
            features_1[i] = v
        for i, feat in enumerate(feats_2.split(" ")):
            (k, v) = feat.split("=")
            features_2[i] = v
        V.append((features_1 - features_2, sign(g_1 - g_2)))
        V.append((features_2 - features_1, sign(g_2 - g_1)))

    return V

w_star = tune()

for s in xrange(0, num_sents):
    hyps_for_one_sent = all_hyps[s * 100:s * 100 + 100]
    (best_score, best) = (-1e300, '')
    for (num, hyp, feats) in hyps_for_one_sent:
        score = 0.0
        for i, feat in enumerate(feats.split(' ')):
            (k, v) = feat.split('=')
            score += w_star[i] * float(v)
        if score > best_score:
            (best_score, best) = (score, hyp)
    try:
        sys.stdout.write("%s\n" % best)
    except (Exception):
        sys.exit(1)

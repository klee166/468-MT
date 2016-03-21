#!/usr/bin/env python
import argparse # optparse is deprecated
from itertools import islice # slicing for iterators

a = 0.16
 
def word_matches(h, ref):
    return sum(1 for w in h if w in ref)

# def meteor(h, ref):
#     return ((percision(h, ref) * recall(h, ref))/ (((1-a) * recall(h, ref)) + ( a * percision(h, ref))))

def percision(h, ref):
    len_h = len(h)
    len_h = len_h + 0.0
    word_m = word_matches(h, ref)
    return (word_m / len_h)

def recall(h, ref):
    len_ref = len(ref)
    len_ref = len_ref + 0.0
    word_m = word_matches(h, ref)
    return (word_m / len_ref)

def meteor(h, ref):
    r = recall(h, ref)
    p = percision(h, ref)
    if (r == 0 or p == 0 ):
        return 0
    else: 
        return ( p * r ) / ( ( (1 - a) * r ) + (a * p) )

 
def main():
    parser = argparse.ArgumentParser(description='Evaluate translation hypotheses.')
    parser.add_argument('-i', '--input', default='data/hyp1-hyp2-ref',
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

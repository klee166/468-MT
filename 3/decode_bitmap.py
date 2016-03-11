import optparse
import sys
import models
from collections import namedtuple

# Three little utility functions:
def bitmap(sequence):
  """ Generate a coverage bitmap for a sequence of indexes """
  return reduce(lambda x,y: x|y, map(lambda i: long('1'+'0'*i,2), sequence), 0)

def bitmap2str(b, n, on='o', off='.'):
  """ Generate a length-n string representation of bitmap b """
  return '' if n==0 else (on if b&1==1 else off) + bitmap2str(b>>1, n-1, on, off)

def extract_english(h): 
  return "" if h.predecessor is None else "%s%s " % (extract_english(h.predecessor), h.phrase.english)

optparser = optparse.OptionParser()
optparser.add_option("-i", "--input", dest="input", default="data/input", help="File containing sentences to translate (default=data/input)")
optparser.add_option("-t", "--translation-model", dest="tm", default="data/tm", help="File containing translation model (default=data/tm)")
optparser.add_option("-l", "--language-model", dest="lm", default="data/lm", help="File containing ARPA-format language model (default=data/lm)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to decode (default=no limit)")
optparser.add_option("-k", "--translations-per-phrase", dest="k", default=1, type="int", help="Limit on number of translations to consider per phrase (default=1)")
optparser.add_option("-s", "--stack-size", dest="s", default=25, type="int", help="Maximum stack size (default=1)")
optparser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False,  help="Verbose mode (default=off)")
opts = optparser.parse_args()[0]

tm = models.TM(opts.tm, opts.k)
lm = models.LM(opts.lm)
french = [tuple(line.strip().split()) for line in open(opts.input).readlines()[:opts.num_sents]]

# tm should translate unknown words as-is with probability 1
for word in set(sum(french,())):
  #print "word is: ", word #added extra 
  if (word,) not in tm:
    tm[(word,)] = [models.phrase(word, 0.0)]

sys.stderr.write("Decoding %s...\n" % (opts.input,))
for f in french:
  # The following code implements a monotone decoding
  # algorithm (one that doesn't permute the target phrases).
  # Hence all hypotheses in stacks[i] represent translations of 
  # the first i words of the input sentence. You should generalize
  # this so that they can represent translations of *any* i words.
  hypothesis = namedtuple("hypothesis", "logprob, lm_state, predecessor, phrase, v ,fi, fj, f_translated")
  #v is a bit map
  #f_translated is the number of french words translated
  initial_hypothesis = hypothesis(0.0, lm.begin(), None, None, bitmap(range(0,0)), 0,0, 0)
  #print "lm begin is ", lm.begin(), <s>
  stacks = [{} for _ in f] + [{}]
  stacks[0][lm.begin()] = initial_hypothesis
  for i, stack in enumerate(stacks[:-1]):
    for h in sorted(stack.itervalues(),key=lambda h: -h.logprob)[:opts.s]: # prune
      for fi in xrange(len(f)):
        for fj in xrange(fi+1, len(f)+1):
          if f[fi:fj] in tm:
            if (bitmap(range(fi,fj)) & h.v == 0):
              new_v = bitmap(range(fi,fj)) | h.v
              f_translated = h.f_translated + (fj-fi)
              if (abs(fi-h.fi) < 2) or (abs(fj-h.fj) < 2) or (abs(fi-bitmap2str(h.v, len(f)).index('.'))<1): 
                for phrase in tm[f[fi:fj]]:
                  logprob = h.logprob + phrase.logprob
                  lm_state = h.lm_state
                  for word in phrase.english.split():
                    (lm_state, word_logprob) = lm.score(lm_state, word)
                    logprob += word_logprob
                  logprob += lm.end(lm_state) if f_translated == len(f) else 0.0 #only added if whole sentence  translated
                  new_hypothesis = hypothesis(logprob, lm_state, h, phrase, new_v, fi, fj, f_translated)
                  if lm_state not in stacks[f_translated] or (stacks[f_translated][lm_state].v == new_v and \
                    abs(stacks[f_translated][lm_state].logprob) > abs(logprob)):
                    stacks[f_translated][lm_state] = new_hypothesis
                  lm_state_del = []
                  for old_lm_state in stacks[f_translated]:
                    if stacks[f_translated][old_lm_state].v == new_v and (old_lm_state != lm_state):
                      if extract_english(stacks[f_translated][old_lm_state]) == extract_english(new_hypothesis):
                        if abs(stacks[f_translated][old_lm_state].logprob)  > abs(logprob):
                          lm_state_del.append(old_lm_state)
                        elif(stacks[f_translated][lm_state] == new_hypothesis):
                          lm_state_del.append(lm_state)
                  for lms in lm_state_del:
                    del stacks[f_translated][lms]

  winner = max(stacks[-1].itervalues(), key=lambda h: h.logprob)
  print extract_english(winner)

  if opts.verbose:
    def extract_tm_logprob(h):
      return 0.0 if h.predecessor is None else h.phrase.logprob + extract_tm_logprob(h.predecessor)
    tm_logprob = extract_tm_logprob(winner)
    sys.stderr.write("LM = %f, TM = %f, Total = %f\n" % 
      (winner.logprob - tm_logprob, tm_logprob, winner.logprob))

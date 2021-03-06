#!/usr/bin/env python

## This program is built on the decode program written for CS468 MT @ JHU.
## The program implements the Greedy hill-climbing algorithm decoder.

import optparse
import sys, os
baseline_path = os.path.join(os.getcwd()[:-1], "en600.468/decoder/")
if baseline_path not in sys.path:
     sys.path.insert(0, baseline_path)
import models
from collections import namedtuple
import re

# Three little utility functions:
def bitmap(sequence):
  """ Generate a coverage bitmap for a sequence of indexes """
  return reduce(lambda x,y: x|y, map(lambda i: long('1'+'0'*i,2), sequence), 0)

def bitmap2str(b, n, on='o', off='.'):
  """ Generate a length-n string representation of bitmap b """
  return '' if n==0 else (on if b&1==1 else off) + bitmap2str(b>>1, n-1, on, off)

def logadd10(x,y):
  """ Addition in logspace (base 10): if x=log(a) and y=log(b), returns log(a+b) """
  return x + math.log10(1 + pow(10,y-x))

def extract_english(h):
  return "" if h.predecessor is None else "%s%s " % (extract_english(h.predecessor), h.phrase.english)

def extract_phrase_seg(h):
	seg_english = []
	if (h.phrase!=None):
		seg_english.append(h.phrase)
	while (h.predecessor !=None):
		h = h.predecessor
		if (h.phrase!=None):
			seg_english.append(h.phrase)
	return seg_english

def get_source_phrase(f):
	M= dict()
	#find all possible f phrase spans
	for fi in xrange(len(f)):
		for fj in xrange(fi+1, len(f)+1):
			if f[fi:fj] in tm:
				if fi in M:
					M[fi].append(fj)
				else:
					M[fi] = [fj]
	#num source words
	return M

#finds the source phrase with the smallest number of source phrases
def find_seed(f, M):
	S = set()
	s_words =0;
	chart = [{} for _ in f] + [{}]
	chart[0][0] = S
	for fi, sums in enumerate(chart[:-1]):
		for v in sums:
			for fj in M[fi]:
				if bitmap(range(fi,fj)) & v == 0:
					new_v = bitmap(range(fi, fj)) | v
					s_words = bitmap2str(new_v, len(f)).count('o')
					if new_v in chart[s_words] and (chart[s_words][new_v] != None):
						chart[s_words][new_v] = min_s(chart[s_words][new_v], sums[v], fi, fj)
					elif(chart[bitmap2str(v, len(f)).count('o')][v]):
						chart[s_words][new_v] = [(fi,fj)]
						chart[s_words][new_v].extend(chart[bitmap2str(v, len(f)).count('o')][v])
					else:
						chart[s_words][new_v] = [(fi, fj)]
	goal = bitmap(range(len(f)))
	if goal in chart[len(f)]:
		#print "chart lenf goal is ", chart[len(f)][goal]
		return chart[len(f)][goal]

#finds the S with the minimum length
def min_s(prev_S, S, fi, fj):
	if (len(prev_S)<(len(S)+ 1)): #+1 indicated adding the new fi-fj
		return prev_S
	else:
		return_list = [(fi,fj)]
		return_list.extend(S)
		return return_list

def find_seed_trans(seg_f, f):
	#for h in sorted(stack.itervalues(),key=lambda h: -h.logprob)[:opts.s]:
	hypothesis = namedtuple("hypothesis", "logprob, lm_state, predecessor, phrase, seg_f")
	initial_hypothesis = hypothesis(0.0, lm.begin(), None, None,seg_f)
	ei = 0
	ej = 0
	seg_e = []
	h = initial_hypothesis
	for x in seg_f:
		phrase = tm[f[x[0]:x[1]]][0]
		logprob = h.logprob + phrase.logprob
		lm_state = h.lm_state
		for word in phrase.english.split():
			(lm_state, word_logprob) = lm.score(lm_state, word)
			logprob += word_logprob
			ej +=1
		logprob += lm.end(lm_state) if x[1] == len(f) else 0.0 #only added if the if statement is true
		seg_e.extend([(ei,ej)])
		ei = ej
		new_hypothesis = hypothesis(logprob, lm_state, h, phrase, seg_f)
		h = new_hypothesis
	return (h)

def neighborhood(h, M, f, seg_f):
	rtn_hyp = []
	#move
	rtn_hyp.extend(split(h, M, f)) #works fine
	rtn_hyp.extend(replace(h)) #works fine
	rtn_hyp.extend(move(h)) #works
	rtn_hyp.extend(swap(h)) #works fine
	rtn_hyp.extend(bireplace(h)) #works
	rtn_hyp.extend(merge(h, M, f)) #works fine...

	return rtn_hyp

def bireplace(h):
	english_seg = extract_phrase_seg(h)
	english_seg.reverse()
	# for phrase in english_seg:
	# 	print "phrase is ", phrase

	# if (f[5:7] in tm):
	# 	for phrase in tm[f[5:7]]:
	# 		print "[5:7]"
	# 		print phrase

	new_english_seg_1 = []
	new_english_seg_2 = []

	for f_span1 in h.seg_f:
		if ((h.seg_f.index(f_span1) + 1) < len(h.seg_f)):
			for phrase1 in tm[f[f_span1[0]:f_span1[1]]]:
				# print "phrase1 is", phrase1
				if phrase1 in english_seg:
					phrase1_current_index =english_seg.index(phrase1)
					phrase1_current = phrase1
					break
					# print "english_temp_seg is ", english_temp_seg
					# print "phrase current is ", phrase
			for phrase1 in tm[f[f_span1[0]:f_span1[1]]]:
				# print "phrase1 is ", phrase
				if phrase1 != phrase1_current:
				# print "phrase2 is ", phrase
					english_temp_seg_insert=english_seg[:]
					english_temp_seg_insert.remove(phrase1_current)
					english_temp_seg_insert.insert(phrase1_current_index, phrase1)
					new_english_seg_1.append(english_temp_seg_insert)
					# print "new_english_seg_1 is", new_english_seg_1
			f_span2 = h.seg_f[(h.seg_f.index(f_span1) + 1)]

			for phrase2 in tm[f[f_span2[0]:f_span2[1]]]:
				if phrase2 in english_seg:
					phrase2_current_index = english_seg.index(phrase2)
					phrase2_current = phrase2

			for phrase2 in tm[f[f_span2[0]:f_span2[1]]]:
				if phrase2 != phrase2_current:
					for english_seg1 in new_english_seg_1:
						english_seg2 = english_seg1[:]
						english_seg2.remove(phrase2_current)
						english_seg2.insert(phrase2_current_index, phrase2)
						new_english_seg_2.append(english_seg2)



	rtn_hyp=find_trans_r_m_s(new_english_seg_2, h)
	return rtn_hyp

def swap(h):
	english_seg = extract_phrase_seg(h)
	english_seg.reverse()

	new_english_seg = []

	for phrase1 in english_seg:
		phrase1_index =english_seg.index(phrase1)
		if (phrase1_index + 1 < len(english_seg)):
			phrase2 = english_seg[phrase1_index + 1]
			english_temp_seg = english_seg[:]
			del english_temp_seg[phrase1_index + 1]
			english_temp_seg.insert(phrase1_index, phrase2)
			new_english_seg.append(english_temp_seg)

	# print "printing swap...."
	# for english_seg in new_english_seg:
	# 	for phrase in english_seg:
	# 		print phrase.english, " "


	rtn_hyp=find_trans_r_m_s(new_english_seg, h)
	return rtn_hyp


def move(h):
	#can't really check it doesn't happen so far..
	english_seg = extract_phrase_seg(h)
	english_seg.reverse()

	new_english_seg = []

	#find the fspan corresponding to the phrase
	for f_span1 in h.seg_f:
		for phrase in tm[f[f_span1[0]:f_span1[1]]]:
			if phrase in english_seg:
				phrase1 = phrase
				phrase1_index = english_seg.index(phrase1)
				break
		index_f_span1 = h.seg_f.index(f_span1)
		if (index_f_span1+1) < len(h.seg_f):
			f_span2 = h.seg_f[index_f_span1+1]
			for phrase in tm[f[f_span2[0]:f_span2[1]]]:
				if phrase in english_seg:
					phrase2 = phrase
					phrase2_index = english_seg.index(phrase2)
					break
			if abs(phrase1_index  - phrase2_index) >=3:
				english_temp_seg = english_seg[:]
				if abs(phrase1_index - index_f_span1) < abs(phrase2_index - (index_f_span1 + 1)):
					del english_temp_seg[phrase2_index]
					english_temp_seg.insert((phrase1_index+1), phrase2)
					new_english_seg.append(english_temp_seg)
				else:
					del english_temp_seg[phrase1_index]
					english_temp_seg.insert((phrase2_index), phrase1)
					new_english_seg.append(english_temp_seg)

	# print "new_english_seg move is ", new_english_seg
	# for english_seg_p in new_english_seg:
	# 	for phrase in english_seg_p:
	# 		print phrase.english, " "
	rtn_hyp=find_trans_r_m_s(new_english_seg, h)
	return rtn_hyp

def replace(h):
	english_seg = extract_phrase_seg(h)
	english_seg.reverse()

	new_english_seg = []

	for f_span in h.seg_f:
		for phrase in tm[f[f_span[0]:f_span[1]]]:
			if phrase in english_seg:
				e_index_del =english_seg.index(phrase)
				phrase_current = phrase
				english_temp_seg = english_seg[:]
				del english_temp_seg[e_index_del]
				# print "english_temp_seg is ", english_temp_seg
				# print "phrase current is ", phrase
				for phrase in tm[f[f_span[0]:f_span[1]]]:
					# print "phrase1 is ", phrase
					if phrase != phrase_current:
						# print "phrase2 is ", phrase
						english_temp_seg_insert = english_temp_seg[:]
						english_temp_seg_insert.insert(e_index_del, phrase)
						new_english_seg.append(english_temp_seg_insert)

	# print "new_english_seg is ", new_english_seg
	# print "new_english_seg is ", new_english_seg

	rtn_hyp=find_trans_r_m_s(new_english_seg, h)
	return rtn_hyp

def find_trans_r_m_s(new_english_seg, h):
	rtn_hyp = []
	seg_f = h.seg_f
	hypothesis = namedtuple("hypothesis", "logprob, lm_state, predecessor, phrase, seg_f")
	for english_seg in new_english_seg:
		initial_hypothesis = hypothesis(0.0, lm.begin(), None, None, seg_f)
		h = initial_hypothesis
		i=0;
		for x in seg_f:
			phrase = english_seg[i]
			logprob = h.logprob + phrase.logprob
			lm_state = h.lm_state
			for word in phrase.english.split():
				(lm_state, word_logprob) = lm.score(lm_state, word)
				logprob += word_logprob
			logprob += lm.end(lm_state) if x[1] == len(f) else 0.0 #only added if the if statement is true
			new_hypothesis = hypothesis(logprob, lm_state, h, phrase, seg_f)
			h = new_hypothesis
			i+=1
		rtn_hyp.append(h)
	return rtn_hyp


def find_trans_split(h, old_fspan , new_fspan_1 , new_fspan_2, new_seg_f, f):

	english_seg = extract_phrase_seg(h)
	english_seg.reverse()
	# print "h sef is ", h.seg_f
	# print "new sef is ", new_seg_f
	# print "english_seg is ", english_seg
	# print "new_fspan_1 is ", new_fspan_1
	# print "new_fspan_2 is ", new_fspan_2
	# print "old_fspan is ", old_fspan
	# print "f is ", f


	phrase1=tm[f[new_fspan_1[0]:new_fspan_1[1]]][0]
	phrase2=tm[f[new_fspan_2[0]:new_fspan_2[1]]][0]

	for phrase in tm[f[old_fspan[0]:old_fspan[1]]]:
		# print "old_fspan[0] is ", old_fspan[0]
		# print "old_fspan[1] is ", old_fspan[1]
		# print "phrase is ", phrase
		if phrase in english_seg:
			e_index_del =english_seg.index(phrase)

	del english_seg[e_index_del]

	#new englsih seg being created
	english_seg.insert(e_index_del,phrase1)
	english_seg.insert((e_index_del+1),phrase2)

	hypothesis = namedtuple("hypothesis", "logprob, lm_state, predecessor, phrase, seg_f")
	initial_hypothesis = hypothesis(0.0, lm.begin(), None, None, new_seg_f)
	h = initial_hypothesis

	i=0;
	for x in new_seg_f:
		phrase = english_seg[i]
		logprob = h.logprob + phrase.logprob
		lm_state = h.lm_state
		for word in phrase.english.split():
			(lm_state, word_logprob) = lm.score(lm_state, word)
			logprob += word_logprob
		logprob += lm.end(lm_state) if x[1] == len(f) else 0.0 #only added if the if statement is true
		new_hypothesis = hypothesis(logprob, lm_state, h, phrase, new_seg_f)
		h = new_hypothesis
		i+=1
	# print "h returning from split ", extract_english(h)
	return h

def split(h, M, f):
	best_seg_f = h.seg_f
	best_hypothesis = h
	rtn_h = []
	for key, values in M.items():
		for value in values:
			if (key,value) in best_seg_f:
				continue
			for x in best_seg_f:
				if (x[0] ==key and value < x[1]) and (M[value]!=None) and (x[1] in M[value]):
					new_seg_f = best_seg_f[:]
					new_seg_f.extend([(x[0],value), (value, x[1])])
					new_seg_f.remove((x[0],x[1]))
					new_seg_f  =  sorted(new_seg_f, key=lambda x: x[0])
					h=find_trans_split(best_hypothesis, x , (x[0],value), (value,x[1]), new_seg_f, f)
					if (h !=None) and (abs(h.logprob) < abs(best_hypothesis.logprob)):
						rtn_h.append(h)
						break
	# print "rtn_h from split is ", rtn_h
	return (rtn_h)

def find_trans_merge(h,old_fspan1 , old_fspan2 , new_fspan, new_seg_f, f):

	english_seg = extract_phrase_seg(h)
	english_seg.reverse()
	# print "english_seg is ", english_seg

	phrase=tm[f[new_fspan[0]:new_fspan[1]]][0]

	for old_phrase_1 in tm[f[old_fspan1[0]:old_fspan1[1]]]:
		# print "phrase is ", phrase
		if old_phrase_1 in english_seg:
			current_old_phrase_1 = old_phrase_1
			old_phrase_1_index = english_seg.index(old_phrase_1)
			break

	for old_phrase_2 in tm[f[old_fspan2[0]:old_fspan2[1]]]:
		# print "phrase is ", phrase
		if old_phrase_2 in english_seg:
			current_old_phrase_2 = old_phrase_2
			break


	english_seg.remove(current_old_phrase_1)
	english_seg.remove(current_old_phrase_2) #basically deleting old_phrase_2_index

	#new english seg being created
	english_seg.insert(old_phrase_1_index,phrase)

	hypothesis = namedtuple("hypothesis", "logprob, lm_state, predecessor, phrase, seg_f")
	initial_hypothesis = hypothesis(0.0, lm.begin(), None, None, new_seg_f)
	h = initial_hypothesis

	i=0;
	for x in new_seg_f:
		phrase = english_seg[i]
		logprob = h.logprob + phrase.logprob
		lm_state = h.lm_state
		for word in phrase.english.split():
			(lm_state, word_logprob) = lm.score(lm_state, word)
			logprob += word_logprob
		logprob += lm.end(lm_state) if x[1] == len(f) else 0.0 #only added if the if statement is true
		new_hypothesis = hypothesis(logprob, lm_state, h, phrase, new_seg_f)
		h = new_hypothesis
		i+=1
	# print "h returning from split ", extract_english(h)
	return h

def merge(h, M, f):
	best_seg_f = h.seg_f
	best_hypothesis = h
	rtn_h = []
	for key, values in M.items():
		for value in values:
			if (key,value) in best_seg_f:
				continue
			for x in best_seg_f:
				if (x[0] ==key and value > x[1]) and ((x[1], value) in best_seg_f):
					new_seg_f = [(key, value)]
					new_seg_f.extend(best_seg_f)
					new_seg_f.remove(x)
					new_seg_f.remove((x[1], value))
					new_seg_f  =  sorted(new_seg_f, key=lambda x: x[0])
					h=find_trans_merge(best_hypothesis, x , (x[1], value), (key, value), new_seg_f, f)
					if (h !=None) and (abs(h.logprob) < abs(best_hypothesis.logprob)):
						rtn_h.append(h)
						break
	# print "rtn_h from split is ", rtn_h
	return (rtn_h)



optparser = optparse.OptionParser()
optparser.add_option("-i", "--input", dest="input", default=baseline_path+"data/input", help="File containing sentences to translate (default=data/input)")
optparser.add_option("-t", "--translation-model", dest="tm", default=baseline_path+"data/tm", help="File containing translation model (default=data/tm)")
optparser.add_option("-l", "--language-model", dest="lm", default=baseline_path+"data/lm", help="File containing ARPA-format language model (default=data/lm)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to decode (default=no limit)")
optparser.add_option("-k", "--translations-per-phrase", dest="k", default=sys.maxint, type="int", help="Limit on number of translations to consider per phrase (default=1)")
optparser.add_option("-s", "--stack-size", dest="s", default=1000, type="int", help="Maximum stack size (default=1)")
optparser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False,  help="Verbose mode (default=off)")
opts = optparser.parse_args()[0]

tm = models.TM(opts.tm, opts.k)
lm = models.LM(opts.lm)

french = [tuple(line.strip().split()) for line in open(opts.input).readlines()[:opts.num_sents]]

# tm should translate unknown words as-is with probability 1
for word in set(sum(french,())):
  if (word,) not in tm:
    tm[(word,)] = [models.phrase(word, 0.0)]

sys.stderr.write("Decoding %s...\n" % (opts.input,))


for f in french:
	hypothesis = namedtuple("hypothesis", "logprob, lm_state, predecessor, phrase, seg_f, seg_e, alignment")
  	M = get_source_phrase(f)
	seg_f = find_seed(f, M)
	seg_f  =  sorted(seg_f, key=lambda x: x[0])
	hypothesis= find_seed_trans(seg_f, f) #find seed translation
	current = hypothesis

	#loop for finding
	for x in xrange(100000000):
		s_current = abs(current.logprob)
		s = s_current
		for h in neighborhood(current, M, f, current.seg_f):
			c=abs(h.logprob)
			if c< s:
				s = c
				best = h
		if s == s_current:
			print extract_english(current)
			break
		else:
			current = best
	# print extract_english(best_hypothesis)

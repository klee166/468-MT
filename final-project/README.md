## Machine Translation for Social Media

**—Collaborated with [Sarah Watanabe](https://github.com/swatana3).**

Currently in Machine Translation, translating social media text is a challenge. User generated content (UGC) is highly noisy (spam, ads), domain unrestricted (anyone anywhere can be there), user-centric (users are given more flexiblilty and choices), generated in high volume, and focused on knowledge and context sharing at the expense of grammatical, spelling, and other linguistic errors.

Therefore, our challenges lies in being able to create a machine translation system that

1. is large-scale and as close to real-time as possible in 
data management,
2. will preserve the meaning of words, and
3. handle errors in linguistics and in canonical writing (verbs, grammers, typos, wrong punctuation, unstructured syntax, etc.).

## Chosing a translation model

Currently, we're considering two approaches: Compositional Distribution Models (CDM) and Neural Machine Translation (NMT) models.

#### Compositional Distribution Models

Distributional semantic modelling hypothesizes that the meaning of a word is related to context (Harris, 1968; Firth, 1957). In this approach, word meanings are represented as vectors based on distribution of co-occuring words within context. This ties semantic similarity to vector similarity, and linear algebra can used to solve for problems.

What CDM does is that it ties DSM to formal semantic rules/models. Thus, instead of word vectors, we now work with sentence vectors. The sentence vectors are generated from the word vectors (there are a number of ways this can be done, a few of approaches being additive, tensor-based, and deep learning).

#### Neural Machine Translation models

Neural-based machine translation research dates back to Forcada and Neco, 1997. The base of most neural-based models is the encoder-decoder architecture. A variable-length input is encoded as a fixed-length vector (or a sequence of vectors of which a subset is chosen during decoding, *à la* Bengio et al., 2013), which is then decoded to a variable-length output. The hidden state *h* is where all the magic of translation happens.

The training data is a parallel corpus of sentence pairs, and the goal is to maximize the log-likelihood of probability of translation from a source to target, just like any traditional SMT model.

#### Which is better?

Recently, work has been done to combine the two approaches. However, there are still cases where traditional SMT models like Moses (a phrase-based model) outperform the former. Thus, one of our goals is to review current literature to answer questions like: in which scenarios is NMT better than tranditional SMT, and what are the properties of sentences for which NMT performs well (for example, source sentence length, vocabulary size)?


## Choosing data

For training, we're considering using either [microtopia](http://www.cs.cmu.edu/~lingwang/microtopia/) or [subtiles from OPUS](http://opus.lingfil.uu.se/OpenSubtitles2016.php) for English-Japanese senence pairs (subtitles because it'd be more representative of colloquial language). Testing can then be done on crawled data from Twitter.

## Resources

##### Neural-based MT
1. [Neural Machine Translation by Jointly Learning to Align and Translate](http://arxiv.org/pdf/1409.0473.pdf). Bengio et al., 2013.
2. [Neural Machine Translation of Rare Words with Subword Units](http://arxiv.org/pdf/1508.07909v3.pdf). Sennrich et al., 2015.
3. [Character-Aware Neural Language Models](http://arxiv.org/pdf/1508.06615.pdf). Kim et al., 2015.
4. [A Character-Level Decoder without Explicit Segmentation for Neural Machine Translation](http://arxiv.org/pdf/1603.06147.pdf). Chung et al., 2016.


##### Compositional Distributional Models
1. [Compositional Operators in Distributional Semantics](https://www.cs.ox.ac.uk/files/6248/kartsaklis-springer.pdf). Kartsaklis, 2014.

##### Works usings Twitter datasets
1. [Automatic Keyword Extraction on Twitter](http://www.cs.cmu.edu/~lingwang/papers/acl2015-3.pdf). Ling et al, 2015.

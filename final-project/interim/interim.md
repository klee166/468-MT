## Implementing a Neural Network Model for Translation of Japanese-English Tweets

**—Collaborated with [Sarah Watanabe](https://github.com/swatana3).**

Currently in Machine Translation, translating social media text is a challenge. User generated content (UGC) is highly noisy (spam, ads), domain unrestricted (anyone anywhere can be there), user-centric (users are given more flexiblilty and choices), generated in high volume, and focused on knowledge and context sharing at the expense of grammatical, spelling, and other linguistic errors.

Therefore, our challenges lies in being able to create a machine translation system that

1. is large-scale and as close to real-time as possible in 
data management,
2. will preserve the meaning of words, and
3. will handle errors in linguistics and in canonical writing (verbs, grammers, typos, wrong punctuation, unstructured syntax, etc.).


## Neural networks for translation

Neural-based machine translation research dates back to Forcada and Neco (1997). While traditional Statistical Machine Translation (SMT) models rely on pre-designed features (like POS tags, etc.), neural machine translation models do not make use of any pre-designed features. That is to say, all features they learn are from training, and this maximizes their performance.

Recently proposed NMT models, like those by Kalchbrenner and Blunsom (2013), Sutskever *et al.* (2014), Cho *et al.* (2014), and Bahdanau *et al.* (2015) have showed comparable performace to state-of-the-art SMT models like Moses (Koehn et al., 2003). The base of all these neural-based models is [mostly] the *encoder-decoder* architecture. A variable-length input is encoded as a fixed-length vector, which is then decoded to a variable-length output (Sutskever *et al.*, 2014; Cho *et al.*, 2014). The hidden state *h* is where all the magic of translation happens.

In this simple encoder-decoder architecture, one is essentially cramming information of an entire sentence into a single vector. This is not reasonable, and indeed, it has been shown that as sentence length increases, the performance of the neural network degrades (Cho *et al.*, 2014).

We will survey the current state-of-the-art neural network architecture (Bahdanau *et al.*, 2015), and use it to translate tweets from Japanese to English.

## Model

The current state-of-the-art NMT model (RNNSearch) makes use of a **Bidirectional RNN (BiRNN)** to encode the input `x` to a *sequence of vectors*, of which a *subset* is chosen during translation by the **Gated Recursive Unit (GRU)** decoder.

We won't go into depth to describe Recursive Neural Networks (RNN) here (see [this](http://karpathy.github.io/2015/05/21/rnn-effectiveness/) blog post by Andrej Karpathy or [this](http://www.wildml.com/2015/09/recurrent-neural-networks-tutorial-part-1-introduction-to-rnns/) tutorial by Denny Britz for well-written introductions), but only focus on the RNN extensions used in the chosen model.

#### The BiRNN Encoder

While in a vanilla RNN the output `y` is dependent on current input `x` and all previous inputs, a bidirectional RNN assumes that `y` is not only dependent on precedding inputs but also on upcoming inputs.

The forward states $\overrightarrow{h_t}$ are computed as

$$ h_t = (1 - z_t) * h_{t-1} + z_t * \tilde{h_t} $$

where `*` represents element-wise operation, and

$$ \tild{h_t} = \tanh ()

## Data

For training, we're considering using either [microtopia](http://www.cs.cmu.edu/~lingwang/microtopia/) or [subtiles from OPUS](http://opus.lingfil.uu.se/OpenSubtitles2016.php) for English-Japanese senence pairs (subtitles because it'd be more representative of colloquial language). Testing can then be done on crawled data from Twitter.

Our `vocabulary_size` is 30,000, that is, we only use 30,000 most frequent words. Any word not in our vocabulary is mapped to `UNKOWN_TOKEN`. For example, say "Johns" in an infrequent word in our training corpus. Then the sentence "Johns Hopkins University is in Baltimore" will be processed as "UNKOWN_TOKEN Hopkins University is in Baltimore".

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

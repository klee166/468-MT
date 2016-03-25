## Machine Translation for Social Media

**—Collaborated with [Sarah Watanabe](https://github.com/swatana3).**

### Introduction

### Chosing a translation model

Currently, we're considering two approaches: Compositional Distribution Models (CDM) and Neural Machine Translation (NMT) models. Recently, there has been work done to combine the two.

#### Compositional Distribution Models

Distributional semantic modelling hypothesizes that the meaning of a word is related to context (Harris, 1968; Firth, 1957). In this approach, word meanings are represented as vectors based on distribution of co-occuring words within context. This ties semantic similarity to vector similarity, and linear algebra can used to solve for problems.

What CDM does is that it ties DSM to formal semantic rules/models. Thus, instead of word vectors, we now work with sentence vectors. The sentence vectors are generated from the word vectors (there are a number of ways this can be done, a few of approaches being additive, tensor-based, and deep learning).

#### Neural Machine Translation models

Neural-based machine translation research dates back to Forcada and and Neco, 1997. The base of most neural-based models is the encoder-decoder architecture. A varibale-length input in encoded as a fixed-length vector (or a sequence of vectors of which a subset is chosen during decoding *à la* Bengio, 2013), which is then decoded to a variable-length translation.


### Choosing data


### Resources

##### Neural-based models
1. [Neural Machine Translation by Jointly Learning to Align and Translate](http://arxiv.org/pdf/1409.0473v6.pdf). Bengio et al., 2013.

##### Compositional Distribution models
1. [Compositional Operators in Distributional Semantics](https://www.cs.ox.ac.uk/files/6248/kartsaklis-springer.pdf). Kartsaklis, 2014.

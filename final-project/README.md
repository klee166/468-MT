## Machine Translation for Social Media

**—Collaborated with [Sarah Watanabe](https://github.com/swatana3).**

### Chosing a translation model

Currently, we're considering two approaches: Compositional Distribution Models (CDM) and Neural Machine Translation (NMT) models.

#### Compositional Distribution Models

Distributional semantic modelling hypothesizes that the meaning of a word is related to context (Harris, 1968; Firth, 1957). In this approach, word meanings are represented as vectors based on distribution of co-occuring words within context. This ties semantic similarity to vector similarity, and linear algebra can used to solve for problems.

What CDM does is that it ties DSM to formal semantic rules/models. Thus, instead of word vectors, we now work with sentence vectors. The sentence vectors are generated from the word vectors (there are a number of ways this can be done, a few of approaches being additive, tensor-based, and deep learning).

#### Neural Machine Translation models

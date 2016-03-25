## Machine Translation for Social Media

**—Collaborated with [Sarah Watanabe](https://github.com/swatana3).**
### Introduction

Currently in Machine Translation, translating social media text is a challenge. User generated content(UGC) is 1.highly noisy, 2. domain unrestricted (anyone anywhere can be there) 3.user-centric (users are given more flexiblilty and choices) 4.generated in high volume 5. focused on knowledge and context sharing at the expense of grammatical, spelling, and other linguistic errors. Therefore, our challenges lies in being able to create a machine translation system that is 1.large-scale and as close to real-time as possible in 
data management, 2. will preserve the meaning of words, and 3. handle errors in linguistics and in canonical writing (verbs, grammers, typos, wrong punctuation, unstructured syntax).

### Chosing a translation model

Currently, we're considering two approaches: Compositional Distribution Models (CDM) and Neural Machine Translation (NMT) models.

#### Compositional Distribution Models

Distributional semantic modelling hypothesizes that the meaning of a word is related to context (Harris, 1968; Firth, 1957). In this approach, word meanings are represented as vectors based on distribution of co-occuring words within context. This ties semantic similarity to vector similarity, and linear algebra can used to solve for problems.

What CDM does is that it ties DSM to formal semantic rules/models. Thus, instead of word vectors, we now work with sentence vectors. The sentence vectors are generated from the word vectors (there are a number of ways this can be done, a few of approaches being additive, tensor-based, and deep learning).

#### Neural Machine Translation models

Neural-based machine translation research dates back to Forcada and and Neco, 1997. The base of most neural-based models is the encoder-decoder architecture. A varibale-length input in encoded as a fixed-length vector (or ), which is then decoded to a variable-length translation.

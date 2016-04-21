## Inflection

**—Collaborated with [Sarah Watanabe](https://github.com/swatana3).**

In Statistical Machine Translation (SMT), translation from a morphologically poor language [like English] to a morphologically rich language [like Czech] is a complex task. Generally, this is accomplished in a two-fold form: (1) The source language word is stemmed to a lemma, and translated to a target language lemma (assume bijection), (2) the target language lemma is then morphologically corrected to give the proper target word (**target side morphology**: translation into lemma, inflection as post-processing).

Here, we implement an inflection generation model which given a Czech lemma generates inflected Czech word with the best accuracy.


##### Data
We work with a parallel corpus of lemmas, morphological features (for our purposes, only POS tags), and inflected forms. All taken from [here](https://catalog.ldc.upenn.edu/LDC2006T01). Read [this](https://ufal.mff.cuni.cz/pdt2.0/doc/manuals/en/a-layer/html/ch01s02.html) for information on the POS tags used.


##### Model Assumptions

1. Bijective mapping from lemmas to morphological features (only POS tags here) to inflected forms
2. No word-reordering
3. No word addition/deletion

We follow a method similar to the generation method of [Factored Translation Models](http://homepages.inf.ed.ac.uk/pkoehn/publications/emnlp2007-factored.pdf) during training stage. Though in the paper they, *given a lemma*, keep track of `count(word, POS)++`, we instead (for simplicity) keep track of `count(word)++` *given a lemma and a POS*.


##### Result from running on `data/dtest` only
| Inflection Generation Method |  Accuracy  |
| --------------- |:---------:|
| Baseline (no inflection) | 0.33 |
| Most likely word given lemma (from counting) | 0.57 |
| Most likely word given lemma + POS (from counting) | 0.59 |

## Usage

The program can only be run the [CLSP cluster](http://wiki.clsp.jhu.edu/view/Introduction_to_the_CLSP_Grid) due to data distribution restrictions.

```
cat data/dtest.lemma | python inflect.py | ./scripts/grade
```

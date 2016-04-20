## Inflection

**—Collaborated with [Sarah Watanabe](https://github.com/swatana3).**

In Statistical Machine Translation (SMT), translation from a morphologically poor language [like English] to a morphologically rich language [like Czech] is a complex task. Generally, this is accomplished in a two-fold form: (1) The source language word is stemmed and translated to a target language word (assume bijection), (2) the target language word is then morphologically corrected (**target side morphology**: translation into lemma, inflection as post-processing).

Here, we implement an inflection generation model which given a Czech lemma generates inflected Czech word with the best accuracy.

| Inflection Generation Method |  Accuracy  |
| --------------- |:---------:|
| Baseline | 0.57  |

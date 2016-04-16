## Reranking

**—Collaborated with [Sarah Watanabe](https://github.com/swatana3).**

We implemented the pairwise ranking optimization (PRO) method described in [Hopkins, *et al.* (2013)](http://www.aclweb.org/anthology/D11-1125). In this, the ranking problem is reduced to a binary classification task which can be solved using any off-the-shelf linear classifier.

| Reranking method |  Accuracy  |
| --------------- |:---------:|
| Baseline | 0.27351  |
| [Manual] Tweaking | 0.27400 |
| PRO | 0.27961 |

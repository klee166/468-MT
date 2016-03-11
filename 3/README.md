## Decoding

**—Collaborated with [Sarah Watanabe](https://github.com/swatana3).**

The goal of our SMT decoding problem is: given a French sentence **f** and a probability distribution $P(e|f)$, find the most probable english translation of **f**.
$$\hat{e} = \arg\max_e P(e|f) = \arg\max_{e} P(f|e)P(e)$$

In SMT literature, this is re-written as
$$\hat{e},\hat(a) = \arg\max_{e,a} P(f,a|e)P(e)$$
to account for word alignment.

**French-English SMT decoder**

| Model           |  Logprob  |
| --------------- |:---------:|
| Beam (default)  | -1439.87  |
| Beam with adjacent phrase swapping |  |
| Beam with "bad" reordering for max jump k=4 | -1435.77 |
| Beam with "good" reordering for max jump k=4 | -1434.08 |

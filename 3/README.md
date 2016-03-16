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
| Beam with adjacent phrase swapping | -1435.77 |
| Beam with "bad" reordering for max jump k=4 | -1435.77 |
| Beam with "good" reordering for max jump k=4 | -1434.08 |
| + target word reordering | -1434.08 |
| + coverage vector | -1434.08 |
| Greedy hill-climbing | -1360.48 |
| Beam with coverage bitmap and stack size of 2000 (run-time ~2 days) | -1344.41 |

## Usage

The program in the main directory uses the Greedy-hill climbing algorithm for decoding. To run it, enter

```
python greedy.py
```

Number of sentences can be set using `-n` option, and stack size using `-s`.

```
python decode.py -s 10000 > output
```
```
python decode.py -n 1
```

For other options, enter
```
python decode.py --help
```

## Word Alignment

French-English SMT word alignment on Hansards (10k words).

| Model           | AER   |
| --------------- |:-----:|
| Dice (default)  | 68.20%  |
| Dice adjusting threshold | 64.40%  |
| Model 1 p(f\|e) | 49.55% |
| + stemming | 44.84% |
| Model 1 p(e\|f) | 40.89% |
| + stemming | 40.23% |


## Usage

You can select the model using `-m` option: use `f2e` for French-to-English and `e2f` for English-to-French alignment. Data file can be loaded using `-d`, and number of sentences can be set using `-n`.

```
./align -n 1000
```

```
./align -n 10000 -m e2f
```

Note, it is assumed that the French and English data files share the same name (either the default vaue, or specified using `-d`), but different suffixes ("f" and "e" respectively).

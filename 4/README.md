## Evaluator

**—Collaborated with [Sarah Watanabe](https://github.com/swatana3).**

| Evaluator       |  Accuracy  |
| --------------- |:---------:|
| Baseline | 0.449312  |
| METEOR | 0.504380 |
| METEOR + stemming | 0.506101 |
| METEOR + stemming + synonyms | 0.505749 |
| METEOR + synonyms | 0.506884 |


## How alpha was chosen
| Accuracy |  Alpha  |
|----------|:-------:|
| 0.503872 | 0.05 |
| 0.504068 | 0.1 |
| 0.504341 | 0.15 |
| 0.504380 | 0.16 |
| 0.503989 | 0.17 |
| 0.503246 | 0.2 |
| 0.503755 | 0.3 |
| 0.502816 | 0.4 |
| 0.501643 | 0.5 |
| 0.500821 | 0.6 |
| 0.499648 | 0.7 |

Thus, the **best to a hundredth percentile** is

| Accuracy |  Alpha  |
|----------|:-------:|
| 0.504380 | 0.16 |

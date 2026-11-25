| language       | status                            |    n_evals |   seconds |   evals_per_s |
|:---------------|:----------------------------------|-----------:|----------:|--------------:|
| C              | ok                                |      1e+06 |     0.003 |   3.44902e+08 |
| C++            | ok                                |      1e+06 |     0.005 |   2.0023e+08  |
| Go             | skipped (toolchain not installed) |    nan     |   nan     | nan           |
| Rust           | skipped (toolchain not installed) |    nan     |   nan     | nan           |
| Java           | skipped (toolchain not installed) |    nan     |   nan     | nan           |
| JavaScript     | ok                                |      1e+06 |     0.052 |   1.93464e+07 |
| TypeScript     | ok                                |      1e+06 |     0.047 |   2.12758e+07 |
| R              | skipped (toolchain not installed) |    nan     |   nan     | nan           |
| Bash/awk       | ok                                | 100000     |     0.016 |   6.14561e+06 |
| Python (loop)  | ok                                | 100000     |     0.021 |   4.75811e+06 |
| Python (numpy) | ok                                |      1e+06 |     0.023 |   4.28517e+07 |

Same arithmetic in every language; interpreters R, awk and pure-Python use N/10. Timings are machine-dependent.

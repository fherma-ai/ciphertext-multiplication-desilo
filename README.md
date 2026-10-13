# Ciphertext multiplication on DESILO

An answer to `ciphertext-multiplication/ckks@1.0.0` with DESILO's CKKS engine
(`desilofhe` 1.17.0). One directory per point, because the envelope builds the
engine from `config.jsonc` and never reads the point.

The measured call is one library call:

```python
cc.engine.multiply(cts[0], cts[1], cc.keys.relinearization)
```

DESILO tensors, relinearises and rescales inside it, so the window holds the
three stages the specification names.

## How the parameters are asked for, and what that costs the comparison

This is where the row differs from the OpenFHE and FIDESlib ones, which are
built from the same file as each other. DESILO is sized by its ladder and its
slots:

| | `solution-s32768-d10` | `solution-s4096-d20` |
| --- | --- | --- |
| `max_level` | 10 | 20 |
| `slot_count` | 32768 | 4096 |
| `mode` / `thread_count` | parallel / every core | parallel / every core |

The ring, the prime sizes and the special primes are the library's to choose,
and it names no security level: nothing in this configuration refuses a set
that fails to reach 128 bits, where OpenFHE refuses one before the context is
built. The point's `security` parameter is therefore attested differently
here, and the board shows it as such.

Because the config cannot state the ring, `init` prints what the engine
reports — the coefficient count, the slot count, the ladder — so the achieved
parameters are in the run's log beside the measurement rather than inferred
from the slot count.

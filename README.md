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
| sized by | the ring | the ladder |
| `log_coeff_count` | 16 | — |
| `log_slot_count` | 15 | — |
| `special_prime_count` | 2 | — |
| `max_level` | — | 20 |
| `slot_count` | — | 4096 |
| `mode` / `thread_count` | parallel / every core | parallel / every core |

The two points are sized by different groups because the library refuses the
other way round. Asked for 32768 slots at `max_level` 10 it answers *The
given slot count is too large*: it picks the ring from the ladder, and ten
levels do not reach a ring that holds 32768 slots. The wide point therefore
names the ring and lets the library fit the ladder into it, which is what the
point wants in any case — the width is the question, the ring is the answer.

The ring, the prime sizes and the special primes are the library's to choose,
and it names no security level: nothing in this configuration refuses a set
that fails to reach 128 bits, where OpenFHE refuses one before the context is
built. The point's `security` parameter is therefore attested differently
here, and the board shows it as such.

Because the config cannot always state the ring, `init` prints what the
engine reports. As of 1.17.0 that is a slot count and a ladder and nothing
else: the ring is not on the engine's surface, so for the row sized by the
ladder it can only be inferred — twenty levels at this library's prime sizes
do not fit a ring below 65536 at any security level worth the name. `init`
also prints the engine's public attributes, so the next version is checked
against the record rather than against memory.

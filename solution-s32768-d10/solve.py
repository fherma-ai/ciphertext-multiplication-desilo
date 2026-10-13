"""One CKKS ciphertext multiplication with DESILO's engine.

`multiply(a, b, relinearization_key)` is the whole answer: the library
tensors, relinearises and rescales in one call, so the measured call holds
the three stages the specification names, as it does for the other answers to
this point.

What differs from the OpenFHE and FIDESlib rows is how the parameters are
asked for. DESILO is sized by its ladder and its slots — `max_level` and
`slot_count` — and chooses the ring and the primes itself; it names no
security level, and nothing refuses a set that does not reach one. So the
ring is reported here rather than declared: `init` prints what the engine
built, which is the only place the achieved parameters appear.
"""
import numpy as np

from fherma import Inputs, Outputs, Point, Tensor


def init(p: Point, cc):
    # What the engine actually built, for the record: the config asks for a
    # ladder and a slot count, and the ring that carries them is the
    # library's answer, not a declaration anyone can read off the config.
    said = []
    for name in ("log_coeff_count", "coeff_count", "slot_count", "log_slot_count",
                 "max_level", "level", "mode", "thread_count"):
        value = getattr(cc.engine, name, None)
        if value is not None:
            said.append(f"{name}={value}")
    print(f"engine: {', '.join(said) or type(cc.engine).__name__}", flush=True)
    print(f"point: slots={p.slots} depth={p.depth} security={p.security} "
          f"precision={p.precision}", flush=True)
    return None


def encoding(cc, inp: Inputs) -> list:
    # Slot i holds element i, as in every other answer to this point.
    return [np.asarray(inp.a.data, dtype=float).reshape(-1),
            np.asarray(inp.b.data, dtype=float).reshape(-1)]


def run(state, cc, cts: list) -> list:
    # Tensor, relinearise, rescale.
    return [cc.engine.multiply(cts[0], cts[1], cc.keys.relinearization)]


def decoding(p: Point, cc, pts: list) -> Outputs:
    values = np.real(np.asarray(pts[0])).tolist()
    return Outputs(c=Tensor((p.slots,), values[:p.slots], "f64"))

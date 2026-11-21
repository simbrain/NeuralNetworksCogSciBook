"""Shared example: one sentence, one attention pattern, one set of value vectors."""
import numpy as np

TOKENS = ["I", "went", "to", "the", "party", "and", "it", "was", "fun"]
IT = TOKENS.index("it")
PARTY = TOKENS.index("party")

# Attention weights for the "it" row (sums to 1; mostly "party").
IT_ROW = np.array([0.04, 0.05, 0.02, 0.06, 0.70, 0.03, 0.10, 0, 0])


def attention_matrix(seed=3):
    """Lower-triangular (causal) attention pattern. Row i = how much token i reads from each token."""
    rng = np.random.default_rng(seed)
    n = len(TOKENS)
    A = np.zeros((n, n))
    for i in range(n):
        w = rng.uniform(0.2, 1.0, i + 1)
        w[i] += 1.0                      # some weight on itself
        if i > 0:
            w[i - 1] += 0.6              # and on the previous token
        A[i, :i + 1] = w / w.sum()
    A[IT] = IT_ROW
    A[TOKENS.index("was"), :8] = [0.02, 0.03, 0.01, 0.04, 0.25, 0.03, 0.45, 0.17]
    A[TOKENS.index("fun"), :9] = [0.02, 0.03, 0.01, 0.03, 0.40, 0.03, 0.10, 0.18, 0.20]
    return A


D = 6
VALUES = np.array([
    [0.2, 0.5, 0.1, 0.3, 0.2, 0.4],   # I
    [0.4, 0.2, 0.3, 0.1, 0.5, 0.2],   # went
    [0.1, 0.3, 0.2, 0.4, 0.1, 0.3],   # to
    [0.3, 0.1, 0.4, 0.2, 0.3, 0.1],   # the
    [0.95, 0.05, 0.9, 0.05, 0.85, 0.1],  # party (distinctive)
    [0.2, 0.4, 0.1, 0.2, 0.3, 0.5],   # and
    [0.3, 0.3, 0.2, 0.5, 0.2, 0.3],   # it
    [0.1, 0.5, 0.3, 0.3, 0.4, 0.2],   # was
    [0.5, 0.2, 0.2, 0.4, 0.3, 0.6],   # fun
])


def it_output():
    return IT_ROW @ VALUES

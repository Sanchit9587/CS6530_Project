"""Small statistics helpers."""


def wilson(k, n, z=1.96):
    """95% Wilson score interval for a proportion k/n (well behaved at k = 0)."""
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return max(0.0, c - h), min(1.0, c + h)

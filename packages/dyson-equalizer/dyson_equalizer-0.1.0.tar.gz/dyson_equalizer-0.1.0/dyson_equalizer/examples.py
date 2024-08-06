import numpy as np


def generate_X(
        m=1000,
        n=2000,
        seed=123
) -> np.array:
    np.random.seed(seed)
    assert m <= n

    # Make a random matrix
    Xr = np.random.normal(loc=0, scale=1, size=(m, n))
    Xr_svd = np.linalg.svd(Xr, full_matrices=False)

    # Set pv
    s_20 = [np.sqrt(1000 * n)] * 10 + [np.sqrt(3 * n)] * 10

    # Y of rank 20
    X_20 = Xr_svd.U[:, :20] @ np.diag(s_20) @ Xr_svd.Vh[:20, :]

    return X_20


def generate_X_with_correlated_noise(
        m=1000,
        n=2000,
        noise_dimensions=10,
        seed=123,
) -> np.array:
    np.random.seed(seed)

    X = generate_X(m=m, n=n)

    A = np.exp(np.random.normal(0, np.sqrt(2), size=(m, noise_dimensions)))
    B = np.exp(np.random.normal(0, np.sqrt(2), size=(noise_dimensions, n)))
    S = A @ B
    S /= S.mean()
    E = np.random.normal(scale=np.sqrt(S))

    return X + E

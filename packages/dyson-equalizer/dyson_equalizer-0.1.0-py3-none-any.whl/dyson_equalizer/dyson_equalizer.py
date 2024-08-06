"""
    The ``dyson_equalizer.dyson_equalizer`` module contains the class DysonEqualizer that can be used
    to easily compute the Dyson Equalizer.

"""
from typing import Self

import numpy as np

from dyson_equalizer.algorithm import compute_scaling_factors, compute_low_rank_approximation_mp, scale_matrix
from dyson_equalizer.plots import plot_mp_eigenvalues, plot_mp_density
from dyson_equalizer.validation import validate_matrix


class DysonEqualizer:
    """
    This class can be used to compute the Dyson Equalizer [1]_ and store all associated results.


    Attributes
    ----------
    Y : (m, n) numpy.array
        The original data matrix

    x_hat : (m) numpy.array
        The normalizing factors for the rows

    y_hat : (n) numpy.array
        The normalizing factors for the columns

    Y_hat : (m, n) numpy.array
        The normalized data matrix so that the variance of the error is 1

    X_bar: (m, n) numpy.array
        The estimated signal matrix. It has rank `r_hat`

    r_hat: int
        The estimated rank of the signal matrix

    S: (m) numpy.array
        The principal values of the data matrix `Y`

    S_hat: (m) numpy.array
        The principal values of the normalized data matrix `Y_hat`

    See Also
    --------
    dyson_equalizer.algorithm.compute_scaling_factors
    dyson_equalizer.algorithm.compute_low_rank_approximation_mp

    References
    ----------
    .. [1] Landa B., Kluger Y., "The Dyson Equalizer: Adaptive Noise Stabilization for Low-Rank Signal
       Detection and Recovery," arXiv, https://arxiv.org/abs/2306.11263

    """
    Y: np.array
    x_hat: np.array = None
    y_hat: np.array = None
    Y_hat: np.array = None
    X_bar: np.array = None
    r_hat: int = None
    S: np.array = None
    S_hat: np.array = None

    def __init__(self, Y: np.array):
        self.Y = validate_matrix(Y)

    def compute(self, use_X_bar: bool = False) -> Self:
        """ Computes the Dyson Equalizer and stores the results.

        Parameters
        ----------
        use_X_bar: bool, optional
            if ``True`` uses `X_bar` instead of the original matrix as input.
            This option may be used iteratively to improve the low rank approximation in some cases

        Returns
        -------
        self : DysonEqualizer
            A reference to this instance
        """
        Y = self.X_bar if use_X_bar else self.Y
        svd = np.linalg.svd(Y, full_matrices=False)
        x_hat, y_hat = compute_scaling_factors(svd)
        Y_hat = scale_matrix(self.Y, 1 / np.sqrt(x_hat), 1 / np.sqrt(y_hat))

        svd_hat = np.linalg.svd(Y_hat, full_matrices=False)
        Y_tr, r_hat = compute_low_rank_approximation_mp(svd_hat)

        X_bar = scale_matrix(Y_tr, np.sqrt(x_hat), np.sqrt(y_hat))

        self.x_hat = x_hat
        self.y_hat = y_hat
        self.Y_hat = Y_hat
        self.X_bar = X_bar
        self.r_hat = r_hat
        self.S = svd.S
        self.S_hat = svd_hat.S

        return self

    def plot_mp_eigenvalues_Y(
            self,
            eigenvalues_to_show: int = 100,
            log_y: bool = True
    ) -> None:
        """  Plots the eigenvalues of ¹⁄ₙYYᵀ and compares to the Marchenko-Pastur threshold

        Parameters
        ----------
        eigenvalues_to_show: int, optional
            The number of eigenvalues to show in the plot (defaults to 100)
        log_y: bool, optional
            Whether the y-axis should be logarithmic (defaults to True)

        Returns
        -------

        See Also
        --------
        dyson_equalizer.plots.plot_mp_eigenvalues

        """
        m, n = sorted(self.Y.shape)
        eigs = self.S ** 2 / n
        plot_mp_eigenvalues(
            eigs, gamma=m/n,
            eigenvalues_to_show=eigenvalues_to_show,
            log_y=log_y,
            matrix_label='¹⁄ₙYYᵀ',
        )

    def plot_mp_eigenvalues_Y_hat(
            self,
            eigenvalues_to_show: int = 100,
            log_y: bool = True
    ) -> None:
        """  Plots the eigenvalues of ¹⁄ₙŶŶᵀ and compares to the Marchenko-Pastur threshold

        Parameters
        ----------
        eigenvalues_to_show: int, optional
            The number of eigenvalues to show in the plot (defaults to 100)
        log_y: bool, optional
            Whether the y-axis should be logarithmic (defaults to True)

        Returns
        -------

        See Also
        --------
        dyson_equalizer.plots.plot_mp_eigenvalues

        """
        m, n = sorted(self.Y_hat.shape)
        eigs = self.S_hat ** 2 / n
        plot_mp_eigenvalues(
            eigs, gamma=m/n,
            eigenvalues_to_show=eigenvalues_to_show,
            log_y=log_y,
            matrix_label='¹⁄ₙŶŶᵀ',
        )

    def plot_mp_density_Y(
            self,
            show_only_significant: int = None,
    ) -> None:
        """Plots the density of eigenvalues of ¹⁄ₙYYᵀ and compares to the Marchenko-Pastur distribution

        This function assumes the input are the eigenvalues of a covariance matrix of a random matrix
        whose entries have variance 1. These eigenvalues follow the Marchenko-Pastur distribution.

        Parameters
        ----------
        show_only_significant: int, optional
            Set this value to show only a small number of significant eigenvalues (defaults to None)
            This option is useful is some of the signal eigenvalues are much bigger than the noise.

        See Also
        --------
        dyson_equalizer.plots.plot_mp_density

        """
    def plot_mp_density_Y_hat(
            self,
            show_only_significant: int = None,
    ) -> None:
        """Plots the density of eigenvalues of ¹⁄ₙŶŶᵀ and compares to the Marchenko-Pastur distribution

        This function assumes the input are the eigenvalues of a covariance matrix of a random matrix
        whose entries have variance 1. These eigenvalues follow the Marchenko-Pastur distribution.

        Parameters
        ----------
        show_only_significant: int, optional
            Set this value to show only a small number of significant eigenvalues (defaults to None)
            This option is useful is some of the signal eigenvalues are much bigger than the noise.

        See Also
        --------
        dyson_equalizer.plots.plot_mp_density

        """
        m, n = sorted(self.Y_hat.shape)
        eigs = self.S_hat ** 2 / n
        plot_mp_density(
            eigs, gamma=m/n,
            show_only_significant=show_only_significant,
            matrix_label='¹⁄ₙŶŶᵀ',
        )

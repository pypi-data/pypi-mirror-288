"""Module for Uncorrelated Linear Discriminant Analysis (ULDA).

This module implements the ULDA algorithm, an extension of the traditional
Linear Discriminant Analysis (LDA). This implementation is based on Ye, J.,& Yu, B. (2005)
with some modifications. It simplifies to the traditional LDA when total
scatter matrix is nonsingular, and is much faster. The algorithm is implemented
as a scikit-learn compatible estimator.
"""

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd

__all__ = ["ULDA"]

class ULDA(BaseEstimator, ClassifierMixin):
    """Uncorrelated Linear Discriminant Analysis (ULDA) classifier.

    ULDA aims to find a linear combination of features that separates
    two or more classes. The resulting combination may be used as a
    linear classifier, or for dimensionality reduction.

    Attributes:
        priors (array-like, shape (n_classes,)): Priors on classes
        n_components (int): Number of components for dimensionality reduction
        classes_ (array): Unique class labels
        n_classes_ (int): Number of unique classes
        priors_ (array): Computed priors for each class
        scaler_ (StandardScaler): Instance of StandardScaler for feature scaling
        scalings_ (array): Scaling coefficients for linear transformation
        means_ (array): Class means after applying scaling and transformation
    """

    def __init__(self, priors=None, n_components=None):
        """Initialize the ULDA classifier with optional priors and components."""
        self.priors = priors
        self.n_components = n_components

    def fit(self, X, y):
        """Fit the ULDA model according to the given training data.

        Parameters:
            X (array-like, shape (n_samples, n_features)): Training vector,
                where n_samples is the number of samples and n_features is the
                number of features.
            y (array-like, shape (n_samples,)): Target values (class labels).

        Returns:
            self: Object
        """
        # Check for missing values in X and y
        if np.any(pd.isnull(y)) or np.any(pd.isnull(X)):
            raise ValueError("No missing values allowed in response or predictors")

        # Convert y to a factor and remove unused categories
        y = pd.Series(y).astype('category').cat.remove_unused_categories()
        self.classes_ = y.cat.categories.values
        self.n_classes_ = len(self.classes_)

        # Estimate or use provided priors
        if self.priors is None:
            self.priors_ = y.value_counts().values / len(y)
        else:
            self.priors_ = self.priors

        # Standardize features and save the column names
        self.scaler_ = StandardScaler()
        X = self.scaler_.fit_transform(X)

        # Perform SVD on the between and within class scatter matrices
        group_means = np.array([np.mean(X[y == k, :], axis=0) for k in self.classes_])
        Hb = group_means * np.sqrt(y.value_counts()).values[:, np.newaxis]
        Hw = X - group_means[y.cat.codes.values]

        # Choose SVD method based on the shape of X
        if X.shape[0] > X.shape[1]:
            _, R = np.linalg.qr(Hw, mode='reduced')
            U, s, Vt = _safer_svd(np.vstack([Hb, R]), full_matrices=False)
        else:
            U, s, Vt = _safer_svd(np.vstack([Hb, Hw]), full_matrices=False)

        # Determine the rank and perform SVD on the projection matrix
        rankT = np.sum(s > max(X.shape) * np.finfo(float).eps * s[0])
        U_p, s_p, Vt_p = _safer_svd(U[:self.n_classes_, :rankT], full_matrices=False)
        rankAll = min(self.n_classes_ - 1, rankT)
        self._max_components = rankAll if self.n_components is None else min(rankAll, self.n_components)

        # Calculate scaling coefficients and class means
        unitSD = np.diag(np.sqrt((len(y) - self.n_classes_) / np.abs(1 - s_p[:self._max_components] ** 2 + 1e-15)))
        self.scalings_ = Vt[:rankT, :].T @ np.diag(1 / s[:rankT]) @ Vt_p[:self._max_components, :].T @ unitSD
        self.means_ = group_means @ self.scalings_
        return self

    def predict(self, X):
        """Perform classification on samples in X.

        Parameters:
            X (array-like, shape (n_samples, n_features)): Samples.

        Returns:
            C (array, shape (n_samples,)): Predicted class label per sample.
        """
        posterior = self.predict_proba(X)
        return self.classes_.take(np.argmax(posterior, axis=1))

    def predict_proba(self, X):
        """Return probability estimates for the test vector X.

        Parameters:
            X (array-like, shape (n_samples, n_features)): Samples.

        Returns:
            P (array, shape (n_samples, n_classes)): Returns the probability
            of the sample for each class in the model.
        """
        ld_scores = self._get_ld_scores(X)
        loglikelihood = ld_scores @ self.means_.T + np.tile(np.log(self.priors_) - 0.5 * np.sum(self.means_**2, axis=1), (ld_scores.shape[0], 1))
        likelihood = np.exp(loglikelihood - np.max(loglikelihood, axis=1).reshape(-1, 1))
        posterior = likelihood / np.sum(likelihood, axis=1).reshape(-1, 1)
        return posterior

    def _get_ld_scores(self, X, scale=True):
        """Compute linear discriminant scores for samples in X.

        Parameters:
            X (array-like, shape (n_samples, n_features)): Samples.
            scale (bool): Whether to scale X according to the previously
            computed scaling parameters.

        Returns:
            ld_scores (array, shape (n_samples, n_components)): Linear
            discriminant scores.
        """
        if scale:
            X = (X - self.scaler_.mean_) / self.scaler_.scale_
        ld_scores = np.dot(X, self.scalings_)
        return ld_scores

def _safer_svd(X, full_matrices=False, max_iter=10):
    """Perform SVD with retries on convergence failure.

    Parameters:
        X (array-like): Matrix to decompose.
        full_matrices (bool): Whether to compute the full-sized U and V matrices.
        max_iter (int): Maximum number of attempts to converge.

    Returns:
        U, s, Vt: SVD result.

    Raises:
        np.linalg.LinAlgError: If SVD does not converge within max_iter attempts.
    """
    for i in range(max_iter):
        try:
            U, s, Vt = np.linalg.svd(X, full_matrices=full_matrices)
            return U, s, Vt
        except np.linalg.LinAlgError as e:
            if "SVD did not converge" in str(e):
                X = np.round(X, decimals=14-i)
            else:
                raise e
    raise np.linalg.LinAlgError("SVD did not converge after multiple attempts.")

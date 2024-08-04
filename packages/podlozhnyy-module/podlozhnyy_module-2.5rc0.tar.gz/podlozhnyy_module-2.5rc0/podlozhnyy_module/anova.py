from scipy.stats import f as fisher
from scipy.stats import studentized_range

from podlozhnyy_module import np, pd


class ANOVA:
    """
    ANalysis Of VAriance implementation with an extra option to run pairwise Tukey HSD procedure

    Parameters
    ----------
    means: array-like
        list of point estimates for the metric
    stds: array-like
        list of sample standard deviations (divided by n - 1)
    nobs: array-like
        list of sample sizes
    names: array-like (optional)
        list of names of compared groups
    repeated: bool (optional)
        indicates if repeated ANOVA must be applied,
        shall be True if observations are preliminary normalized
        which means that for each observed object the corresponding object's average
        is deducted from the observed value of this object in every group
    """

    def __init__(self, means, stds, nobs, names=None, repeated: bool = False) -> None:
        size = len(nobs)

        if size == 1:
            raise ValueError(f"Arrays size must be greater than one")
        for array in [means, stds]:
            if size != len(array):
                raise ValueError(
                    f"Length of arrays must be the same - {size, len(array)} received"
                )
        if names and len(names) != size:
            raise ValueError(
                f"Incorrect length of `names` array - {len(names)}, must be {size}"
            )

        self.means = means
        self.stds = stds
        self.nobs = nobs
        self.names = names

        self.N, self.k = sum(self.nobs), len(self.nobs)

        # if repeated anova then df = (n - 1)(k - 1)
        self.df_w = self.N - self.k - nobs[0] + 1 if repeated else self.N - self.k
        self.df_b = self.k - 1

    @property
    def mean_squared_error_within_groups(self) -> float:
        ss_w = sum([(self.nobs[i] - 1) * self.stds[i] ** 2 for i in range(self.k)])
        ms_w = ss_w / self.df_w
        return ms_w

    @property
    def mean_squared_error_between_groups(self) -> float:
        ss_b = sum([self.nobs[i] * self.means[i] ** 2 for i in range(self.k)]) - sum(
            [self.nobs[i] * self.means[i] for i in range(self.k)]
        ) ** 2 / sum([self.nobs[i] for i in range(self.k)])
        ms_b = ss_b / self.df_b
        return ms_b

    def one_way_anova(self) -> dict:
        """
        Performs standard one-way analysis of variance on the basis of Fisher criterion
        """
        f_statistic = (
            self.mean_squared_error_between_groups
            / self.mean_squared_error_within_groups
        )
        p_value = fisher.sf(f_statistic, dfn=self.df_b, dfd=self.df_w)

        return {
            "f-statistic": f_statistic,
            "p-value": p_value,
        }

    def tukey_hsd(self) -> dict:
        """
        Conservative Tukey HSD multiple comparisons method.
        The most common and recommended test in the literature (Hurlburt, 2006; Zar, 2010).
        It's recommended for groups of similar sizes and verifies only PAIRED (not complex) hypotheses.

        Note: it happens that in ANOVA the null hypothesis is rejected, and post-hoc tests do not detect differences, since their power is lower.
        In this case, it is necessary to increase the sample size.
        """
        means = np.array(self.means)
        nobs = np.array(self.nobs)

        if np.unique(nobs).shape[0] == 1:
            factor = 2 / nobs[0]
        else:
            factor = 1 / nobs + 1 / nobs.reshape(-1, 1)

        standard_errors = np.sqrt(self.mean_squared_error_within_groups / 2 * factor)
        mean_absolute_differences = np.abs(means.reshape(-1, 1) - means)

        q_statistic = mean_absolute_differences / standard_errors
        p_values = studentized_range.sf(x=q_statistic, k=self.k, df=self.df_w)

        return {
            "q-statistic": q_statistic,
            "p-values": p_values,
        }

    def heatmap(self, alpha: float = 0.05) -> pd.DataFrame:
        """
        Returns data frame NxN of a paired comparisons with -1, 0, 1 values in the cells;
        where 1 means that the metric for the group in the row is significantly higher than for the group in the column,
        -1 means opposite and 0 identifies the absence of statistically significant difference.

        Parameters
        ----------
        alpha: float
            acceptable probability of making a Type I error
        """
        means = np.array(self.means)

        direction = 2 * (means.reshape(-1, 1) - means > 0) - 1
        significance = 1 * (self.tukey_hsd()["p-values"] <= alpha)
        heatmap = direction * significance

        return pd.DataFrame(heatmap, index=self.names, columns=self.names)

    def rank(self, alpha: float = 0.05) -> pd.Series:
        """
        Returns one number (rank) for every group that means how many of others are significantly worse
        (in case if number is positive) or better (if number is negative)

        Parameters
        ----------
        alpha: float
            acceptable probability of making a Type I error
        """
        rank = self.heatmap(alpha).sum(axis=1)
        return rank

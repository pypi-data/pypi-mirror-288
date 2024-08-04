import json
from typing import Literal

from scipy.stats import multivariate_t, norm

from podlozhnyy_module import np


class ProportionTest:
    """
    General class for multivariate testing approach for proportions.
    Measure statistics and p-value for the conversion from `base` to `target`.

    Parameters
    ----------
    input: str | dict
        Is taken in the format of a dictionary or a string identical to:
        '{`variant`: "<name>", `groups`: <list of names>, `base`: <list of numbers>, `target`: <list of numbers>}'
        Where the following convention takes place:
            1. `<name>` is the name of the particular group to get p-value for
            2. `<list of names>` contains the list of all the experiment groups, including control
            3. `<list of numbers>` contains one number per group and ordered in accordance with `<list of names>`
    base: str
        conversion denominator name
    target: str
        conversion numerator name
    groups: str
        experiment variant names
    variant: str
        variant to compute p-value for

    Note: at least two lists of numbers must be provided!
    While it may be an arbitrary higher number of supplied metrics, only those two specified in `base` and `target` are used
    """

    def __init__(
        self, input: str | dict, base: str, target: str, groups: str, variant: str
    ) -> None:

        if isinstance(input, dict):
            self.data = input
        elif isinstance(input, str):
            self.data = json.loads(input)
        else:
            raise TypeError("Incorrect `input` type, " "should be str or dict")

        if groups not in self.data.keys():
            raise KeyError(
                "Incorrect `groups` value, "
                f"{groups} list with group names missing from data"
            )
        else:
            self.groups = groups

        if base not in self.data.keys():
            raise KeyError(
                "Incorrect `base` value, " f"there is no {base} metric in provided data"
            )
        else:
            self.base = base

        if target not in self.data.keys():
            raise KeyError(
                "Incorrect `target` value, "
                f"there is no {target} metric in provided data"
            )
        else:
            self.target = target

        if self.data[variant] not in self.data[groups]:
            raise KeyError(
                "Incorrect `variant` value, "
                f"{variant} group is not on the `groups` list"
            )
        else:
            self.variant = variant

        for counter in [base, target]:
            if len(self.data[counter]) != len(self.data[groups]):
                raise ValueError(
                    f"Length of `{counter}` list ({len(self.data[counter])}) "
                    f"must coincide with the length of `groups` list ({len(self.data[groups])})"
                )

    def _prepare_data(self) -> None:

        names = self.data[self.groups].copy()
        n_samples = self.data[self.base].copy()
        p_samples = self.data[self.target].copy()

        if "control" in names:
            control_name = "control"
        elif "vdefault" in names:
            control_name = "vdefault"
        else:
            control_name = names[0]

        self.n_control = n_samples.pop(names.index(control_name))
        self.p_control = p_samples.pop(names.index(control_name))
        names.remove(control_name)

        self.names = names
        self.control_name = control_name

        self.n_samples = np.array(n_samples)
        self.p_samples = np.array(p_samples)

    @property
    def statistic(self) -> np.ndarray:

        diff = self.p_samples / self.n_samples - self.p_control / self.n_control
        var = self.variance  # to be identified in subclass
        statistic = diff / np.sqrt(var * (1 / self.n_samples + 1 / self.n_control))

        return statistic

    def _calculate_pvalue(self, alternative: str) -> None:

        if alternative not in {"two-sided", "greater", "less"}:
            raise ValueError(
                "Incorrect type of alternative, "
                "should be one of the following: 'two-sided', 'greater', 'less'"
            )

    def groups_results(self) -> dict:
        """
        Returns statistic for the entire set of experiments

        Parameters
        ----------
        alternative: str
            type of alternative hypothesis
        """
        self._prepare_data()

        output = dict.fromkeys(
            [
                "variant",
                "statistic",
                "p-value",
            ]
        )
        output["variant"] = self.names
        output["statistic"] = self.statistic

        return output

    def variant_pvalue(self, **kwargs) -> float:
        """
        Returns p-value for specified `variant`

        Keyword Arguments
        ----------
        alternative: str
            type of alternative hypothesis
        """

        pvalues = self.groups_results(**kwargs).get("p-value")

        if self.data[self.variant] == self.control_name:
            return None
        elif not isinstance(pvalues, np.ndarray):
            return pvalues
        else:
            return pvalues[self.names.index(self.data[self.variant])]


class Dunnett(ProportionTest):
    """
    Dunnett's T-test approach for proportions.
    Returns statistic and p-value of Dunnett's T-test for the specific group, where the metric is the conversion from `base` to `target`.
    """

    def _prepare_data(self) -> None:

        super()._prepare_data()

        # control group is included
        self.df = self.n_samples.sum() + self.n_control - self.n_samples.size - 1

        # multivariate student distribution matrix
        self.rho = 1 + self.n_control / self.n_samples
        self.rho = 1 / np.sqrt(self.rho[:, None] * self.rho[None, :])
        np.fill_diagonal(self.rho, 1)

    @property
    def variance(self) -> np.ndarray:

        var = (
            np.sum(self.p_samples * (1 - self.p_samples / self.n_samples))
            + self.p_control * (1 - self.p_control / self.n_control)
        ) / self.df

        return var

    def _calculate_pvalue(
        self,
        statistic: np.ndarray,
        alternative: str,
        random_state: int,
    ) -> np.ndarray:

        super()._calculate_pvalue(alternative)

        mvt = multivariate_t(shape=self.rho, df=self.df, seed=random_state)
        statistic = statistic.reshape(-1, 1)

        if alternative == "two-sided":
            pvalue = 1 - mvt.cdf(np.abs(statistic), lower_limit=-np.abs(statistic))
        elif alternative == "greater":
            pvalue = 1 - mvt.cdf(statistic, lower_limit=-np.inf)
        elif alternative == "less":
            pvalue = 1 - mvt.cdf(np.inf, lower_limit=statistic)

        return pvalue

    def groups_results(
        self,
        alternative: Literal["two-sided", "less", "greater"] = "two-sided",
        random_state: int = 2024,
    ) -> dict:
        """
        Returns statistic for the entire set of experiments

        Parameters
        ----------
        alternative: str
            type of alternative hypothesis
        random_state: int
            seed for multivariate student distribution
        """

        output = super().groups_results()

        output["p-value"] = self._calculate_pvalue(
            output["statistic"],
            alternative,
            random_state,
        )

        return output


class Ztest(ProportionTest):
    """
    Z-test approach for proportions.
    Returns statistic and p-value of classic Z criterion for the specific group, where the metric is the conversion from `base` to `target`.
    """

    @property
    def variance(self) -> np.ndarray:

        P = (self.p_samples + self.p_control) / (self.n_samples + self.n_control)
        var = P * (1 - P)

        return var

    def _calculate_pvalue(
        self,
        statistic: np.ndarray,
        alternative: str,
    ) -> np.ndarray:

        super()._calculate_pvalue(alternative)

        if alternative == "two-sided":
            pvalue = 2 * (1 - norm.cdf(np.abs(statistic)))
        elif alternative == "greater":
            pvalue = 1 - norm.cdf(statistic)
        elif alternative == "less":
            pvalue = norm.cdf(statistic)

        return pvalue

    def groups_results(
        self,
        alternative: Literal["two-sided", "less", "greater"] = "two-sided",
    ) -> dict:
        """
        Returns statistic for the entire set of experiments

        Parameters
        ----------
        alternative: str
            type of alternative hypothesis
        """

        output = super().groups_results()

        output["p-value"] = self._calculate_pvalue(
            output["statistic"],
            alternative,
        )

        return output

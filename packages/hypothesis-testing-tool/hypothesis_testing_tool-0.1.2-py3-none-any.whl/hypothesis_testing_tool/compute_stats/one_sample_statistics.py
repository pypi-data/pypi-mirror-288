from scipy import stats
import numpy as np


class OneSampleTest:
    def __init__(
        self,
        data: list,
        null_population_mean: float,
        alternative: str = "two-sided",
    ):

        if len(data) < 2:
            raise Exception("Input data must have at least two data points")

        elif len(set(data)) == 1:
            raise Exception("Input data must not have identical elements")

        self.data = data
        self.null_population_mean = null_population_mean
        self.t_test_results = stats.ttest_1samp(
            a=self.data,
            popmean=self.null_population_mean,
            alternative=alternative,
        )

    def calculate_ci(self, alpha: float = 0.05) -> dict:
        __standard_error = np.std(self.data, ddof=1) / np.sqrt(len(self.data))
        __margin_of_error = stats.t.ppf((1 + (1 - alpha)) / 2, len(self.data) - 1) * __standard_error

        return {
            "lower_bound": np.mean(self.data) - __margin_of_error,
            "point_estimate": np.mean(self.data),
            "upper_bound": np.mean(self.data) + __margin_of_error,
            "null_population_mean": self.null_population_mean,
        }

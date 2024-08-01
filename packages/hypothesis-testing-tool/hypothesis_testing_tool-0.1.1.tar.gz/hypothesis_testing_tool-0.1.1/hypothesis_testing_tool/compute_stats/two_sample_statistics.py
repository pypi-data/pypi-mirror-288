from scipy import stats


class TwoSampleTest:
    def __init__(self, group_a: list, group_b: list, alternative: str = "two-sided", equal_var=True):
        self.group_a = group_a
        self.group_b = group_b
        self.alternative = alternative
        self.t_test_results = stats.ttest_ind(
            a=self.group_a,
            b=self.group_b,
            equal_var=equal_var,
            alternative=alternative,
        )

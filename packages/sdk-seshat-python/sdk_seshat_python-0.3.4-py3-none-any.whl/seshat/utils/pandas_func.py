from pandas.core.dtypes.common import is_numeric_dtype


class PandasPercentile:
    def __init__(self, quantiles):
        self.quantiles = quantiles

    def get_percentile(self, value):
        for i, quantile in enumerate(self.quantiles):
            if value <= quantile:
                return (i + 1) * 10
        return 100

    def __call__(self, *args, **kwargs):
        return self.get_percentile(*args, **kwargs)


def get_zero_value(col):
    if is_numeric_dtype(col):
        return 0
    else:
        return ""

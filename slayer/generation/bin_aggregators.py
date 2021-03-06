import numpy as np


def aggregator(weight_function):
    return {'sum': weighted_sum,
            'mean': weighted_mean}[weight_function]


def weighted_mean(index, slice_area, counts, weights, value_type='float32'):
    weighted = np.bincount(index, minlength=slice_area, weights=weights)
    weighted_counts = weighted/counts
    # The NaNs here represent the places with no measurements
    return weighted_counts


def weighted_sum(index, slice_area, counts, weights, value_type='float32'):
    weighted = np.bincount(index, minlength=slice_area, weights=weights)
    if value_type == 'float32':
        weighted = weighted.astype(float)
        # The NaNs here represent the places with no measurements
        weighted[counts == 0.0] = np.nan
    return weighted

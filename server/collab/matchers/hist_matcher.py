from . import pairwise_matcher
from sklearn.metrics.pairwise import euclidean_distances


class HistogramMatcher(pairwise_matcher.PairwiseMatcher):
    cmp_fn = euclidean_distances

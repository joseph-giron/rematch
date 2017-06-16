from . import hist_matcher

import sklearn.metric.pairwise.euclidean_distances as cmp_fn


class MnemonicHistogramMatcher(hist_matcher.PairwiseMatcher):
  vector_type = 'mnemonic_hist'
  match_type = 'mnemonic_hist'
  matcher_name = "Mnemonic Histogram"
  matcher_description = ("Matches functions according to thier mnemonic "
                         "listing using histogram and a distance metric.")

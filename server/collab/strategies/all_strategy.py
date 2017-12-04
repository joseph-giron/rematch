from .strategy import Strategy


class AllStrategy(Strategy):
  strategy_name = 'All'
  strategy_type = 'all_strategy'
  strategy_description = ("The most brute strategy, runs all matchers on all "
                          "pairs, regardless of size, previous matching "
                          "results or any other potential optimization. This "
                          "makes this strategy the slowest possible, but it "
                          "provides as many results as possible (which can be "
                          "an advantage or a disadvantage at the same time).")

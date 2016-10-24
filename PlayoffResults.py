import LahmanHandler as LH
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from sknn.mlp import Regressor, Layer
import itertools


class PlayoffResults():
    class Stats():
        def __init__(self, wins, ops, hr, walks, k):
            self.wins = wins
            self.ops = ops
            self.hr = hr
            self.walks = walks
            self.k = k

        def stat_arr(self):
            return [self.ops, self.hr, self.walks, self.k]

    def __init__(self):
        self.lahman = LH.LahmanHandler()
        self.results = defaultdict(PlayoffResults.Stats)

    def get_results(self):
        teams = self.lahman.find_playoff_teams()
        ops_dict = self.lahman.calc_OPS(teams)
        pitching = self.lahman.calc_pitching(teams)
        wins = self.lahman.get_playoff_wins()

        for key, wins in wins.items():
            ops = ops_dict[key]
            hr, walks, k = ([x for x in pitching[key]])
            stats = PlayoffResults.Stats(wins, ops, hr, walks, k)
            self.results[key] = stats

    def make_charts(self):
        for key, value in self.results.items():
            plt.scatter(value.ops, value.wins)

        plt.ylabel("Wins")
        plt.xlabel("OPS")
        plt.title("OPS for Playoff Teams Since Introducing Wild Card (1995)")
        plt.show()

    def learn_data(self):
        x = []
        y = []
        x_ = []
        all_stats = []
        for year, stats in self.results.items():
            all_stats += [stats.stat_arr()]
            y += [stats.wins]

        x = all_stats[:int((len(all_stats)/2))]
        x_ = all_stats[int(len(all_stats)/2):]
        y_test = y[:int((len(y)/2))]

        x_ = np.array([x_])
        x = np.array([x])
        y = np.array([y])
        all_stats = np.array([all_stats])

        nn = Regressor(
            layers=[
                Layer("Rectifier", units=100),
                Layer("Softmax")],
            learning_rate=0.001,
            n_iter=30)
        nn.fit(all_stats, y)

        predictions = nn.predict(all_stats)

        print(predictions)
if __name__ == '__main__':
    numbers = PlayoffResults()
    numbers.get_results()
    numbers.learn_data()

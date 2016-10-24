import LahmanHandler as LH
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from sknn.mlp import Classifier, Layer


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
        first_half = []
        fh_wins = []
        second_half = []
        sh_wins = []
        key_t = []

        for key, stats in self.results.items():
            if key[0] < 2006:
                first_half += [stats.stat_arr()]
                fh_wins += [stats.wins]
            else:
                second_half += [stats.stat_arr()]
                sh_wins += [stats.wins]
                key_t += [key]

        x_ = np.array([second_half])
        x = np.array([first_half])
        y_learn = np.array([fh_wins])

        nn = Classifier(
            layers=[
                Layer("Sigmoid", units=100),
                Layer("Softmax")],
            learning_rate=0.01,
            n_iter=50)
        nn.fit(x, y_learn)

        prdt = nn.predict(x_)

        for i in range(len(second_half)):
            if prdt[0][i] >= 10 or sh_wins[i] >= 11:
                print((str(key_t[i])+" actually won "+str(sh_wins[i])+" and " +
                       "was predicted with "+str(prdt[0][i])))
        
if __name__ == '__main__':
    numbers = PlayoffResults()
    numbers.get_results()
    numbers.learn_data()

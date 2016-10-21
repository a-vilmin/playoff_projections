import MySQLdb as SQL
from collections import defaultdict


class LahmanHandler():
    def __init__(self):
        self.db = SQL.connect(host="localhost", user="vilmin",
                              passwd="sas_4_Lyfe", db="stats")

        self.cursor = self.db.cursor()

    def execute_command(self, command):
        self.cursor.execute(command)
        return self.cursor.fetchall()

    def find_playoff_teams(self):
        sql = "SELECT yearID, teamID FROM teams WHERE (DivWin = 'Y' OR "
        sql += "WCWin = 'Y') AND yearID >= 1995"

        query = self.execute_command(sql)
        teams = defaultdict(list)
        for each in query:
            year, team = each
            teams[year] += [team]
        return teams

    def get_offs_query(self, team, year):
        line = "SELECT AB, H, 2B, 3B, HR, BB, HBP, SF FROM teams WHERE "
        line += "teamID = '" + team + "' AND yearID = " + str(year)
        return line

    def calc_OPS(self, teams):
        ops_results = {}

        for year, field in teams.items():
            for team in field:
                query = self.get_offs_query(team, year)
                stats = self.execute_command(query)
                ab, h, doub, trip, hr, bb, hbp, sf = stats[0]
                sin = h - doub - trip - hr

                slg = (sin+2*doub+3*trip+4*hr)/ab
                obp = h + bb + int('0'+hbp)
                obp /= ab + bb + int('0'+sf) + int('0'+hbp)
                ops = slg + obp

                ops_results[(year, team)] = ops
        return ops_results

    def get_pitch_query(self, team, year):
        line = "SELECT HRA, BBA, SOA FROM teams WHERE "
        line += "teamID = '" + team + "' AND yearID = " + str(year)
        return line

    def calc_pitching(self, teams):
        pitch_results = {}

        for year, field in teams.items():
            for team in field:
                query = self.get_pitch_query(team, year)
                stats = self.execute_command(query)

                pitch_results[(year, team)] = stats[0]
        return pitch_results

if __name__ == '__main__':
    handler = LahmanHandler()
    teams = handler.find_playoff_teams()

    ops = handler.calc_OPS(teams)
    pitch_stats = handler.calc_pitching(teams)

    for key, item in pitch_stats.items():
        print(str(key[0]) + " " + key[1] + str(item))

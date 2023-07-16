# Simulate a sports tournament

import csv
import sys
import random

# Number of simluations to run
N = 1000


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    teams = []

    # Open the file in read mode
    with open(sys.argv[1], "r") as file:
        reader = csv.DictReader(file)
        # Get each row in reader
        for row in reader:
            # Append each row in teams
            teams.append(row)
        for i in range(len(teams)):
            teams[i]["rating"] = int(teams[i]["rating"])

    counts = {}
    # Get all all teams from team
    for i in range(len(teams)):
        # Set all team winning to zero
        counts[teams[i]["team"]] = 0

    # Sumulate the tournaments
    for i in range(N):
        winner = simulate_tournament(teams)
        counts[winner] += 1

    # Print each team's chances of winning, according to simulation
    for team in sorted(counts, key=lambda team: counts[team], reverse=True):
        print(f"{team}: {counts[team] * 100 / N:.1f}% chance of winning")


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""
    rating1 = team1["rating"]
    rating2 = team2["rating"]
    probability = 1 / (1 + 10 ** ((rating2 - rating1) / 600))
    return random.random() < probability


def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""
    winners = []

    # Simulate games for all pairs of teams
    for i in range(0, len(teams), 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])

    return winners


def simulate_tournament(teams):
    """Simulate a tournament. Return name of winning team."""
    # Sumulate the first round and get the winners
    winner = simulate_round(teams)

    # check to see if there is only one winner
    while len(winner) != 1:
        winner = simulate_round(winner)

    # Return the winner
    return winner[0]["team"]


if __name__ == "__main__":
    main()

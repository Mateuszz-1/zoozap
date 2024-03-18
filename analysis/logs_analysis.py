import json
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

def read_battle_logs(filename='battle_logs.json'):
    battle_logs = []
    with open(filename, 'r') as file:
        for line in file:
            try:
                battle_log = json.loads(line)
                battle_logs.append(battle_log)
            except json.JSONDecodeError:
                # If a line is not a valid JSON object, skip it
                print(f"Skipping invalid JSON line: {line} \n\n")
    return battle_logs

battle_logs = read_battle_logs()
df = pd.DataFrame(battle_logs)

print("\n\nWins Per team:")
wins_by_player = df['winner'].value_counts()
print(wins_by_player)

def plot_wins():
    wins_by_player.plot(kind='bar')
    plt.xlabel('Player')
    plt.ylabel('Wins')
    plt.title('Wins by Player')
    plt.show()

# Is there a correlation between team health & winning
def wins_based_on_health(row):
    if row['team1_starting_health'] > row['team2_starting_health']:
        return 'More Health Won' if row['winner'] == 'Team 1' else 'Less Health Won'
    elif row['team1_starting_health'] < row['team2_starting_health']:
        return 'More Health Won' if row['winner'] == 'Team 2' else 'Less Health Won'
    else:
        return 'Equal Health'

df['health_difference'] = df['team1_starting_health'] - df['team2_starting_health']
df['team1_won'] = df['winner'].apply(lambda x: 1 if x == 'Team 1' else 0)
correlation, p_value = pearsonr(df['health_difference'], df['team1_won'])
print(f"\nCorrelation coefficient between health difference and winning: {correlation}")
print(f"P-value: {p_value}\n")
df['wins_based_on_health'] = df.apply(wins_based_on_health, axis=1)
wins_by_health = df['wins_based_on_health'].value_counts()
print(wins_by_health)

# Distribution of remaining creatures
df['remaining_creatures_count'] = df['remaining_creatures'].apply(len)
outcome_counts = df['remaining_creatures_count'].value_counts().sort_index()
avg_remaining_creatures = df['remaining_creatures_count'].mean()
print(f"\nAverage remaining creatures on the winning team: {avg_remaining_creatures:.2f}\n")

def plot_remaining_creatures():
    all_outcomes = pd.Series(index=range(1, 7), data=0).add(outcome_counts, fill_value=0)

    # Define colours for each outcome
    colours = ['red', 'green', 'green', 'yellow', 'orange', 'red', 'red']

    plt.figure(figsize=(10, 6))
    all_outcomes.plot(kind='bar', color=colours)
    plt.title('Number of Remaining Creatures at the End of Battles')
    plt.xlabel('Number of Remaining Creatures')
    plt.ylabel('Number of Battles')
    plt.xticks(range(0, 7), labels=[str(i) for i in range(0, 7)])
    plt.show()

# Number of turns per battle
avg_turns = df['turns'].mean()
max_turns = df['turns'].max()
min_turns = df['turns'].min()
print(f"Average number of turns per battle: {avg_turns:.2f}")
print(f"Maximum number of turns in a battle: {max_turns}")
print(f"Minimum number of turns in a battle: {min_turns}\n")

def plot_turns_per_battle():
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['turns'], marker='o', linestyle='-', color='blue')
    plt.title('Turns Taken to Win Each Battle')
    plt.xlabel('Battle Number')
    plt.ylabel('Number of Turns')
    plt.grid(True)
    plt.show()

# Trends in regards to a creature being prone to winning or losing
winning_creatures = df.apply(lambda x: pd.Series(x['team1'] if x['winner'] == 'team1' else x['team2']), axis=1).stack().value_counts()
losing_creatures = df.apply(lambda x: pd.Series(x['team2'] if x['winner'] == 'team1' else x['team1']), axis=1).stack().value_counts()

winning_creatures_series = df.apply(lambda x: pd.Series(x['team1'] if x['winner'] == 'team1' else x['team2']), axis=1).stack()
ties_win = winning_creatures_series.value_counts().max() == winning_creatures_series.value_counts()
most_common_winning = ', '.join(winning_creatures_series.value_counts()[ties_win].index.tolist())
print(f"Most common winning creature(s): {most_common_winning}")

def plot_winning_creatures():
    plt.figure(figsize=(10, 6))
    winning_creatures.plot(kind='bar', color='skyblue')
    plt.title('Number of Wins per Creature')
    plt.xlabel('Creature')
    plt.ylabel('Number of Wins')
    plt.xticks(rotation=45)
    plt.show()

losing_creatures_series = df.apply(lambda x: pd.Series(x['team2'] if x['winner'] == 'team1' else x['team1']), axis=1).stack()
ties_lose = losing_creatures_series.value_counts().max() == losing_creatures_series.value_counts()
most_common_losing = ', '.join(losing_creatures_series.value_counts()[ties_lose].index.tolist())
print(f"Most common losing creature(s): {most_common_losing}\n")

def plot_losing_creatures():
    plt.figure(figsize=(10, 6))
    losing_creatures.plot(kind='bar', color='skyblue')
    plt.title('Number of Losses per Creature')
    plt.xlabel('Creature')
    plt.ylabel('Number of Losses')
    plt.xticks(rotation=45)
    plt.show()

# Total number of times a creature appears (a creature may simply appear more than another and as such be most winning/losing)
all_creatures_series = pd.concat([df['team1'].explode(), df['team2'].explode()])
total_creature_counts = all_creatures_series.value_counts()

def plot_creature_appearances():
    plt.figure(figsize=(10, 6))
    total_creature_counts.plot(kind='bar', color='skyblue')

    plt.title('Total Appearances of Each Creature in Battles')
    plt.xlabel('Creature')
    plt.ylabel('Number of Appearances')
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.show() 

while True:
    print("What plot would you like to see?\n1) Wins by Player\n2) Remaining Creatures\n3) Turns per Battle\n4) Winning Creatures\n5) Losing Creatures\n6) Number of Creature Appearances\n7) Exit")
    plot = input("1/2/3/4/5/6/7: ")
    if plot == "1":
        plot_wins()
    elif plot == "2":
        plot_remaining_creatures()
    elif plot == "3":
        plot_turns_per_battle()
    elif plot == "4":
        plot_winning_creatures()
    elif plot == "5":
        plot_losing_creatures()
    elif plot == "6":
        plot_creature_appearances()
    else:
        exit()
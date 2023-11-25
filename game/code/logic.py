import random
from .creatures import creatures_dict

def calculate_type_multiplier(move_type, defender):
    multiplier = 1.0
    if move_type in defender["weakness"]:
        multiplier *= 2  # Double damage for weaknesses
    if move_type in defender["resistance"]:
        multiplier *= 0.5  # Half damage for resistances
    return multiplier

def status_moves_logic(attacker, defender, move_name, terrain_conditions):
    if move_name == "Inferno Trap":
        # Fire type creatures are immune to burn
        if "fire" in defender["type"]:
            return "no_effect"
        # There is a 50% chance of applying burn
        if random.random() <= 0.5:
            # Assign burn as status so that the creature takes damage at the end of each turn
            defender["status"] = "Burn"
            # Burn deals 6.25% of the defender's max HP as damage at the end of each turn
            damage = defender["stats"]["hp"] * 0.0625
            defender["stats"]["hp"] = max(0, defender["stats"]["hp"] - damage)
            # Burn halves the defender's Attack stat
            defender["stats"]["atk"] *= 0.5
        else:
            return "missed"
    elif move_name == "Quake Tremors":
        # Lower the defender's Speed stat by 17%
        defender["stats"]["spd"] *= 0.83
        return "success"
    elif move_name == "Misty Veil":
        # Raise the attacker's Special Defense stat by 20%
        attacker["stats"]["sp_def"] *= 1.2
        return "success"
    elif move_name == "Gusty Wind":
        # There is a 30% chance of confusing the defender
        if random.random() <= 0.3:
            # Assign confusion as status so that the creature has a 50% chance of attacking itself each turn
            defender["status"] = "Confused"
            # Confusion lasts for 1-4 turns
            defender["status_duration"] = random.randint(1, 4)
            return "success"
        else:
            return "missed"
    elif move_name == "Static Charge":
        # Electric type creatures are immune to paralysis
        if "electric" in defender["type"]:
            return "no_effect"
        # There is a 30% chance of paralyzing the defender
        if random.random() <= 0.3:
            # Assign paralysis as status so that the creature has a 25% chance of not being able to move each turn
            defender["status"] = "Paralyzed"
            # The Speed stat is reduced by 75% while paralyzed
            defender["stats"]["spd"] *= 0.25
            return "success"
        else:
            return "missed"
    elif move_name == "Spore Cloud":
        # There is a 75% chance of putting the defender to sleep
        if random.random() <= 0.75:
            # Assign sleep as status so that the creature cannot move
            defender["status"] = "Sleep"
            # Sleep lasts for 1-3 turns
            defender["status_duration"] = random.randint(1, 3)
            return "success"
        else:
            return "missed"
    elif move_name == "Mirror Shine":
        # If the attacker has a status effect, give the attacker's status to the defender
        if attacker["status"]:
            defender["status"] = attacker["status"]
            # Reset the attacker's status
            attacker["status"] = None
            return "success"
        # If the attacker has no status effect, the move has no effect
        else:
            return "no_effect"
    elif move_name == "Shadow Hold":
        # Trap the defender permanently (this means no substitutions) until it faints
        defender["status"] = "Trapped"
        return "success"
    elif move_name == "Frost Chill":
        # There is a 20% chance of freezing the defender
        if random.random() <= 0.2:
            # Assign freeze as status so that the creature cannot move
            defender["status"] = "Frozen"
            # Freeze is a permanent condition that has a probability to end randomly each turn
            return "success"
        else:
            return "missed"
    elif move_name == "Toxic Spikes":
        # Toxic spikes can be applied twice, any use afterwards does nothing
        # Toxic spikes poison any creature that switches in on the defender's side
        if terrain_conditions["toxic_spikes"] == False:
            # 1 layer deals 12.5% of the defender's max HP each turn
            terrain_conditions["toxic_spikes"] = True
        else:
            # 2 layers start dealing 6.25% of the defender's max HP each turn but increase by 6.25% each turn
            terrain_conditions["super_toxic_spikes"] = True
        return "success"
    elif move_name == "Steel Wall":
        # Raise the attacker's Defense stat by 40%
        attacker["stats"]["def"] *= 1.4
        return "success"
    elif move_name == "Fairy Dust":
        # Heal the attacker by 50% of its max HP
        heal_amount = attacker["stats"]["hp"] * 0.5
        attacker["stats"]["hp"] += heal_amount
        return "success"
    elif move_name == "Stun Spore":
        # Electric type creatures are immune to paralysis
        if "electric" in defender["type"]:
            return "no_effect"
        # There is a 75% chance of paralyzing the defender
        if random.random() <= 0.75:
            # Assign paralysis as status so that the creature has a 25% chance of not being able to move each turn
            defender["status"] = "Paralyzed"
            return "success"
        else:
            return "missed"
    else:
        return "error"
            

def apply_move(attacker_name, defender_name, move_name, terrain_conditions):
    # Retrieves the attacker's data from the creatures dictionary using the attacker's name.
    attacker = creatures_dict[attacker_name]

    # Retrieves the defender's data from the creatures dictionary using the defender's name.
    defender = creatures_dict[defender_name]

    # Retrieves the move object from the attacker's moves list using the move's name
    move = next(move for move in attacker["moves"] if move["name"] == move_name)

    # Calculates the effectiveness of the move based on the defender's type, weaknesses, and resistances.
    type_multiplier = calculate_type_multiplier(move["type"], defender)

    # Damage Calculation for damaging moves (physical or special)
    if move["category"] in ["physical", "special"]:
        # If the move is physical, uses the attacker's Attack stat and defender's Defense stat in the calculation.
        if move["category"] == "physical":
            damage = ((attacker["stats"]["atk"] / defender["stats"]["def"]) * move["power"]) * type_multiplier
        else:  # If the move is special, uses the attacker's Special Attack stat and defender's Special Defense stat.
            damage = ((attacker["stats"]["sp_atk"] / defender["stats"]["sp_def"]) * move["power"]) * type_multiplier
        # Ensures that damage is at least 1 (no negative or zero damage)
        damage = max(1, damage)
        # Reduces the defender's HP by the calculated damage, but not below 0
        defender["stats"]["hp"] = max(0, defender["stats"]["hp"] - damage)
        # Prints a message indicating the move used and the damage dealt
        print(f"{attacker_name} used {move_name}! It dealt {damage:.2f} damage to {defender_name}.")

    # Applying Status Effects
    if move["category"] == "status":
        status_success = status_moves_logic(attacker, defender, move_name, terrain_conditions)
        print(f"{attacker_name} used {move_name}!")
        if status_success == "success":
            print("It was successful!")
        elif status_success == "missed":
            print("But it missed!")
        elif status_success == "no_effect":
            print("But it had no effect!")
        else:
            print("Something went wrong!")


"""
Initial proof of concept for base battle mechanics.
Damage moves working, status moves not working (properly).
Moves are applied by a random creature from each team.
Random moves are chosen each turn.
Speed stat is not taken into account.
There is no active hp or status for creatures.
A crash will occur if a status check is performed on a creature with no status.
The battle ends when one team has no more creatures.
"""
"""
team1 = []
team2 = []
for i in range(6):
    team1.append(random.choice(list(creatures_dict.keys())))
    team2.append(random.choice(list(creatures_dict.keys())))
print(team1) # for testing
print(team2) # for testing

terrain_conditions = {"toxic_spikes": False, "super_toxic_spikes": False}
"""
"""while team1 and team2:
    attacker_name = random.choice(team1)
    defender_name = random.choice(team2)
    move_name = random.choice(creatures_dict[attacker_name]["moves"])["name"]
    apply_move(attacker_name, defender_name, move_name, terrain_conditions)
    if creatures_dict[defender_name]["stats"]["hp"] == 0:
        team2.remove(defender_name)
        print(f"{defender_name} has fainted!")
    attacker_name, defender_name = defender_name, attacker_name
    move_name = random.choice(creatures_dict[attacker_name]["moves"])["name"]
    apply_move(attacker_name, defender_name, move_name, terrain_conditions)
    if creatures_dict[defender_name]["stats"]["hp"] == 0:
        team1.remove(defender_name)
        print(f"{defender_name} has fainted!")
    print()"""
"""print("Team1: " + str(team1))
print("Team2: " + str(team2))
if team1:
    print("Team 1 wins!")
else:
    print("Team 2 wins!")"""
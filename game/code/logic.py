import random
from .creatures import creatures_dict

def calculate_type_multiplier(move_type, defender):
    multiplier = 1.0
    if move_type in defender["creature"]["weakness"]:
        multiplier *= 2  # Double damage for weaknesses
    if move_type in defender["creature"]["resistance"]:
        multiplier *= 0.5  # Half damage for resistances
    return multiplier

def status_moves_logic(attacker, defender, move, terrain_conditions):
    if move["effect"] == "burn":
        # Fire type creatures are immune to burn
        if "fire" in defender["creature"]["type"]:
            return "no_effect"
        # There is a move["probability"] chance of applying burn
        if random.random() <= move["probability"]:
            # Assign burn as status so that the creature takes damage at the end of each turn
            defender["status"].append("Burn")
            # Burn lasts for 3-6 turns
            defender["status_duration"].append(random.randint(3, 6))
            # Burn halves the defender's Attack stat
            defender["stats"]["atk"] *= 0.5
        else:
            return "missed"
    elif move["effect"] == "lower_spd":
        # Lower the defender's Speed stat by 17%
        defender["stats"]["spd"] *= 0.83
        return "success"
    elif move["effect"] == "raise_sp_def":
        # Raise the attacker's Special Defence stat by 20%
        attacker["stats"]["sp_def"] *= 1.2
        return "success"
    elif move["effect"] == "confuse":
        # There is a move["probability"] chance of confusing the defender
        if random.random() <= move["probability"]:
            # Assign confusion as status so that the creature has a 50% chance of attacking itself each turn
            defender["status"].append("Confused")
            # Confusion lasts for 1-3 turns
            defender["status_duration"].append(random.randint(1, 3))
            return "success"
        else:
            return "missed"
    elif move["effect"] == "paralyse":
        # Electric type creatures are immune to paralysis
        if "electric" in defender["creature"]["type"]:
            return "no_effect"
        # There is a move["probability"] chance of paralysing the defender
        if random.random() <= move["probability"]:
            # Assign paralysis as status so that the creature has a 20% chance of not being able to move each turn
            defender["status"].append("Paralysed")
            # Paralysis lasts for 100 turns - which is unlikely. This is because it has a 20% chance of ending each turn.
            defender["status_duration"].append(100)
            # The Speed stat is reduced by 75% while paralysed
            defender["stats"]["spd"] *= 0.25
            return "success"
        else:
            return "missed"
    elif move["effect"] == "sleep":
        # There is a move["probability"] chance of putting the defender to sleep
        if random.random() <= move["probability"]:
            # Assign sleep as status so that the creature cannot move
            defender["status"].append("Sleep")
            # Sleep lasts for 1-3 turns
            defender["status_duration"].append(random.randint(1, 3))
            return "success"
        else:
            return "missed"
    elif move["effect"] == "reflect_effect":
        # If the attacker has a status effect, give the attacker's status to the defender
        if attacker["status"] != []:
            for status in attacker["status"]:
                defender["status"].append(status)
            for duration in attacker["status_duration"]:
                defender["status_duration"].append(duration)
            # Reset the attacker's status
            attacker["status"] = []
            return "success"
        # If the attacker has no status effect, the move has no effect
        else:
            return "no_effect"
    elif move["effect"] == "prevent_escape":
        # Trap the defender permanently (this means no substitutions) until it faints
        defender["status"].append("Trapped")
        # Trap lasts for 100 turns - which is unlikely. This is because it should not end until the defender faints.
        defender["status_duration"].append(100)
        return "success"
    elif move["effect"] == "freeze":
        # There is a move["probability"] chance of freezing the defender
        if random.random() <= move["probability"]:
            # Assign freeze as status so that the creature cannot move
            defender["status"].append("Frozen")
            # Freeze lasts for 100 turns - which is unlikely. This is because it has a 30% chance of ending each turn.
            defender["status_duration"].append(100)
            return "success"
        else:
            return "missed"
    elif move["effect"] == "poison_terrain":
        # Toxic spikes can be applied twice, any use afterwards does nothing
        # Toxic spikes poison any creature that switches in on the defender's side
        if terrain_conditions["toxic_spikes"] == False:
            # 1 layer deals 12.5% of the defender's max HP each turn
            terrain_conditions["toxic_spikes"] = True
        else:
            # 2 layers start dealing 6.25% of the defender's max HP each turn but increase by 6.25% each turn
            terrain_conditions["super_toxic_spikes"] = True
        return "success"
    elif move["effect"] == "raise_def":
        # Raise the attacker's Defence stat by 40%
        attacker["stats"]["def"] *= 1.4
        return "success"
    elif move["effect"] == "heal":
        # Heal the attacker by 50% of its max HP
        heal_amount = attacker["stats"]["hp"] * 0.5
        attacker["stats"]["hp"] += heal_amount
        return "success"
    else:
        return "error"

def trapped_check(creature):
    if "Trapped" in creature["status"]:
        return True
    else:
        return False

def can_act_check(creature):
    return_statement = True
    for status in creature["status"]:
        # Confusion has a 50% chance of causing the creature to hurt itself
        if status == "Confused":
            if random.random() <= 0.5:
                damage = (creature["stats"]["atk"] / creature["stats"]["def"]) * 40
                creature["stats"]["hp"] = max(0, creature["stats"]["hp"] - damage)
                creature["status_duration"][creature["status"].index(status)] -= 1
                return_statement = False
            else:
                creature["status_duration"][creature["status"].index(status)] -= 1
        # Paralysis has a 20% chance of preventing the creature from moving
        elif status == "Paralysed":
            if random.random() <= 0.2:
                creature["status_duration"][creature["status"].index(status)] -= 1
                return_statement = False
            else:
                creature["status_duration"][creature["status"].index(status)] -= 1
        # Sleep lasts for a certain number of turns
        elif status == "Sleep":
            creature["status_duration"][creature["status"].index(status)] -= 1
            return_statement = False
        # Freeze has a 30% chance of ending each turn
        elif status == "Frozen":
            if random.random() <= 0.3:
                creature["status_duration"][creature["status"].index(status)] = 0
            else:
                return_statement = False
        else:
            return_statement = None
    # Remove status effects that have expired
    removed_status = []
    for status in creature["status"]:
        if creature["status_duration"][creature["status"].index(status)] == 0:
            removed_status.append(status)
            creature["status_duration"].remove(creature["status_duration"][creature["status"].index(status)])
            creature["status"].remove(status)
    return {"return_statement": return_statement, "removed_status": removed_status}
                
def burn_check(creature):
    damage_statement = ""
    removed_status = False
    for status in creature["status"]:
    # Burn deals 6.25% of the creature's max HP as damage at the end of each turn
        if status == "Burn":
            max_health = creatures_dict[creature["creature_data"]["name"]]["stats"]["hp"]
            damage = int(max_health * 0.0625)
            creature["stats"]["hp"] = max(0, creature["stats"]["hp"] - damage)
            damage_statement = f"{creature['name']} took {damage} damage from burn!"
            creature["status_duration"][creature["status"].index(status)] -= 1
            # Remove burn if it has expired
            if creature["status_duration"][creature["status"].index(status)] == 0:
                creature["status_duration"].remove(creature["status_duration"][creature["status"].index(status)])
                creature["status"].remove(status)
                removed_status = True
    return {"damage_statement": damage_statement, "removed_status": removed_status}

def apply_move(first_player, second_player, attacker, defender, move_name):
    # Retrieves the move object from the attacker's moves list using the move's name
    move = next(move for move in attacker["creature"]["moves"] if move["name"] == move_name)

    # Calculates the effectiveness of the move based on the defender's type, weaknesses, and resistances.
    type_multiplier = calculate_type_multiplier(move["type"], defender)

    # Damage Calculation for damaging moves (physical or special)
    if move["category"] in ["physical", "special"]:
        # If the move is physical, uses the attacker's Attack stat and defender's Defence stat in the calculation.
        if move["category"] == "physical":
            damage = int(((attacker["stats"]["atk"] / defender["stats"]["def"]) * move["power"]) * type_multiplier)
        else:  # If the move is special, uses the attacker's Special Attack stat and defender's Special Defence stat.
            damage = int(((attacker["stats"]["sp_atk"] / defender["stats"]["sp_def"]) * move["power"]) * type_multiplier)
        # Ensures that damage is at least 1 (no negative or zero damage)
        damage = max(1, damage)
        # Reduces the defender's HP by the calculated damage, but not below 0
        defender["stats"]["hp"] = max(0, defender["stats"]["hp"] - damage)
        # Prints a message indicating the move used and the damage dealt
        print(f"{first_player} {attacker['creature']['name']} used {move_name}! It dealt {damage:.2f} damage to {second_player} {defender['creature']['name']}.")

    # Applying Status Effects
    if move["category"] == "status":
        terrain_conditions = {"toxic_spikes": False, "super_toxic_spikes": False}
        status_success = status_moves_logic(attacker, defender, move, terrain_conditions)
        print(f"{first_player} {attacker['creature']['name']} used {move_name}!")
        if status_success == "success":
            print("It was successful!")
        elif status_success == "missed":
            print("But it missed!")
        elif status_success == "no_effect":
            print("But it had no effect!")
        else:
            print("Something went wrong!")


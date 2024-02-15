import socket
import random
import json
from code import logic

def main():
    server_socket, client1, client2 = establish_connection()
    team1, team2, active_creature1, active_creature2 = setup_teams()
    
    while team1 and team2:
        attack_switch(client1, client2, active_creature1, active_creature2)

        player1_choice = client1.recv(1024).decode()
        player2_choice = client2.recv(1024).decode()
        if logic.trapped_check(active_creature1):
            client1.sendall("You are trapped and cannot switch out!".encode())
            player1_choice = "attack"
        if logic.trapped_check(active_creature2):
            client2.sendall("You are trapped and cannot switch out!".encode())
            player2_choice = "attack"

        if player1_choice == "attack":
            player1_move = player1_move_choice(client1, active_creature1)
        elif player1_choice == "switch":
            active_creature1 = player1_switch(team1, active_creature1, client1, client2)
        
        if player2_choice == "attack":
            player2_move = player2_move_choice(client2, active_creature2)
        elif player2_choice == "switch":
            active_creature2 = player2_switch(team2, active_creature2, client1, client2)

        if player1_choice == "attack" and player2_choice == "attack":
            player1_can_act, player2_can_act, player1_can_act_check, player2_can_act_check = both_attack(active_creature1, active_creature2, player1_move, player2_move, client1, client2)
        elif player1_choice == "attack":
            player1_can_act, player1_can_act_check = player1_attack(active_creature1, active_creature2, player1_move, client1, client2)
        elif player2_choice == "attack":
            player2_can_act, player2_can_act_check = player2_attack(active_creature1, active_creature2, player2_move, client1, client2)
        
        player1_can_act = locals().get('player1_can_act', None)
        player2_can_act = locals().get('player2_can_act', None)
        did_creatures_act(player1_can_act, player2_can_act, client1, client2)

        did_creatures_burn(active_creature1, active_creature2, client1, client2)

        player1_can_act_check = locals().get('player1_can_act_check', None)
        player2_can_act_check = locals().get('player2_can_act_check', None)
        any_status_removed(player1_can_act_check, player2_can_act_check, active_creature1, active_creature2, client1, client2)

        active_creature1, active_creature2 = switch_fainted(active_creature1, active_creature2, team1, team2, client1, client2)

    if team1:
        print("Team 1 wins!")
    else:
        print("Team 2 wins!")
    close_game(client1, client2, server_socket)


def establish_connection():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(2)

    print("Server started, waiting for players...")

    # Accept Player 1
    client1, address1 = server_socket.accept()
    print(f"Player 1 connected from {address1}")
    client1.sendall("Welcome Player 1, you are the first to join".encode())

    # Receive name from Player 1
    """player1_name = client1.recv(1024).decode()
    print(f"Player 1's name is {player1_name}")"""

    # Accept Player 2
    client2, address2 = server_socket.accept()
    print(f"Player 2 connected from {address2}")
    client2.sendall(f"Welcome Player 2. Player 1 has already joined.".encode())

    return server_socket, client1, client2

def setup_teams():
    team1 = []
    team2 = []
    for i in range(6):
        pool1 = list(logic.creatures_dict.keys())
        pool2 = list(logic.creatures_dict.keys())
        creature_name1 = random.choice(pool1)
        creature_name2 = random.choice(pool2)
        creature_data1 = logic.creatures_dict[creature_name1]
        creature_data2 = logic.creatures_dict[creature_name2]
        pool1.remove(creature_name1)
        pool2.remove(creature_name2)
        team1.append({"creature": creature_data1, "stats": creature_data1["stats"], "status": [], "status_duration": []})
        team2.append({"creature": creature_data2, "stats": creature_data2["stats"], "status": [], "status_duration": []})
    print(team1) # for testing
    print(team2) # for testing
    active_creature1 = team1[0]
    active_creature2 = team2[0]
    return team1, team2, active_creature1, active_creature2

def attack_switch(client1, client2, active_creature1, active_creature2):
    client1.sendall(f"Your active creature is {active_creature1['creature']['name']}. Your available moves are:\n".encode())
    for move in active_creature1["creature"]["moves"]:
        if move["category"] == "physical" or move["category"] == "special":
            client1.sendall(f"{move['name']} | Type: {move['type']} | Category: {move['category']} | Power: {move['power']} | Accuracy: {move['accuracy']}\n".encode())
        else:
            client1.sendall(f"{move['name']} | Type: {move['type']} | Category: {move['category']} | Effect: {move['effect']}\n".encode())
    client2.sendall(f"Your active creature is {active_creature2['creature']['name']}. Your available moves are:\n".encode())
    for move in active_creature2["creature"]["moves"]:
        if move["category"] == "physical" or move["category"] == "special":
            client2.sendall(f"{move['name']} | Type: {move['type']} | Category: {move['category']} | Power: {move['power']} | Accuracy: {move['accuracy']}\n".encode())
        else:
            client2.sendall(f"{move['name']} | Type: {move['type']} | Category: {move['category']} | Effect: {move['effect']}\n".encode())
    attack_or_switch = json.dumps(["attack", "switch"])
    client1.sendall(attack_or_switch.encode())
    client2.sendall(attack_or_switch.encode())
    client1.sendall(f"Your opponent's active creature is {active_creature2['creature']['name']}.\nWould you like to [attack] or [switch]?".encode())
    client2.sendall(f"Your opponent's active creature is {active_creature1['creature']['name']}.\nWould you like to [attack] or [switch]?".encode())

def player1_move_choice(client1, active_creature1):
    player1_moves = get_moves(active_creature1)
    serialised_player1_moves = json.dumps(player1_moves)
    client1.sendall(serialised_player1_moves.encode())
    client1.sendall("Which move would you like to use?".encode())
    player1_move = client1.recv(1024).decode()
    return player1_move

def player1_switch(team1, active_creature1, client1, client2):
    if team1:
        for creature in team1:
            if creature["creature"]["name"] == active_creature1["creature"]["name"]:
                continue
            client1.sendall(f"{creature['creature']['name']} | HP: {creature['stats']['hp']}/{creature['creature']['stats']['hp']}\n".encode())
        client1.sendall("Which creature would you like to switch to?".encode())
        player1_switch = client1.recv(1024).decode()
        for creature in team1:
            if creature["creature"]["name"] == player1_switch:
                active_creature1 = creature
                break
        client1.sendall(f"You have switched to {active_creature1['creature']['name']}!".encode())
        client2.sendall(f"Player1 switched to {active_creature1['creature']['name']}!".encode())
    return active_creature1

def player2_move_choice(client2, active_creature2):
    player2_moves = get_moves(active_creature2)
    serialised_player2_moves = json.dumps(player2_moves)
    client2.sendall(serialised_player2_moves.encode())
    client2.sendall("Which move would you like to use?".encode())
    player2_move = client2.recv(1024).decode()
    return player2_move

def player2_switch(team2, active_creature2, client1, client2):
    if team2:
        for creature in team2:
            if creature["creature"]["name"] == active_creature2["creature"]["name"]:
                continue
            client2.sendall(f"{creature['creature']['name']} | HP: {creature['stats']['hp']}/{creature['creature']['stats']['hp']}\n".encode())
        client2.sendall("Which creature would you like to switch to?".encode())
        player2_switch = client2.recv(1024).decode()
        for creature in team2:
            if creature["creature"]["name"] == player2_switch:
                active_creature2 = creature
                break
        client1.sendall(f"Player2 has switched to {active_creature2['creature']['name']}!".encode())
        client2.sendall(f"You have switched to {active_creature2['creature']['name']}!".encode())
    return active_creature2

def both_attack(active_creature1, active_creature2, player1_move, player2_move, client1, client2):
    player1_first = False
    player2_first = False
    player1_can_act = True
    player2_can_act = True
    random_turn = 0
    if active_creature1['stats']['spd'] > active_creature2['stats']['spd']:
        player1_first = True
    elif active_creature1['stats']['spd'] < active_creature2['stats']['spd']:
        player2_first = True
    else:
        random_turn = random.randint(1, 2)
    
    if ((player1_first == True) or (random_turn == 1)):
        player1_can_act_check = logic.can_act_check(active_creature1)
        if player1_can_act_check['return_statement'] == False: # if the creature is unable to act
            player1_can_act = False
        if player1_can_act:
            logic.apply_move(active_creature1, active_creature2, player1_move)
        if active_creature2['stats']['hp'] == 0:
            client1.sendall(f"{active_creature2['creature']['name']} has fainted!".encode())
            client2.sendall(f"{active_creature2['creature']['name']} has fainted!".encode())
        else:
            player2_can_act_check = logic.can_act_check(active_creature2)
            if player2_can_act_check['return_statement'] == False: # if the creature is unable to act
                player2_can_act = False
            if player2_can_act:
                logic.apply_move(active_creature2, active_creature1, player2_move)
                if active_creature1['stats']['hp'] == 0:
                    client1.sendall(f"{active_creature1['creature']['name']} has fainted!".encode())
                    client2.sendall(f"{active_creature1['creature']['name']} has fainted!".encode())
    elif ((player2_first == True) or (random_turn == 2)):
        player2_can_act_check = logic.can_act_check(active_creature2)
        if player2_can_act_check['return_statement'] == False: # if the creature is unable to act
            player2_can_act = False
        if player2_can_act:
            logic.apply_move(active_creature2, active_creature1, player2_move)
        if active_creature1['stats']['hp'] == 0:
            client1.sendall(f"{active_creature1['creature']['name']} has fainted!".encode())
            client2.sendall(f"{active_creature1['creature']['name']} has fainted!".encode())
        else:
            player1_can_act_check = logic.can_act_check(active_creature1)
            if player1_can_act_check['return_statement'] == False: # if the creature is unable to act
                player1_can_act = False
            if player1_can_act:
                logic.apply_move(active_creature1, active_creature2, player1_move)
                if active_creature2['stats']['hp'] == 0:
                    client1.sendall(f"{active_creature2['creature']['name']} has fainted!".encode())
                    client2.sendall(f"{active_creature2['creature']['name']} has fainted!".encode())
    return player1_can_act, player2_can_act, player1_can_act_check, player2_can_act_check

def player1_attack(active_creature1, active_creature2, player1_move, client1, client2):
    player1_can_act_check = logic.can_act_check(active_creature1)
    player1_can_act = True
    if player1_can_act_check['return_statement'] == False: # if the creature is unable to act
        player1_can_act = False
    if player1_can_act:
        logic.apply_move(active_creature1, active_creature2, player1_move)
    if active_creature2['stats']['hp'] == 0:
        client1.sendall(f"{active_creature2['creature']['name']} has fainted!".encode())
        client2.sendall(f"{active_creature2['creature']['name']} has fainted!".encode())
    return player1_can_act, player1_can_act_check

def player2_attack(active_creature1, active_creature2, player2_move, client1, client2):
    player2_can_act_check = logic.can_act_check(active_creature2)
    player2_can_act = True
    if player2_can_act_check['return_statement'] == False: # if the creature is unable to act
        player2_can_act = False
    if player2_can_act:
        logic.apply_move(active_creature2, active_creature1, player2_move)
    if active_creature1['stats']['hp'] == 0:
        client1.sendall(f"{active_creature1['creature']['name']} has fainted!".encode())
        client2.sendall(f"{active_creature1['creature']['name']} has fainted!".encode())
    return player2_can_act, player2_can_act_check

def did_creatures_act(player1_can_act, player2_can_act, client1, client2):
    if player1_can_act is not None and player2_can_act is not None:
        if not player1_can_act and not player2_can_act:
            client1.sendall("Both creatures are unable to act!".encode())
            client2.sendall("Both creatures are unable to act!".encode())
    elif player1_can_act is not None:
        if not player1_can_act:
            client1.sendall("Your creature was unable to act!".encode())
            client2.sendall("Your opponent's creature was unable to act!".encode())
    elif player2_can_act is not None:
        if not player2_can_act:
            client1.sendall("Your opponent's creature was unable to act!".encode())
            client2.sendall("Your creature was unable to act!".encode())

def did_creatures_burn(active_creature1, active_creature2, client1, client2):
    if active_creature1['stats']['hp'] != 0:
        player1_burn_check = logic.burn_check(active_creature1)
        if player1_burn_check['damage_statement'] != "":
            client1.sendall(f"Player1's {player1_burn_check['damage_statement']}".encode())
            client2.sendall(f"Player1's {player1_burn_check['damage_statement']}".encode())
            if active_creature1['stats']['hp'] == 0:
                client1.sendall(f"Player1's {active_creature1['creature']['name']} has fainted!".encode())
                client2.sendall(f"Player1's {active_creature1['creature']['name']} has fainted!".encode())
    if active_creature2['stats']['hp'] != 0:
        player2_burn_check = logic.burn_check(active_creature2)
        if player2_burn_check['damage_statement'] != "":
            client1.sendall(f"Player2's {player2_burn_check['damage_statement']}".encode())
            client2.sendall(f"Player2's {player2_burn_check['damage_statement']}".encode())
            if active_creature2['stats']['hp'] == 0:
                client1.sendall(f"Player2's {active_creature2['creature']['name']} has fainted!".encode())
                client2.sendall(f"Player2's {active_creature2['creature']['name']} has fainted!".encode())

def any_status_removed(player1_can_act_check, player2_can_act_check, active_creature1, active_creature2, client1, client2):
    if player1_can_act_check is not None:
        if player1_can_act_check['removed_status'] != [] and active_creature1['stats']['hp'] != 0:
            client1.sendall(f"{player1_can_act_check['removed_status']} has been cured from Player1's {active_creature1['creature']['name']}!".encode())
            client2.sendall(f"{player1_can_act_check['removed_status']} has been cured from Player1's {active_creature1['creature']['name']}!".encode())
    if player2_can_act_check is not None:
        if player2_can_act_check['removed_status'] != [] and active_creature2['stats']['hp'] != 0:
            client1.sendall(f"{player2_can_act_check['removed_status']} has been cured from Player2's {active_creature2['creature']['name']}!".encode())
            client2.sendall(f"{player2_can_act_check['removed_status']} has been cured from Player2's {active_creature2['creature']['name']}!".encode())

def switch_fainted(active_creature1, active_creature2, team1, team2, client1, client2):
    if active_creature1['stats']['hp'] == 0:
        team1.remove(active_creature1)
        active_creature1 = None
        if team1:
            for creature in team1:
                client1.sendall(f"{creature['creature']['name']} | HP: {creature['stats']['hp']}/{creature['creature']['stats']['hp']}\n".encode())
            client1.sendall("Which creature would you like to switch to?".encode())
            player1_switch = client1.recv(1024).decode()
            for creature in team1:
                if creature["creature"]["name"] == player1_switch:
                    active_creature1 = creature
                    break
            client1.sendall(f"You have switched to {active_creature1['creature']['name']}!".encode())
            client2.sendall(f"Player1 switched to {active_creature1['creature']['name']}!".encode())
    if active_creature2['stats']['hp'] == 0:
        team2.remove(active_creature2)
        active_creature2 = None
        if team2:
            for creature in team2:
                client2.sendall(f"{creature['creature']['name']} | HP: {creature['stats']['hp']}/{creature['creature']['stats']['hp']}\n".encode())
            client2.sendall("Which creature would you like to switch to?".encode())
            player2_switch = client2.recv(1024).decode()
            for creature in team2:
                if creature["creature"]["name"] == player2_switch:
                    active_creature2 = creature
                    break
            client1.sendall(f"Player2 has switched to {active_creature2['creature']['name']}!".encode())
            client2.sendall(f"You have switched to {active_creature2['creature']['name']}!".encode())
    return active_creature1, active_creature2

def close_game(client1, client2, server_socket):
    # Keep the server running
    input("Press Enter to exit...")

    client1.close()
    client2.close()
    server_socket.close()

def get_moves(creature):
    return creature["creature"]["moves"]

def get_team(team):
    return team

if __name__ == "__main__":
    main()
        
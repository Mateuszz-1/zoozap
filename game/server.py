import socket
import msgpack
import time
import struct
import random
from code import logic


def send_message(client, message, message_type):
    if message_type == 'text':
        # Encode the text message
        encoded_message = message.encode()
        prefix = b'T'
    elif message_type == 'msgpack':
        # Pack the message using MessagePack
        encoded_message = msgpack.packb(message, use_bin_type=True)
        prefix = b'M'
    else:
        raise ValueError("Invalid message type")
    
    # Add prefix and length onto message
    message_length = len(encoded_message)
    header = prefix + struct.pack(">I", message_length)
    full_message = header + encoded_message
    
    client.sendall(full_message)

def main():
    server_socket, client1, client2 = establish_connection()
    team1, team2, active_creature1, active_creature2 = setup_teams()
    
    while team1 and team2:
        attack_switch(client1, client2, active_creature1, active_creature2)

        player1_choice = client1.recv(1024).decode()
        player2_choice = client2.recv(1024).decode()
        if logic.trapped_check(active_creature1):
            send_message(client1, "You are trapped and cannot switch out!", "text")
            player1_choice = "attack"
        if logic.trapped_check(active_creature2):
            send_message(client2, "You are trapped and cannot switch out!", "text")
            player2_choice = "attack"

        if player1_choice == "attack":
            player1_move = player_move_choice(client1, active_creature1)
        elif player1_choice == "switch":
            active_creature1 = player_switch(team1, active_creature1, client1, client2, "Player1")
        
        if player2_choice == "attack":
            player2_move = player_move_choice(client2, active_creature2)
        elif player2_choice == "switch":
            active_creature2 = player_switch(team2, active_creature2, client1, client2, "Player2")

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

        active_creature1 = switch_fainted(active_creature1, team1, client1, client2, "Player1")
        active_creature2 = switch_fainted(active_creature2, team2, client2, client1, "Player2")

    print("Team 1:", team1)
    print("Team 2:", team2)
    print("Team 1 count:", len(team1))
    print("Team 2 count:", len(team2))
    if team1:
        print("Team 1 wins!")
        send_message(client1, "You win!", "text")
        send_message(client2, "You lose!", "text")
    else:
        print("Team 2 wins!")
        send_message(client1, "You lose!", "text")
        send_message(client2, "You win!", "text")
    close_game(client1, client2, server_socket)

def fix_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    time.sleep(1)
    server_socket.close()
    time.sleep(1)

def establish_connection():
    retry_counter = 1
    while True:
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(('localhost', 12345))
            server_socket.listen(2)
            break
        except OSError as e:
            if e.errno == 48:
                if retry_counter == 1:
                    print("Server address is already in use. Trying again up to 10 times.")
                if retry_counter <= 10:
                    if retry_counter > 1:
                        print(f"Address already in use. Retrying... ({retry_counter}/10)")
                    fix_socket()
                    retry_counter += 1
                else:
                    try_again = input("Server was unable to start. Would you like to continue trying? (y/n) ")
                    if try_again.lower() == "y":
                        retry_counter = 1
                    else:
                        exit()

    print("Server started, waiting for players...")

    # Accept Player 1
    client1, address1 = server_socket.accept()
    print(f"Player 1 connected from {address1}")
    send_message(client1, "Welcome Player 1, you are the first to join", "text")

    # Accept Player 2
    client2, address2 = server_socket.accept()
    print(f"Player 2 connected from {address2}")
    send_message(client2, "Welcome Player 2. Player 1 has already joined.", "text")

    return server_socket, client1, client2

def populate_team(team):
    pool = list(logic.creatures_dict.keys())
    for i in range(6):
        creature_name = random.choice(pool)
        creature_data = logic.creatures_dict[creature_name]
        pool.remove(creature_name)
        team.append({"creature": creature_data, "stats": creature_data["stats"], "status": [], "status_duration": []})
    return team

def setup_teams():
    team1 = []
    team2 = []
    team1 = populate_team(team1)
    team2 = populate_team(team2)
    print(get_team_creature_names(team1))
    print(get_team_creature_names(team2))
    active_creature1 = team1[0]
    active_creature2 = team2[0]
    return team1, team2, active_creature1, active_creature2

def attack_switch(client1, client2, active_creature1, active_creature2):
    send_message(client1, f"Your active creature is {active_creature1['creature']['name']}. Your available moves are:", "text")
    for move in active_creature1["creature"]["moves"]:
        if move["category"] == "physical" or move["category"] == "special":
            send_message(client1, f"{move['name']} | Type: {move['type']} | Category: {move['category']} | Power: {move['power']} | Accuracy: {move['accuracy']}", "text")
        else:
            send_message(client1, f"{move['name']} | Type: {move['type']} | Category: {move['category']} | Effect: {move['effect']}", "text")
    send_message(client2, f"Your active creature is {active_creature2['creature']['name']}. Your available moves are:", "text")
    for move in active_creature2["creature"]["moves"]:
        if move["category"] == "physical" or move["category"] == "special":
            send_message(client2, f"{move['name']} | Type: {move['type']} | Category: {move['category']} | Power: {move['power']} | Accuracy: {move['accuracy']}", "text")
        else:
            send_message(client2, f"{move['name']} | Type: {move['type']} | Category: {move['category']} | Effect: {move['effect']}", "text")
    attack_or_switch = ["attack", "switch"]
    send_message(client1, attack_or_switch, "msgpack")
    send_message(client2, attack_or_switch, "msgpack")
    send_message(client1, f"Your opponent's active creature is {active_creature2['creature']['name']}.\nWould you like to [attack] or [switch]?", "text")
    send_message(client2, f"Your opponent's active creature is {active_creature1['creature']['name']}.\nWould you like to [attack] or [switch]?", "text")

def player_move_choice(client, active_creature):
    player_moves = get_moves(active_creature)
    send_message(client, player_moves, "msgpack")
    player1_moves_names = get_moves_names(active_creature)
    send_message(client, player1_moves_names, "msgpack")
    send_message(client, "Which move would you like to use?", "text")
    player_move = client.recv(1024).decode()
    return player_move

def player_switch(team, active_creature, player_client, opponent_client, player_name):
    if team:
        for creature in team:
            if creature["creature"]["name"] == active_creature["creature"]["name"]:
                continue
            send_message(player_client, f"{creature['creature']['name']} | HP: {creature['stats']['hp']}/{creature['creature']['stats']['hp']}\n", "text")
        team_creature_names = get_team_creature_names(team)
        send_message(player_client, team_creature_names, "msgpack")
        send_message(player_client, "Which creature would you like to switch to?", "text")
        switch_in_creature = player_client.recv(1024).decode()
        for creature in team:
            if creature["creature"]["name"] == switch_in_creature:
                active_creature = creature
                break
        print(f"{player_name} has switched to {active_creature['creature']['name']}!")
        send_message(player_client, f"You have switched to {active_creature['creature']['name']}!", "text")
        send_message(opponent_client, f"Player1 switched to {active_creature['creature']['name']}!", "text")
    return active_creature

def both_attack(active_creature1, active_creature2, player1_move, player2_move, client1, client2):
    player1_first = False
    player2_first = False
    player1_can_act = True
    player2_can_act = True
    player1_can_act_check = {"return_statement": True, "removed_status": []}
    player2_can_act_check = {"return_statement": True, "removed_status": []}
    random_turn = 0
    if active_creature1['stats']['spd'] > active_creature2['stats']['spd']:
        player1_first = True
    elif active_creature1['stats']['spd'] < active_creature2['stats']['spd']:
        player2_first = True
    else:
        random_turn = random.randint(1, 2)
    
    if ((player1_first == True) or (random_turn == 1)):
        player1_can_act_check = logic.can_act_check(active_creature1)
        player1_can_act = False if player1_can_act_check['return_statement'] == False else True # if the creature is unable to act
        if player1_can_act:
            move_results = logic.apply_move("Player1's", "Player2's", active_creature1, active_creature2, player1_move)
            send_message(client1, move_results, "text")
            send_message(client2, move_results, "text")
        if active_creature2['stats']['hp'] == 0:
            print(f"Player2's {active_creature2['creature']['name']} has fainted!")
            send_message(client1, f"Player2's {active_creature2['creature']['name']} has fainted!", "text")
            send_message(client2, f"Your {active_creature2['creature']['name']} has fainted!", "text")
        else:
            player2_can_act_check = logic.can_act_check(active_creature2)
            player2_can_act = False if player2_can_act_check['return_statement'] == False else True # if the creature is unable to act
            if player2_can_act:
                move_results = logic.apply_move("Player2's", "Player1's", active_creature2, active_creature1, player2_move)
                send_message(client1, move_results, "text")
                send_message(client2, move_results, "text")
                if active_creature1['stats']['hp'] == 0:
                    print(f"Player1's {active_creature1['creature']['name']} has fainted!")
                    send_message(client1, f"Your {active_creature1['creature']['name']} has fainted!", "text")
                    send_message(client2, f"Player1's {active_creature1['creature']['name']} has fainted!", "text")
    elif ((player2_first == True) or (random_turn == 2)):
        player2_can_act_check = logic.can_act_check(active_creature2)
        player2_can_act = False if player2_can_act_check['return_statement'] == False else True # if the creature is unable to act
        if player2_can_act:
            move_results = logic.apply_move("Player2's", "Player1's", active_creature2, active_creature1, player2_move)
            send_message(client1, move_results, "text")
            send_message(client2, move_results, "text")
        if active_creature1['stats']['hp'] == 0:
            print(f"Player1's {active_creature1['creature']['name']} has fainted!")
            send_message(client1, f"Your {active_creature1['creature']['name']} has fainted!", "text")
            send_message(client2, f"Player1's {active_creature1['creature']['name']} has fainted!", "text")
        else:
            player1_can_act_check = logic.can_act_check(active_creature1)
            player1_can_act = False if player1_can_act_check['return_statement'] == False else True # if the creature is unable to act
            if player1_can_act:
                move_results = logic.apply_move("Player1's", "Player2's", active_creature1, active_creature2, player1_move)
                send_message(client1, move_results, "text")
                send_message(client2, move_results, "text")
                if active_creature2['stats']['hp'] == 0:
                    print(f"Player2's {active_creature2['creature']['name']} has fainted!")
                    send_message(client1, f"Player2's {active_creature2['creature']['name']} has fainted!", "text")
                    send_message(client2, f"Your {active_creature2['creature']['name']} has fainted!", "text")
    return player1_can_act, player2_can_act, player1_can_act_check, player2_can_act_check

def player1_attack(active_creature1, active_creature2, player1_move, client1, client2):
    player1_can_act_check = logic.can_act_check(active_creature1)
    player1_can_act = True
    if player1_can_act_check['return_statement'] == False: # if the creature is unable to act
        player1_can_act = False
    if player1_can_act:
        move_results = logic.apply_move("Player1's", "Player2's", active_creature1, active_creature2, player1_move)
        send_message(client1, move_results, "text")
        send_message(client2, move_results, "text")
    if active_creature2['stats']['hp'] == 0:
        print(f"Player2's {active_creature2['creature']['name']} has fainted!")
        send_message(client1, f"Player2's {active_creature2['creature']['name']} has fainted!", "text")
        send_message(client2, f"Your {active_creature2['creature']['name']} has fainted!", "text")
    return player1_can_act, player1_can_act_check

def player2_attack(active_creature1, active_creature2, player2_move, client1, client2):
    player2_can_act_check = logic.can_act_check(active_creature2)
    player2_can_act = True
    if player2_can_act_check['return_statement'] == False: # if the creature is unable to act
        player2_can_act = False
    if player2_can_act:
        move_results = logic.apply_move("Player2's", "Player1's", active_creature2, active_creature1, player2_move)
        send_message(client1, move_results, "text")
        send_message(client2, move_results, "text")
    if active_creature1['stats']['hp'] == 0:
        print(f"Player1's {active_creature1['creature']['name']} has fainted!")
        send_message(client1, f"Your {active_creature1['creature']['name']} has fainted!", "text")
        send_message(client2, f"Player1's {active_creature1['creature']['name']} has fainted!", "text")
    return player2_can_act, player2_can_act_check

def did_creatures_act(player1_can_act, player2_can_act, client1, client2):
    if player1_can_act is not None and player2_can_act is not None:
        if not player1_can_act and not player2_can_act:
            send_message(client1, "Both creatures are unable to act!", "text")
            send_message(client2, "Both creatures are unable to act!", "text")
    elif player1_can_act is not None:
        if not player1_can_act:
            send_message(client1, "Your creature was unable to act!", "text")
            send_message(client2, "Your opponent's creature was unable to act!", "text")
    elif player2_can_act is not None:
        if not player2_can_act:
            send_message(client1, "Your opponent's creature was unable to act!", "text")
            send_message(client2, "Your creature was unable to act!", "text")

def did_creatures_burn(active_creature1, active_creature2, client1, client2):
    if active_creature1['stats']['hp'] != 0:
        player1_burn_check = logic.burn_check(active_creature1)
        if player1_burn_check['damage_statement'] != "":
            print(f"Player1's {player1_burn_check['damage_statement']}")
            send_message(client1, f"Player1's {player1_burn_check['damage_statement']}", "text")
            send_message(client2, f"Player1's {player1_burn_check['damage_statement']}", "text")
            if active_creature1['stats']['hp'] == 0:
                print(f"Player1's {active_creature1['creature']['name']} has fainted!")
                send_message(client1, f"Your {active_creature1['creature']['name']} has fainted!", "text")
                send_message(client2, f"Player1's {active_creature1['creature']['name']} has fainted!", "text")
    if active_creature2['stats']['hp'] != 0:
        player2_burn_check = logic.burn_check(active_creature2)
        if player2_burn_check['damage_statement'] != "":
            print(f"Player2's {player2_burn_check['damage_statement']}")
            send_message(client1, f"Player2's {player2_burn_check['damage_statement']}", "text")
            send_message(client2, f"Your {player2_burn_check['damage_statement']}", "text")
            if active_creature2['stats']['hp'] == 0:
                print(f"Player2's {active_creature2['creature']['name']} has fainted!")
                send_message(client1, f"Player2's {active_creature2['creature']['name']} has fainted!", "text")
                send_message(client2, f"Your {active_creature2['creature']['name']} has fainted!", "text")

def any_status_removed(player1_can_act_check, player2_can_act_check, active_creature1, active_creature2, client1, client2):
    if player1_can_act_check is not None:
        if player1_can_act_check['removed_status'] != [] and active_creature1['stats']['hp'] != 0:
            send_message(client1, f"{player1_can_act_check['removed_status']} has been cured from Player1's {active_creature1['creature']['name']}!", "text")
            send_message(client2, f"{player1_can_act_check['removed_status']} has been cured from Player1's {active_creature1['creature']['name']}!", "text")
    if player2_can_act_check is not None:
        if player2_can_act_check['removed_status'] != [] and active_creature2['stats']['hp'] != 0:
            send_message(client1, f"{player2_can_act_check['removed_status']} has been cured from Player2's {active_creature2['creature']['name']}!", "text")
            send_message(client2, f"{player2_can_act_check['removed_status']} has been cured from Player2's {active_creature2['creature']['name']}!", "text")

def switch_fainted(active_creature, team, player_client, opponent_client, player_name):
    if active_creature['stats']['hp'] == 0:
        team.remove(active_creature)
        active_creature = None
        if team:
            for creature in team:
                send_message(player_client, f"{creature['creature']['name']} | HP: {creature['stats']['hp']}/{creature['creature']['stats']['hp']}\n", "text")
            team_creature_names = get_team_creature_names(team)
            send_message(player_client, team_creature_names, "msgpack")
            send_message(player_client, "Which creature would you like to switch to?", "text")
            player_switch = player_client.recv(1024).decode()
            for creature in team:
                if creature["creature"]["name"] == player_switch:
                    active_creature = creature
                    break
            print(f"{player_name} has switched to {active_creature['creature']['name']}!")
            send_message(player_client, f"You have switched to {active_creature['creature']['name']}!", "text")
            send_message(opponent_client, f"Player1 has switched to {active_creature['creature']['name']}!", "text")
    return active_creature

def close_game(client1, client2, server_socket):
    # Keep the server running
    input("Press Enter to exit...")

    client1.close()
    client2.close()
    server_socket.close()
    time.sleep(1)

def get_moves(creature):
    return creature["creature"]["moves"]

def get_moves_names(creature):
    moves = []
    for move in creature["creature"]["moves"]:
        moves.append(move["name"])
    return moves

def get_team_creature_names(team):
    team_creature_names = []
    for creature in team:
        team_creature_names.append(creature["creature"]["name"])
    return team_creature_names

if __name__ == "__main__":
    main()
        
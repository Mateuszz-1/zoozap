import socket
import random
from code import logic

def main():
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

    team1 = []
    team2 = []
    for i in range(6):
        creature_name1 = random.choice(list(logic.creatures_dict.keys()))
        creature_name2 = random.choice(list(logic.creatures_dict.keys()))
        creature_data1 = logic.creatures_dict[creature_name1]
        creature_data2 = logic.creatures_dict[creature_name2]
        team1.append({"creature": creature_data1, "stats": creature_data1["stats"], "status": [], "status_duration": []})
        team2.append({"creature": creature_data2, "stats": creature_data2["stats"], "status": [], "status_duration": []})
    print(team1) # for testing
    print(team2) # for testing
    active_creature1 = team1[0]
    active_creature2 = team2[0]
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
    client1.sendall("Your opponent's active creature is {active_creature2['creature']['name']}".encode())
    client2.sendall("Your opponent's active creature is {active_creature1['creature']['name']}".encode())
    client1.sendall("Would you like to [attack] or [switch]?".encode())
    client2.sendall("Would you like to [attack] or [switch]?".encode())
    player1_choice = client1.recv(1024).decode()
    player2_choice = client2.recv(1024).decode()
    if player1_choice == "attack":
        client1.sendall("Which move would you like to use?".encode())
        player1_move = client1.recv(1024).decode()
    else:
        client1.sendall("Which creature would you like to switch to?".encode())
        client1.sendall("Your available creatures are:".encode())
        for creature in team1:
            client1.sendall(f"{creature['creature']['name']} | HP: {creature['stats']['hp']}/{creature['creature']['stats']['hp']}".encode())
        player1_switch = client1.recv(1024).decode()
        active_creature1 = team1[player1_switch]
    if player2_choice == "attack":
        client2.sendall("Which move would you like to use?".encode())
        player2_move = client2.recv(1024).decode()
    else:
        client2.sendall("Which creature would you like to switch to?".encode())
        client2.sendall("Your available creatures are:".encode())
        for creature in team2:
            client2.sendall(f"{creature['creature']['name']} | HP: {creature['stats']['hp']}/{creature['creature']['stats']['hp']}".encode())
        player2_switch = client2.recv(1024).decode()
        active_creature2 = team2[player2_switch]
    if player1_choice == "attack" and player2_choice == "attack":
        if active_creature1['stats']['spd'] >= active_creature2['stats']['spd']:
            logic.apply_move(active_creature1, active_creature2, player1_move)
            if active_creature2['stats']['hp'] == 0:
                team2.remove(active_creature2)
                client1.sendall(f"{active_creature2['creature']['name']} has fainted!".encode())
                client2.sendall(f"{active_creature2['creature']['name']} has fainted!".encode())
            else:
                logic.apply_move(active_creature2, active_creature1, player2_move)
                if active_creature1['stats']['hp'] == 0:
                    team1.remove(active_creature1)
                    client1.sendall(f"{active_creature1['creature']['name']} has fainted!".encode())
                    client2.sendall(f"{active_creature1['creature']['name']} has fainted!".encode())
    while team1 and team2:
        pass
    if team1:
        print("Team 1 wins!")
    else:
        print("Team 2 wins!")
    # Keep the server running
    input("Press Enter to exit...")

    client1.close()
    client2.close()
    server_socket.close()

if __name__ == "__main__":
    main()

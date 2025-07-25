import os
import random

PLAYER_FILE = "savefile.txt"


def main():
    while True:
        print("""
---------------- Welcome to Sundrop Caves! ----------------
You spent all your money to get the deed to a mine, a small
backpack, a simple pickaxe and a magical portal stone.

How quickly can you get the 500 GP you need to retire
and live happily ever after?
-----------------------------------------------------------

--- Main Menu ----
(N)ew game
(L)oad saved game
(Q)uit
------------------
        """)
        choice = input("Your choice? ").strip().lower()
        if choice == 'n':
            new_game()
        elif choice == 'l':
            load_game()
        elif choice == 'q':
            print("Goodbye miner!")
            break
        else:
            print("Invalid choice!")


def new_game():
    name = input("Greetings, miner! What is your name? ")
    mine_map = [['?' for _ in range(10)] for _ in range(10)]
    mine_map[0][0] = 'T'
    place_minerals(mine_map)
    player = {
        "name": name,
        "gp": 0,
        "backpack_size": 10,
        "load": 0,
        "day": 1,
        "steps": 0,
        "pickaxe_level": 1,
        "position": [0, 0],
        "portal": None,
        "ore": {"copper": 0, "silver": 0, "gold": 0},
        "map": mine_map
    }
    print(f"Pleased to meet you, {name}. Welcome to Sundrop Town!")
    town_menu(player)


def place_minerals(mine_map):
    minerals = ['C'] * 10 + ['S'] * 6 + ['G'] * 4
    for symbol in minerals:
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if mine_map[y][x] == '?':
                mine_map[y][x] = symbol
                break


def load_game():
    if not os.path.exists(PLAYER_FILE):
        print("No saved game found.")
        return
    with open(PLAYER_FILE, "r") as file:
        lines = [line.strip() for line in file.readlines()]
    name = lines[0]
    gp = int(lines[1])
    backpack_size = int(lines[2])
    load = int(lines[3])
    day = int(lines[4])
    steps = int(lines[5])
    pickaxe_level = int(lines[6])
    pos_x, pos_y = map(int, lines[7].split(','))
    portal_x, portal_y = lines[8].split(',')
    portal = [int(portal_x), int(portal_y)] if portal_x != 'None' else None
    ores = {'copper': int(lines[9]), 'silver': int(lines[10]), 'gold': int(lines[11])}
    mine_map = [list(line) for line in lines[12:]]

    player = {
        "name": name, "gp": gp, "backpack_size": backpack_size,
        "load": load, "day": day, "steps": steps,
        "pickaxe_level": pickaxe_level,
        "position": [pos_x, pos_y],
        "portal": portal, "ore": ores,
        "map": mine_map
    }
    print(f"Welcome back, {player['name']}!")
    town_menu(player)


def town_menu(player):
    while True:
        sell_ore(player)
        print(f"\nDAY {player['day']}")
        print("""
----- Sundrop Town -----
(B)uy stuff
See Player (I)nformation
See Mine (M)ap
(E)nter mine
Sa(V)e game
(Q)uit to main menu
------------------------
        """)
        choice = input("Your choice? ").strip().lower()
        if choice == 'b':
            buy_stuff(player)
        elif choice == 'i':
            show_player_info(player)
        elif choice == 'm':
            show_map(player)
        elif choice == 'e':
            enter_mine(player)
        elif choice == 'v':
            save_game(player)
        elif choice == 'q':
            break
        else:
            print("Invalid choice!")


def sell_ore(player):
    total = 0
    prices = {
        "copper": random.randint(1, 3),
        "silver": random.randint(5, 8),
        "gold": random.randint(10, 18)
    }
    for ore in ["copper", "silver", "gold"]:
        qty = player.get("ore", {}).get(ore, 0)
        if qty > 0:
            gp = qty * prices[ore]
            print(f"You sell {qty} {ore} ore for {gp} GP.")
            total += gp
            player["ore"][ore] = 0
    player["gp"] += total
    if total > 0:
        print(f"You now have {player['gp']} GP!")
    player["load"] = 0
    if player["gp"] >= 500:
        print(f"\nWoo-hoo! Well done, {player['name']}, you have {player['gp']} GP!")
        print(f"You now have enough to retire after {player['day']} days and {player['steps']} steps! You win!\n")
        exit()


def buy_stuff(player):
    while True:
        next_pickaxe = player["pickaxe_level"] + 1
        pickaxe_price = {2: 50, 3: 150}.get(next_pickaxe)
        backpack_cost = player["backpack_size"] * 2
        print(f"""
----------------------- Shop Menu -------------------------
(P)ickaxe upgrade to Level {next_pickaxe} for {pickaxe_price} GP
(B)ackpack upgrade to carry {player['backpack_size'] + 2} items for {backpack_cost} GP
(L)eave shop
-----------------------------------------------------------
GP: {player['gp']}
-----------------------------------------------------------
        """)
        choice = input("Your choice? ").strip().lower()
        if choice == 'b':
            if player["gp"] >= backpack_cost:
                player["gp"] -= backpack_cost
                player["backpack_size"] += 2
                print(f"Congratulations! You can now carry {player['backpack_size']} items!")
            else:
                print("You don't have enough GP!")
        elif choice == 'p' and pickaxe_price:
            if player["gp"] >= pickaxe_price:
                player["gp"] -= pickaxe_price
                player["pickaxe_level"] += 1
                print(f"Congratulations! You can now mine level {player['pickaxe_level']} ores!")
            else:
                print("You don't have enough GP!")
        elif choice == 'l':
            break
        else:
            print("Invalid choice!")


def show_player_info(player):
    print(f"""
----- Player Information -----
Name: {player['name']}
Pickaxe level: {player['pickaxe_level']}
Load: {player['load']} / {player['backpack_size']}
GP: {player['gp']}
Steps taken: {player['steps']}
------------------------------
""")


def show_map(player):
    portal_pos = player.get("portal")
    px, py = player["position"]
    print("\n+--------------------+")
    for y in range(10):
        row = ""
        for x in range(10):
            if abs(x - px) <= 1 and abs(y - py) <= 1:
                if [x, y] == player["position"]:
                    row += "M "
                elif portal_pos and [x, y] == portal_pos:
                    row += "P "
                else:
                    row += f"{player['map'][y][x]} "
            else:
                row += "? "
        print("|" + row.strip() + "|")
    print("+--------------------+")
    
def show_map(player):
    portal_pos = player.get("portal")
    px, py = player["position"]
    print("\n+--------------------+")
    for y in range(10):
        row = ""
        for x in range(10):
            if abs(x - px) <= 1 and abs(y - py) <= 1:
                if [x, y] == player["position"]:
                    row += "M "
                elif portal_pos and [x, y] == portal_pos:
                    row += "P "
                else:
                    row += f"{player['map'][y][x]} "
            else:
                row += "? "
        print("|" + row.strip() + "|")
    print("+--------------------+")



def enter_mine(player):
    print(f"\nDAY {player['day']}")
    moves = 20
    x, y = player["position"]

    while moves > 0:
        print(f"Turns left: {moves}    Load: {player['load']} / {player['backpack_size']}    Steps: {player['steps']}")
        action = input("(WASD) to move, (M)ap, (P)ortal, (Q)uit to town: ").strip().lower()
        if action == 'm':
            show_map(player)
            continue
        elif action == 'p':
            player["portal"] = [x, y]
            print("You place your portal stone here and zap back to town.")
            return
        elif action in ['w', 'a', 's', 'd']:
            new_x, new_y = x, y
            if action == 'w' and y > 0:
                new_y -= 1
            elif action == 's' and y < 9:
                new_y += 1
            elif action == 'a' and x > 0:
                new_x -= 1
            elif action == 'd' and x < 9:
                new_x += 1

            x, y = new_x, new_y
            player["position"] = [x, y]
            player["map"][y][x] = player["map"][y][x]
            player["steps"] += 1
            moves -= 1

            symbol = player["map"][y][x]
            if symbol in ['C', 'S', 'G']:
                if (symbol == 'C') or (symbol == 'S' and player["pickaxe_level"] >= 2) or (symbol == 'G' and player["pickaxe_level"] == 3):
                    ore_type = {'C': 'copper', 'S': 'silver', 'G': 'gold'}[symbol]
                    max_gain = {'C': 5, 'S': 3, 'G': 2}[symbol]
                    gained = random.randint(1, max_gain)
                    space = player["backpack_size"] - player["load"]
                    actual_gain = min(gained, space)
                    player["ore"][ore_type] += actual_gain
                    player["load"] += actual_gain
                    print(f"You mined {actual_gain} piece(s) of {ore_type}.")
                    player["map"][y][x] = " "
                else:
                    print("Your pickaxe cannot mine this mineral.")
            else:
                print("There's nothing valuable here.")
        elif action == 'q':
            break
        else:
            print("Invalid action!")
    player["day"] += 1


def save_game(player):
    with open(PLAYER_FILE, "w") as file:
        file.write(f"{player['name']}\n")
        file.write(f"{player['gp']}\n")
        file.write(f"{player['backpack_size']}\n")
        file.write(f"{player['load']}\n")
        file.write(f"{player['day']}\n")
        file.write(f"{player['steps']}\n")
        file.write(f"{player['pickaxe_level']}\n")
        file.write(f"{player['position'][0]},{player['position'][1]}\n")
        file.write(f"{player.get('portal', [None, None])[0]},{player.get('portal', [None, None])[1]}\n")
        for ore in ["copper", "silver", "gold"]:
            file.write(f"{player['ore'][ore]}\n")
        for row in player["map"]:
            file.write("".join(row) + "\n")
    print("Game saved.")


main()
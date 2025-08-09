from random import randint

player = {}
game_map = []
fog = []

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}
pickaxe_price = [50, 150]
mineral_pieces = {'copper': (1, 5), 'silver': (1, 3), 'gold': (1, 2)}
prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    map_file = open(filename, 'r')
    global MAP_WIDTH
    global MAP_HEIGHT
    map_struct.clear()
    
    # TODO: Add your map loading code here
    for line in map_file:
        line = line.strip()
        if line:
            map_struct.append(list(line))
    if map_struct:
        MAP_WIDTH = len(map_struct[0])
        MAP_HEIGHT = len(map_struct)
    else:
        print("Error; Empty map file")
        map_file.close()
        return False

    map_file.close()
    return True

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    x , y = player['x'], player['y']
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            nx , ny = x + dx, y + dy
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                fog[ny][nx] = game_map[ny][nx]
    return

def initialize_game(game_map, fog, player):
    # initialize map
    load_map("level1.txt", game_map)

    # TODO: initialize fog
def initialize_fog(fog):
    fog.clear()
    for _ in range(MAP_HEIGHT):
        fog.append(['?'] * MAP_WIDTH)
    # TODO: initialize player
    #   You will probably add other entries into the player dictionary
    player['name'] = ""
    player['x'] = 0
    player['y'] = 0
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['day'] = 1
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['load'] = 0
    player['max_load'] = 10
    player['pickaxe'] = 1
    player['portal_x'] = 0
    player['portal_y'] = 0
    
    clear_fog(fog, player)
    return True

def clear_fog(fog, player): 
    x, y = player['x'], player['y']
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                fog[ny][nx] = game_map[ny][nx]

def initialize_game(game_map, fog, player):
    if not load_map("level1.txt", game_map):
        return False
    initialize_fog(fog)

# This function draws the entire map, covered by the fof
def draw_map(game_map, fog, player):
    print("+" + "-" * MAP_WIDTH + "+")
    for y in range(MAP_HEIGHT):
        print("|", end="")
        for x in range(MAP_WIDTH):
            if x == player['x'] and y == player['y'] and player.get('in_mine', False):
                print("M", end="")
            elif x == player['portal_x'] and y == player['portal_y'] and not player.get('in_mine', False):
                print("P", end="")
            elif x == 0 and y == 0 and not player.get('in_mine', False):
                print("T", end="")
            else:
                print(fog[y][x], end="")
        print("|")
    print("+" + "-" * MAP_WIDTH + "+")


# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    x , y = player['x'], player['y']
    print("+" + "---" * 3 + "+")
    for dy in[-1, 0, 1]:
        print("|", end="")
        for dx in [-1, 0, 1]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                if dx == player['x'] and dy == player['y']:
                    print("M", end="")
                elif game_map[ny][nx] == ' ':
                    print(" ", end="")
                else:
                    print(f"{game_map[ny][nx]}", end="")
            else:
                print("#", end="")
        print("|")
    print("+" + "---" * 3 + "+")

# This function shows the information for the player
def show_information(player):
    print("\n--- Player Information ---")
    print(f"Name: {player['name']}")
    print(f"Current position: ({player['x']}, {player['y']})")
    print(f"Pickaxe level: {player['pickaxe']} ({' copper' if player['pickaxe'] == 1 else ' silver' if player['pickaxe'] == 2 else ' copper, silver, gold'})")
    print(f"Gold:{player['gold']}")
    print(f"Silver: {player['silver']}")
    print(f"Copper: {player['copper']}")
    print("--------------------------")
    print(f"Load: {player['load']} / {player['max_load']}")
    print("--------------------------")
    print(f"GP: {player['GP']}")
    print(f"Steps taken: {player['steps']}")
    print("--------------------------")
    print(f"DAY {player['day']}")
    

# This function saves the game
def save_game(game_map, fog, player):
    f = open("saved_game.txt", "w")

    for key, value in player.items():
        if isinstance(value , (int, str)):
            f.write(f"{key}:{value}\n")
        
    f.write("fog:\n")
    for row in fog:
        f.write("".join(row) + "\n")
    f.write("map:\n")
    for row in game_map:
        f.write("".join(row) + "\n")
    
    f.close()
    print("Game saved successfully.")
    return True
 
# This function loads the game
def load_game(game_map, fog, player):
    f = open("saved_game.txt", "r")
    lines = f.readlines()
    f.close()
    
    # Reset structures
    player.clear()
    fog.clear()
    game_map.clear()
    
    # 1. Load player data
    i = 0
    while i < len(lines) and lines[i].strip() != "fog:":
        key, value = lines[i].strip().split(":", 1)
        if value.isdigit():
            player[key] = int(value)
        else:
            player[key] = value
        i += 1
    
    # 2. Load fog data
    i += 1 
    while i < len(lines) and lines[i].strip() != "map:":
        fog.append(list(lines[i].strip()))
        i += 1
    
    # 3. Load map data 
    i += 1 
    while i < len(lines):
        game_map.append(list(lines[i].strip()))
        i += 1
    
    # Update global map dimensions
    global MAP_WIDTH, MAP_HEIGHT
    MAP_WIDTH = len(game_map[0]) if game_map else 0
    MAP_HEIGHT = len(game_map) if game_map else 0
    
    print("Game loaded.")
    return True

def sell_ores(player):
    total = 0
    if player['copper'] > 0:
        copper_price = randint(*prices['copper'])
        total += player['copper'] * copper_price
        print(f"You sell {player['copper']} copper ore for {player['copper'] * copper_price} GP.")
        player['copper'] = 0
    
    if player['silver'] > 0:
        silver_price = randint(*prices['silver'])
        total += player['silver'] * silver_price
        print(f"You sell {player['silver']} silver ore for {player['silver'] * silver_price} GP.")
        player['silver'] = 0
    
    if player['gold'] > 0:
        gold_price = randint(*prices['gold'])
        total += player['gold'] * gold_price
        print(f"You sell {player['gold']} gold ore for {player['gold'] * gold_price} GP.")
        player['gold'] = 0
    
    if total > 0:
        player['GP'] += total
        print(f"You now have {player['GP']} GP!")
    
    player['load'] = 0
def check_win_condition(player):
    if player['GP'] >= WIN_GP:
        print(f"\nWoo-hoo! Well done, {player['name']}, you have {player['GP']} GP!")
        print("You now have enough to retire and play video games every day.")
        print(f"And it only took you {player['day']} days and {player['steps']} steps! You win!\n")
        return True
    return False
def show_main_menu():
    print("\n--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
    print("(Q)uit")
    print("------------------")

def show_town_menu():
    # TODO: Show Day
    print(f"\nDAY {player['day']}")
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")
def show_shop_menu():
    print("\n--- Shop Menu ---")
    print(f"(B)ackpack upgrade to carry {player['max_load'] + 2} items for {player['max_load'] * 2} GP")
    print("(L)eave shop")
    print("------------------")
    print(f"GP: {player['GP']}")
    print("------------------")

def show_mine_menu():
    print(f"\nDAY {player['day']}")
    draw_view(game_map, fog, player)
    print(f"Turns left: {player['turns']} | Load: {player['load']} / {player['max_load']} | Steps: {player['steps']}")
    print(" (WASD) to move")
    print(" (M)ap, (I)nformation, (P)ortal, (Q)uit to Main Menu")

def mine_mineral(player, mineral):
    if player['load'] >= player['max_load']:
        print("Your backpack is full!")
        return False
    
    mineral_type = mineral_names.get(mineral, '')
    if not mineral_type:
        return False
    
    if (mineral_type == 'silver' and player['pickaxe'] < 2) or (mineral_type == 'gold' and player['pickaxe'] < 3):
        print(f"You need a better pickaxe to mine {mineral_type}!")
        return False
    
    pieces = randint(*mineral_pieces[mineral_type])
    available_space = player['max_load'] - player['load']
    pieces = min(pieces, available_space)
    
    player[mineral_type] += pieces
    player['load'] += pieces
    print(f"You mined {pieces} piece(s) of {mineral_type}.")
    
    if player['load'] >= player['max_load']:
        print("Your backpack is full!")
    
    return True
def move_player(player, dx, dy):
    new_x = player['x'] + dx
    new_y = player['y'] + dy
    
    if not (0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT):
        print("You can't move there - it's the edge of the mine!")
        return False
    
    mineral = game_map[new_y][new_x]
    
    if mineral == 'T' and new_x == 0 and new_y == 0:
        print("You return to town.")
        player['in_mine'] = False
        player['day'] += 1
        player['turns'] = TURNS_PER_DAY
        sell_ores(player)
        return True
    
    if mineral in ['C', 'S', 'G']:
        if not mine_mineral(player, mineral):
            return False
    
    player['x'] = new_x
    player['y'] = new_y
    player['steps'] += 1
    player['turns'] -= 1
    clear_fog(fog, player)
    
    if player['turns'] <= 0:
        print("You are exhausted.")
        use_portal(player)
        return True
    
    return True
def use_portal(player):
    player ['portal_x'] = player['x']
    player ['portal_y'] = player['y']
    player['in_mine'] = False
    player['day'] += 1
    player['turns'] = TURNS_PER_DAY
    print("You use the portal stone to return to town.")
    sell_ores(player)

def buy_backpack_upgrade(player):
    cost = player['max_load'] * 2
    if player ['GP'] >= cost:
        player['GP'] -= cost
        player['max_load'] += 2
        print(f"You bought a backpack upgrade! You can now carry {player['max_load']} items.")
    else:
        print(" You dont have enough GP!")
#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 1000 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

# TODO: The game!
while True:
    if game_state == "main":
        show_main_menu()
        choice = input(" Your choice?").upper()

        if choice == 'N':
            player_name = input("Greetings, miner! What is your name? ")
            player['name'] = player_name
            print(f"Plseased to meet you , {player_name}. Welcome to Sundrop Caves!")
            if initialize_game(game_map, fog, player):
                game_state = "town"
            else:
                print("Failed to initialize game. Exiting.")
                break
        elif choice == 'L':
            if load_game(game_map, fog, player):
                game_state = "town"
        elif choice == 'Q':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

    elif game_state == "town":
        show_town_menu()
        choice = input(" Your choice?").upper()

        if choice == 'B':
            shop_state = True
            while shop_state:
                show_shop_menu()
                shop_choice = input(" Your choice?").upper()
                if shop_choice == 'B':
                    buy_backpack_upgrade(player)
                elif shop_choice == 'L':
                    shop_state = False
                else:
                    print("Invalid choice. Please try again.")
        elif choice == 'I':
            show_information(player)
        elif choice == 'M':
            draw_map(game_map, fog, player)
        elif choice == 'E':
            player['in_mine'] = True
            if player['portal_x'] != 0 or player['portal_y'] != 0:
                player['x'] = player['portal_x']
                player['y'] = player['portal_y']
            else:
                player['x'] = 0
                player['y'] = 0
            game_state = "mine"
        elif choice == 'V':
            save_game(game_map, fog, player)
        elif choice == 'Q':
            game_state = "main"
        else:
            print("Invalid choice. Please try again.")

        if not player.get('in_mine', False) and check_win_condition(player):
            game_state = "main"

    elif game_state == "mine":
        show_mine_menu()
        action = input("Action?").upper()
        dx, dy = 0, 0
        if action in ['W', 'A', 'S', 'D']:
            if action == 'W':
                dy = -1
            elif action == 'A':
                dx = -1
            elif action == 'S':
                dy = 1
            elif action == 'D':
                dx = 1

            if move_player(player, dx, dy):
                if not player.get('in_mine', False):
                    game_state = "town"
        elif action == 'M':
            draw_map(game_map, fog, player)
        elif action == 'I':
            show_information(player)
        elif action == 'P':
            use_portal(player)
            game_state = "town"
        elif action == 'Q':
            game_state = "main"
        else:
            print("Invalid action. Please try again.")

        if player.get('turns', 0) <= 0 and player.get('in_mine', False):
            use_portal(player)
            game_state = "town"
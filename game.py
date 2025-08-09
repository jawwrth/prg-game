from random import randint

player = {}
game_map = []
fog = []

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 1000  # goal to win

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}
pickaxe_price = [50, 150]  # legacy list (not used directly)
mineral_pieces = {'copper': (1, 5), 'silver': (1, 3), 'gold': (1, 2)}
prices = {'copper': (1, 3), 'silver': (5, 8), 'gold': (10, 18)}

# -------------------------
# File / score utilities
# -------------------------
def read_top_score():
    # open in a+ so it is created if missing, then read from start
    f = open("top_score.txt", "a+")
    f.seek(0)
    content = f.read().strip()
    f.close()
    if content.isdigit():
        return int(content)
    return 0

def write_top_score(score):
    f = open("top_score.txt", "w")
    f.write(str(int(score)))
    f.close()

def update_top_score_if_needed(player):
    top = read_top_score()
    if player.get('GP', 0) > top:
        write_top_score(player['GP'])
        print("🎉 New top GP score!")

def show_top_score():
    top = read_top_score()
    print(f"🏆 Top GP ever achieved: {top}")

# -------------------------
# Map load / fog functions
# -------------------------
def load_map(filename, map_struct):
    map_struct.clear()
    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    if len(lines) == 0:
        print("Error: Empty map file")
        return False

    for line in lines:
        line = line.rstrip("\n").rstrip("\r")
        line = line.strip()
        if line:
            map_struct.append(list(line))

    if not map_struct:
        print("Error: No valid map data")
        return False

    global MAP_WIDTH, MAP_HEIGHT
    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)
    return True

def initialize_fog(fog):
    fog.clear()
    for _ in range(MAP_HEIGHT):
        fog.append(['?'] * MAP_WIDTH)

def clear_fog(fog, player):
    x, y = player['x'], player['y']
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                fog[ny][nx] = game_map[ny][nx]

# -------------------------
# Game initialization
# -------------------------
def initialize_game(game_map, fog, player):
    if not load_map("level1.txt", game_map):
        return False

    initialize_fog(fog)

    player['name'] = ""
    player['x'] = 0
    player['y'] = 0
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['warehouse_copper'] = 0
    player['warehouse_silver'] = 0
    player['warehouse_gold'] = 0
    player['day'] = 1
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['load'] = 0
    player['max_load'] = 10
    player['pickaxe'] = 1           # pickaxe level (1=copper,2=silver,3=gold)
    player['portal_x'] = 0
    player['portal_y'] = 0
    player['in_mine'] = False

    clear_fog(fog, player)
    return True

# -------------------------
# Drawing / view functions
# -------------------------
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

def draw_view(game_map, fog, player):
    x, y = player['x'], player['y']
    print("+" + "---" * 3 + "+")
    for dy in [-1, 0, 1]:
        print("|", end="")
        for dx in [-1, 0, 1]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                if nx == player['x'] and ny == player['y']:
                    print(" M ", end="")
                elif game_map[ny][nx] == ' ':
                    print("   ", end="")
                else:
                    print(f" {game_map[ny][nx]} ", end="")
            else:
                print(" # ", end="")
        print("|")
    print("+" + "---" * 3 + "+")

# -------------------------
# Player info / save/load
# -------------------------
def show_information(player):
    print("\n--- Player Information ---")
    print(f"Name: {player['name']}")
    print(f"Current position: ({player['x']}, {player['y']})")
    px = player.get('pickaxe', 1)
    px_name = 'copper' if px == 1 else 'silver' if px == 2 else 'gold'
    print(f"Pickaxe level: {player['pickaxe']} ({px_name})")
    print(f"Gold ore: {player['gold']}")
    print(f"Silver ore: {player['silver']}")
    print(f"Copper ore: {player['copper']}")
    print("--------------------------")
    print(f"Load: {player['load']} / {player['max_load']}")
    print("--------------------------")
    print(f"GP: {player['GP']}")
    print(f"Warehouse copper: {player.get('warehouse_copper', 0)}")
    print(f"Warehouse silver: {player.get('warehouse_silver', 0)}")
    print(f"Warehouse gold: {player.get('warehouse_gold', 0)}")
    print(f"Steps taken: {player['steps']}")
    print("--------------------------")
    print(f"DAY {player['day']}")

def save_game(game_map, fog, player):
    f = open("saved_game.txt", "w")
    for key, value in player.items():
        if isinstance(value, (int, str)):
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

def load_game(game_map, fog, player):
    f = open("saved_game.txt", "r")
    lines = f.readlines()
    f.close()

    if len(lines) == 0:
        print("Error: Saved game file is empty.")
        return False

    player.clear()
    fog.clear()
    game_map.clear()

    i = 0
    while i < len(lines) and lines[i].strip() != "fog:":
        parts = lines[i].strip().split(":", 1)
        if len(parts) == 2:
            key, value = parts
            # keep numeric fields as ints, otherwise string
            if value.lstrip("-").isdigit():
                player[key] = int(value)
            else:
                player[key] = value
        i += 1

    i += 1
    while i < len(lines) and lines[i].strip() != "map:":
        fog.append(list(lines[i].strip()))
        i += 1

    i += 1
    while i < len(lines):
        game_map.append(list(lines[i].strip()))
        i += 1

    global MAP_WIDTH, MAP_HEIGHT
    MAP_WIDTH = len(game_map[0]) if game_map else 0
    MAP_HEIGHT = len(game_map) if game_map else 0

    print("Game loaded.")
    return True

# -------------------------
# Selling ores
# -------------------------
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
        # update top score if GP increased
        update_top_score_if_needed(player)

    player['load'] = 0

# -------------------------
# Warehouse functions
# -------------------------
def warehouse_menu(player):
    while True:
        print("\n--- Warehouse ---")
        print(f"Carrying: Copper: {player['copper']}, Silver: {player['silver']}, Gold: {player['gold']}")
        print(f"Stored: Copper: {player['warehouse_copper']}, Silver: {player['warehouse_silver']}, Gold: {player['warehouse_gold']}")
        print("(D)eposit minerals")
        print("(W)ithdraw minerals")
        print("(S)ell stored minerals")
        print("(L)eave warehouse")
        choice = input("Your choice? ").upper()

        if choice == 'D':
            mineral = input("Which mineral to deposit? (C)opper, (S)ilver, (G)old: ").upper()
            if mineral in ['C', 'S', 'G']:
                mineral_type = mineral_names[mineral]
                amount_str = input(f"How much {mineral_type} to deposit? (max {player[mineral_type]}): ")
                if amount_str.isdigit():
                    amount = int(amount_str)
                    if amount <= 0:
                        print("Amount must be positive.")
                    elif amount <= player[mineral_type]:
                        player[mineral_type] -= amount
                        player[f'warehouse_{mineral_type}'] += amount
                        print(f"Deposited {amount} {mineral_type} to warehouse.")
                    else:
                        print("You don't have that much.")
                else:
                    print("Invalid amount.")
            else:
                print("Invalid mineral type.")

        elif choice == 'W':
            mineral = input("Which mineral to withdraw? (C)opper, (S)ilver, (G)old: ").upper()
            if mineral in ['C', 'S', 'G']:
                mineral_type = mineral_names[mineral]
                amount_str = input(f"How much {mineral_type} to withdraw? (max {player[f'warehouse_{mineral_type}']}): ")
                if amount_str.isdigit():
                    amount = int(amount_str)
                    if amount <= 0:
                        print("Amount must be positive.")
                    elif amount <= player[f'warehouse_{mineral_type}']:
                        if player['load'] + amount <= player['max_load']:
                            player[f'warehouse_{mineral_type}'] -= amount
                            player[mineral_type] += amount
                            player['load'] += amount
                            print(f"Withdrew {amount} {mineral_type} from warehouse.")
                        else:
                            print("Not enough space in your backpack!")
                    else:
                        print("Not enough in warehouse.")
                else:
                    print("Invalid amount.")
            else:
                print("Invalid mineral type.")

        elif choice == 'S':
            total = 0
            if player['warehouse_copper'] > 0:
                copper_price = randint(*prices['copper'])
                total += player['warehouse_copper'] * copper_price
                print(f"You sell {player['warehouse_copper']} warehouse copper ore for {player['warehouse_copper'] * copper_price} GP.")
                player['warehouse_copper'] = 0

            if player['warehouse_silver'] > 0:
                silver_price = randint(*prices['silver'])
                total += player['warehouse_silver'] * silver_price
                print(f"You sell {player['warehouse_silver']} warehouse silver ore for {player['warehouse_silver'] * silver_price} GP.")
                player['warehouse_silver'] = 0

            if player['warehouse_gold'] > 0:
                gold_price = randint(*prices['gold'])
                total += player['warehouse_gold'] * gold_price
                print(f"You sell {player['warehouse_gold']} warehouse gold ore for {player['warehouse_gold'] * gold_price} GP.")
                player['warehouse_gold'] = 0

            if total > 0:
                player['GP'] += total
                print(f"You now have {player['GP']} GP!")
                update_top_score_if_needed(player)

        elif choice == 'L':
            break
        else:
            print("Invalid choice.")

# -------------------------
# Win condition
# -------------------------
def check_win_condition(player):
    if player['GP'] >= WIN_GP:
        print(f"\nWoo-hoo! Well done, {player['name']}, you have {player['GP']} GP!")
        print("You now have enough to retire and play video games every day.")
        print(f"And it only took you {player['day']} days and {player['steps']} steps! You win!\n")
        update_top_score_if_needed(player)
        return True
    return False

# -------------------------
# Menus (town / shop / warehouse)
# -------------------------
def show_main_menu():
    print("\n--- Main Menu ---")
    print("(N)ew game")
    print("(L)oad saved game")
    print("(T)op score")
    print("(Q)uit")
    print("------------------")

def show_town_menu():
    print(f"\nDAY {player['day']}")
    print("--- Sundrop Town ---")
    print("(B)uy stuff")
    print("(H) Warehouse")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("---------------------")

def show_shop_menu():
    print("\n--- Shop Menu ---")
    print(f"(B)ackpack upgrade to carry {player['max_load'] + 2} items for {player['max_load'] * 2} GP")
    print(f"(P)ickaxe upgrade to level {player['pickaxe'] + 1} for {pickaxe_upgrade_cost(player)} GP")
    print("(L)eave shop")
    print("------------------")
    print(f"GP: {player['GP']}")
    print("------------------")

def show_mine_menu():
    print(f"\nDAY {player['day']}")
    draw_view(game_map, fog, player)
    print(f"Turns left: {player['turns']} | Load: {player['load']} / {player['max_load']} | Steps: {player['steps']}")
    print("(WASD) to move")
    print("(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu")

def pickaxe_upgrade_cost(player):
    # cost scales with current pickaxe level
    return player['pickaxe'] * 100

# -------------------------
# Mining & movement
# -------------------------
def mine_mineral(player, mineral):
    if player['load'] >= player['max_load']:
        print("Your backpack is full!")
        return False

    mineral_type = mineral_names.get(mineral, '')
    if not mineral_type:
        return False

    # check pickaxe requirement
    if (mineral_type == 'silver' and player['pickaxe'] < 2) or (mineral_type == 'gold' and player['pickaxe'] < 3):
        print(f"You need a better pickaxe to mine {mineral_type}!")
        return False

    base_pieces = randint(*mineral_pieces[mineral_type])

    # pickaxe gives bonus pieces: each level above 1 adds +1 piece (simple)
    bonus = max(0, player['pickaxe'] - 1)
    pieces = base_pieces + bonus

    available_space = player['max_load'] - player['load']
    pieces = min(pieces, available_space)

    player[mineral_type] += pieces
    player['load'] += pieces
    print(f"You mined {pieces} piece(s) of {mineral_type} (base {base_pieces} + bonus {bonus}).")

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

    # Returning to town (tile 'T' at 0,0)
    if mineral == 'T' and new_x == 0 and new_y == 0:
        print("You return to town.")
        player['in_mine'] = False
        player['day'] += 1
        player['turns'] = TURNS_PER_DAY
        sell_ores(player)
        return True

    # if stepped on mineral tile
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

# -------------------------
# Portal & shop actions
# -------------------------
def use_portal(player):
    player['portal_x'] = player['x']
    player['portal_y'] = player['y']
    player['in_mine'] = False
    player['day'] += 1
    player['turns'] = TURNS_PER_DAY
    sell_ores(player)
    print("You place your portal stone here and zap back to town.")

def buy_backpack_upgrade(player):
    cost = player['max_load'] * 2
    if player['GP'] >= cost:
        player['GP'] -= cost
        player['max_load'] += 2
        print(f"Congratulations! You can now carry {player['max_load']} items!")
    else:
        print("You don't have enough GP!")

def buy_pickaxe_upgrade(player):
    cost = pickaxe_upgrade_cost(player)
    if player['GP'] >= cost:
        # limit pickaxe level to 3 (gold) to keep original logic (1..3)
        if player['pickaxe'] >= 3:
            print("You already have the best pickaxe!")
            return
        player['GP'] -= cost
        player['pickaxe'] += 1
        print(f"You upgraded your pickaxe to level {player['pickaxe']}!")
    else:
        print("You don't have enough GP to upgrade your pickaxe.")

# -------------------------
# Main game loop
# -------------------------
game_state = "main"
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print(f"How quickly can you get the {WIN_GP} GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

while True:
    if game_state == "main":
        show_main_menu()
        choice = input("Your choice? ").upper()

        if choice == 'N':
            player_name = input("Greetings, miner! What is your name? ")
            player['name'] = player_name
            print(f"Pleased to meet you, {player_name}. Welcome to Sundrop Town!")
            if initialize_game(game_map, fog, player):
                game_state = "town"
            else:
                print("Failed to initialize game. Exiting.")
                break

        elif choice == 'L':
            if load_game(game_map, fog, player):
                game_state = "town"

        elif choice == 'T':
            show_top_score()

        elif choice == 'Q':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

    elif game_state == "town":
        show_town_menu()
        choice = input("Your choice? ").upper()

        if choice == 'B':
            shop_state = True
            while shop_state:
                show_shop_menu()
                shop_choice = input("Your choice? ").upper()

                if shop_choice == 'B':
                    buy_backpack_upgrade(player)
                elif shop_choice == 'P':
                    buy_pickaxe_upgrade(player)
                elif shop_choice == 'L':
                    shop_state = False
                else:
                    print("Invalid choice. Please try again.")

        elif choice == 'H':
            warehouse_menu(player)

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
        action = input("Action? ").upper()

        if action in ['W', 'A', 'S', 'D']:
            dx, dy = 0, 0
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
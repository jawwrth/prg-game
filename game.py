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

    f.close()
    print("Game saved successfully.")
    return True
 
# This function loads the game
def load_game(game_map, fog, player):
    # load map
    # load fog
    # load player
    return

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
#    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

def show_town_menu():
    print()
    # TODO: Show Day
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")
            

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
    
    

import numpy as np
import requests
from IPython.display import display
import pandas as pd

def split_list(lst, chunk_size):
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

pokeID = 1
dexNum_list = []
name_list = []
type_one_list = []
type_two_list = []
ability_one_list = []
ability_two_list = []
ability_three_list = []
hp_list = []
attack_list = []
defense_list = []
spattack_list = []
spdefense_list = []
speed_list = []

all_movelist_list = []
print("Running PokeDex Analyzer...")
while pokeID <= 1017: #1017 is the latest pokemon as of now in the restAPI (Ogerpon)
    url = f"https://pokeapi.co/api/v2/pokemon/{pokeID}"
    url_text = f"https://pokeapi.co/api/v2/pokemon-species/{pokeID}"
    response = requests.get(url)
    response_text = requests.get(url_text)

    if response.status_code == 200:
        pokeData = response.json()
    # Creating a list for each attribute
    name = [name['name'] for name in pokeData['forms']]
    removed_name = name.pop(0)
    name_list.append(removed_name)
    abilities = [ability['ability']['name'] for ability in pokeData['abilities']]
    if len(abilities) == 1:
        ability_one_list.append(abilities[0])
        ability_two_list.append("---")
        ability_three_list.append("---")
    elif len(abilities) == 2:
        ability_one_list.append(abilities[0])
        ability_two_list.append(abilities[1])
        ability_three_list.append("---")
    elif len(abilities) == 3:
        ability_one_list.append(abilities[0])
        ability_two_list.append(abilities[1])
        ability_three_list.append(abilities[2])
    types = [poke_type['type']['name'] for poke_type in pokeData['types']]
    if len(types) == 1:
        type_one_list.append(types[0])
        type_two_list.append("---")
    elif len(types) == 2:
        type_one_list.append(types[0])
        type_two_list.append(types[1])

    # Stats
    stats_names = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
    stats = []
    if response.status_code == 200:
        for stat in pokeData['stats']:
            stats.append(stat["base_stat"])
        hp_list.append(stats[0])
        attack_list.append(stats[1])
        defense_list.append(stats[2])
        spattack_list.append(stats[3])
        spdefense_list.append(stats[4])
        speed_list.append(stats[5])

    ###Flavor Text
    text = []
    if response.status_code == 200:
        pokeText = response_text.json()
        for entry in pokeText['flavor_text_entries']:
            if entry["version"]["name"] == "x" and entry["language"]["name"] == "en":
                text = entry["flavor_text"]
                #print(text)

    # Moves
    movelist = []
    move_learn_level = []
    split_list(abilities, 1)
    #print("\nMoveset: ")  # Movesets will be from the latest generation said Pokemon appears in
    if "scarlet-violet" in str(pokeData):
        for move in pokeData['moves']:
            for version_group_detail in move["version_group_details"]:
                if (version_group_detail["version_group"]["name"] == "scarlet-violet" and
                        version_group_detail["move_learn_method"]["name"] == "level-up"):
                    movelist.append(move["move"]["name"])
                    level_learned_at = version_group_detail["level_learned_at"]
                    move_learn_level.append(level_learned_at)

    if "sword-shield" in str(pokeData) and "scarlet-violet" not in str(pokeData):
        for move in pokeData['moves']:
            for version_group_detail in move["version_group_details"]:
                if (version_group_detail["version_group"]["name"] == "sword-shield" and
                        version_group_detail["move_learn_method"]["name"] == "level-up"):
                    movelist.append(move["move"]["name"])
                    level_learned_at = version_group_detail["level_learned_at"]
                    move_learn_level.append(level_learned_at)

    if "ultra-sun-ultra-moon" in str(pokeData) and ("scarlet-violet" and "sword-shield") not in str(pokeData):
        for move in pokeData['moves']:
            for version_group_detail in move["version_group_details"]:
                if (version_group_detail["version_group"]["name"] == "ultra-sun-ultra-moon" and
                        version_group_detail["move_learn_method"]["name"] == "level-up"):
                    movelist.append(move["move"]["name"])
                    level_learned_at = version_group_detail["level_learned_at"]
                    move_learn_level.append(level_learned_at)

    ###print_sorted_list_vertically(move_learn_level, movelist)
    combined_list = []
    # Combine the two given lists into one
    for i in range(len(move_learn_level)):
        combined_list.append(move_learn_level[i])
        combined_list.append(movelist[i])

    # Sort the levels in the result list by making each level-move pair into a list, then sorting the lists within the list
    list_nest = []
    for i in range(0, len(combined_list), 2):
        list_nest.append([str(combined_list[i]), str(combined_list[i + 1])])

    list_nest.sort(key=lambda x: int(x[0]))

    '''for sublist in list_nest:
        print(" ".join(sublist))'''
    all_movelist_list.append(list_nest)

    #Use dynamic variable adjusting to adjust
    move_lists_dict = {}
    max_move_real = 35

    for i in range(1, max_move_real + 1):
        current_list_key = f"move_{i}_list"
        move_lists_dict[current_list_key] = []

    for pokemon_moveset_real in all_movelist_list:
        for i, moves in enumerate(pokemon_moveset_real):
            current_list_key = f"move_{i + 1}_list"
            move_lists_dict.setdefault(current_list_key, []).append(moves)

        current_length = len(pokemon_moveset_real)
        if current_length < max_move_real:
            for i in range(current_length, max_move_real):
                current_list_key = f"move_{i + 1}_list"
                move_lists_dict.setdefault(current_list_key, []).append("")

    # Retrieving move_1_list and storing it in a separate variable
    move_1_saved_list = move_lists_dict["move_1_list"]
    move_2_saved_list = move_lists_dict["move_2_list"]
    move_3_saved_list = move_lists_dict["move_3_list"]
    move_4_saved_list = move_lists_dict["move_4_list"]
    move_5_saved_list = move_lists_dict["move_5_list"]
    move_6_saved_list = move_lists_dict["move_6_list"]
    move_7_saved_list = move_lists_dict["move_7_list"]
    move_8_saved_list = move_lists_dict["move_8_list"]
    move_9_saved_list = move_lists_dict["move_9_list"]
    move_10_saved_list = move_lists_dict["move_10_list"]
    move_11_saved_list = move_lists_dict["move_11_list"]
    move_12_saved_list = move_lists_dict["move_12_list"]
    move_13_saved_list = move_lists_dict["move_13_list"]
    move_14_saved_list = move_lists_dict["move_14_list"]
    move_15_saved_list = move_lists_dict["move_15_list"]
    move_16_saved_list = move_lists_dict["move_16_list"]
    move_17_saved_list = move_lists_dict["move_17_list"]
    move_18_saved_list = move_lists_dict["move_18_list"]
    move_19_saved_list = move_lists_dict["move_19_list"]
    move_20_saved_list = move_lists_dict["move_20_list"]
    move_21_saved_list = move_lists_dict["move_21_list"]
    move_22_saved_list = move_lists_dict["move_22_list"]
    move_23_saved_list = move_lists_dict["move_23_list"]
    move_24_saved_list = move_lists_dict["move_24_list"]
    move_25_saved_list = move_lists_dict["move_25_list"]
    move_26_saved_list = move_lists_dict["move_26_list"]
    move_27_saved_list = move_lists_dict["move_27_list"]
    move_28_saved_list = move_lists_dict["move_28_list"]
    move_29_saved_list = move_lists_dict["move_29_list"]
    move_30_saved_list = move_lists_dict["move_30_list"]
    move_31_saved_list = move_lists_dict["move_31_list"]
    move_32_saved_list = move_lists_dict["move_32_list"]
    move_33_saved_list = move_lists_dict["move_33_list"]
    move_34_saved_list = move_lists_dict["move_34_list"]
    move_35_saved_list = move_lists_dict["move_35_list"]

    dexNum_list.append(pokeID)
    pokeID += 1
# Create Dataframe
# Add values to pandas Dataframe and convert to CSV
df = pd.DataFrame({'DexNum': dexNum_list,
                   'Name': name_list,
                   'Type1': type_one_list,
                   'Type2': type_two_list,
                   'Ability1': ability_one_list,
                   'Ability2': ability_two_list,
                   'Ability3': ability_three_list,
                   'HP': hp_list,
                   'Attack': attack_list,
                   'Defense': defense_list,
                   'Sp.Attack': spattack_list,
                   'Sp.Defense': spdefense_list,
                   'Speed': speed_list,
                    "move1": move_1_saved_list,
                    "move2": move_2_saved_list,
                    "move3": move_3_saved_list,
                    "move4": move_4_saved_list,
                    "move5": move_5_saved_list,
                    "move6": move_6_saved_list,
                    "move7": move_7_saved_list,
                    "move8": move_8_saved_list,
                    "move9": move_9_saved_list,
                    "move10": move_10_saved_list,
                    "move11": move_11_saved_list,
                    "move12": move_12_saved_list,
                    "move13": move_13_saved_list,
                    "move14": move_14_saved_list,
                    "move15": move_15_saved_list,
                    "move16": move_16_saved_list,
                    "move17": move_17_saved_list,
                    "move18": move_18_saved_list,
                    "move19": move_19_saved_list,
                    "move20": move_20_saved_list,
                    "move21": move_21_saved_list,
                    "move22": move_22_saved_list,
                    "move23": move_23_saved_list,
                    "move24": move_24_saved_list,
                    "move25": move_25_saved_list,
                    "move26": move_26_saved_list,
                    "move27": move_27_saved_list,
                    "move28": move_28_saved_list,
                    "move29": move_29_saved_list,
                    "move30": move_30_saved_list,
                    "move31": move_31_saved_list,
                    "move32": move_32_saved_list,
                    "move33": move_33_saved_list,
                    "move34": move_34_saved_list,
                    "move35": move_35_saved_list
                   })


#Step 1: Check if the given move is the last in the list
#Step 2: Append the move based on its position to its respective position list



pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

display(df)

df.to_csv('df.csv', index=False)

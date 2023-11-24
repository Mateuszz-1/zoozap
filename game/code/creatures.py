from moves import moves_dict

"""
This file contains all the creatures in the game. Each creature is a dictionary with the following keys:
name: The name of the creature
stats: A dictionary of the creature's stats
    HP: The creature's health points
    ATK: The creature's attack
    DEF: The creature's defense
    SP_ATK: The creature's special attack
    SP_DEF: The creature's special defense
    SPD: The creature's speed
type: A list of the creature's types
weakness: A list of the creature's weaknesses
resistance: A list of the creature's resistances
moves: A list of the creature's moves
"""
creatures = [
    {
        "name": "LEGENDARY1",
        "stats": {"hp": 90, "atk": 130, "def": 130, "sp_atk": 95, "sp_def": 85, "spd": 100},
        "type": ["fire", "earth"],
        "weakness": ["water", "air"],
        "resistance": ["grass", "electric"],
        "moves": [moves_dict["Lava Plume"], moves_dict["Rock Throw"], moves_dict["Inferno Trap"]]
    },
    {
        "name": "LEGENDARY2",
        "stats": {"hp": 85, "atk": 95, "def": 90, "sp_atk": 130, "sp_def": 100, "spd": 100},
        "type": ["air", "electric"],
        "weakness": ["earth", "fire"],
        "resistance": ["water", "grass"],
        "moves": [moves_dict["Storm Blast"], moves_dict["Electric Shock"], moves_dict["Gusty Wind"]]
    },
    {
        "name": "MYTHICAL1",
        "stats": {"hp": 80, "atk": 110, "def": 80, "sp_atk": 115, "sp_def": 95, "spd": 120},
        "type": ["water", "electric"],
        "weakness": ["grass", "earth"],
        "resistance": ["fire", "air"],
        "moves": [moves_dict["Tsunami Wave"], moves_dict["Electric Shock"], moves_dict["Misty Veil"]]
    },
    {
        "name": "MYTHICAL2",
        "stats": {"hp": 95, "atk": 100, "def": 95, "sp_atk": 100, "sp_def": 110, "spd": 100},
        "type": ["grass"],
        "weakness": ["fire", "air"],
        "resistance": ["water", "electric"],
        "moves": [moves_dict["Nature's Wrath"], moves_dict["Grass Knot"], moves_dict["Spore Cloud"]]
    },
    {
        "name": "pLEGENDARY1",
        "stats": {"hp": 95, "atk": 120, "def": 90, "sp_atk": 90, "sp_def": 85, "spd": 120},
        "type": ["air", "grass"],
        "weakness": ["fire", "earth"],
        "resistance": ["water", "electric"],
        "moves": [moves_dict["Gale Force"], moves_dict["Grass Knot"], moves_dict["Fairy Dust"]]
    },
    {
        "name": "pLEGENDARY2",
        "stats": {"hp": 100, "atk": 120, "def": 100, "sp_atk": 80, "sp_def": 100, "spd": 100},
        "type": ["electric", "earth"],
        "weakness": ["fire", "air"],
        "resistance": ["water", "grass"],
        "moves": [moves_dict["Thunder Roar"], moves_dict["Quake Tremors"], moves_dict["Static Charge"]]
    },
    {
        "name": "pLEGENDARY3",
        "stats": {"hp": 90, "atk": 95, "def": 85, "sp_atk": 120, "sp_def": 110, "spd": 100},
        "type": ["fire", "air"],
        "weakness": ["water", "electric"],
        "resistance": ["grass", "earth"],
        "moves": [moves_dict["Flaming Vortex"], moves_dict["Air Cutter"], moves_dict["Mirror Shine"]]
    },
    {
        "name": "pLEGENDARY4",
        "stats": {"hp": 85, "atk": 85, "def": 100, "sp_atk": 120, "sp_def": 110, "spd": 100},
        "type": ["water", "air"],
        "weakness": ["electric", "fire"],
        "resistance": ["earth", "grass"],
        "moves": [moves_dict["Aqua Tornado"], moves_dict["Air Cutter"], moves_dict["Frost Chill"]]
    },
    {
        "name": "REG1",
        "stats": {"hp": 80, "atk": 100, "def": 80, "sp_atk": 100, "sp_def": 80, "spd": 100},
        "type": ["fire"],
        "weakness": ["water", "earth"],
        "resistance": ["grass", "electric"],
        "moves": [moves_dict["Fireball"], moves_dict["Flame Burst"], moves_dict["Inferno Trap"]]
    },
    {
        "name": "REG2",
        "stats": {"hp": 100, "atk": 110, "def": 100, "sp_atk": 70, "sp_def": 80, "spd": 80},
        "type": ["earth"],
        "weakness": ["air", "grass"],
        "resistance": ["electric", "fire"],
        "moves": [moves_dict["Rock Throw"], moves_dict["Earthquake"], moves_dict["Quake Tremors"]]
    },
    {
        "name": "REG3",
        "stats": {"hp": 85, "atk": 70, "def": 95, "sp_atk": 100, "sp_def": 95, "spd": 95},
        "type": ["water"],
        "weakness": ["electric", "grass"],
        "resistance": ["fire", "earth"],
        "moves": [moves_dict["Water Pulse"], moves_dict["Tsunami Wave"], moves_dict["Misty Veil"]]
    },
    {
        "name": "REG4",
        "stats": {"hp": 100, "atk": 90, "def": 115, "sp_atk": 75, "sp_def": 90, "spd": 70},
        "type": ["water", "earth"],
        "weakness": ["electric", "grass"],
        "resistance": ["fire", "air"],
        "moves": [moves_dict["Water Pulse"], moves_dict["Rock Throw"], moves_dict["Misty Veil"]]
    },
    {
        "name": "REG5",
        "stats": {"hp": 95, "atk": 105, "def": 95, "sp_atk": 75, "sp_def": 85, "spd": 85},
        "type": ["grass", "earth"],
        "weakness": ["air", "fire"],
        "resistance": ["water", "electric"],
        "moves": [moves_dict["Grass Knot"], moves_dict["Earthquake"], moves_dict["Spore Cloud"]]
    },
    {
        "name": "REG6",
        "stats": {"hp": 80, "atk": 80, "def": 90, "sp_atk": 110, "sp_def": 90, "spd": 90},
        "type": ["water", "grass"],
        "weakness": ["electric", "air"],
        "resistance": ["fire", "earth"],
        "moves": [moves_dict["Water Pulse"], moves_dict["Grass Knot"], moves_dict["Misty Veil"]]
    },
    {
        "name": "REG7",
        "stats": {"hp": 85, "atk": 105, "def": 80, "sp_atk": 95, "sp_def": 85, "spd": 90},
        "type": ["fire", "grass"],
        "weakness": ["water", "air"],
        "resistance": ["earth", "electric"],
        "moves": [moves_dict["Fireball"], moves_dict["Grass Knot"], moves_dict["Inferno Trap"]]
    },
    {
        "name": "REG8",
        "stats": {"hp": 90, "atk": 100, "def": 100, "sp_atk": 80, "sp_def": 85, "spd": 85},
        "type": ["earth", "air"],
        "weakness": ["grass", "fire"],
        "resistance": ["water", "electric"],
        "moves": [moves_dict["Rock Throw"], moves_dict["Air Cutter"], moves_dict["Quake Tremors"]]
    },
    {
        "name": "REG9",
        "stats": {"hp": 80, "atk": 75, "def": 85, "sp_atk": 105, "sp_def": 100, "spd": 95},
        "type": ["grass", "electric"],
        "weakness": ["fire", "earth"],
        "resistance": ["water", "air"],
        "moves": [moves_dict["Grass Knot"], moves_dict["Electric Shock"], moves_dict["Spore Cloud"]]
    },
    {
        "name": "REG10",
        "stats": {"hp": 90, "atk": 90, "def": 90, "sp_atk": 90, "sp_def": 90, "spd": 90},
        "type": ["water", "fire"],
        "weakness": ["grass", "electric"],
        "resistance": ["earth", "air"],
        "moves": [moves_dict["Water Pulse"], moves_dict["Fireball"], moves_dict["Misty Veil"]]
    },
    {
        "name": "REG11",
        "stats": {"hp": 95, "atk": 100, "def": 90, "sp_atk": 85, "sp_def": 85, "spd": 85},
        "type": ["earth", "fire"],
        "weakness": ["water", "grass"],
        "resistance": ["air", "electric"],
        "moves": [moves_dict["Rock Throw"], moves_dict["Flame Burst"], moves_dict["Quake Tremors"]]
    },
    {
        "name": "REG12",
        "stats": {"hp": 85, "atk": 85, "def": 85, "sp_atk": 95, "sp_def": 95, "spd": 95},
        "type": ["air", "electric"],
        "weakness": ["earth", "fire"],
        "resistance": ["water", "grass"],
        "moves": [moves_dict["Air Cutter"], moves_dict["Electric Shock"], moves_dict["Gusty Wind"]]
    },
    {
        "name": "REG13",
        "stats": {"hp": 80, "atk": 85, "def": 80, "sp_atk": 105, "sp_def": 100, "spd": 90},
        "type": ["electric"],
        "weakness": ["earth", "fire"],
        "resistance": ["water", "air"],
        "moves": [moves_dict["Electric Shock"], moves_dict["Thunder Punch"], moves_dict["Static Charge"]]
    },
    {
        "name": "REG14",
        "stats": {"hp": 90, "atk": 90, "def": 95, "sp_atk": 85, "sp_def": 90, "spd": 90},
        "type": ["grass", "water"],
        "weakness": ["fire", "electric"],
        "resistance": ["earth", "air"],
        "moves": [moves_dict["Grass Knot"], moves_dict["Water Pulse"], moves_dict["Spore Cloud"]]
    },
    {
        "name": "REG15",
        "stats": {"hp": 85, "atk": 90, "def": 85, "sp_atk": 95, "sp_def": 90, "spd": 95},
        "type": ["air"],
        "weakness": ["electric", "fire"],
        "resistance": ["earth", "grass"],
        "moves": [moves_dict["Air Cutter"], moves_dict["Gusty Wind"], moves_dict["Mirror Shine"]]
    },
    {
        "name": "REG16",
        "stats": {"hp": 80, "atk": 100, "def": 85, "sp_atk": 95, "sp_def": 90, "spd": 90},
        "type": ["fire", "electric"],
        "weakness": ["water", "earth"],
        "resistance": ["air", "grass"],
        "moves": [moves_dict["Fireball"], moves_dict["Electric Shock"], moves_dict["Static Charge"]]
    }
]

# Create a dictionary of all the creatures
creatures_dict = {creature["name"]: creature for creature in creatures}

"""
This file contains all the moves in the game. Each move is a dictionary with the following keys:
name: The name of the move
type: The type of the move
category: The category of the move (special, physical, or status)
power: The power of the move (if applicable)
accuracy: The accuracy of the move (if applicable)
effect: The effect of the move (if applicable)
"""
all_moves = [
    # Damaging Moves
    {"name": "Fireball", "type": "fire", "category": "special", "power": 80, "accuracy": 100},
    {"name": "Rock Throw", "type": "earth", "category": "physical", "power": 75, "accuracy": 95},
    {"name": "Water Pulse", "type": "water", "category": "special", "power": 80, "accuracy": 100},
    {"name": "Air Cutter", "type": "air", "category": "special", "power": 75, "accuracy": 95},
    {"name": "Electric Shock", "type": "electric", "category": "physical", "power": 80, "accuracy": 100},
    {"name": "Grass Knot", "type": "grass", "category": "special", "power": 70, "accuracy": 100},
    {"name": "Earthquake", "type": "earth", "category": "physical", "power": 100, "accuracy": 100},
    {"name": "Thunder Punch", "type": "electric", "category": "physical", "power": 75, "accuracy": 100},
    {"name": "Flame Burst", "type": "fire", "category": "special", "power": 70, "accuracy": 100},

    # Unique Moves for Legendary/Mythical/Pseudo-Legendary Creatures
    {"name": "Lava Plume", "type": "fire", "category": "special", "power": 110, "accuracy": 85},
    {"name": "Storm Blast", "type": "air", "category": "special", "power": 110, "accuracy": 85},
    {"name": "Tsunami Wave", "type": "water", "category": "special", "power": 110, "accuracy": 85},
    {"name": "Nature's Wrath", "type": "grass", "category": "special", "power": 110, "accuracy": 85},
    {"name": "Gale Force", "type": "air", "category": "physical", "power": 110, "accuracy": 85},
    {"name": "Thunder Roar", "type": "electric", "category": "special", "power": 110, "accuracy": 85},
    {"name": "Flaming Vortex", "type": "fire", "category": "special", "power": 110, "accuracy": 85},
    {"name": "Aqua Tornado", "type": "water", "category": "special", "power": 110, "accuracy": 85},

    # Status Moves
    {"name": "Inferno Trap", "type": "fire", "category": "status", "effect": "burn", "probability": 0.5},
    {"name": "Quake Tremors", "type": "earth", "category": "status", "effect": "lower_spd", "probability": 1},
    {"name": "Misty Veil", "type": "water", "category": "status", "effect": "raise_sp_def", "probability": 1},
    {"name": "Gusty Wind", "type": "air", "category": "status", "effect": "confuse", "probability": 0.3},
    {"name": "Static Charge", "type": "electric", "category": "status", "effect": "paralyse", "probability": 0.3},
    {"name": "Spore Cloud", "type": "grass", "category": "status", "effect": "sleep", "probability": 0.75},
    {"name": "Mirror Shine", "type": "psychic", "category": "status", "effect": "reflect_effect", "probability": 1},
    {"name": "Shadow Hold", "type": "dark", "category": "status", "effect": "prevent_escape", "probability": 1},
    {"name": "Frost Chill", "type": "ice", "category": "status", "effect": "freeze", "probability": 0.2},
    {"name": "Toxic Spikes", "type": "poison", "category": "status", "effect": "poison_terrain", "probability": 1},
    {"name": "Steel Wall", "type": "steel", "category": "status", "effect": "raise_def", "probability": 1},
    {"name": "Fairy Dust", "type": "fairy", "category": "status", "effect": "heal", "probability": 1},
    {"name": "Stun Spore", "type": "grass", "category": "status", "effect": "paralyse", "probability": 0.75},
]

# Create a dictionary of all the moves
moves_dict = {move["name"]: move for move in all_moves}



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
    {"name": "Inferno Trap", "type": "fire", "category": "status", "effect": "Burn"},
    {"name": "Quake Tremors", "type": "earth", "category": "status", "effect": "Lower Speed"},
    {"name": "Misty Veil", "type": "water", "category": "status", "effect": "Raise Special Defense"},
    {"name": "Gusty Wind", "type": "air", "category": "status", "effect": "Confuse"},
    {"name": "Static Charge", "type": "electric", "category": "status", "effect": "Paralyze"},
    {"name": "Spore Cloud", "type": "grass", "category": "status", "effect": "Sleep"},
    {"name": "Mirror Shine", "type": "psychic", "category": "status", "effect": "Reflect Damage"},
    {"name": "Shadow Hold", "type": "dark", "category": "status", "effect": "Prevent Escape"},
    {"name": "Frost Chill", "type": "ice", "category": "status", "effect": "Freeze"},
    {"name": "Toxic Spikes", "type": "poison", "category": "status", "effect": "Poison"},
    {"name": "Steel Wall", "type": "steel", "category": "status", "effect": "Raise Defense"},
    {"name": "Fairy Dust", "type": "fairy", "category": "status", "effect": "Heal"},
    {"name": "Stun Spore", "type": "grass", "category": "status", "effect": "Paralyze"}
]

# Create a dictionary of all the moves
moves_dict = {move["name"]: move for move in all_moves}


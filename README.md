# ZooZap

## Overview

Welcome to **ZooZap**, a strategy game that combines the excitement of creature based battles with the strategic depth of a trading card game. In ZooZap, players engage in battles using a deck of creature cards, each boasting unique abilities and stats. The game's objective is to defeat your opponent's creatures, leading your team to victory.

## Gameplay Mechanics

At the start of ZooZap, each player is dealt a hand of 6 creature cards from a pool of 20 unique cards; each one representing a creature. During each turn, players can choose to:

- **Attack:** Use one of their active creature's moves to damage or inflict status effects on the opponent's active creature.
- **Switch:** Swap their active creature with another from their hand, especially useful when facing a type disadvantage.

The game continues in turns, with the aim to strategically use your creatures' abilities to defeat all creatures of the opposing team. The player to eliminate all opposing creatures wins the game.

## Unique Features

While ZooZap currently focuses on core gameplay mechanics, its development serves a greater purpose. The game is being used as a platform to develop and analyze various AI approaches. The goal is to determine the most effective AI strategy for the game, assess the fairness of the game mechanics, and explore potential applications of AI beyond the game context.

## Technology Stack

ZooZap is currently implemented in Python, featuring command-line interface (CLI) gameplay. The game's logic is built purely in Python, making it accessible and easy to run. The future development plans include integrating a Graphical User Interface (GUI) and finalizing the technology stack for AI development.

## Status Conditions

ZooZap incorporates various status conditions that can affect the outcome of battles. These conditions include:
- **Burnt:** Attack stat is halved and 6.25% max health dealt as damage at the end of each turn. Burn lasts 1-3 turns.
- **Paralysed:** 25% chance to not be able to move each turn & speed stat is lowered by 75%. Paralysis has a 20% chance to end each turn.
- **Sleeping:** A sleeping creature cannot move, sleep lasts 1-3 turns.
- **Trapped:** The creature cannot be swapped out of active combat till it faints.
- **Frozen:** A frozen creature cannot move. Freeze has a 30% chance to end each turn.
- **Confused:** A confused creature has a 50% chance to hurt itself instead of executing a move. Confusion lasts 1-3 turns.
Understanding and utilizing these status conditions effectively can be key to mastering the game.

## License

ZooZap is developed as part of a final year project at a university. The project is currently closed-source to maintain academic integrity and prevent plagiarism.

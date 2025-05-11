!!! To run this game, make sure you have Python 3 and MiniSAT installed.  
!!!The game works both from a terminal or directly in an IDE (like PyCharm or VS Code), as long as `minisat` is accessible from the system PATH.
(https://minisat.readthedocs.io/en/latest/index.html)

# The Cat Conspiracy — A Logic-Based SAT Game

This project is a small interactive Python game that mixes storytelling with logic. In it, seven cats form a secret network of friendships and rivalries. Your task is to find out whether their conspiracy can stand without contradictions — or if it falls apart under the weight of logic.

## About the Project

The Cat Conspiracy is a playful application of SAT solving. Each relationship between two cats is translated into logical rules and encoded in CNF (Conjunctive Normal Form). These rules are then passed to the MiniSAT solver, which checks if the set of relationships is logically consistent.

This project was created as a creative way to apply SAT solving to something more interactive and fun than traditional examples.

## How It Works

- You are introduced to a short story about seven cats: Mimi, Zuzu, Leo, Mia, Tom, Cleo, and Felix.
- You can either:
  - Generate a random network of friendships and rivalries.
  - Manually choose the relationships between cats.
- The program translates these relationships into a CNF formula.
- The formula is passed to MiniSAT to check whether the relationships make sense from a logical point of view.
- If the result is satisfiable, the game explains who the loyal cats are and who are acting against the plan.

## Running the Game

### Requirements

- Python 3
- MiniSAT installed and accessible from the command line (`minisat` should be in your system PATH)

### To start the game:
Run it in your IDE.

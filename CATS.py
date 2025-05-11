import subprocess
import random
import os

CATS = ["Mimi", "Zuzu", "Leo", "Mia", "Tom", "Cleo", "Felix"]
CAT_IDS = {cat: i + 1 for i, cat in enumerate(CATS)}

def show_intro():
    print("\n🐾 Welcome to the Kingdom of Cats...")
    print("Before exploring this world, press [1] to read the story.")
    print("Or press [2] to skip directly to the conspiracy logic.\n")

def show_story():
    print("\n📖 THE CAT CONSPIRACY \n")
    print("Far beyond the lands known to men,in the dark streets of Timisoara, lies the Kingdom of Cats.")
    print("A place of purring peace by day and silent plots by night.")
    print("In the shadows of alleys and under rooftops, seven cats whisper and plan to take over our city.")
    print("They speak not of fish or naps, but of power, loyalty... and betrayal.")
    print("Mimi, the elegant; Zuzu, the suspicious; Leo, the ambitious;")
    print("Mia, the gentle; Tom, the cunning; Cleo, the silent one; and Felix, the wild cat.")
    print("Some forge alliances. Others spread distrust. Some lie.")
    print("But only if their logic holds — only if no contradiction emerges — can their secret alliance rise.")
    print("Otherwise... the whole plan collapses into meows and claw marks.\n")

def main_menu():
    print("=== MAIN MENU ===")
    print("1. Generate a random set of alliances")
    print("2. Customize alliances (Yes/No per pair)")
    print("0. Exit\n")
def make_clause(cat1, cat2, relation):
    a = CAT_IDS[cat1]
    b = CAT_IDS[cat2]
    if relation == "friend":
        return [[a, -b], [-a, b]], (cat1, cat2, "friend")  # A ↔ B
    elif relation == "enemy":
        return [[-a, -b]], (cat1, cat2, "enemy")  # NOT (A ∧ B)
    else:
        return [], None
def generate_random_clauses():
    print("\n Generating random alliances and rivalries...")
    clauses = []
    relations = []
    pairs = [(a, b) for i, a in enumerate(CATS) for b in CATS[i + 1:]]

    for cat1, cat2 in pairs:
        relation = random.choice(["friend", "enemy"])
        print(f"{cat1} and {cat2} are {'friends' if relation == 'friend' else 'enemies'}.")
        new_clauses, rel = make_clause(cat1, cat2, relation)
        clauses.extend(new_clauses)
        if rel:
            relations.append(rel)
    activation_clause = [i for i in range(1, len(CATS) + 1)]
    clauses.append(activation_clause)
    print("📌 Forcing: at least one cat must be in the alliance.\n")

    return clauses, relations
def customize_clauses():
    print("\n🛠️ Build your own conspiracy:")
    clauses = []
    relations = []
    for i in range(len(CATS)):
        for j in range(i + 1, len(CATS)):
            cat1, cat2 = CATS[i], CATS[j]
            while True:
                ans = input(f"Are {cat1} and {cat2} allies? (Yes/No/Skip): ").strip().lower()
                if ans == "yes":
                    new_clauses, rel = make_clause(cat1, cat2, "friend")
                    clauses.extend(new_clauses)
                    if rel:
                        relations.append(rel)
                    break
                elif ans == "no":
                    new_clauses, rel = make_clause(cat1, cat2, "enemy")
                    clauses.extend(new_clauses)
                    if rel:
                        relations.append(rel)
                    break
                elif ans == "skip":
                    break
                else:
                    print("Please enter Yes, No or Skip.")
    activation_clause = [i for i in range(1, len(CATS) + 1)]
    clauses.append(activation_clause)
    print("📌 Forcing: at least one cat must be in the alliance.\n")
    return clauses, relations
def write_cnf(clauses, filename="cat_conspiracy.cnf"):
    with open(filename, "w") as f:
        f.write(f"p cnf {len(CATS)} {len(clauses)}\n")
        for clause in clauses:
            f.write(" ".join(str(lit) for lit in clause) + " 0\n")
    print(f"\n📝 CNF written to {filename}:")
    with open(filename, "r") as f:
        print(f.read())

    return filename
def run_minisat(cnf_file):
    output_file = "result.out"
    try:
        result = subprocess.run(
            ["minisat", cnf_file, output_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        with open(output_file, "r") as f:
            lines = f.read().strip().splitlines()

        print("🔎 MiniSAT raw output:")
        print("\n".join(lines))

        if not lines:
            print(" No output from MiniSAT.")
            return None, None

        if lines[0] == "UNSAT":
            print("\n❌ The conspiracy is logically broken. UNSATISFIABLE.")
            return "UNSAT", {}

        elif lines[0] == "SAT":
            print("\n✅ The conspiracy holds! SATISFIABLE.")
            if len(lines) < 2:
                print(" SAT, but no variable assignments returned.")
                return "SAT", {}

            assignments = {}
            for val in lines[1].split():
                if val == "0":
                    continue
                var = int(val)
                cat = [c for c, idx in CAT_IDS.items() if idx == abs(var)][0]
                assignments[cat] = var > 0
            return "SAT", assignments

        else:
            print(" Unexpected MiniSAT output.")
            return None, None

    except FileNotFoundError:
        print(" MiniSAT not found. Please install it and ensure it's in your PATH.")
        return None, None


def analyze_and_print_verdict(assignments, relations):
    print("\n🔍 ANALYSIS REPORT — Who's loyal, who's fake?\n")

    for cat in CATS:
        status = assignments.get(cat, False)
        if not status:
            print(f" {cat} chose not to join the conspiracy.")
            continue
        broken_relations = 0
        for rel in relations:
            cat1, cat2, kind = rel

            if cat not in (cat1, cat2):
                continue
            other_cat = cat2 if cat == cat1 else cat1
            other_status = assignments.get(other_cat, False)

            if kind == "friend" and other_status != status:
                broken_relations += 1
            elif kind == "enemy" and other_status == status:
                broken_relations += 1

        if broken_relations == 0:
            print(f"😺 {cat} is a loyal ally. Their logic holds strong.")
        else:
            print(f"😼 {cat} is an IMPOSTOR! They betrayed {broken_relations} relationship(s).")
def start_program():
    show_intro()
    while True:
        choice = input("Your choice (1 or 2): ").strip()
        if choice == "1":
            show_story()
            break
        elif choice == "2":
            break
        else:
            print("Invalid choice. Try again.")

    while True:
        main_menu()
        choice = input("Select option: ").strip()
        if choice == "1":
            clauses, relations = generate_random_clauses()
            break
        elif choice == "2":
            clauses, relations = customize_clauses()
            break
        elif choice == "0":
            print("Goodbye!")
            return
        else:
            print("Invalid option.")

    cnf_file = write_cnf(clauses)
    result, assignments = run_minisat(cnf_file)

    if result == "SAT":
        if assignments:
            analyze_and_print_verdict(assignments, relations)
        else:
            print(" No variable assignments to analyze.")
    elif result == "UNSAT":
        print("💥 The conspiracy was doomed from the start.")
    else:
        print("⚠️ Something went wrong. Could not analyze result.")
if __name__ == "__main__":
    start_program()

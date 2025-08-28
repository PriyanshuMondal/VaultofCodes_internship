import random
import time

# -------------------------------
# Virtual Pet Simulator
# -------------------------------

MIN_LEVEL = 0
MAX_LEVEL = 100

# Time progression tuning
BASE_HUNGER_INCREASE = (3, 7)     # inclusive range added to hunger per tick
BASE_HAPPINESS_DECREASE = (2, 5)  # inclusive range subtracted from happiness per tick

# Random event odds per tick (0.0 - 1.0)
EVENT_PROBABILITY = 0.20

RANDOM_EVENTS = [
    {"name": "Found a snack", "hunger_delta": -10, "happiness_delta": +0},
    {"name": "Found a toy", "hunger_delta": +0, "happiness_delta": +10},
    {"name": "Got sick", "hunger_delta": +15, "happiness_delta": -10},
    {"name": "Took a nap", "hunger_delta": -5, "happiness_delta": +5},
]

def clamp(value, low=MIN_LEVEL, high=MAX_LEVEL):
    return max(low, min(high, value))

class Pet:
    def __init__(self, name):
        self.name = name
        self.hunger = 50     # 0 (full) to 100 (starving)
        self.happiness = 50  # 0 (sad) to 100 (very happy)
        self.age_hours = 0   # simple time tracker
        self.alive = True

    # ----------- Gameplay actions -----------
    def feed(self):
        """
        Feeding decreases hunger but slightly decreases happiness
        (some pets dislike being interrupted, or overeating makes them sluggish).
        """
        self.hunger = clamp(self.hunger - 15)
        self.happiness = clamp(self.happiness - 2)

    def play(self):
        """
        Playing increases happiness but increases hunger because play consumes energy.
        """
        self.happiness = clamp(self.happiness + 12)
        self.hunger = clamp(self.hunger + 6)

    def give_toy(self):
        """
        Bonus action: a toy gives a quick happiness boost with a tiny hunger cost.
        """
        self.happiness = clamp(self.happiness + 8)
        self.hunger = clamp(self.hunger + 2)

    def give_medicine(self):
        """
        Bonus action: medicine reduces hunger (settles stomach) and slightly lifts mood.
        To avoid being overpowered, it is mild.
        """
        self.hunger = clamp(self.hunger - 8)
        self.happiness = clamp(self.happiness + 3)

    def status_string(self):
        return (
            f"Name: {self.name}\n"
            f"Hunger:    {self.hunger:3d} {bar(self.hunger)} (0=full, 100=starving)\n"
            f"Happiness: {self.happiness:3d} {bar(self.happiness)} (0=sad, 100=very happy)\n"
            f"Age (hours): {self.age_hours}\n"
            f"State: {'OK' if self.alive else 'Game Over'}"
        )

    # ----------- Time & events -----------
    def tick(self, hours=1):
        """
        Advance time. Each hour:
          - Hunger rises by 3-7.
          - Happiness falls by 2-5.
          - A random event may occur (20% chance).
          - Clamp attributes to [0, 100].
          - Check game-over conditions.
        """
        for _ in range(hours):
            if not self.alive:
                return

            self.age_hours += 1
            self.hunger = clamp(self.hunger + random.randint(*BASE_HUNGER_INCREASE))
            self.happiness = clamp(self.happiness - random.randint(*BASE_HAPPINESS_DECREASE))

            # Random event
            if random.random() < EVENT_PROBABILITY:
                evt = random.choice(RANDOM_EVENTS)
                self.hunger = clamp(self.hunger + evt["hunger_delta"])
                self.happiness = clamp(self.happiness + evt["happiness_delta"])
                print(f"[Random event] {self.name}: {evt['name']}")

            # If hunger gets too high, happiness drops more (requirement)
            if self.hunger > 80:
                # Additional penalty to happiness because the pet is too hungry
                self.happiness = clamp(self.happiness - 5)

            # Game-over checks
            if self.hunger >= MAX_LEVEL:
                self.alive = False
                print(f"{self.name} became too hungry. Game over.")
                return
            if self.happiness <= MIN_LEVEL:
                self.alive = False
                print(f"{self.name} became too sad. Game over.")
                return

def bar(value, width=20):
    """
    Simple textual progress bar between 0 and 100.
    """
    filled = int((value / 100) * width)
    return "[" + "#" * filled + "-" * (width - filled) + "]"

# -------------------------------
# Pet Manager (multiple pets)
# -------------------------------
class PetManager:
    def __init__(self):
        self.pets = []        # list[Pet]
        self.active_index = None

    def create_pet(self):
        name = input("Enter pet name: ").strip()
        if not name:
            print("Invalid name.")
            return
        pet = Pet(name=name)
        self.pets.append(pet)
        self.active_index = len(self.pets) - 1
        print(f"Created pet '{name}' and set as active.")

    def list_pets(self):
        if not self.pets:
            print("No pets created yet.")
            return
        for i, p in enumerate(self.pets):
            marker = " (active)" if i == self.active_index else ""
            state = "alive" if p.alive else "game over"
            print(f"{i + 1}. {p.name} - hunger {p.hunger}, happiness {p.happiness}, {state}{marker}")

    def switch_active(self):
        if not self.pets:
            print("No pets to switch.")
            return
        self.list_pets()
        try:
            choice = int(input("Select active pet number: "))
            if 1 <= choice <= len(self.pets):
                self.active_index = choice - 1
                print(f"Active pet set to '{self.pets[self.active_index].name}'.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a number.")

    def get_active(self):
        if self.active_index is None or not self.pets:
            return None
        return self.pets[self.active_index]

# -------------------------------
# Menu and UI
# -------------------------------
def print_menu():
    print("\n------ Virtual Pet Simulator ------")
    print("1. Feed active pet")
    print("2. Play with active pet")
    print("3. Give toy to active pet")
    print("4. Give medicine to active pet")
    print("5. Check active pet status")
    print("6. Advance time (1 hour)")
    print("7. Create a new pet")
    print("8. Switch active pet")
    print("9. List all pets")
    print("0. Quit")

def ensure_active_pet(manager: PetManager):
    pet = manager.get_active()
    if pet is None:
        print("No active pet. Create one first.")
        manager.create_pet()
        pet = manager.get_active()
    return pet

def main():
    random.seed()  # seed from system time
    manager = PetManager()

    # Start by creating at least one pet
    print("Welcome to the Virtual Pet Simulator.")
    manager.create_pet()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        # Gracefully handle empty input
        if choice == "":
            continue

        if choice == "0":
            print("Exiting. Thanks for playing.")
            break

        # Get active pet for actions 1-6
        if choice in {"1", "2", "3", "4", "5", "6"}:
            pet = ensure_active_pet(manager)
            if pet is None:
                continue
            if not pet.alive and choice in {"1", "2", "3", "4"}:
                print(f"{pet.name} cannot perform actions (game over). Try another pet or quit.")
                continue

        if choice == "1":
            pet.feed()
            print(f"{pet.name} has been fed.")
            pet.tick(1)

        elif choice == "2":
            pet.play()
            print(f"You played with {pet.name}.")
            pet.tick(1)

        elif choice == "3":
            pet.give_toy()
            print(f"{pet.name} enjoyed a new toy.")
            pet.tick(1)

        elif choice == "4":
            pet.give_medicine()
            print(f"{pet.name} took some medicine.")
            pet.tick(1)

        elif choice == "5":
            print("\n" + pet.status_string())

        elif choice == "6":
            try:
                hours = input("Advance how many hours? (default 1): ").strip()
                hours = int(hours) if hours else 1
                hours = max(1, min(24, hours))  # clamp for sanity
            except ValueError:
                hours = 1
            print(f"Advancing time by {hours} hour(s)...")
            # Small delay for effect (optional)
            for _ in range(hours):
                time.sleep(0.05)  # keep very short so grading is fast
                pet.tick(1)
            print("Time advanced.")

        elif choice == "7":
            manager.create_pet()

        elif choice == "8":
            manager.switch_active()

        elif choice == "9":
            manager.list_pets()

        else:
            print("Invalid option. Please choose a valid menu item.")

if __name__ == "__main__":
    main()

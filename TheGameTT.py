import random


# Character Classes
class Character:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class
        self.health = 100
        self.max_health = 100
        self.inventory = Inventory()
        self.set_stats()

    def set_stats(self):
        if self.char_class == "Warrior":
            self.strength = 15
            self.agility = 10
            self.magic = 5
        elif self.char_class == "Mage":
            self.strength = 5
            self.agility = 10
            self.magic = 15
        elif self.char_class == "Rogue":
            self.strength = 10
            self.agility = 15
            self.magic = 5

    def show_stats(self):
        return f"{self.name} the {self.char_class} - Health: {self.health}, Strength: {self.strength}, Agility: {self.agility}, Magic: {self.magic}"

    def use_item(self, item, enemy=None):
        if item == "Health Potion":
            self.health = min(self.health + 30, self.max_health)
            return f"{self.name} used a Health Potion and restored 30 health points!"
        elif item == "Magic Ring" and enemy:
            damage = random.randint(20, 40)
            enemy.health -= damage
            return f"{self.name} used the Magic Ring and dealt {damage} damage to {enemy.name}!"
        elif item == "Antidote":
            self.health = min(self.health + 70, self.max_health)
            return f"{self.name} used the Antidote and restored 70 health points!"
        else:
            return f"{item} has no effect."



# Inventory System
class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        print(f"{item} added to inventory.")

    def show_inventory(self):
        if self.items:
            print("Inventory: " + ", ".join(self.items))
            return True
        else:
            print("Inventory is empty.")
            return False

    def use_item(self, player, item, enemy=None):
        if item in self.items:
            self.items.remove(item)
            return player.use_item(item, enemy)
        else:
            return "Item not found in inventory."


# Combat System
class Enemy:
    def __init__(self, name, health, strength):
        self.name = name
        self.health = health
        self.strength = strength

    def attack(self, player):
        damage = random.randint(5, self.strength)
        player.health -= damage
        return damage


def combat(player, enemy):
    print(f"A wild {enemy.name} appears!")
    while player.health > 0 and enemy.health > 0:
        action = input(f"{player.name}, choose an action: [Attack, Defend, Magic, Inventory] ").lower()

        if action == "attack":
            damage = random.randint(5, player.strength)
            enemy.health -= damage
            print(f"{player.name} dealt {damage} damage to {enemy.name}. Enemy health: {enemy.health}")

        elif action == "defend":
            print(f"{player.name} braces against the attack.")

        elif action == "magic" and player.char_class == "Mage":
            damage = random.randint(5, player.magic + 10)
            enemy.health -= damage
            print(f"{player.name} casts a spell, dealing {damage} damage. Enemy health: {enemy.health}")

        elif action == "inventory":
            if player.inventory.show_inventory():
                item = input("Type the name of the item to use it, or 'back' to exit: ").title()
                if item.lower() != "back":
                    result = player.inventory.use_item(player, item, enemy)
                    print(result)
                    if "Magic Ring" in result:
                        print(f"Enemy health: {enemy.health}")
            else:
                print("Nothing to use in the inventory.")

        else:
            print("Invalid action or action not allowed for your class.")

        if enemy.health > 0:
            damage = enemy.attack(player)
            print(f"{enemy.name} attacks {player.name} for {damage} damage. {player.name}'s health: {player.health}")

    if player.health <= 0:
        print(f"{player.name} has been defeated!")
        return False
    else:
        print(f"{player.name} defeated {enemy.name}!")
        return True


# Story Progression and Decisions
def game_story(player):
    print(f"Welcome to the Kingdom of Pythonia, {player.name}!")
    story_stage = 1
    while story_stage <= 5 and player.health > 0:
        print(f"\n--- Stage {story_stage} ---")
        if story_stage == 1:
            print(f"{player.name} finds a crossroad. To the left, a dark forest. To the right, a mountain trail.")
            choice = input("Choose your path: [forest, mountain] ").lower()
            if choice == "forest":
                enemy = Enemy("Goblin", 30, 10)
                if combat(player, enemy):
                    player.inventory.add_item("Health Potion")
                    print(f"{player.name} found a Health Potion!")
            else:
                enemy = Enemy("Bandit", 40, 12)
                combat(player, enemy)

        elif story_stage == 2:
            print(f"{player.name} arrives at a village under siege.")
            choice = input("Do you [help] the villagers or [ignore] them? ").lower()
            if choice == "help":
                enemy = Enemy("Ogre", 50, 15)
                combat(player, enemy)
            player.inventory.add_item("Magic Ring")

        elif story_stage == 3:
            print(f"{player.name} reaches the castle where the evil overlord awaits.")
            enemy = Enemy("Overlord", 80, 20)
            combat(player, enemy)

        elif story_stage == 4:
            print(f"{player.name} encounters a cursed swamp.")
            choice = input("Do you [enter] the swamp or [avoid] it? ").lower()
            if choice == "enter":
                enemy = Enemy("Poisonous Serpent", 60, 15)
                combat(player, enemy)
                player.inventory.add_item("Antidote")
                print(f"{player.name} found an Antidote!")

        elif story_stage == 5:
            print(f"{player.name} reaches the dragon's lair.")
            choice = input("Do you [fight] the dragon or [negotiate]? ").lower()
            if choice == "fight":
                enemy = Enemy("Dragon", 100, 25)
                combat(player, enemy)
                return "heroic" if player.health > 0 else "tragic"
            elif choice == "negotiate":
                print(f"The dragon agrees to ally with {player.name}.")
                return "mystic"

        story_stage += 1

    if player.health <= 0:
        print(f"Game over, {player.name}.")
        return "tragic"


# Main Game Loop
def main():
    print("Welcome to the Adventure Game!")
    name = input("Enter your character's name: ")
    char_class = input("Choose a class [Warrior, Mage, Rogue]: ").capitalize()
    player = Character(name, char_class)
    print(player.show_stats())

    ending = game_story(player)

    if ending == "heroic":
        print(f"Congratulations, {player.name}! You've completed the game with a heroic ending!")
    elif ending == "mystic":
        print(f"Congratulations, {player.name}! You've completed the game with a mystic ending!")
    elif ending == "tragic":
        print(f"Alas, {player.name}, your journey ends in tragedy.")


if __name__ == "__main__":
    main()
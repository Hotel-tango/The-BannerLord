import random as r
import time as t
import json as j

# Text adventure loosely based off of Mount and Blade II: Bannerlord
# Try it, very good game

def error(code="N/A", function="N/A", fatal=False, message="N/A", unusual=False):
    print("")
    print("")
    print("ERROR")
    if not fatal:
        print(f"Error code: {code}")
        print(f"Location: {function}")

    if fatal:
        raise RuntimeError(message)
    
    if unusual:
        raise RuntimeWarning(message)
    
    print("")
    print("")
    # 0: Debug return for testing
    # 1: Issue with a variable having a string or value not accepted, can be created by bypassing match-case guard of invalid inputs. Most likely a coding error.
    # 2: Variable value has gone into a range not accepted

class Player:

    def __init__(self, name):
        self.name = name
        self.max_hp = 50
        self.hp = 50
        self.level = 0
        self.strength = 0
        self.armour_name = "Rags"
        self.armour_red = 0
        self.money = 0
        self.skill_p = 0
        self.inventory = []
        self.party = []

    def get_tier(self):
        self.tier = self.level // 10 + 1

    def level_up(self):
        if self.level < 0:
            error(fatal=True, message="Code 2, level is negative")
        if self.skill_p < 0:
            error(unusual=True, message="Code 2, skill points is negative")
        self.level += 1
        self.max_hp += 5
        self.hp = self.max_hp
        self.skill_p += 1
        self.get_tier()
        

    def skill_point_question(self):
        if self.skill_p > 0:
            print("Which skills would you like to increase:\n"
                  "1. Strength: +0.1 damage multiplier\n"
                  "2. Max hp: +5 to max hp")
            while True:
                choice = input("> ").lower()
                match choice:
                    case "strength":
                        self.upgrade_skill(choice)
                        break
                    case "1":
                        self.upgrade_skill("strength")
                        break
                    case "max hp":
                        self.upgrade_skill(choice)
                        break
                    case "2":
                        self.upgrade_skill("max hp")
                        break
                    case "exit":
                        break
                    case _:
                        print("Invalid input")
            if choice != "exit":
                self.skill_p -= 1

        else:
            print("You have no skill points to use.")

    def upgrade_skill(self, skill):
        match skill:
            case "strength":
                self.strength += 0.1
            case "max hp":
                self.max_hp += 5
                self.hp += 5
            case _:
                error(fatal=True, message="Code 1\n fix this skill issue (lol)")

    def take_damage(self, damage, attacker):
        final_damage = round(damage * (1 - self.armour_red / 100))
        damage_blocked = damage - final_damage
        self.hp -= final_damage
        if self.hp < 1:
            print(f"You died by the hands of {attacker}.")
        else:
            print(f"{attacker} did {final_damage} against you, your armour blocked {damage_blocked}. Your hp is now {self.hp}.")

        if damage < 0:
            error(unusual=True, message="Code 2, negative damage passed to take_damage")

    def __str__(self):
        return(f"{self.name}'s statistics:\n"
               f"Level: {self.level}\n"
               f"Strength: {self.strength}\n"
               f"Max HP: {self.max_hp}\n"
               f"Current HP: {self.hp}\n"
               f"Armour: {self.armour_name}, {self.armour_red}% reduction to damage\n"
               f"Available skill points: {self.skill_p}\n"
               f"Inventory: {", ".join(str(Item) for Item in self.inventory)}\n"
               f"Party: {", ".join(self.party)}")

class Soldier:
    def __init__(self, name, tier, hp, damage, armour, armour_red, mount):
        self.name = name
        self.tier = tier
        self.hp = hp
        self.damage = damage
        self.armour = armour
        self.armour_red = armour_red
        self.mount = mount

    def __str__(self):
        print(f"""
        {self.name}
        {self.tier}
        {self.hp}
        {self.damage}
        {self.armour}
        {self.armour_red}
        {self.mount}
        """)

    def get_stats(self):
        if self.tier == 1:
            self.hp = 75
            self.damage = 10
            self.armour = "Rags"
            self.armour_red = 0
            self.mount = "N/A"
        elif self.tier == 2:
            self.hp = 100
            self.damage = 25
            self.armour = "Gambeson"
            self.armour_red = 15
            self.mount = "N/A"
        elif self.tier == 3:
            self.hp = 125
            self.damage = 40
            self.armour = "Chainmail"
            self.armour_red = 30
            self.mount = "N/A"
        elif self.tier == 4:
            self.hp = 125
            self.damage = 45
            self.armour = "Lamellar"
            self.armour_red = 65
            self.mount = "N/A"
        elif self.tier == 5:
            self.hp = 125
            self.damage = 50
            self.armour = "Plate"
            self.armour_red = 80
            self.mount = "N/A"
        elif self.tier == 6:
            self.hp = 150
            self.damage = 75
            self.armour = "Plate"
            self.armour_red = 80
            self.mount = "Horse"
        else:
            error(fatal=True, message="Code 2, troop tier isn't in accepted range")
    
class Item:
    def __init__(self, name, damage, hp_restore, value):
        self.name = name
        self.damage = damage
        self.hp_restore = hp_restore
        self.value = value
    
    def __str__(self):
        return self.name

class Town:

    def __init__(self, name, armour_shop, weapon_shop, misc_shop, mount_shop, tavern, owner, kingdom, available_recruits):
        self.name = name
        self.armour_shop = armour_shop
        self.weapon_shop = weapon_shop
        self.misc_shop = misc_shop
        self.mount_shop = mount_shop
        self.tavern = tavern
        self.owner = owner
        self.kingdom = kingdom
        self.available_recruits = available_recruits
        self.shops = {
            "Armour shop": self.armour_shop,
            "Weapon shop": self.weapon_shop,
            "Miscellaneous shop": self.misc_shop,
            "Tavern": self.tavern,
            "Mount shop": self.mount_shop
        }

    def __str__(self):
        return (
            f"You have arrived at {self.name}.\n"
            f"{self.name} is owned by {self.owner} and is part of the {self.kingdom}.\n"
            f"There are {self.available_recruits} available recruits in the town.\n"
            f"\n"
        )
    
    def store(self, type, available_items):
        type = str(type).capitalize()
        print(f"You have arrived at the {type}")
        print("Which of the following items would you like to purchase?")

    def options(self):
        while True:
            print(f"You're currently at {self.name}, owned by {self.owner} of the {self.kingdom}.")
            iteration = 0
            shop_list = {}
            for name, exists in self.shops.items():
                if exists:
                    iteration += 1
                    shop_list[iteration] = name
            print("This town has a:" if len(shop_list) == 1 else "This town has:")
            print("\n".join(f"{k}: {v}" for k, v in shop_list.items()))
            print("")
            choice = input("Which would you like to enter?: ").capitalize()
            if choice.isdigit():
                choice = int(choice)
            else:
                pass

            if choice in shop_list.keys():
                selected_shop = shop_list[choice]
                break
            elif choice in shop_list.values():
                selected_shop = choice
                break
            else:
                print("Invalid input, type a number corresponding to the shop you want to enter, or its name.\n")

        match selected_shop:
            case "Armour shop":
                self.store("Armour shop", r.randint(2, 6))
            case "Weapon shop":
                self.store("Weapon shop", r.randint(2, 6))
            case "miscellaneous shop":
                self.store("miscellaneous shop", r.randint(4, 9))
            case "Tavern":
                # The tavern is gonna be a place to recruit companions, or get jobs. Dunno yet, so we'll pass
                pass
            case "Mount shop":
                self.store("Mount shop", r.randint(1, 5))
            case _:
                error(fatal=True, message="Code 1")

    def recruit(self, recruitment_amount):
        print(f"Available recruits: {self.available_recruits}")
        self.recruitment_amount = input("How many recruits would you like to recruit?")
        for self.recruitment_amount in range:
            player.party.append("Recruit")
    

def debug():
    debugging = input("Enter debug mode: ")
    debug_town = Town("John's town", True, True, True, True, True, "John Doe", "Kingdom of John", 10)
    while debugging == "y":
        print("")
        print(f"Debug commands: \n"
              "1: Player skill point test\n"
              "2: Inventory test\n"
              "3: Error test\n"
              "4: Crash error test\n"
              "5: Unusual error test"
              "6: Town test\n"
              "print: Prints information about: town, player\n"
              "give dev weapon: Gives an overpowered weapon\n"
              "give dev consumable: Gives an overpowered consumable\n"
              "add party: Adds a dummy to the party"
              "armours: Prints all armours and their stats"
              "\n"
              "To exit debug mode, type n\n")
        debug_choice = input("Debug choice: ")
        if debug_choice == "1":
            print("")
            player.skill_p = 5
            print(player.strength)
            print(player.max_hp)
            player.skill_point_question()
            print(player.strength)
            print(player.max_hp)
        elif debug_choice == "2":
                    print("")
                    obj = Item("dev object", 5, 5, 5)
                    player.inventory.append(obj)
                    print(f"Inventory: {", ".join(str(Item) for Item in player.inventory)}\n")
        elif debug_choice == "3":
            print("")
            error(0, "John Debug's place of residence")
        elif debug_choice == "4":
            error(fatal=True, message="Debug crash")
        elif debug_choice == "5":
            error(unusual=True, message="Debug unusual error")
        elif debug_choice == "6":
            print("")
            print(debug_town)
            debug_town.options()
        elif debug_choice == "print":
            print(player)
            print("")
            print("Was (player) now (town)")
            print("")
            print(debug_town)
            print("")
            print("Was (town) now (recruit)")
            print("")
            print(recruit)
            print("")
            print("Was (recruit) now (militia)")
            print("")
            print(militia)
            print("")
            print("Was (militia) now (warrior)")
            print("")
            print(warrior)
            print("")
            print("Was (warrior) now (veteran)")
            print("")
            print(veteran)
            print("")
            print("Was (veteran) now (man_at_arms)")
            print("")
            print(man_at_arms)
            print("")
            print("Was (man_at_arms) now (knight)")
            print("")
            print(knight)
            
        elif debug_choice == "give dev weapon":
            dev_weapon = Item("dev weapon", 500, 0, 5000)
            player.inventory.append(dev_weapon)
        elif debug_choice == "give dev consumable":
            dev_consumable = Item("dev consumable", 0, 500, 500)
            player.inventory.append(dev_consumable)
        elif debug_choice == "add party":
            player.party.append("Dummy")
        elif debug_choice == "armour":
            print("""
            Rags: 0
            Gambeson: 15
            Chainmail: 30
            Lamellar: 65
            Plate: 80
            """)
        else:
            if debugging == "n" or debug_choice == "n":
                print("Exiting debug mode")
                print("")
                print("")
                print("")
                print("")
                print("")
                print("")
                print("Welcome to")
                print("""
                  ________            ____                              __                   __
                 /_  __/ /_  ___     / __ )____ _____  ____  ___  _____/ /   ____  _________/ /
                  / / / __ \/ _ \   / __  / __ `/ __ \/ __ \/ _ \/ ___/ /   / __ \/ ___/ __  / 
                 / / / / / /  __/  / /_/ / /_/ / / / / / / /  __/ /  / /___/ /_/ / /  / /_/ /  
                /_/ /_/ /_/\___/  /_____/\__,_/_/ /_/_/ /_/\___/_/  /_____/\____/_/   \__,_/   
                """)
                print("""
                    

                """)
                break

print("Welcome to")
print("""
  ________            ____                              __                   __
 /_  __/ /_  ___     / __ )____ _____  ____  ___  _____/ /   ____  _________/ /
  / / / __ \/ _ \   / __  / __ `/ __ \/ __ \/ _ \/ ___/ /   / __ \/ ___/ __  / 
 / / / / / /  __/  / /_/ / /_/ / / / / / / /  __/ /  / /___/ /_/ / /  / /_/ /  
/_/ /_/ /_/\___/  /_____/\__,_/_/ /_/_/ /_/\___/_/  /_____/\____/_/   \__,_/   
""")
print("""
      

""")

# Initializing classes
player = Player(str(input("What is your name?: ")))

recruit = Soldier("Recruit", 1)
militia = Soldier("Militia", 2)
warrior = Soldier("Warrior", 3)
veteran = Soldier("Veteran", 4)
man_at_arms = Soldier("Man-at-Arms", 5)
knight = Soldier("Knight", 6)

recruit.get_stats()
militia.get_stats()
warrior.get_stats()
veteran.get_stats()
man_at_arms.get_stats()
knight.get_stats()


debug()
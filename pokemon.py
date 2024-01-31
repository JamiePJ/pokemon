''' Add multiple moves per pokemon. Add Move class
Add taking user inputs to choose attack/use item/switch pokemon. Multiplayer inputs for 2 players?
Add simple AI trainer that picks moves to fight back
Add XP for defeating pokemon + levelling up when XP limit reached
Evolve pokemon when certain level reached - use time module (.sleep) to simulate evolve animation
Add pokemon stats - Speed, Attack, Defence, Special, HP. Modify attack method to use stats. Modify levelling up & evolving to change stats
Add status effects e.g. poisoned, sleep
Add more types
Move PP
'''

# type dictionaries
type_effectiveness = {"super effective": 2.0, "not very effective": 0.5, "no effect": 0}
super_effective = type_effectiveness["super effective"]
not_very_effective = type_effectiveness["not very effective"]
no_effect = type_effectiveness["no effect"]
type_chart = {
    "Water": {"Fire": super_effective, "Grass": not_very_effective, "Water": not_very_effective},
    "Fire": {"Water": not_very_effective, "Grass": super_effective, "Fire": not_very_effective},
    "Grass": {"Fire": not_very_effective, "Water": super_effective, "Grass": not_very_effective},
    "Normal": {}
}

# create Pokemon class
## ADD moveset later, moves stored in dictionary of dictionaries (?) to store move name with damage & type
class Pokemon:
    ## add status effects e.g. poisoned
    def __init__(self, name, level, type_, current_health, is_knocked_out, moves):
        self.name = name
        self.level = level
        self.type = type_
        self.max_health = level
        self.health = current_health
        self.is_knocked_out = is_knocked_out
        self.moveset = moves

    def __repr__(self):
        return self.name

    def lose_health(self, damage):
        # method for decreasing health and print advising health lost
        self.health -= damage
        if self.health > 0:
            print(f"{self.name} was damaged and lost {damage} health points. "
                  f"{self.name} has {self.health} health points remaining.")
        elif self.health <= 0:
            print(f"{self.name} was damaged and lost {damage} health points. "
                  f"{self.name} has no health points remaining.")
            self.knock_out()
        return self.health

    def gain_health(self, restore_points):
        # method for gaining health and print advising health gained
        if (self.health + restore_points) <= self.max_health:
            self.health += restore_points
            print(f"{self.name} was healed and gained {restore_points} health points. "
                  f"{self.name} has {self.health} health points remaining.")
        elif (self.health + restore_points) > self.max_health:
            self.health = self.max_health
            print(f"{self.name} was healed to full health")
        return self.health

    def knock_out(self):
        # method for knocking out pokemon when health gets to 0. Print advising pokemon knocked out
        self.is_knocked_out = True
        print(f"{self.name} was knocked out!")
        return self.is_knocked_out

    def revive(self, restore_points):
        # revive a knocked-out pokemon and restore some health. Print advising pokemon revived with x health
        self.is_knocked_out = False
        self.health += restore_points
        print(f"{self.name} was revived and now has {self.health} health points.")
        return self.health

    def attack(self, enemy_pokemon):
        # method for my pokemon attacking enemy pokemon. Includes damage based on type. Print advising attack and how much damage dealt
        ## replace "attack value" with move damage value later on + add attack type from moveset
        ## ADD STAB attack bonus when move type matches pokemon type - see note at top re Move as class
        attack_value = 30
        # check if current pokemon is knocked out
        if self.is_knocked_out:
            print(f"{self.name} is knocked out and cannot attack. Switch to a different pokemon")
            return
        else:
            type_modifier = type_chart[self.type].get(enemy_pokemon.type, 1)
            if type_modifier == 1:
                print(f"{self.name} used Attack on enemy {enemy_pokemon.name}!")
            elif type_modifier == super_effective:
                print(f"{self.name} used Attack on enemy {enemy_pokemon.name}! It was super effective!")
            elif type_modifier == not_very_effective:
                print(f"{self.name} used Attack on enemy {enemy_pokemon.name}! It wasn't very effective...")
            elif type_modifier == no_effect:
                print(f"{self.name} used Attack on enemy {enemy_pokemon.name}. It had no effect.")
            # STAB modifier
            # if self.type == self.move.type: stab_bonus = 1.5 else stab_bonus = 1.0
            damage = attack_value * type_modifier # * stab_bonus
            enemy_pokemon.lose_health(damage)

# create Trainer class
class Trainer:
    ## add "items" instead of "potions" e.g. revives, poison heal
    def __init__(self, name, pokemons, potions, current_pokemon):
        self.name = name
        self.pokemons = pokemons # list
        self.potions = potions
        self.current_pokemon = self.pokemons[current_pokemon]

    def __repr__(self):
        return self.name

    def use_potion(self):
        # method for using potion on trainer's current active pokemon. Print advising potion used
        # check if current pokemon is at max health. Prevent potion use if true
        # MOVED TO choice() FUNCTION
        # if self.current_pokemon.health == self.current_pokemon.max_health:
        #     print(f"{self.current_pokemon} is at full health and cannot be healed any further.")
        #     return
        # else:
        # check if potions available to use
            if self.potions > 2:
                self.potions -= 1
                print(f"{self.name} used a potion on {self.current_pokemon}. "
                      f"{self.name} has {self.potions} potions remaining.")
                self.current_pokemon.gain_health(20)
            elif self.potions == 2:
                self.potions -= 1
                print(f"{self.name} used a potion on {self.current_pokemon}. "
                      f"{self.name} has {self.potions} potion remaining.")
                self.current_pokemon.gain_health(20)
            else:
                self.potions -= 1
                print(f"{self.name} used a potion on {self.current_pokemon}. "
                      f"{self.name} has no potions remaining.")
            # MOVED TO choice() FUNCTION
            # else:
            #     print(f"{self.name} has no potions remaining.")

    def use_revive(self):
        print(f"{self.name} used a revive on {self.current_pokemon}.")
        self.current_pokemon.revive(30)

    def attack_other_trainer(self, enemy_trainer):
        # method for attacking other trainer's current active pokemon. Print advising attack happening
        enemy_trainer_pokemon = enemy_trainer.current_pokemon
        print(f"{self.name} chose to attack {enemy_trainer.name}'s {enemy_trainer_pokemon}.")
        self.current_pokemon.attack(enemy_trainer_pokemon)
        # if enemy pokemon is knocked out by attack, check for remaining pokemon
        if enemy_trainer_pokemon.is_knocked_out == True:
            enemy_trainer.check_remaining_pokemon()
        else:
            return

    def switch_pokemon(self, switch_to_pokemon):
        # method for switching current pokemon with another non-knocked out pokemon. Print advising pokemon being switched in and out
        ## when asking for user input, convert switch-to pokemon choice from pokemon name to list index
        # check if switched in pokemon is valid choice
        try:
            self.pokemons[switch_to_pokemon]
        except IndexError:
            print("This is not a valid switch, choose again")
            return
        # check if switched in pokemon is same as active pokemon
        if self.pokemons[switch_to_pokemon] == self.current_pokemon:
            print("This Pokemon is already active. Choose another pokemon to switch to or choose another option.")
        else:
        # check if switched in pokemon is knocked out
            if self.pokemons[switch_to_pokemon].is_knocked_out:
                print("You cannot switch to a Pokemon that has been knocked out.  Please choose again")
            else:
                print(f"{self.name} switched from {self.current_pokemon} to {self.pokemons[switch_to_pokemon]}.")
                self.current_pokemon = self.pokemons[switch_to_pokemon]
        return self.current_pokemon

    def check_remaining_pokemon(self):
        # method to check whether all trainer's pokemon are knocked out
        remaining_pokemon = []
        for mon in self.pokemons:
            if mon.is_knocked_out == False:
                remaining_pokemon.append(mon)
        if len(remaining_pokemon) > 1:
            print(f"{self.name}'s remaining Pokemon are {remaining_pokemon}.")
            switch_to_choice = input("Which Pokemon do you want to switch to?")
            # loop through list of remaining pokemon to select using string of Pokemon name
            for mon in remaining_pokemon:
                if switch_to_choice.lower() in mon.name.lower():
                    switch_to_index = self.pokemons.index(mon)
                    self.switch_pokemon(switch_to_index)
                    return
            # check if input matches name of remaining pokemon
            if switch_to_choice.lower() not in remaining_pokemon:
                print("That is not a valid choice, please choose again")
                self.check_remaining_pokemon()
        elif len(remaining_pokemon) == 1:
            print(f"{self.name}'s last remaining pokemon is {remaining_pokemon}.")
            switch_to_index = self.pokemons.index(remaining_pokemon[0])
            self.switch_pokemon(switch_to_index)
        else:
            print(f"{self.name} has no Pokemon remaining! {self.name} whited out!")

class Move:
    def __init__(self, name, type_, attack_base_power, status_effect):
        self.name = name
        self.type = type_
        self.attack_base_power = attack_base_power
        self.status_effect = status_effect

    def __repr__(self):
        return self.name

# game flow
def start():
    player1_name = input("Hello player 1! What is your name?")
    player1 = Trainer(player1_name, [squirtle, charmander], 2, 0)
    player2_name = input("Hello player 2! What is your name?")
    player2 = Trainer(player2_name, [charmander2, bulbasaur, squirtle2], 5, 0)
    print(f"{player1.name} challenges {player2.name} to a battle!")
    print(f"{player2.name} sent out {player2.current_pokemon}!")
    print(f"{player1.current_pokemon} I choose you!")
    return player1, player2

def choice(player1, player2):
    user_choice = input(f"What would you like to do {player1.name}? Attack, Use Potion or Switch Pokemon?")
    if "attack" in user_choice.lower():
        player1.attack_other_trainer(player2)
    elif "potion" in user_choice.lower():
        # check if current pokemon is at max health. Prevent potion use if true
        if player1.current_pokemon.health == player1.current_pokemon.max_health:
            print(f"{player1.current_pokemon} is at full health and cannot be healed any further.")
            choice(player1, player2)
        else:
            if player1.potions == 0:
                print(f"{player1.name} has no potions remaining.")
                choice(player1, player2)
            else:
                player1.use_potion()
    elif "switch" in user_choice.lower():
        switch_choice = input("Which Pokemon do you want to switch to?")
        print("functionality to be added")

def game():
    player1, player2 = start()
    # keep game running while either player has pokemon available
    while player1.current_pokemon.is_knocked_out == False and player2.current_pokemon.is_knocked_out == False:
        choice(player1, player2)
        choice(player2, player1)
    # end game
    print("The battle is over!")
    return

# testing
tackle = Move("Tackle", "Normal", 35, None)
squirtle = Pokemon("Squirtle", 100, "Water", 100, False, [tackle])
squirtle2 = Pokemon("Squirtle", 100, "Water", 100, False, [tackle])
charmander = Pokemon("Charmander", 100, "Fire", 100, False, [tackle])
charmander2 = Pokemon("Charmander", 100, "Fire", 100, False, [tackle])
bulbasaur = Pokemon("Bulbasaur", 100, "Grass", 100, False, [tackle])
player = Trainer("Player", [squirtle, charmander], 2, 0)
# rival = Trainer("Rival Gary", [charmander2, bulbasaur, squirtle2], 5, 0)


print(squirtle.moveset)

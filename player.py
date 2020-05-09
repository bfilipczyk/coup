
import ai
import random
class Player:
    def __init__(self, cards=[], money=2, name=-1, is_bot=False, health=2):
        self.cards = cards
        self.money = money
        self.name = name
        self.is_bot = is_bot
        self.health = 2

    def losingCard(self):
        # todo wybór
        if self.is_bot:
            choice = random.randint(0,self.health-1)
        else:
            print("Player ", self.name)
            print("Wybierz karte do odrzucenia")
            self.showCards()
            choice = int(input())
        card = self.cards[choice]
        self.cards.remove(card)
        self.health -= 1
        return card

    def tellCard(self, cardtype):
        if cardtype == 'russia':
            print("Russia")
        elif cardtype == 'protest':
            print("Protest")
        elif cardtype == 'media':
            print("Media")
        elif cardtype == 'police':
            print("Police")
        else:
            print("UE")

    def showCards(self):
        for i in range(0,len(self.cards)):
            print(i)
            self.tellCard(self.cards[i])

    def choosingCards(self):
        #todo wybór
        if self.is_bot:
            if self.health == 2:
                choice = random.sample([0, 1, 2, 3], 2)
            else:
                choice = random.sample([0, 1, 2], 1)
        else:
            print("Choose cards to return")
            self.showCards()
            #if self.health == 2:
            choice = [int(input()), int(input())]
            #else:
            #    choice = [int(input())]
        card = []
        for i in choice:
            card.append(self.cards[i])
        for i in card:
            self.cards.remove(i)
        return card

    def chooseAction(self, known_cards, enemy_hp):
        if self.money >= 10:
            return 2
        if self.is_bot:
            return ai.ai_action(known_cards, self.cards,self.money, enemy_hp)

        accepted = 0
        while accepted != 1:
            print("Choose your action")
            action = int(input())
            if action == 2 and self.money < 7:
                print("Not enough money")
                accepted = 0
            elif action == 4 and self.money < 3:
                print("Not enough money")
                accepted = 0
            else:
                accepted = 1

        return action

    def challanging(self, known_cards, action_type, block, enemy_hp):
        if self.is_bot:
            choice = ai.ai_challange(known_cards, self.cards, block, action_type, enemy_hp)
            if choice == 1:
                print("Player: ", self.name, " challenges")
                return choice
            else:
                print("Player: ", self.name, " doesn't challenge")
                return choice
        print("Player ", self.name, " do you challange? 0 - no 1 - yes")
        return int(input())

    def blocking(self, known_cards, action_type):
        if self.is_bot:
            choice = ai.ai_block(self.cards, action_type)
            if choice == 1:
                print("Player: ", self.name, " blocks")
                return choice
            else:
                print("Player: ", self.name, " doesn't blocks")
                return choice
        print("Player ", self.name, " do you block? 0 - no 1 - yes")
        return int(input())

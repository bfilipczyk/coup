
import ai
import random
from gui import Game_gui


class Player:
    def __init__(self, cards=[], money=2, name=-1, is_bot=False, health=2):
        self.cards = cards
        self.money = money
        self.name = name
        self.is_bot = is_bot
        self.health = 2

    def losingCard(self, gui):
        if self.is_bot:
            choice = random.randint(0, self.health-1)
        else:
            gui.Refresh_Players(self.money, self.cards, self.is_bot)
            gui.Show_text(7)
            choice = gui.Choose_cards()
        card = self.cards[choice]
        self.cards.remove(card)
        self.health -= 1
        return card

    def choosingCards(self, gui):
        if self.is_bot:
            choice = random.sample([0, 1, 2, 3], 2)
            card = []
            for i in choice:
                card.append(self.cards[i])
            for i in card:
                self.cards.remove(i)
            return card
        else:
            gui.Refresh_Players(self.money, self.cards, self.is_bot)
            gui.Show_text(7)
            card = []
            choice = gui.Choose_cards()
            card.append(self.cards[choice])
            self.cards.remove(card[0])
            gui.Refresh_Players(self.money, self.cards, False)
            choice = gui.Choose_cards()
            card.append(self.cards[choice])
            self.cards.remove(card[1])
            return card

    def chooseAction(self, known_cards, enemy_hp, gui):
        if self.money >= 10:
            return 2
        if self.is_bot:
            return ai.ai_action(known_cards, self.cards,self.money, enemy_hp)
        return gui.Choose_action(self.money)

    def challanging(self, known_cards, action_type, block, enemy_hp, gui):
        if self.is_bot:
            choice = ai.ai_challange(known_cards, self.cards, block, action_type, enemy_hp)
            if choice == 1:
                gui.Show_text(4, name=self.name, choice=True)
                return choice
            else:
                gui.Show_text(4, name=self.name, choice=False)
                return choice
        gui.Show_text(3, name=self.name)
        return gui.Block_Chall()

    def blocking(self, known_cards, action_type, gui):
        if self.is_bot:
            choice = ai.ai_block(self.cards, action_type)
            if choice == 1:
                gui.Show_text(6, name=self.name, choice=True)
                return choice
            else:
                gui.Show_text(6, name=self.name, choice=False)
                return choice
        gui.Show_text(5, name=self.name)
        return gui.Block_Chall()

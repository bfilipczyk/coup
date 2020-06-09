"""This module defines player class."""
import random
import ai


class Player:
    """Player object representing single player."""
    def __init__(self, cards=None, money=2, name=-1, is_bot=False):
        """Inits Player class."""
        self.cards = cards
        self.money = money
        self.name = name
        self.is_bot = is_bot
        self.health = 2

    def losing_card(self, gui):
        """Return card from player's hand back."""
        if self.is_bot:
            choice = random.randint(0, self.health-1)
        else:
            gui.refresh_players(self.money, self.cards, self.is_bot)
            gui.show_text(7)
            choice = gui.choose_cards()
        card = self.cards[choice]
        self.cards.remove(card)
        self.health -= 1
        return card

    def choosing_cards(self, gui):
        """Returns 2 cards from player's hand."""
        if self.is_bot:
            if self.health == 2:
                choice = random.sample([0, 1, 2, 3], 2)
            else:
                choice = random.sample([0, 1, 2], 2)
            card = []
            for i in choice:
                card.append(self.cards[i])
            for i in card:
                self.cards.remove(i)
            return card
        gui.refresh_players(self.money, self.cards, self.is_bot)
        gui.show_text(7)
        card = []
        choice = gui.choose_cards()
        card.append(self.cards[choice])
        self.cards.remove(card[0])
        gui.refresh_players(self.money, self.cards, False)
        choice = gui.choose_cards()
        card.append(self.cards[choice])
        self.cards.remove(card[1])
        return card

    def choose_action(self, known_cards, enemy_hp, gui):
        """Allows players to choose action."""
        if self.money >= 10:
            return 2
        if self.is_bot:
            return ai.ai_action(known_cards, self.cards, self.money, enemy_hp)
        return gui.choose_action(self.money)

    def challenging(self, known_cards, action_type, block, enemy_hp, gui):
        """Allows players to choose if the want to challenge action."""
        if self.is_bot:
            choice = ai.ai_challenge(known_cards, self.cards, block, action_type, enemy_hp)
            if choice == 1:
                gui.show_text(4, name=self.name, choice=True)
                return choice
            gui.show_text(4, name=self.name, choice=False)
            return choice
        gui.show_text(3, name=self.name)
        return gui.block_chall()

    def blocking(self, action_type, gui):
        """Allows players to choose if the want to block action."""
        if self.is_bot:
            choice = ai.ai_block(self.cards, action_type)
            if choice:
                gui.show_text(6, name=self.name, choice=True)
                return True
            gui.show_text(6, name=self.name, choice=False)
            return False
        gui.show_text(5, name=self.name)
        return gui.block_chall()

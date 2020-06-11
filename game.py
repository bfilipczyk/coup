"""This module defines logic behind game."""
import random
from player import Player
from gui import GameGui


class Game:
    """Game class"""
    def __init__(self, player, bot):
        """Inits game object."""
        self.deck = []
        self.known_cards = []
        self.players = []
        self.round_count = 0
        self.active_player = None
        self.target_player = None
        self.alive_count = 2
        self.interface = GameGui()
        self.players.append(player)
        self.players.append(bot)
        for i in range(0, 2):
            # creating player
            cards = []
            player = Player(cards, 2, i, False)
            self.players.append(player)
        self.players[1].is_bot = True

    def pull_card(self, amount):
        """Returns cards from list of unused cards."""
        cards = random.sample(self.deck, amount)
        for i in cards:
            self.deck.remove(i)
        if amount == 1:
            return cards[0]
        return cards

    def reset(self):
        """Resets state of game"""
        self.deck = ['russia', 'russia', 'russia', 'protest', 'protest', 'protest', 'media', 'media', 'media', 'police',
                     'police', 'police', 'ue', 'ue', 'ue']
        self.known_cards = []
        self.round_count = 0
        self.active_player = None
        self.target_player = None
        self.alive_count = 2

        # pulling cards
        cards = self.pull_card(4)
        for i in range(2):
            hand = [cards[i], cards[i + 2]]
            # creating player
            self.players[i].cards = hand
            self.players[i].money = 2
            self.players[i].health = 2

    def gui_refresh(self):
        """Refreshes game screen."""
        self.interface.clear_middle()
        self.interface.refresh_players(self.players[0].money, self.players[0].cards, self.players[0].is_bot)
        self.interface.refresh_players(self.players[1].money, self.players[1].cards, self.players[1].is_bot)
        self.interface.refresh_known_cards(self.known_cards)

    def do_action(self, action_type):
        """Make actions effects take place."""
        # USA
        if action_type == 'usa':
            self.active_player.money += 1

        # local businessmen
        elif action_type == 'local businessmen':
            self.active_player.money += 2
        # affair
        elif action_type == "affair":
            self.active_player.money -= 7
            # utrata karty
            self.known_cards.append(self.target_player.losing_card(self.interface))
        # media
        elif action_type == "media":
            self.active_player.cards.extend(self.pull_card(2))
            # wybieranie kart
            cards = self.active_player.choosing_cards(self.interface)
            self.deck.extend(cards)
        # protest
        elif action_type == "protest":
            self.active_player.money -= 3
            # utrata karty
            self.known_cards.append(self.target_player.losing_card(self.interface))
        # police
        elif action_type == "police":
            money = 0
            if self.target_player.money < 2:
                money = self.target_player.money
            else:
                money = 2

            self.target_player.money -= money
            self.active_player.money += money

        # Russia
        else:
            self.active_player.money += 3

    def changing_player(self):
        """Changes current player."""
        tmp = self.active_player
        self.active_player = self.target_player
        self.target_player = tmp

    def do_challenge(self, active=1, card1=''):
        """Makes challenge effects take place"""
        if active:  # sprawdza który gracz jest sprawdzany
            self.known_cards.append(self.target_player.losing_card(self.interface))
            self.active_player.cards.remove(card1)
            self.deck.append(card1)
            self.active_player.cards.append(self.pull_card(1))
        else:
            self.known_cards.append(self.active_player.losing_card(self.interface))
            self.target_player.cards.remove(card1)
            self.deck.append(card1)
            self.target_player.cards.append(self.pull_card(1))

    def challenge(self, action_type, block=0):
        """Checks if challenge is successful."""
        if action_type == "media":  # media
            if 'media' in self.active_player.cards:
                self.do_challenge(1, 'media')
                return True
            self.known_cards.append(self.active_player.losing_card(self.interface))
            return False

        elif action_type == "protest":  # protest
            if block == 1:
                if 'ue' in self.target_player.cards:
                    self.do_challenge(0, 'ue')
                    return False
                self.known_cards.append(self.target_player.losing_card(self.interface))
                return True
            else:
                if 'protest' in self.active_player.cards:
                    self.do_challenge(1, 'protest')
                    return True
                self.known_cards.append(self.active_player.losing_card(self.interface))
                return False
        elif action_type == "police":  # police
            if block == 1:
                if 'media' in self.target_player.cards:
                    self.do_challenge(0, 'media')
                    return False
                elif 'police' in self.target_player.cards:
                    self.do_challenge(0, 'police')
                    return False
                else:
                    self.known_cards.append(self.target_player.losing_card(self.interface))
                    return True
            else:
                if 'police' in self.active_player.cards:
                    self.do_challenge(1, 'police')
                    return True
                else:
                    self.known_cards.append(self.active_player.losing_card(self.interface))
                    return False
        elif action_type == "russia":  # Russia
            if 'russia' in self.active_player.cards:
                self.do_challenge(1, 'russia')
                return True
            else:
                self.known_cards.append(self.active_player.losing_card(self.interface))
                return False
        else:
            if 'russia' in self.target_player.cards:
                self.do_challenge(0, 'russia')
                return False
            self.known_cards.append(self.target_player.losing_card(self.interface))
            return True

    def check_health(self):
        """Returns player's name if it drops to 0."""
        if self.active_player.health <= 0:
            return self.target_player.name
        if self.target_player.health <= 0:
            return self.active_player.name
        return -1

    def play(self):
        """Main function responsible for playing game.

        If one of the players' hp drops to 0 game end and waits for restart.
        """
        block_action = ['local businessmen', 'protest', 'police']
        challenge_action = ['media', 'protest', 'police', 'russia']
        s_player_index = random.randint(0, 1)
        if s_player_index == 1:
            self.active_player = self.players[1]
            self.target_player = self.players[0]
        else:
            self.active_player = self.players[0]
            self.target_player = self.players[1]
        while self.alive_count > 1:
            self.gui_refresh()
            self.interface.refresh()
            self.interface.show_text(1, name=self.active_player.name)
            action_type = self.active_player.choose_action(self.known_cards, self.target_player.health, self.interface)
            self.interface.show_text(2, action=action_type)
            do = 1  # czy akcja sie wykona
            corb = 0  # sprawdza czy przed blokowanie karta nie została sprawdzona
            if action_type in challenge_action:
                if self.target_player.challenging(self.known_cards, action_type, False, self.active_player.health,
                                                  self.interface):
                    corb = 1
                    do = self.challenge(action_type)
                    end = self.check_health()
                    if end != -1:
                        break
            if action_type in block_action and corb == 0:
                if self.target_player.blocking(action_type, self.interface):
                    if self.active_player.challenging(self.known_cards, action_type, True, self.target_player.health,
                                                      self.interface):
                        do = self.challenge(action_type, 1)
                        end = self.check_health()
                        if end != -1:
                            break
                    else:
                        do = 0
            if do:
                self.do_action(action_type)
                end = self.check_health()
                if end != -1:
                    break
            self.changing_player()
            self.round_count += 1
        if self.active_player.health > 0:
            return self.interface.win_message(self.active_player.name)
        return self.interface.win_message(self.target_player.name)


def main():

    player = Player([], 2, "Player", False)
    bot = Player([], 2, "Bottimus", True)
    game = Game(player, bot)
    game.reset()
    while True:
        if game.play():
            game.reset()


if __name__ == '__main__':
    main()

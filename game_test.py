import unittest
from player import Player
import game


class GameTest(unittest.TestCase):
    def setUp(self):
        player = Player([], 2, "Player", False)
        bot = Player([], 2, "Bottimus", True)
        self.game = game.Game(player, bot)
        self.game.reset()

    def test_pull_card_reduce_deck(self):
        # given
        amount = 1

        # when
        deck_len_expected = len(self.game.deck) - amount

        # method tested
        self.game.pull_card(amount)

        # then
        self.assertEqual(deck_len_expected,len(self.game.deck))

    def test_pull_card_returns_enough_cards(self):
        # given
        amount = 3

        # method tested
        hand = self.game.pull_card(amount)

        # then
        self.assertEqual(amount, len(hand))

    def test_changing_players(self):
        # given
        self.game.active_player = self.game.players[0]
        self.game.target_player = self.game.players[1]

        # method tested
        self.game.changing_player()

        # then
        self.assertEqual(self.game.players[1], self.game.active_player)

    def test_check_health(self):
        # given
        self.game.active_player = self.game.players[0]
        self.game.target_player = self.game.players[1]
        self.game.target_player.health = 0

        # method tested
        tmp = self.game.check_health()

        # then
        self.assertEqual(tmp, self.game.active_player.name)

    def test_affair_action(self):
        # given
        self.game.active_player = self.game.players[0]
        self.game.target_player = self.game.players[1]
        self.game.active_player.money = 8

        # method tested
        self.game.do_action('affair')

        # then
        self.assertEqual(self.game.target_player.health, 1)
        self.assertEqual(self.game.active_player.money, 1)
        self.assertEqual(len(self.game.known_cards), 1)

    def test_police_action(self):
        # given
        self.game.active_player = self.game.players[0]
        self.game.target_player = self.game.players[1]

        # method tested
        self.game.do_action('police')

        # then
        self.assertEqual(self.game.target_player.money, 0)
        self.assertEqual(self.game.active_player.money, 4)



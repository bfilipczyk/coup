from player import Player
import random
import player


class Game:

    def __init__(self):
        self.deck = []
        self.knownCards = []
        self.players = []
        self.roundCount = 0
        self.active_player = None
        self.target_player = None
        self.aliveCount = 2

        for i in range(0, 2):
            # setting name
            name = i
            # creating player
            cards = []
            player = Player(cards, 2, i, False)
            self.players.append(player)
        self.players[1].is_bot = True

    def pull_card(self, amount):
        cards = random.sample(self.deck, amount)
        for i in cards:
            self.deck.remove(i)
        return cards

    def reset(self):
        self.deck = ['russia', 'russia', 'russia', 'protest', 'protest', 'protest', 'media', 'media', 'media', 'police',
                     'police', 'police', 'ue', 'ue', 'ue']  # 0/Russia 1/protest 2/media 3/police 4/UE
        self.knownCards = []
        self.roundCount = 0
        self.active_player = None
        self.target_player = None
        self.aliveCount = 2

        # pulling cards
        cards = self.pull_card(4)
        for i in range(0, 2):
            hand = [cards[i], cards[i+2]]
            # setting name
            name = i
            # creating player
            self.players[i].cards = hand
            self.players[i].money = 2
            self.players[i].health = 2

    def do_action(self, action_type):
        # USA
        if action_type == 0:
            self.active_player.money += 1

        # local businessmen
        elif action_type == 1:
            self.active_player.money += 2

        # affair
        elif action_type == 2:
            self.active_player.money -=7
            # utrata karty
            self.knownCards.append(self.target_player.losingCard())
        # media
        elif action_type == 3:
            self.active_player.cards.extend(self.pull_card(2))
            print(len(self.active_player.cards))
            # wybieranie kart
            cards = self.active_player.choosingCards()
            self.deck.extend(cards)
        # protest
        elif action_type == 4:
            self.active_player.money -= 3
            # utrata karty
            self.knownCards.append(self.target_player.losingCard())
        # police
        elif action_type == 5:
            money = 0
            if self.target_player.money == 1:
                money = 1
            else:
                money = 2

            self.target_player.money -= money
            self.active_player.money += money

        # Russia
        else:
            self.active_player.money += 3

    def changingPlayer(self):
        tmp = self.active_player
        self.active_player = self.target_player
        self.target_player = tmp

    def do_challange(self, active=1, card1=''):
        if active:  # sprawdza który gracz jest sprawdzany
            self.knownCards.append(self.target_player.losingCard())
            self.active_player.cards.remove(card1)
            self.deck.append(card1)
            self.active_player.cards.append(self.pull_card(1))
        else:
            self.knownCards.append(self.active_player.losingCard())
            self.target_player.cards.remove(card1)
            self.deck.append(card1)
            self.target_player.cards.append(self.pull_card(1))

    def challange(self, action_type,block=0):
        if action_type == 3:  # media
            if 'media' in self.active_player.cards:
                self.do_challange(1,'media')
                return 1
            else:
                self.knownCards.append(self.active_player.losingCard())
                return 0

        elif action_type == 4:  # protest
            if block == 1:
                if 'ue' in self.target_player.cards:
                    self.do_challange(0,'ue')
                    return 0
                else:
                    self.knownCards.append(self.target_player.losingCard())
                    return 1
            else:
                if 'protest' in self.active_player.cards:
                    self.do_challange(1,'protest')
                    return 1
                else:
                    self.knownCards.append(self.active_player.losingCard())
                    return 0
        elif action_type == 5:  # police
            if block == 1:
                if 'media' in self.target_player.cards:
                    self.do_challange(0, 'media')
                    return 0
                elif 'police' in self.target_player.cards:
                    self.do_challange(0, 'police')
                    return 0
                else:
                    self.knownCards.append(self.target_player.losingCard())
                    return 1
            else:
                if 'police' in self.active_player.cards:
                    self.do_challange(1,'police')
                    return 1
                else:
                    self.knownCards.append(self.active_player.losingCard())
                    return 0
        elif action_type == 6:  # Russia
            if 'russia' in self.active_player.cards:
                self.do_challange(1, 'russia')
                return 1
            else:
                self.knownCards.append(self.active_player.losingCard())
                return 0
        else:
            if 'russia' in self.target_player.cards:
                self.do_challange(0, 'russia')
                return 0
            else:
                self.knownCards.append(self.target_player.losingCard())
                return 1

    def checkHealth(self):
        if self.active_player.health == 0:
            return self.target_player.name
        if self.target_player.health == 0:
            return self.active_player.name
        return -1

    def tellCard(self,type):
        if type == 'russia':
            print("Russia")
        elif type == 'protest':
            print("Protest")
        elif type == 'media':
            print("Media")
        elif type == 'police':
            print("Police")
        else:
            print("UE")

    def tellActions(self):
        print("Action types")
        print("0 - USA, 1 - local businessmen, 2 - affair, 3 - media, 4 - protest, 5 - police, 6 - Russia")

    def state(self, player):
        print("\n\n\n")
        print("Player ",player.name)
        print("Your cards:")
        for i in player.cards:
            self.tellCard(i)
        print("Known cards:")
        for i in self.knownCards:
            self.tellCard(i)
        print("Your funds: ", player.money)
        self.tellActions()

    def showChosenAction(self, action_type):
        if action_type == 0:
            print("USA")
        elif action_type == 1:
            print("local businessmen")
        elif action_type == 2:
            print("affair")
        elif action_type == 3:
            print("media")
        elif action_type == 4:
            print("protest")
        elif action_type == 5:
            print("police")
        else:
            print("Russia")

    def play(self):
        blockAction = [1,4,5]
        challangeAction = [3,4,5,6]
        sPlayerIndex = random.randint(0, 1)
        if sPlayerIndex == 1:
            self.active_player = self.players[1]
            self.target_player = self.players[0]
        else:
            self.active_player = self.players[0]
            self.target_player = self.players[1]
        while self.aliveCount>1:
            self.state(self.players[0])
            action_type = self.active_player.chooseAction(self.knownCards, self.target_player.health)
            if self.active_player.is_bot:
                print()
                print("Player: ", self.active_player.name, " choses action:")
                self.showChosenAction(action_type)
            else:
                print()
                print("Player: ", self.active_player.name, " chose action:")
                self.showChosenAction(action_type)
            do = 1  # czy akcja sie wykona
            corb = 0  # sprawdza czy przed blokowanie karta nie została sprawdzona
            if action_type in challangeAction:
                if self.target_player.challanging(self.knownCards, action_type, False, self.active_player.health):
                    corb = 1
                    do = self.challange(action_type)
                    end = self.checkHealth()
                    if end != -1:
                        break
            if action_type in blockAction and corb == 0:
                if self.target_player.blocking(self.knownCards, action_type):
                    if self.active_player.challanging(self.knownCards, action_type,True, self.target_player.health):
                        do = self.challange(action_type, 1)
                        end = self.checkHealth()
                        if end != -1:
                            break
                    else:
                        do = 0
            if do:
                self.do_action(action_type)
                end = self.checkHealth()
                if end != -1:
                    break
            self.changingPlayer()
            self.roundCount += 1
        if self.active_player.health>0:
            return self.active_player.name
        else:
            return self.target_player.name





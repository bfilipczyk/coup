"""This module defines actions of AI."""
import random
import itertools


class Result:
    """Holds values of specific action choice."""
    def __init__(self):
        """Inits Result class"""
        self.value = 0
        self.times = 0

    def weight(self):
        """Returns calculated weight of an action."""
        if self.times == 0:
            return -100
        return self.value / self.times


def add_to_deck(known_cards, player_cards):
    """Returns list of all possible cards player can have."""
    deck = []
    russia = 3
    protest = 3
    media = 3
    police = 3
    ue = 3
    for card in known_cards:
        if card == 'russia':
            russia -= 1
        elif card == 'protest':
            protest -= 1
        elif card == 'media':
            media -= 1
        elif card == 'police':
            police -= 1
        elif card == 'ue':
            ue -= 1
    for card in player_cards:
        if card == 'russia':
            russia -= 1
        elif card == 'protest':
            protest -= 1
        elif card == 'media':
            media -= 1
        elif card == 'police':
            police -= 1
        elif card == 'ue':
            ue -= 1
    for _ in range(russia):
        deck.append('russia')
    for _ in range(protest):
        deck.append('protest')
    for _ in range(media):
        deck.append('media')
    for _ in range(police):
        deck.append('police')
    for _ in range(ue):
        deck.append('ue')
    return deck


def ai_action(known_cards, player_cards, player_money, enemy_hp):
    """Calculates action for AI."""
    deck = add_to_deck(known_cards, player_cards)
    enemy_deck = itertools.combinations(deck, enemy_hp)
    actions = ['usa', 'local businessmen', 'affair', 'media', 'protest', 'police', 'russia']
    usa = Result()
    local_businessmen = Result()
    media = Result()
    police = Result()
    russia = Result()
    protest = Result()
    affair = Result()

    if player_money < 3:
        actions.remove('affair')
        actions.remove('protest')
    elif player_money < 7:
        actions.remove('affair')
    for hand in enemy_deck:
        for _ in range(0, 1000):
            choice = random.choice(actions)
            if choice == 'usa':
                usa.value += 1
                usa.times += 1
            elif choice == 'local businessmen':
                block = random.choice([0, 1])  # 1-przeciwnik blokuje 0-przeciwnik nie blokuje
                if block == 0:
                    local_businessmen.value += 2
                    local_businessmen.times += 1
                else:
                    checkp = random.choice([0, 1])  # 1-ai sprawdza gracza
                    if checkp == 0:
                        local_businessmen.times += 1
                    else:
                        if 'russia' in hand:
                            local_businessmen.value += -10
                            local_businessmen.times += 1
                        else:
                            local_businessmen.value += 12
                            local_businessmen.times += 1
            elif choice == 'affair':
                affair.value += 10
                affair.times += 1
            elif choice == 'media':
                checka = random.choice([0, 1])  # 1-gracz sprawdza ai
                if checka == 0:
                    media.value += 2
                    media.times += 1
                else:
                    if 'media' in player_cards:
                        media.value += 12
                        media.times += 1
                    else:
                        media.value += -10
                        media.times += 1
            elif choice == 'protest':
                checka = random.choice([0, 1])
                if checka == 0:
                    block = random.choice([0, 1])
                    if block == 0:
                        protest.value += 10
                        protest.times += 1
                    else:
                        checkp = random.choice([0, 1])
                        if checkp == 0:
                            protest.value += 0
                            protest.times += 1
                        else:
                            if 'ue' in hand:
                                protest.value += -10
                                protest.times += 1
                            else:
                                protest.value += 20
                                protest.times += 1
                else:
                    if 'protest' in player_cards:
                        protest.value += 20
                        protest.times += 1
                    else:
                        protest.value += -13
                        protest.times += 1
            elif choice == 'police':
                checka = random.choice([0, 1])
                if checka == 0:
                    block = random.choice([0, 1])
                    if block == 0:
                        police.value += 3
                        police.times += 1
                    else:
                        checkp = random.choice([0, 1])
                        if checkp == 0:
                            police.value += 0
                            police.times += 1
                        else:
                            if 'media' or 'police' in hand:
                                police.value += -10
                                police.times += 1
                            else:
                                police.value += 13
                                police.times += 1
                else:
                    if 'police' in player_cards:
                        police.value += 14
                        police.times += 1
                    else:
                        police.value += -10
                        police.times += 1
            else:
                checka = random.choice([0, 1])
                if checka == 0:
                    russia.value += 3
                    russia.times += 1
                else:
                    if 'russia' in player_cards:
                        russia.value += 13
                        russia.times += 1
                    else:
                        russia.value += -10
                        russia.times += 1
    best_action = 0
    results = [usa, local_businessmen, affair, media, protest, police, russia]
    for i in range(len(results)):
        if results[best_action].weight() < results[i].weight():
            best_action = i
    tmp = ['usa', 'local businessmen', 'affair', 'media', 'protest', 'police', 'russia']
    return tmp[best_action]


def ai_block(player_cards, action_type):
    """Calculates if AI should block action."""
    block = Result()
    noblock = Result()
    for _ in range(0, 1000):
        if action_type == "local businessmen":  # 1 - local businessmen,
            block = random.choice([True, False])  # true-ai blokuje false-ai nie blokuje
            if block:
                check = random.choice([True, False])
                if check:
                    if 'russia' in player_cards:
                        block.value += 12
                        block.times += 1
                    else:
                        block.value -= 10
                        block.times += 1
                else:
                    block.value += 2
                    block.times += 1
            else:
                noblock.value += -2
                noblock.times += 1
        elif action_type == "protest":  # 4 - protest
            block = random.choice([True, False])
            if block:
                check = random.choice([True, False])
                if check:
                    if 'ue' in player_cards:
                        block.value += 10
                        block.times += 1
                    else:
                        block.value += -20
                        block.times += 1
                else:
                    block.value += 0
                    block.times += 1
            else:
                noblock.value += -10
                noblock.times += 1
        else:  # 5 - police
            block = random.choice([True, False])
            if block:
                check = random.choice([True, False])
                if check:
                    if 'police' or 'media' in player_cards:
                        block.value += 10
                        block.times += 1
                    else:
                        block.value += -10
                        block.times += 1
                else:
                    block.value += 3
                    block.times += 1
            else:
                noblock.value += -3
                noblock.times += 1

    if block.weight() > noblock.weight():
        return True
    return False


def ai_challenge(known_cards, player_cards, block, action_type, enemy_hp):
    """Calculates if AI should challenge."""

    deck = add_to_deck(known_cards, player_cards)
    enemy_deck = itertools.combinations(deck, enemy_hp)

    check = Result()
    nocheck = Result()

    for hand in enemy_deck:
        for _ in range(0, 1000):
            if action_type == "media":  # media
                checkp = random.choice([True, False])
                if checkp:
                    if 'media' in hand:
                        check.value += -12
                        check.times += 1
                    else:
                        check.value += 12
                        check.times += 1
                else:
                    nocheck.value += -2
                    nocheck.times += 1
            elif action_type == "protest":  # protest
                if block:
                    checkp = random.choice([True, False])
                    if checkp:
                        if 'ue' in hand:
                            check.value += -10
                            check.times += 1
                        else:
                            check.value += 20
                            check.times += 1
                    else:
                        nocheck.value += 0
                        nocheck.times += 1
                else:
                    checkp = random.choice([True, False])
                    if checkp:
                        if 'protest' in hand:
                            check.value += -20
                            check.times += 1
                        else:
                            check.value += 13
                            check.times += 1
                    else:
                        nocheck.value += -10
                        nocheck.times += 1
            elif action_type == "police":  # police
                if block:
                    checkp = random.choice([True, False])
                    if checkp:
                        if 'media' or 'police' in hand:
                            check.value += -10
                            check.times += 1
                        else:
                            check.value += 13
                            check.times += 1
                    else:
                        nocheck.value += 0
                        nocheck.times += 1
                else:
                    checkp = random.choice([True, False])
                    if checkp:
                        if 'police' in hand:
                            check.value += -13
                            check.times += 1
                        else:
                            check.value += 10
                            check.times += 1
                    else:
                        nocheck.value += -3
                        nocheck.times += 1
            elif action_type == "Russia":  # Russia
                checkp = random.choice([True, False])
                if checkp:
                    if 'russia' in hand:
                        check.value += -13
                        check.times += 1
                    else:
                        check.value += 10
                        check.times += 1
                else:
                    nocheck.value += -3
                    nocheck.times += 1
            else:
                checkp = random.choice([True, False])
                if checkp:
                    if 'russia' in enemy_deck:
                        check.value += -10
                        check.times += 1
                    else:
                        check.value += 13
                        check.times += 1
                else:
                    nocheck.value += 0
                    nocheck.times += 1

    if check.weight() > nocheck.weight():
        return True
    return False

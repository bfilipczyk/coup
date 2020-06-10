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
    actions = ['usa', 'local bisnessmen', 'affair', 'media', 'protest', 'police', 'russia']
    usa = Result()
    local_bisnessmen = Result()
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
            elif choice == 'local bisnessmen':
                block = random.choice([0, 1])  # 1-przeciwnik blokuje 0-przeciwnik nie blokuje
                if block == 0:
                    local_bisnessmen.value += 2
                    local_bisnessmen.times += 1
                else:
                    checkp = random.choice([0, 1])  # 1-ai sprawdza gracza
                    if checkp == 0:
                        local_bisnessmen.times += 1
                    else:
                        if 'russia' in hand:
                            local_bisnessmen.value += -10
                            local_bisnessmen.times += 1
                        else:
                            local_bisnessmen.value += 12
                            local_bisnessmen.times += 1
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
    results = [usa, local_bisnessmen, affair, media, protest, police, russia]
    for i in range(len(results)):
        if results[best_action].weight() < results[i].weight():
            best_action = i
    tmp = ['usa', 'local bisnessmen', 'affair', 'media', 'protest', 'police', 'russia']
    return tmp[best_action]


def ai_block(player_cards, action_type):
    """Calculates if AI should block action."""
    block_value = 0
    block_times = 0
    noblock_value = 0
    noblock_times = 0
    for _ in range(0, 1000):
        if action_type == "local businessmen":  # 1 - local businessmen,
            block = random.choice([True, False])  # true-ai blokuje false-ai nie blokuje
            if block:
                check = random.choice([True, False])
                if check:
                    if 'russia' in player_cards:
                        block_value += 12
                        block_times += 1
                    else:
                        block_value -= 10
                        block_times += 1
                else:
                    block_value += 2
                    block_times += 1
            else:
                noblock_value += -2
                noblock_times += 1
        elif action_type == "protest":  # 4 - protest
            block = random.choice([True, False])
            if block:
                check = random.choice([True, False])
                if check:
                    if 'ue' in player_cards:
                        block_value += 10
                        block_times += 1
                    else:
                        block_value += -20
                        block_times += 1
                else:
                    block_value += 0
                    block_times += 1
            else:
                noblock_value += -10
                noblock_times += 1
        else:  # 5 - police
            block = random.choice([True, False])
            if block:
                check = random.choice([True, False])
                if check:
                    if 'police' or 'media' in player_cards:
                        block_value += 10
                        block_times += 1
                    else:
                        block_value += -10
                        block_times += 1
                else:
                    block_value += 3
                    block_times += 1
            else:
                noblock_value += -3
                noblock_times += 1

    b_weight = block_value/block_times
    nb_weight = noblock_value/noblock_times

    if b_weight > nb_weight:
        return True
    return False


def ai_challenge(known_cards, player_cards, block, action_type, enemy_hp):
    """Calculates if AI should challenge."""

    deck = add_to_deck(known_cards, player_cards)
    enemy_deck = itertools.combinations(deck, enemy_hp)

    check_value = 0
    check_times = 0
    nocheck_value = 0
    nocheck_times = 0

    for hand in enemy_deck:
        for _ in range(0, 1000):
            if action_type == "media":  # media
                checkp = random.choice([True, False])
                if checkp:
                    if 'media' in hand:
                        check_value += -12
                        check_times += 1
                    else:
                        check_value += 12
                        check_times += 1
                else:
                    nocheck_value += -2
                    nocheck_times += 1
            elif action_type == "protest":  # protest
                if block:
                    checkp = random.choice([True, False])
                    if checkp:
                        if 'ue' in hand:
                            check_value += -10
                            check_times += 1
                        else:
                            check_value += 20
                            check_times += 1
                    else:
                        nocheck_value += 0
                        nocheck_times += 1
                else:
                    checkp = random.choice([True, False])
                    if checkp:
                        if 'protest' in hand:
                            check_value += -20
                            check_times += 1
                        else:
                            check_value += 13
                            check_times += 1
                    else:
                        nocheck_value += -10
                        nocheck_times += 1
            elif action_type == "police":  # police
                if block:
                    checkp = random.choice([True, False])
                    if checkp:
                        if 'media' or 'police' in hand:
                            check_value += -10
                            check_times += 1
                        else:
                            check_value += 13
                            check_times += 1
                    else:
                        nocheck_value += 0
                        nocheck_times += 1
                else:
                    checkp = random.choice([True, False])
                    if checkp:
                        if 'police' in hand:
                            check_value += -13
                            check_times += 1
                        else:
                            check_value += 10
                            check_times += 1
                    else:
                        nocheck_value += -3
                        nocheck_times += 1
            elif action_type == "Russia":  # Russia
                checkp = random.choice([True, False])
                if checkp:
                    if 'russia' in hand:
                        check_value += -13
                        check_times += 1
                    else:
                        check_value += 10
                        check_times += 1
                else:
                    nocheck_value += -3
                    nocheck_times += 1
            else:
                checkp = random.choice([True, False])
                if checkp:
                    if 'russia' in enemy_deck:
                        check_value += -10
                        check_times += 1
                    else:
                        check_value += 13
                        check_times += 1
                else:
                    nocheck_value += 0
                    nocheck_times += 1

    c_weight = check_value / check_times
    nc_weight = nocheck_value / nocheck_times

    if c_weight > nc_weight:
        return True
    return False

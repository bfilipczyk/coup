import random
import itertools


def add_to_deck(known_cards, player_cards):
    deck = []
    russia = 3
    protest = 3
    media = 3
    police = 3
    ue = 3
    for x in known_cards:
        if x == 'russia':
            russia -= 1
        if x == 'protest':
            protest -= 1
        if x == 'media':
            media -= 1
        if x == 'police':
            police -= 1
        if x == 'ue':
            ue -= 1
    for i in player_cards:
        if i == 'russia':
            russia -= 1
        if i == 'protest':
            protest -= 1
        if i == 'media':
            media -= 1
        if i == 'police':
            police -= 1
        if i == 'ue':
            ue -= 1
    for i in range(0,russia):
        deck.append('russia')
    for i in range(0, protest):
        deck.append('protest')
    for i in range(0, media):
        deck.append('media')
    for i in range(0, police):
        deck.append('police')
    for i in range(0,ue):
        deck.append('ue')
    return deck


def ai_action(known_cards, player_cards, player_money, enemy_hp):
    deck = add_to_deck(known_cards, player_cards)
    enemy_deck = itertools.combinations(deck, enemy_hp)
    actions = ['usa', 'local bisnessmen', 'affair', 'media', 'protest', 'police', 'russia']
    if player_money < 7:
        actions.remove('affair')
        actions.remove('protest')
    elif player_money < 3:
        actions.remove('protest')

    result = dict()
    for k in actions:
        result[k] = {'value': 0, 'times': 0}

    for i in enemy_deck:
        for j in range(0,   1000):
            choice = random.choice(actions)
            if choice == 'usa':
                result[choice]['value'] += 1
                result[choice]['times'] += 1
            elif choice == 'local bisnessmen':
                block = random.choice([0, 1])  # 1-przeciwnik blokuje 0-przeciwnik nie blokuje
                if block == 0:
                    result[choice]['value'] += 2
                    result[choice]['times'] += 1
                else:
                    checkp = random.choice([0, 1])  # 1-ai sprawdza gracza
                    if checkp == 0:
                        result[choice]['times'] += 1
                    else:
                        if 'russia' in i:
                            result[choice]['value'] += -10
                            result[choice]['times'] += 1
                        else:
                            result[choice]['value'] += 12
                            result[choice]['times'] += 1
            elif choice == 'affair':
                result[choice]['value'] += 10
                result[choice]['times'] += 1
            elif choice == 'media':
                checka = random.choice([0, 1])  # 1-gracz sprawdza ai
                if checka == 0:
                    result[choice]['value'] += 2
                    result[choice]['times'] += 1
                else:
                    if 'media' in player_cards:
                        result[choice]['value'] += 12
                        result[choice]['times'] += 1
                    else:
                        result[choice]['value'] += -10
                        result[choice]['times'] += 1
            elif choice == 'protest':
                checka = random.choice([0, 1])
                if checka == 0:
                    block = random.choice([0, 1])
                    if block == 0:
                        result[choice]['value'] += 10
                        result[choice]['times'] += 1
                    else:
                        checkp = random.choice([0, 1])
                        if checkp == 0:
                            result[choice]['value'] += 0
                            result[choice]['times'] += 1
                        else:
                            if 'ue' in enemy_deck:
                                result[choice]['value'] += -10
                                result[choice]['times'] += 1
                            else:
                                result[choice]['value'] += 20
                                result[choice]['times'] += 1
                else:
                    if 'protest' in player_cards:
                        result[choice]['value'] += 20
                        result[choice]['times'] += 1
                    else:
                        result[choice]['value'] += -13
                        result[choice]['times'] += 1
            elif choice == 'police':
                checka = random.choice([0, 1])
                if checka == 0:
                    block = random.choice([0, 1])
                    if block == 0:
                        result[choice]['value'] += 3
                        result[choice]['times'] += 1
                    else:
                        checkp = random.choice([0, 1])
                        if checkp == 0:
                            result[choice]['value'] += 0
                            result[choice]['times'] += 1
                        else:
                            if 'media' or 'police' in enemy_deck:
                                result[choice]['value'] += -10
                                result[choice]['times'] += 1
                            else:
                                result[choice]['value'] += 13
                                result[choice]['times'] += 1
                else:
                    if 'police' in player_cards:
                        result[choice]['value'] += 14
                        result[choice]['times'] += 1
                    else:
                        result[choice]['value'] += -10
                        result[choice]['times'] += 1
            else:
                checka = random.choice([0, 1])
                if checka == 0:
                    result[choice]['value'] += 3
                    result[choice]['times'] += 1
                else:
                    if 'russia' in player_cards:
                        result[choice]['value'] += 13
                        result[choice]['times'] += 1
                    else:
                        result[choice]['value'] += -10
                        result[choice]['times'] += 1
    best_action = 'usa'
    k=0
    for i in result:
        b_weight = result[best_action]['value']/result[best_action]['times']
        n_weight = result[i]['value']/result[i]['times']
        if n_weight > b_weight:
            best_action = i
    tmp=['usa', 'local bisnessmen', 'affair', 'media','protest', 'police', 'russia']
    for i in range(0, len(tmp)):
        if tmp[i] == best_action:
            return i


def ai_block(player_cards,action_type):
    block_value = 0
    block_times = 0
    noblock_value = 0
    noblock_times = 0
    for i in range(0, 1000):
        if action_type == 1:  # 1 - local businessmen,
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
        elif action_type == 4:  # 4 - protest
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

    if b_weight> nb_weight:
        return 1
    else:
        return 0


def ai_challange(known_cards, player_cards, block, action_type, enemy_hp):

    deck = add_to_deck(known_cards, player_cards)
    enemy_deck = itertools.combinations(deck, enemy_hp)

    check_value = 0
    check_times = 0
    nocheck_value = 0
    nocheck_times = 0

    for i in enemy_deck:
        for j in range(0, 1000):
            if action_type == 3:  # media
                checkp = random.choice([True, False])
                if checkp:
                    if 'media' in i:
                        check_value += -12
                        check_times += 1
                    else:
                        check_value += 12
                        check_times += 1
                else:
                    nocheck_value += -2
                    nocheck_times += 1
            elif action_type == 4:  # protest
                if block:
                    checkp = random.choice([True, False])
                    if checkp:
                        if 'ue' in i:
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
                        if 'protest' in enemy_deck:
                            check_value += -20
                            check_times += 1
                        else:
                            check_value += 13
                            check_times += 1
                    else:
                        nocheck_value += -10
                        nocheck_times += 1
            elif action_type == 5:  # police
                if block:
                    checkp = random.choice([True, False])
                    if checkp:
                        if 'media' or 'police' in enemy_deck:
                            check_value += -10
                            check_times += 1
                        else:
                            check_value += 13
                            check_times += 1
                    else:
                        nocheck_value += 0
                        nocheck_times +=1
                else:
                    checkp = random.choice([True, False])
                    if checkp:
                        if 'police' in enemy_deck:
                            check_value += -13
                            check_times += 1
                        else:
                            check_value += 10
                            check_times += 1
                    else:
                        nocheck_value += -3
                        nocheck_times += 1
            elif action_type == 6:  # Russia
                checkp = random.choice([True, False])
                if checkp:
                    if 'russia' in i:
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
        return 1
    else:
        return 0








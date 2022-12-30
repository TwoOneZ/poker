import itertools
import copy

rank_dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
             '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

red_joker_cards = ['2D', '2H', '3D', '3H', '4D', '4H', '5D', '5H', '6D', '6H', '7D', '7H', '8D', '8H',
                   '9D', '9H', 'TD', 'TH', 'JD', 'JH', 'QD', 'QH', 'KD', 'KH', 'AD', 'AH'] #ранги красных карт которыми может быть джокер

black_joker_cards = ['2C', '2S', '3C', '3S', '4C', '4S', '5C', '5S', '6C', '6S', '7C', '7S', '8C', '8S',
                     '9C', '9S', 'TC', 'TS', 'JC', 'JS', 'QC', 'QS', 'KC', 'KS', 'AC', 'AS'] #ранги черных карт которыми может быть джокер


def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""

    return sorted([rank_dict[card[0]] for card in hand], reverse=True)


def flush(hand):
    """Возвращает True, если все карты одной масти"""

    return len(set([card[1] for card in hand])) == 1


def sublist_in_list(main_list, sublist):
    return any(main_list[idx: idx + len(sublist)] == sublist
               for idx in range(len(main_list) - len(sublist) + 1))


def straight(ranks):
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""

    all_ranks = list(range(1, 15))
    ranks = list(set(ranks))

    if 14 in ranks:
        ranks.insert(0, 1)

    return sublist_in_list(all_ranks, ranks) and len(ranks) >= 5


def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""

    for rank in ranks:
        if ranks.count(rank) == n:
            return rank

    return None


def two_pair(ranks):
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""
    pairs = []
    ranks_grouped = itertools.groupby(ranks, key=lambda rank: rank)

    for key, group in ranks_grouped:
        if len(list(group)) == 2:
            pairs.append(key)
        if len(pairs) == 2:
            return pairs

    return None


def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """

    combo = list(itertools.combinations(hand, 5))
    return max(combo, key=hand_rank)


def replace_two_joker(hand, black_card, red_card):
    """Заменяет каждого джокера на карты(black_card - для черного и
    red_card - для красного джокеров) возвращает измененную "руку" """

    joker_hand = copy.deepcopy(hand)
    for idx in range(len(joker_hand)):
        if joker_hand[idx] == '?R':
            joker_hand[idx] = red_card
        elif joker_hand[idx] == '?B':
            joker_hand[idx] = black_card

    return joker_hand


def replace_one_joker(hand, card):
    """Заменяет джокера на карту(card) возвращает измененную "руку" """

    joker_hand = copy.deepcopy(hand)
    for idx in range(len(joker_hand)):
        if joker_hand[idx][0] == '?':
            joker_hand[idx] = card

    return joker_hand


def wild_hands(hand):
    """Возвращает список из всех возможных вариантов "руки" при замене джокера"""

    if '?B' in hand and '?R' in hand:
        hand_combination = [replace_two_joker(hand, black, red) for black in black_joker_cards
                            for red in red_joker_cards if black not in hand and red not in hand]
    elif '?R' in hand:
        hand_combination = [replace_one_joker(hand, card) for card in red_joker_cards if card not in hand]
    elif '?B' in hand:
        hand_combination = [replace_one_joker(hand, card) for card in black_joker_cards if card not in hand]
    else:
        hand_combination = [hand]

    return hand_combination


def best_wild_hand(hand):
    """best_hand но с джокерами"""

    all_combinations = []
    for combo in wild_hands(hand):
        all_combinations.extend(itertools.combinations(combo, 5))

    return max(all_combinations, key=hand_rank)


def test_best_hand():
    print("test_best_hand...")
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('Done')


def test_best_wild_hand():
    print("test_best_wild_hand...")
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('Done')


if __name__ == '__main__':
    test_best_hand()
    test_best_wild_hand()
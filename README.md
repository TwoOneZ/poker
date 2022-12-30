# poker
Реализована функция best_hand, которая принимает на вход покерную "руку" (hand) из 7ми карт и возвращает лучшую (относительно значения, возвращаемого hand_rank) "руку" из 5ти карт.

У каждой карты есть масть(suit) и ранг(rank)

Масти: трефы (clubs, C), пики (spades, S), червы (hearts, H), бубны (diamonds, D)

Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)

Пример работы:

Входные данные: "6C 7C 8C 9C TC 5C JS"
Реализована функция best_wild_hand, которая принимает на вход покерную "руку" (hand) из 7ми карт и возвращает лучшую (относительно значения, возвращаемого hand_rank) "руку" из 5ти карт. Кроме прочего в данном варианте "рука" может включать джокера.

Джокеры могут заменить карту любой масти и ранга того же цвета, в колоде два джокера. Черный джокер '?B' может быт использован в качестве треф или пик любого ранга, красный джокер '?R' - в качестве черв и бубен любого ранга.

Пример работы:

Входные данные: "TD TC 5H 5C 7C ?R ?B"

print(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
Результат:

('TD', 'TC', '7C', 'TH', 'TS')
Прохождение тестов
Тесты:

def test_best_hand():
    print("test_best_hand...")
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


def test_best_wild_hand():
    print("test_best_wild_hand...")
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')
Результаты:

test_best_hand...
OK
test_best_wild_hand...
OK

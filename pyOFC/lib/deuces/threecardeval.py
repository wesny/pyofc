from card import Card

STR_RANKS = '23456789TJQKA'

def _find_straight(prev, next):
    if prev == 5:
        return 5
    else:
        return prev + 1 if next != 0 else 0

def make_straight(cardsUsed, rank):
    newCards = cardsUsed[:]
    newCards.insert(0, cardsUsed[12])
    newCards[rank+1] = 1
    return 5 == reduce(lambda prev, next: _find_straight(prev, next), newCards)

# Allows Deuces to evaluate 3 card hands
def fill_hand(hand):
    cardsUsed = [0 for i in xrange(13)]
    for card in hand:
        cardsUsed[Card.get_rank_int(card)] = 1
    toFill = 2
    for i in xrange(13):
        if toFill == 0:
            break
        if cardsUsed[i] == 0 and not make_straight(cardsUsed, i):
            cardsUsed[i] = 2
            toFill -= 1
    new_hand = hand[:]
    suit = ['s', 'd']
    for i in xrange(13):
        if cardsUsed[i] == 2:
            card_string = STR_RANKS[i] + suit[0]
            suit = suit[1:]
            new_hand.append(Card.new(card_string))
    return new_hand

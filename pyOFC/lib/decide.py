from random import sample
from ofc_hand import Hand
from lib.deuces import Deck, Card
import itertools
import time

SUIT_MAP = {
    1:0,
    2:1,
    4:2,
    8:3
}

# Represents a possible hand placement that can be simulated
class Possible_Hand:

    def __init__(self, game, cards_to_place, order_to_place):
        self.hand = Hand('')
        self.hand.top = game.computer_hand.top[:]
        self.hand.middle = game.computer_hand.middle[:]
        self.hand.bottom = game.computer_hand.bottom[:]
        self.order_to_place = order_to_place
        for i in xrange(len(cards_to_place)):
            self.hand.add_card(cards_to_place[i], order_to_place[i])
        self.rating = -1
        self.times_run = 0
        self.deck = Deck()
        self.deck.cards = game.deck.cards[:]

    def run_hand(self):
        run_hand = Hand('')
        run_hand.top = self.hand.top[:]
        run_hand.middle = self.hand.middle[:]
        run_hand.bottom = self.hand.bottom[:]
        top_len = len(run_hand.top)
        mid_len = len(run_hand.middle)
        bot_len = len(run_hand.bottom)
        card_samp = sample(self.deck.cards, 13-top_len-mid_len-bot_len)
        run_hand.top.extend(card_samp[:3-top_len])
        run_hand.middle.extend(card_samp[3-top_len:3-top_len+5-mid_len])
        run_hand.bottom.extend(card_samp[3-top_len+5-mid_len:3-top_len+5-mid_len+5-bot_len])
        ev = run_hand.evaluate_hand()
        if self.times_run == 0:
            self.rating = ev
        else:
            self.rating = int((self.rating * self.times_run + ev) / self.times_run + 1)
        self.times_run += 1

# Decides where to place cards given, using Monte Carlo Simulations
def place_cards(game, cards_to_place, fivecardtime=5, onecardtime=3, explain=False):
    possible_hands = []
    possible_placements = []
    if len(game.computer_hand.top) < 3:
        possible_placements.append(0)
    if len(game.computer_hand.middle) < 5:
        possible_placements.append(1)
    if len(game.computer_hand.bottom) < 5:
        possible_placements.append(2)
    if len(possible_placements) == 1:
        explanation = ''
        if explain:
            explanation = "There is only one possible placement remaining."
        return possible_placements, explanation
    if len(cards_to_place) == 5:
        pairs = [[] for _ in xrange(13)]
        flushes = [[] for _ in xrange(4)]
        flush_place = []
        pair_place = []
        for i in xrange(5):
            suit_int = SUIT_MAP[Card.get_suit_int(cards_to_place[i])]
            rank_int = Card.get_rank_int(cards_to_place[i])
            pairs[rank_int].append(i)
            flushes[suit_int].append(i)
        for suit in flushes:
            if len(suit) >= 4:
                flush_place = suit
                break
        if flush_place == []:
            for val in pairs:
                if len(val) >= 2:
                    pair_place.append(val)
    for p in itertools.product(possible_placements, repeat=len(cards_to_place)):
        to_append = True
        if len(cards_to_place) == 5:
            if flush_place != []:
                placement = p[flush_place[0]]
                for place in flush_place:
                    if p[place] != placement:
                        to_append = False
                        break
            elif pair_place != []:
                for pair in pair_place:
                    placement = p[pair[0]]
                    for place in pair:
                        if p[place] != placement:
                            to_append = False
                            break
        if to_append and p.count(0) < 4:
            possible_hands.append(Possible_Hand(game, cards_to_place, p))
    start = time.time()
    max_time = fivecardtime if len(cards_to_place) == 5 else onecardtime
    num_sims = 0
    while(time.time() - start < max_time):
        for hand in possible_hands:
            hand.run_hand()
        num_sims += 1
    best_order_to_place = possible_hands[0].order_to_place
    best_rating = possible_hands[0].rating
    next_best_rating = possible_hands[1].rating
    for hand in possible_hands:
        if hand.rating < best_rating:
            next_best_rating = best_rating
            best_rating = hand.rating
            best_order_to_place = hand.order_to_place
    explanation = ''
    if explain:
        explanation = 'After %d Monte Carlo simulations of %d possible hands, this configuration was chosen with an average hand strength of %d with the next best of %d (lower is better).' % (num_sims, len(possible_hands), best_rating, next_best_rating)
    return best_order_to_place, explanation

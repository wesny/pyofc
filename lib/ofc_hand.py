#!/usr/bin/env python

from lib.deuces import Card, Evaluator

evaluator = Evaluator()

class Hand:

    def __init__(self, player_name):
        self.player_name = player_name
        self.top = []
        self.middle = []
        self.bottom = []

    def add_card(self, card, hand_num):
        if hand_num == 0:
            if len(self.top) == 3:
                return False
            self.top.append(card)
        elif hand_num == 1:
            if len(self.middle) == 5:
                return False
            self.middle.append(card)
        elif hand_num == 2:
            if len(self.bottom) == 5:
                return False
            self.bottom.append(card)
        return True

    def clear(self):
        self.top = []
        self.middle = []
        self.bottom = []

    def print_hand(self):
        print self.player_name
        filled_top = self.top[:] + [-1 for i in xrange(3 - len(self.top))]
        filled_middle = self.middle[:] + [-1 for i in xrange(5 - len(self.middle))]
        filled_bottom = self.bottom[:] + [-1 for i in xrange(5 - len(self.bottom))]
        Card.print_pretty_cards(filled_top)
        Card.print_pretty_cards(filled_middle)
        Card.print_pretty_cards(filled_bottom)

    def evaluate_hand(self):
        top_count = evaluator.evaluate([], self.top)
        middle_count = evaluator.evaluate([], self.middle)
        bottom_count = evaluator.evaluate([], self.bottom)
        if not (top_count >= middle_count >= bottom_count):
            return 7463*3
        else:
            return top_count + middle_count + bottom_count

def return_hand_vals(computer_hand, player_hand):
    c_top = evaluator.evaluate([], computer_hand.top)
    c_middle = evaluator.evaluate([], computer_hand.middle)
    c_bottom = evaluator.evaluate([], computer_hand.bottom)
    p_top = evaluator.evaluate([], player_hand.top)
    p_middle = evaluator.evaluate([], player_hand.middle)
    p_bottom = evaluator.evaluate([], player_hand.bottom)
    return c_top, c_middle, c_bottom, p_top, p_middle, p_bottom

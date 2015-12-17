from lib.deuces import Card, Deck, Evaluator
from lib.decide import place_cards
from lib.ofc_hand import Hand
from lib.deuces.termcolor import colored
import os
import argparse

evaluator = Evaluator()

class Game:

    def __init__(self):
        self.computer_hand = Hand("Computer")
        self.player_hand = Hand("Player")
        self.score = 0
        self.num_hands = 0
        self.deck = Deck()
        self.explanation = ''

    def _run_x_cards(self, num_cards):
        if self.num_hands % 2 == 0:
            self._player_play(num_cards)
            self._comp_play(num_cards)
        else:
            self._comp_play(num_cards)
            self._player_play(num_cards)


    def _player_play(self, num_cards):
        message = ''
        five_cards = self.deck.draw(num_cards)
        cards_to_play = five_cards[:]
        while (not cards_to_play == []):
            inp = ''
            while inp not in ['1', '2','3', 'x']:
                self.print_screen()
                if message != '':
                    print colored(message, "red")
                Card.print_pretty_cards(cards_to_play)
                print "^^^^^^^^"
                inp = raw_input("Where would you like to place this card? (1, 2, 3 | x to reset): ")
                if inp not in ['1', '2','3', 'x']:
                    message = "Input was not the list 1, 2, 3, x"
            if inp == 'x':
                self.player_hand.top = [x for x in self.player_hand.top if x not in five_cards]
                self.player_hand.middle = [x for x in self.player_hand.middle if x not in five_cards]
                self.player_hand.bottom = [x for x in self.player_hand.bottom if x not in five_cards]
                cards_to_play = five_cards[:]
            else:
                if not self.player_hand.add_card(cards_to_play[0], int(inp)-1):
                    message = "Hand is full. Pick a different hand."
                else:
                    cards_to_play = cards_to_play[1:]
                    message = ''
            if cards_to_play == []:
                self.print_screen()
                inp = raw_input("Confirm and end turn? (y/n): ")
                if inp not in 'Yy':
                    self.player_hand.top = [x for x in self.player_hand.top if x not in five_cards]
                    self.player_hand.middle = [x for x in self.player_hand.middle if x not in five_cards]
                    self.player_hand.bottom = [x for x in self.player_hand.bottom if x not in five_cards]
                    cards_to_play = five_cards[:]

    def _comp_play(self, num_cards):
        five_cards = self.deck.draw(num_cards)
        order, self.explanation = place_cards(self, five_cards, onecardtime=onecardtime, fivecardtime=fivecardtime, explain=explain)
        for i in xrange(len(five_cards)):
            self.computer_hand.add_card(five_cards[i], order[i])

    def run_5_card(self):
        self._run_x_cards(5)

    def run_1_card(self):
        self._run_x_cards(1)

    def evaluate_hands(self):
        player_raw_score = self.player_hand.evaluate_hand()
        computer_raw_score = self.computer_hand.evaluate_hand()
        if player_raw_score == computer_raw_score == 7463*3:
            temp_score = 0
        elif player_raw_score == 7463*3:
            temp_score = -6
            self.score -= 6
        elif computer_raw_score == 7463*3:
            temp_score = 6
            self.score += 6
        else:
            c_top = evaluator.evaluate([], self.computer_hand.top)
            c_middle = evaluator.evaluate([], self.computer_hand.middle)
            c_bottom = evaluator.evaluate([], self.computer_hand.bottom)
            p_top = evaluator.evaluate([], self.player_hand.top)
            p_middle = evaluator.evaluate([], self.player_hand.middle)
            p_bottom = evaluator.evaluate([], self.player_hand.bottom)
            temp_score = 0
            if c_top > p_top:
                temp_score += 1
            elif c_top < p_top:
                temp_score -= 1
            if c_middle > p_middle:
                temp_score += 1
            elif c_middle < p_middle:
                temp_score -= 1
            if c_bottom > p_bottom:
                temp_score += 1
            elif c_bottom < p_bottom:
                temp_score -= 1
            if abs(temp_score) == 3:
                temp_score *= 2
            self.score += temp_score
        self.print_screen()
        message = ''
        if temp_score == 0:
            message = "You both busted!"
        elif temp_score == -6:
            message = 'You busted or were scooped!'
        elif temp_score == 6:
            message = 'You scooped or your opponent busted!'
        else:
            message = 'You scored %d points on this hand' % (temp_score)
        print message
        inp = ''
        while (inp not in ["Y","y","N","n"]):
            inp = raw_input("Would you like to play another hand? (y/n): ")
            if (inp in ["N","n"]):
                exit(0)
        self.explanation = ''
        self.num_hands += 1
        self.computer_hand.clear()
        self.player_hand.clear()
        self.deck.shuffle()

    def print_screen(self):
        os.system('clear')
        if self.explanation != '':
            print self.explanation
        name_spacing = "                                                       "
        if self.score == 0:
            player_score = " (" + str(self.score) + ")"
            computer_score = " (" + str(self.score) + ")"
            cps_len = len(" (" + str(self.score) + ")")
        elif self.score > 0:
            player_score = colored(" (+" + str(self.score) + ")", 'green')
            computer_score = colored(" (-" + str(self.score) + ")", 'red')
            cps_len = len(" (-" + str(self.score) + ")")
        else:
            player_score = colored(" (" + str(self.score) + ")", 'red')
            computer_score = colored(" (+" + str(-self.score) + ")", 'green')
            cps_len = len(" (+" + str(-self.score) + ")")
        print colored(self.computer_hand.player_name, attrs=['bold']) + computer_score + name_spacing[len(self.computer_hand.player_name) + cps_len:] + colored(self.player_hand.player_name, attrs=['bold']) + player_score
        filled_top_computer = self.computer_hand.top[:] + [-1 for i in xrange(3 - len(self.computer_hand.top))]
        filled_middle_computer = self.computer_hand.middle[:] + [-1 for i in xrange(5 - len(self.computer_hand.middle))]
        filled_bottom_computer = self.computer_hand.bottom[:] + [-1 for i in xrange(5 - len(self.computer_hand.bottom))]
        filled_top_player = self.player_hand.top[:] + [-1 for i in xrange(3 - len(self.player_hand.top))]
        filled_middle_player = self.player_hand.middle[:] + [-1 for i in xrange(5 - len(self.player_hand.middle))]
        filled_bottom_player = self.player_hand.bottom[:] + [-1 for i in xrange(5 - len(self.player_hand.bottom))]
        hand_pairs = [(filled_top_computer, filled_top_player), (filled_middle_computer, filled_middle_player), (filled_bottom_computer, filled_bottom_player)]
        hand_num = 1
        for hand in hand_pairs:
            spacing = "                             " if hand_num == 1 else "           "
            for i in xrange(6):
                print Card.return_pretty_cards_line(hand[0], i) + spacing + Card.return_pretty_cards_line(hand[1], i) + ("".join([" " for _ in xrange(20)]) if hand_num == 0 else "  ") + (colored(str(hand_num), "blue") if i == 2 else " ")
            hand_num += 1
        print "".join(["_" for i in xrange(99)])
            

def play():
    game = Game()
    while(1):
        game.run_5_card()
        for _ in xrange(8):
            game.run_1_card()
        game.evaluate_hands()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play Open Face Chinese Poker')
    parser.add_argument('--fivecardtime', '-f', type=int, default=5, help='# of seconds used for computer to place initial cards (Default: 5)')
    parser.add_argument('--onecardtime', '-o', type=int, default=3, help='# of seconds used for computer to place subsequent cards (Default: 3)')
    parser.add_argument("-e", "--explain", action="store_true", help="Print explanation")
    args = parser.parse_args()
    fivecardtime = args.fivecardtime
    onecardtime = args.onecardtime
    explain = args.explain
    play()

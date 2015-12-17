from lib.deuces import Card, Evaluator
from ofc_hand import Hand

board = [
        Card.new('2d'),
        Card.new('Kd'),
        Card.new('Jd')
    ]
board2 = [
        Card.new('2h'),
        Card.new('3h'),
        Card.new('4h')
        #Card.new('5h'),
        #Card.new('7d')
    ]

# h = Hand("Hand")
# h.add_card(Card.new('2h'), 0)
# h.add_card(Card.new('Kh'), 0)
# h.add_card(Card.new('2h'), 1)
# h.add_card(Card.new('Kh'), 1)
# h.add_card(Card.new('2h'), 2)
# h.add_card(Card.new('Kh'), 2)
# h.print_hand()

evaluator = Evaluator()
# print evaluator.evaluate(board, [])
print evaluator.evaluate(board2, [])
print u"\u2663".encode('utf-8')
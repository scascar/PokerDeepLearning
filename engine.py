# Simple engine for heads up
from treys import Card, Evaluator, Deck
from constants import Actions, Street
import operator


class Engine:
    def __init__(self, starting_stack=500, big_blind=20, small_blind=10):
        self.starting_stack = starting_stack
        self.big_blind = big_blind
        self.small_blind = small_blind
        self.deck = Deck()

    def new_hand(self):
        print("=============   NEW HAND   ================")
        self.deck = Deck()
        self.sb_cards = self.deck.draw(2)
        self.bb_cards = self.deck.draw(2)
        self.community_cards = self.deck.draw(5)
        self.pot = [0, 0]
        self.street_actions = [self.small_blind, self.big_blind]
        self.current_raise = self.big_blind
        self.turn = 0
        self.current_street = Street.PREFLOP
        self.winner = -1
        print('NEW STREET ====== ', str(self.current_street))

    def get_call_value(self):
        return abs(int(self.street_actions[0] - self.street_actions[1]))

    def get_bet_range(self):
        if self.street_actions == [self.small_blind, self.big_blind]:
            return [2*self.big_blind, self.starting_stack]
        elif self.street_actions == [0, 0]:
            return [self.big_blind, self.starting_stack - self.pot[self.turn] - self.street_actions[self.turn]]
        else:
            return [self.current_raise*2, self.starting_stack - self.pot[self.turn] - self.street_actions[self.turn]]

    def is_sb_turn(self):
        # new street
        if self.turn == 0:
            print('Small Blind to play')
            return True
        else:
            print('Big Blind to play')
            return False

    def play_action(self, action, amount):
        if self.winner == -1:
            if action == Actions.FOLD:
                print('folding')
                self.current_street = Street.FINISHED
                self.winner = (self.turn+1) % 2
                self.pot = list(
                    map(operator.add, self.pot, self.street_actions))
            elif action == Actions.CALL:
                check = False
                if self.street_actions == [0, 0]:
                    check = True
                    print("checking")
                else:
                    print("calling")
                    self.street_actions[self.turn] = max(self.street_actions)
                    self.pot = list(
                        map(operator.add, self.pot, self.street_actions))
                    print(self.street_actions)

                self.turn = (self.turn+1) % 2

                if check == False or self.turn == 1:
                    if self.current_street == Street.RIVER:
                        self.current_street == Street.FINISHED
                        self.winner = self.eval_winner()

                    else:
                        self.current_street = Street(
                            self.current_street.value + 1)
                        self.turn = 1
                        self.current_raise = 0
                        self.street_actions = [0, 0]

                        print('NEW STREET ====== ', str(self.current_street))
                print('pot:', str(self.pot))

            elif action == Actions.BET:

                self.current_raise = amount
                self.street_actions[self.turn] += amount
                print('raising to ', str(self.street_actions[self.turn]))
                self.turn = (self.turn+1) % 2
        else:
            print('HAND FINISHED, WINNER IS: ', str(self.winner))

    def eval_winner(self):
        eval = Evaluator()
        if eval.evaluate(self.sb_cards, self.community_cards) < eval.evaluate(self.bb_cards, self.community_cards):
            return 0
        else:
            return 1

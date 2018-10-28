# Simple engine for heads up
from treys import Card, Evaluator, Deck
from enum import Enum
import operator


class street(Enum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    FINISHED = 4


class actions(Enum):
    FOLD = 0
    CALL = 1
    BET = 2


class Engine:
    def __init__(self, starting_stack=500, big_blind=20, small_blind=10):
        self.starting_stack = starting_stack
        self.big_blind = big_blind
        self.small_blind = small_blind
        self.deck = Deck()

    def new_hand(self):
        self.deck = Deck()
        self.sb_cards = self.deck.draw(2)
        self.bb_cards = self.deck.draw(2)
        self.community_cards = self.deck.draw(5)
        self.pot = [0, 0]
        self.street_actions = [self.small_blind, self.big_blind]
        self.current_raise = self.big_blind
        self.turn = 0
        self.current_street = street.PREFLOP
        self.winner = -1

    def get_call_value(self):
        return abs(self.street_actions[0] - self.street_actions[1])

    def get_bet_range(self):
        if self.street_actions == [self.small_blind, self.big_blind]:
            return [2*self.big_blind, self.starting_stack]
        elif self.street_actions == [0, 0]:
            return [self.big_blind, self.starting_stack - self.pot[self.turn] - self.street_actions[self.turn]]

    def is_sb_turn(self):
        # new street
        if self.current_street is not street.PREFLOP and self.street_actions == [-1, -1]:
            return False
        elif self.turn == 0:
            return True
        else:
            return False

    def play_action(self, action, amount):
        if action == action.FOLD:
            self.current_street == street.FINISHED
            self.winner = (self.turn+1) % 2
            self.pot = map(operator.add, self.pot, self.street_actions)
        elif action == actions.CALL:
            if self.current_street == street.RIVER:
                self.current_street == street.FINISHED
                self.winner = self.eval_winner()
                self.pot = map(operator.add, self.pot, self.street_actions)

            else:
                self.current_street += 1
                self.turn = 1
                self.current_raise = 0

        elif action == actions.BET:
            self.current_raise
            self.street_actions[self.turn] += amount
            self.turn = (self.turn+1) % 2

    def eval_winner(self):
        eval = Evaluator()
        if eval.evluate(self.sb_cards, self.community_cards) < eval.evaluate(self.bb_cards, self.community_cards):
            return 0
        else:
            return 1

import numpy as np
from pypokerengine.utils.card_utils import estimate_hole_card_win_rate


# Big ugly wrapper for all poker related functions
class PokerUtils:

    def __init__(self):
        self.suits = {'H': 0,
                      'C': 1,
                      'S': 2,
                      'D': 3}

        self.indexes = {
            '2': 0,
            '3': 1,
            '4': 2,
            '5': 3,
            '6': 4,
            '7': 5,
            '8': 6,
            '9': 7,
            'T': 8,
            'J': 9,
            'Q': 10,
            'K': 11,
            'A': 12

        }

    def get_suit(self, card):
        return self.suits.get(card[0], 0)

    def get_card_value_index(self, card):
        return self.indexes.get(card[1], 0)

    def get_card_total_index(self, card):
        return (self.get_suit(card)+1)*(self.get_card_value_index(card)+1) - 1

    def get_street_values(self, cards):
        street = np.zeros(52)
        for card in cards:
            street[self.get_card_total_index(card)] = 1

    def is_suited(self, cards):
        if self.get_suit(cards[0]) == self.get_suit(cards[1]):
            return True
        else:
            return False

    def is_pocket(self, cards):
        if self.get_card_value_index(cards[0]) == self.get_card_value_index(cards[1]):
            return True
        else:
            return False

    def is_connector(self, cards):
        diff = abs(self.get_card_value_index(
            cards[0]) - self.get_card_value_index(cards[1]))
        if diff == 1 or diff == 12:
            return True
        else:
            return False

    def is_one_gapper(self, cards):
        diff = abs(self.get_card_value_index(
            cards[0]) - self.get_card_value_index(cards[1]))
        # missing A3 but who cares
        if diff == 2:
            return True
        else:
            return False

    def two_broadways(self, cards):
        minimal_card = min(self.get_card_value_index(
            cards[0]), self.get_card_value_index(cards[1]))
        if minimal_card >= 8:
            return True
        else:
            return False

    def highest_card(self, cards):
        return max(self.get_card_value_index(cards[0]), self.get_card_value_index(cards[1]))

    def has_low_card(self, cards):
        minimal_card = min(self.get_card_value_index(
            cards[0]), self.get_card_value_index(cards[1]))
        if minimal_card < 5:
            return True
        else:
            return False

    def flop_is_monotone(self, cards):
        if self.get_suit(cards[0]) == self.get_suit(cards[1]) and self.get_suit(cards[1]) == self.get_suit(cards[2]):
            return True
        else:
            return False

    def flop_is_two_suited(self, cards):
        if self.flop_is_monotone(cards):
            return False
        if self.get_suit(cards[0]) == self.get_suit(cards[1]) or self.get_suit(cards[1]) == self.get_suit(cards[2]) or self.get_suit(cards[0]) == self.get_suit(cards[2]):
            return True
        else:
            return False

    def hand_strength_estimation(self, nb_sim, cards, community):
        return estimate_hole_card_win_rate(nb_simulation=nb_sim, nb_player=2, hole_card=cards, community_card=community)

        # action history : round_state["action_histories"][street]

    def get_street_actions(self, eff_stack, action_history):
        # only the first 3 actions per player. There is no sense in 7 betting
        actions = np.zeros(6)
        for i in range(min(6, len(action_history))):
            actions[i] = action_history[i]['amount'] / eff_stack
        return actions

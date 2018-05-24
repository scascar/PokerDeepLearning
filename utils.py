import numpy as np


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

    # action history : round_state["action_histories"][street]
    def get_street_actions(self, eff_stack, action_history):
        # only the first 3 actions per player. There is no sense in 7 betting
        actions = np.zeros(6)
        for i in range(min(6, len(action_history))):
            actions[i] = action_history[i]['amount'] / eff_stack
        return actions

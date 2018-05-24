from pypokerengine.api.emulator import Emulator
from utils import PokerUtils
import numpy as np


class CustomEmulator:

    def __init__(self, starting_stack, small_blind):
        self.pok = PokerUtils()
        self.starting_stack = 500
        self.small_blind = 10
        self.emulator = Emulator()
        self.emulator.set_game_rule(
            player_num=2, max_round=10, small_blind_amount=small_blind, ante_amount=0)

        self.players_info = {
            "bb_player": {"name": "bb_player", "stack": starting_stack},
            "sb_player": {"name": "sb_player", "stack": starting_stack},
        }

        self.initial_game_state = self.emulator.generate_initial_game_state(
            self.players_info)

        self.street = 'preflop'
        self.events = []
        self.game_state = []

        self.players_cards = [np.zeros(52), np.zeros(52)]
        self.cards_feature = [np.zeros(52), np.zeros(52), np.zeros(52)]

        self.actions_feature = [np.zeros(6), np.zeros(
            6), np.zeros(6), np.zeros(6)]

    def is_round_finished(self):
        for e in self.events:
            if(e['type'] == 'event_round_finish'):
                return True
        return False

    def new_street(self):
        for e in self.events:
            if(e['type'] == 'event_new_street'):
                self.street = e['street']
                return self.street
        return False

    def make_cards_feature(self):
        if(self.street == 'preflop'):
            for i in range(2):
                self.players_cards[i][self.pok.get_card_total_index(
                    self.game_state['table'].seats.players[i].hole_card[0].__str__())] = 1
                self.players_cards[i][self.pok.get_card_total_index(
                    self.game_state['table'].seats.players[i].hole_card[1].__str__())] = 1
        elif(self.street == 'flop'):
            for card in self.events[0]['round_state']['community_card']:
                self.cards_feature[0][self.pok.get_card_total_index(card)] = 1
        elif(self.street == 'turn'):
            self.cards_feature[1][self.pok.get_card_total_index(
                self.events[0]['round_state']['community_card'][3])] = 1
        elif(self.street == 'river'):
            self.cards_feature[2][self.pok.get_card_total_index(
                self.events[0]['round_state']['community_card'][4])] = 1

    def make_actions_feature(self):
        if(self.street == 'preflop'):
            self.actions_feature[0] = self.pok.get_street_actions(
                self.starting_stack, self.events[0]['round_state']['action_histories']['preflop'])
        elif(self.street == 'flop'):
            self.actions_feature[1] = self.pok.get_street_actions(
                self.starting_stack, self.events[0]['round_state']['action_histories']['flop'])
        elif(self.street == 'turn'):
            self.actions_feature[2] = self.pok.get_street_actions(
                self.starting_stack, self.events[0]['round_state']['action_histories']['turn'])
        elif(self.street == 'river'):
            self.actions_feature[3] = self.pok.get_street_actions(
                self.starting_stack, self.events[0]['round_state']['action_histories']['river'])

    def make_features(self):
        # actions are made every street
        self.make_actions_feature()
        if(self.new_street != False):
            self.make_cards_feature()

    def get_minraise_amount(self):
        for e in self.events:
            if(e['type'] == 'event_ask_player'):
                return e['valid_actions'][2]['amount']['min']

    def get_all_in_amount(self):
        for e in self.events:
            if(e['type'] == 'event_ask_player'):
                return e['valid_actions'][2]['amount']['max']

    def get_call_amount(self):
        for e in self.events:
            if(e['type'] == 'event_ask_player'):
                return e['valid_actions'][1]['amount']

    def get_sb_reward(self):
        for e in self.events:
            if(e['type'] == 'event_round_finish'):
                if(e['winners'][0]['uuid'] == 'sb_player'):
                    return (e['winners'][0]['stack'] - self.starting_stack)
                else:
                    return -(e['winners'][0]['stack'] - self.starting_stack)

    def play_action(self, action):
        if(action == 0):
            self.game_state, self.events = self.emulator.apply_action(
                self.game_state, 'fold', 0)
        elif(action == 1):
            self.game_state, self.events = self.emulator.apply_action(
                self.game_state, 'call', self.get_call_amount())
        elif(action == 2):
            self.game_state, self.events = self.emulator.apply_action(
                self.game_state, 'raise', self.get_minraise_amount())
        elif(action == 3):
            self.game_state, self.events = self.emulator.apply_action(
                self.game_state, 'raise', self.get_all_in_amount())

    def new_hand(self):
        self.initial_game_state = self.emulator.generate_initial_game_state(
            self.players_info)

        self.street = 'preflop'

        self.game_state, self.events = self.emulator.start_new_round(
            self.initial_game_state)

        self.players_cards = [np.zeros(52), np.zeros(52)]
        self.cards_feature = [np.zeros(52), np.zeros(52), np.zeros(52)]

        self.actions_feature = [np.zeros(6), np.zeros(
            6), np.zeros(6), np.zeros(6)]

        self.make_features()

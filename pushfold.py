from pypokerengine.api.emulator import Emulator
from utils import PokerUtils
import numpy as np


class PushFoldEmulator:

    def __init__(self, starting_stack, small_blind):
        self.pok = PokerUtils()
        self.starting_stack = starting_stack
        self.small_blind = 10
        self.emulator = Emulator()
        self.emulator.set_game_rule(
            player_num=2, max_round=10, small_blind_amount=small_blind, ante_amount=0)

        self.hole_cards = {}
        self.players_info = {
            "bb_player": {"name": "bb_player", "stack": starting_stack},
            "sb_player": {"name": "sb_player", "stack": starting_stack},
        }

        self.initial_game_state = self.emulator.generate_initial_game_state(
            self.players_info)

        self.players_cards = [np.zeros(13), np.zeros(13)]
        self.suited = [0, 0]
        self.street = 'preflop'
        self.events = []
        self.game_state = []

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

    def save_cards(self):
        for player in self.game_state['table'].seats.players:
            self.hole_cards[player.uuid] = [card.__str__()
                                            for card in player.hole_card]

    def get_hand_feature(self):
        if(self.street == 'preflop'):
            self.save_cards()
            for i in range(2):
                self.players_cards[i][self.pok.get_card_value_index(
                    self.game_state['table'].seats.players[i].hole_card[0].__str__())] = 1
                self.players_cards[i][self.pok.get_card_value_index(
                    self.game_state['table'].seats.players[i].hole_card[1].__str__())] = 1

                if self.pok.is_suited([self.game_state['table'].seats.players[i].hole_card[0].__str__(), self.game_state['table'].seats.players[i].hole_card[1].__str__()]):
                    self.suited[i] = 1
                else:
                    self.suited[i] = 0

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
            if self.get_all_in_amount() == -1:
                self.game_state, self.events = self.emulator.apply_action(
                    self.game_state, 'call', self.get_call_amount())
            else:
                self.game_state, self.events = self.emulator.apply_action(
                    self.game_state, 'raise', self.get_all_in_amount())

    def new_hand(self, starting_stack):
        self.initial_game_state = self.emulator.generate_initial_game_state(
            self.players_info)

        self.street = 'preflop'
        self.hole_cards = {}
        self.starting_stack = starting_stack
        self.players_info = {
            "bb_player": {"name": "bb_player", "stack": starting_stack},
            "sb_player": {"name": "sb_player", "stack": starting_stack},
        }

        self.initial_game_state = self.emulator.generate_initial_game_state(
            self.players_info)
        self.game_state, self.events = self.emulator.start_new_round(
            self.initial_game_state)

        self.players_cards = [np.zeros(13), np.zeros(13)]

        self.get_hand_feature()

    def get_action_histories_text(self, hole_cards=False):
        if(hole_cards == True):
            print(self.hole_cards)

        histo = self.events[0]['round_state']['action_histories']
        hand_text = ""
        for k, v in histo.items():
            if(len(v) > 0):
                hand_text += k+'\n'
                for a in v:
                    if(a['action'] == 'RAISE'):
                        hand_text += a['uuid'] + \
                            ' raises to ' + str(a['amount']) + '\n'
                    elif(a['action'] == 'FOLD'):
                        hand_text += a['uuid'] + ' folds\n'
                    elif(a['action'] == 'CALL' and a['amount'] == 0):
                        hand_text += a['uuid'] + ' checks\n'
                    else:
                        hand_text += a['uuid'] + ' ' + \
                            a['action'] + ' ' + str(a['amount']) + '\n'

        return hand_text

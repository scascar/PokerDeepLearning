from pypokerengine.api.emulator import Emulator


class customEmulator:

    def __init__(self, starting_stack, small_blind):
        self.starting_stack = 500
        self.small_blind = 10
        self.emulator = Emulator()
        self.emulator.set_game_rule(
            player_num=2, max_round=10, small_blind_amount=small_blind, ante_amount=0)

        self.players_info = {
            "sb_player": {"name": "sb_player", "stack": starting_stack},
            "bb_player": {"name": "bb_player", "stack": starting_stack},
        }

        self.initial_game_state = self.emulator.generate_initial_game_state(
            self.players_info)

        self.events = []

    def is_round_finished(self):
        for e in self.events:
            if(e['type'] == 'event_round_finish'):
                return True
        return False

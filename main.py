

from utils import PokerUtils
from engine import Engine
from constants import Actions

e = Engine()
e.new_hand()
e.is_sb_turn()
e.play_action(Actions.BET, 100)
e.is_sb_turn()
print('to call: ', str(e.get_call_value()))
print('bet range: ', str(e.get_bet_range()))
e.play_action(Actions.BET, e.get_bet_range()[0])
e.is_sb_turn()
e.play_action(Actions.CALL, 0)
e.is_sb_turn()
e.play_action(Actions.CALL, 0)
e.is_sb_turn()
e.play_action(Actions.CALL, 0)

print('bet range: ', str(e.get_bet_range()))
e.is_sb_turn()
e.play_action(Actions.BET, e.get_bet_range()[0])
e.is_sb_turn()
e.play_action(Actions.CALL, 0)
e.is_sb_turn()
e.play_action(Actions.CALL, 0)
e.is_sb_turn()
e.play_action(Actions.CALL, 0)
e.is_sb_turn()
e.play_action(Actions.CALL, 0)

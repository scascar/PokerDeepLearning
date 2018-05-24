from utils import PokerUtils
from emulator import CustomEmulator
import numpy as np

emul = CustomEmulator(500, 10)
emul.new_hand()
sb_feat = np.concatenate([emul.players_cards[0], np.concatenate(
    emul.cards_feature), np.concatenate(emul.actions_feature)])
print(sb_feat.shape)

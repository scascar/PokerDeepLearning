from utils import pokerUtils

pok = pokerUtils()

print(pok.get_card_total_index('DA'))

print(pok.get_street_actions(100, [{'action': 'SMALLBLIND', 'uuid': 'sb_player', 'amount': 10, 'add_amount': 10}, {'action': 'BIGBLIND', 'uuid': 'bb_player', 'amount': 20, 'add_amount': 10}, {
      'action': 'RAISE', 'uuid': 'sb_player', 'amount': 100, 'add_amount': 80, 'paid': 90}, {'action': 'CALL', 'uuid': 'bb_player', 'amount': 100, 'paid': 80}]))

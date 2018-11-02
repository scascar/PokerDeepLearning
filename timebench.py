from engine import Engine

en = Engine()

for i in range(1000):
    if i % 100 == 0:
        print(str(i/10), "%")
    en.new_hand()
    while en.winner == -1:

        en.play(3)

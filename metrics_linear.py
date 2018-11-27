import numpy as np

# very unoptimized code. But we have fast cpus nowadays :)


def compute_nash_pusher(model):
    matrix = np.zeros((13, 13))

    print("computing pusher")
    print("\tpocket pairs")
    # pocket pairs
    for i in range(13):
        cards = np.zeros(2)
        cards[0] = (12-i)/12
        cards[1] = (12-i)/12
        suited = 0
        sb = 1
        starting_stack_bb = 20
        push = 0
        while push == 0:
            feat = np.concatenate(
                [cards, np.array([suited, sb, starting_stack_bb*20/400])]).reshape((1, 5))
            pred = model.predict(feat)
            push = np.argmax(pred)
            if push == 0:
                starting_stack_bb -= 0.1
                if starting_stack_bb < 1:
                    push = 1
            else:
                matrix[i][i] = starting_stack_bb

    print("\tsuited cards")
    # suited
    for i in range(13):
        for j in range(13):
            # not pocket pairs
            if j != i:
                cards = np.zeros(2)
                cards[0] = (12-i)/12
                cards[1] = (12-j)/12
                suited = 1
                sb = 1
                starting_stack_bb = 20
                push = 0
                while push == 0:
                    feat = np.concatenate(
                        [cards, np.array([suited, sb, starting_stack_bb*20/400])]).reshape((1, 5))
                    pred = model.predict(feat)
                    push = np.argmax(pred)
                    if push == 0:
                        starting_stack_bb -= 0.1
                    if starting_stack_bb < 1:
                        push = 1
                    else:
                        if j > i:
                            matrix[i][j] = starting_stack_bb
                        else:
                            matrix[j][i] = starting_stack_bb

    print("\toffsuit cards")
    # offsuit
    for i in range(13):
        for j in range(13):
            # not pocket pairs
            if j != i:
                cards = np.zeros(2)
                cards[0] = (12-i)/12
                cards[1] = (12-j)/12
                suited = 0
                sb = 1
                starting_stack_bb = 20
                push = 0
                while push == 0:
                    feat = np.concatenate(
                        [cards, np.array([suited, sb, starting_stack_bb*20/400])]).reshape((1, 5))

                    pred = model.predict(feat)
                    push = np.argmax(pred)
                    if push == 0:
                        starting_stack_bb -= 0.1
                    if starting_stack_bb < 1:
                        push = 1
                    else:
                        if j < i:
                            matrix[i][j] = starting_stack_bb
                        else:
                            matrix[j][i] = starting_stack_bb

    return matrix


def compute_nash_caller(model):
    print("Computing caller range")
    print("\tpocket pairs")
    matrix = np.zeros((13, 13))

    # pocket pairs
    for i in range(13):
        cards = np.zeros(2)
        cards[0] = (12-i)/12
        cards[1] = (12-i)/12
        suited = 0
        sb = 0
        starting_stack_bb = 20
        push = 0
        while push == 0:
            feat = np.concatenate(
                [cards, np.array([suited, sb, starting_stack_bb*20/400])]).reshape((1, 5))
            pred = model.predict(feat)
            push = np.argmax(pred)
            if push == 0:
                starting_stack_bb -= 0.1
                if starting_stack_bb < 1:
                    push = 1
            else:
                matrix[i][i] = starting_stack_bb

    print("\tsuited cards")
    # suited
    for i in range(13):
        for j in range(13):
            # not pocket pairs
            if j != i:
                cards = np.zeros(2)
                cards[0] = (12-i)/12
                cards[1] = (12-j)/12
                suited = 1
                sb = 0
                starting_stack_bb = 20
                push = 0
                while push == 0:
                    feat = np.concatenate(
                        [cards, np.array([suited, sb, starting_stack_bb*20/400])]).reshape((1, 5))
                    pred = model.predict(feat)
                    push = np.argmax(pred)
                    if push == 0:
                        starting_stack_bb -= 0.1
                    if starting_stack_bb < 1:
                        push = 1
                    else:
                        if j > i:
                            matrix[i][j] = starting_stack_bb
                        else:
                            matrix[j][i] = starting_stack_bb

    # offsuit
    print("\toffsuit cards")
    for i in range(13):
        for j in range(13):
            # not pocket pairs
            if j != i:
                cards = np.zeros(2)
                cards[0] = (12-i)/12
                cards[1] = (12-j)/12
                suited = 0
                sb = 0
                starting_stack_bb = 20
                push = 0
                while push == 0:
                    feat = np.concatenate(
                        [cards, np.array([suited, sb, starting_stack_bb*20/400])]).reshape((1, 5))

                    pred = model.predict(feat)
                    push = np.argmax(pred)
                    if push == 0:
                        starting_stack_bb -= 0.1
                    if starting_stack_bb < 1:
                        push = 1
                    else:
                        if j < i:
                            matrix[i][j] = starting_stack_bb
                        else:
                            matrix[j][i] = starting_stack_bb

    return matrix

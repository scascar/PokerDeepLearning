import numpy as np


def compute_nash_pusher(model):
    matrix = np.zeros((13, 13))

    # pocket pairs
    for i in range(13):
        cards = np.zeros(13)
        cards[12-i] = 1
        suited = 0
        sb = 1
        starting_stack_bb = 20
        push = 0
        while push == 0:
            feat = np.concatenate(
                [cards, np.array([suited, sb, starting_stack_bb*20/400])]).reshape((1, 16))
            pred = model.predict(feat)
            push = np.argmax(pred)
            if push == 0:
                starting_stack_bb -= 0.1
                if starting_stack_bb < 1:
                    push = 1
            else:
                matrix[i][i] = starting_stack_bb

    # suited
    for i in range(13):
        for j in range(13):
            # not pocket pairs
            if j != i:
                cards = np.zeros(13)
                cards[12-i] = 1
                cards[12-j] = 1
                suited = 1
                sb = 1
                starting_stack_bb = 20
                push = 0
                while push == 0:
                    feat = np.concatenate(
                        [cards, np.array([suited, sb, starting_stack_bb*20/400])]).reshape((1, 16))
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
    for i in range(13):
        for j in range(13):
            # not pocket pairs
            if j != i:
                cards = np.zeros(13)
                cards[12-i] = 1
                cards[12-j] = 1
                suited = 0
                sb = 1
                starting_stack_bb = 20
                push = 0
                while push == 0:
                    feat = np.concatenate(
                        [cards, np.array([suited, sb, starting_stack_bb*20/400])]).reshape((1, 16))

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
    matrix = np.zeros((13, 13))

    # pocket pairs
    for i in range(13):
        cards = np.zeros(13)
        cards[12-i] = 1
        suited = 0
        sb = 0
        starting_stack_bb = 20
        push = 0
        while push == 0:
            feat = np.concatenate(
                [cards, np.array([suited, sb, starting_stack_bb*20/400])]).reshape((1, 16))
            pred = model.predict(feat)
            push = np.argmax(pred)
            if push == 0:
                starting_stack_bb -= 0.1
                if starting_stack_bb < 1:
                    push = 1
            else:
                matrix[i][i] = starting_stack_bb

    # suited
    for i in range(13):
        for j in range(13):
            # not pocket pairs
            if j != i:
                cards = np.zeros(13)
                cards[12-i] = 1
                cards[12-j] = 1
                suited = 1
                sb = 0
                starting_stack_bb = 20
                push = 0
                while push == 0:
                    feat = np.concatenate(
                        [cards, np.array([suited, sb, starting_stack_bb*20/400])]).reshape((1, 16))
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
    for i in range(13):
        for j in range(13):
            # not pocket pairs
            if j != i:
                cards = np.zeros(13)
                cards[12-i] = 1
                cards[12-j] = 1
                suited = 0
                sb = 0
                starting_stack_bb = 20
                push = 0
                while push == 0:
                    feat = np.concatenate(
                        [cards, np.array([suited, sb, starting_stack_bb*20/400])]).reshape((1, 16))

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

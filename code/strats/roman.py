import random
import numpy as np


def strategy(history, memory):

    if history.shape[1] >= 1:
        cooperation_prob = np.mean(history[1, :])
        choice = np.random.choice(a=[0, 1], p=[1-cooperation_prob, cooperation_prob])

    else:
        choice = 1

    return choice, None
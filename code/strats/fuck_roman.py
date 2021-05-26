
import numpy as np


def strategy(history, strat):
    EXPLOIT = 0
    BE_NICE = 1
    current_round = history.shape[1]
    opponentsActions = history[1]
    myActions = history[0]

    if strat is None:
        strat = "investigate"
    else:
        if strat == "exploit":
            return EXPLOIT, strat
        if strat == "be nice":
            return BE_NICE, strat

    if current_round == 40:
        print("round 40")
        my_cooperation = np.mean(myActions)
        opponent_cooperation = np.mean(opponentsActions)

        my_pre_action = myActions[:-1]
        opp_now_action = opponentsActions[1:]
        if sum(my_pre_action - opp_now_action) == 0:
            return BE_NICE, "be nice"
        revenge_counter = (1 - opp_now_action) - (1 - my_pre_action)
        # 1 = You fuck me for no reason
        # 0 = You fuck me back because I fucked you last turn
        # -1 = I fucked you and you didn't do anything
        if min(revenge_counter) == 0:
            # If you never let me get away with betraying you
            return BE_NICE, "be nice"
        if opponent_cooperation == 1:
            return BE_NICE, "be nice"
        if opponent_cooperation == 0:
            return BE_NICE, "be nice"
        if abs(opponent_cooperation - 0.5) < 0.05:
            return BE_NICE, "be nice"
        if abs(my_cooperation - opponent_cooperation) <= 0.1:
            print("Fuck you Roman")
            return EXPLOIT, "exploit"
        return BE_NICE, "be nice"

    if strat == "investigate":
        if current_round % 3:
            return BE_NICE, strat
        else:
            return EXPLOIT, strat
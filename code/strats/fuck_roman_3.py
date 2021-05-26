
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

    if current_round >= 30:
        my_cooperation = np.mean(myActions)
        opponent_cooperation = np.mean(opponentsActions)
        original_opponent_cooperation = np.mean(opponentsActions[:10])
        recent_opponent_cooperation = np.mean(opponentsActions[-15:])

        my_pre_action = myActions[:-1]
        opp_now_action = opponentsActions[1:]
        revenge_counter = (1 - opp_now_action) - (1 - my_pre_action)
        # 1 = You fuck me for no reason
        # 0 = You fuck me back because I fucked you last turn, or there was no fucking
        # -1 = I fucked you and you didn't do anything
        if opponent_cooperation == 1:
            # alwaysCooperate
            return BE_NICE, "be nice"
        if opponent_cooperation == 0:
            # alwaysDefect
            return BE_NICE, "be nice"
        if recent_opponent_cooperation == 0:
            # grimTrigger
            return BE_NICE, "be nice"
        if sum(np.abs(revenge_counter)) == 0:
            # Tit for tat or detective
            return BE_NICE, "be nice"
        if min(revenge_counter) == 0:
            # joss
            return BE_NICE, "be nice"

        close_to_fifty = abs(opponent_cooperation - 0.5) < 0.08
        proportional_vengenge = abs(np.mean(recent_opponent_cooperation - 0.75)) < 0.1

        if proportional_vengenge and not close_to_fifty:
            # Fuck you roman
            return EXPLOIT, "exploit"

    if strat == "investigate":
        if current_round % 4:
            return BE_NICE, strat
        else:
            return EXPLOIT, strat
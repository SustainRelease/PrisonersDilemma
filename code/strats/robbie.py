

# For the first 100 turns use the revenge and forgiveness strategy. If somebody is mean
# to me, I take revenge on them. The length of the revenge increases each time.
# If I notice that somebody is acting randomly, then always be nice,
# If they have been honest for 100 turns, start playing with them to see if they will
# respond when you are negative
import numpy as np


def strategy(history, memory):
    EXPLOIT = 0
    BE_NICE = 1
    current_round = history.shape[1]
    opponentsActions = history[1]
    myActions = history[0]
    betray_round = 100

    if memory is not None:
        if memory["strat"] == "exploit":
            return EXPLOIT, memory
        if memory["strat"] == "be nice":
            return BE_NICE, memory

    def set_fixed_strategy(do_exploit: bool) -> (int, dict):
        if do_exploit:
            return EXPLOIT, {"strat": "exploit"}
        else:
            return BE_NICE, {"strat": "be nice"}

    if current_round == 0:
        memory = {
            "times_forgiven": 0,
            "mad_counter": 0,
            "strat": "revenge_and_forgiveness"
        }
        return BE_NICE, memory

    just_betrayed = opponentsActions[-1] == EXPLOIT
    average_enemy_action = np.average(opponentsActions)

    if current_round >= 30:
        # If they are random, always be nice
        average_enemy_action = np.average(opponentsActions)
        if average_enemy_action >= 0.45 and average_enemy_action <= 0.55:
            return set_fixed_strategy(do_exploit=True)
    if current_round == betray_round:
        if average_enemy_action == 1:
            memory["strat"] = "betray_and_check"


    if memory["strat"]=="revenge_and_forgiveness":
        if just_betrayed:
            punishment = 2 * 3**memory["times_forgiven"]
            if memory['times_forgiven'] >= 4:
                return set_fixed_strategy(do_exploit=True)
            memory["mad_counter"] += punishment

        i_am_mad = bool(memory["mad_counter"])
        if i_am_mad:
            memory["mad_counter"] -= 1
            if memory["mad_counter"] == 0:
                memory["times_forgiven"] += 1
            return EXPLOIT, memory
        return BE_NICE, memory

    if memory["strat"] == "betray_and_check":
        if current_round == betray_round:
            return EXPLOIT, memory
        if current_round == betray_round + 1:
            return BE_NICE, memory
        if current_round == betray_round + 2:
            return BE_NICE, memory
        if current_round == betray_round + 3:
            recent_actions = opponentsActions[-2:]
            first_action = recent_actions[0]
            second_action = recent_actions[1]
            average_enemy_recent_action = np.average(recent_actions)
            if first_action == EXPLOIT and second_action == BE_NICE:
                memory["strat"] = "revenge_and_forgiveness"
                return BE_NICE, memory
            return set_fixed_strategy(do_exploit=True)

    return BE_NICE, memory



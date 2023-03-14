from copy import deepcopy
from typing import Type

import numpy as np
from tqdm import tqdm

from classes import Agent, InformationSet, KuhnPokerDealer


def run_cfr(
    iset: Type[InformationSet],
    player: Type[Agent],
    opponent: Type[Agent],
    episode: int,
    arrival_prob_1: float,
    arrival_prob_2: float,
    dealer: Type[KuhnPokerDealer],
):
    """
    The function implements the counterfactual regret minimization algorithm.
    
    Args:
        iset (InformationSet): The information set for the current player.
        player (Player): The current player.
        opponent (Player): The opponent player.
        episode (int): The current episode number.
        arrival_prob_1 (float): The arrival probability of player 1.
        arrival_prob_2 (float): The arrival probability of player 2.
        dealer (Dealer): The dealer object representing the game being played.
        
    Returns:
        float: The counterfactual value for the current player and strategy.
    """
    
    if len(iset.history) > 1:
        if iset.history[-1] == iset.history[-2]:
            if iset.history[-1].name == "pass":
                # pass-pass
                utility = +1
            elif iset.history[-1].name == "bet":
                # pass-bet-bet
                # bet-bet
                utility = +2

            high_card_player = dealer.return_higher_card_player()
            return utility if player.label == high_card_player.label else -utility
        elif (iset.history[-2].name == "bet") and (iset.history[-1].name == "pass"):
            # pass-bet-pass
            # bet-pass
            utility = +1
            return utility if iset.active_player_label == player.label else -utility

    cfv = 0
    cfv_action = np.repeat(0, len(iset.legal_actions))

    iset_to_str = f"{str(iset.holding_card)}_{','.join([action.name[0] for action in iset.history])}"

    def _set_strategy_if_not_exists_and_players_turn(p):
        if (iset_to_str not in p.strategy) and (iset.active_player_label == p.label):
            p.strategy[iset_to_str] = np.repeat(
                1 / len(iset.legal_actions), len(iset.legal_actions)
            )

    # we want to make copy of opponent to get current episode's strategy.
    # as opposed to referencing original opponent object
    # we don't want to update the original opponent object
    # passed to run_cfr function call
    opponent_dc = deepcopy(opponent)

    _set_strategy_if_not_exists_and_players_turn(player)
    _set_strategy_if_not_exists_and_players_turn(opponent_dc)

    if iset.active_player_label == player.label:
        active_strategy = player.strategy[iset_to_str]
    else:
        active_strategy = opponent_dc.strategy[iset_to_str]

    for index, action in enumerate(iset.legal_actions):
        if iset.active_player_label == 1:
            next_iset = InformationSet(
                holding_card=iset.holding_card,
                active_player_label=2,
                history=iset.history + (action,),
            )

            cfv_action[index] = run_cfr(
                next_iset,
                player,
                opponent,
                episode,
                active_strategy[index] * arrival_prob_1,
                arrival_prob_2,
                dealer,
            )

        elif iset.active_player_label == 2:
            next_iset = InformationSet(
                holding_card=iset.holding_card,
                active_player_label=1,
                history=iset.history + (action,),
            )
            cfv_action[index] = run_cfr(
                next_iset,
                player,
                opponent,
                episode,
                arrival_prob_1,
                active_strategy[index] * arrival_prob_2,
                dealer,
            )

    cfv = sum(active_strategy * cfv_action)

    def _check_strategy_or_regret_exists(p):
        if iset_to_str not in p.cumulative_regret:
            p.cumulative_regret[iset_to_str] = np.repeat(0, len(iset.legal_actions))
        if iset_to_str not in player.cumulative_strategy:
            p.cumulative_strategy[iset_to_str] = np.repeat(0, len(iset.legal_actions))

    if iset.active_player_label == player.label:
        if player.label == 1:
            _check_strategy_or_regret_exists(player)
            player.cumulative_regret[iset_to_str] = player.cumulative_regret[
                iset_to_str
            ] + (arrival_prob_2 * (cfv_action - cfv))
            player.cumulative_strategy[iset_to_str] = player.cumulative_strategy[
                iset_to_str
            ] + (arrival_prob_1 * player.strategy[iset_to_str])
        else:
            _check_strategy_or_regret_exists(player)
            player.cumulative_regret[iset_to_str] = player.cumulative_regret[
                iset_to_str
            ] + (arrival_prob_1 * (cfv_action - cfv))
            player.cumulative_strategy[iset_to_str] = player.cumulative_strategy[
                iset_to_str
            ] + (arrival_prob_2 * player.strategy[iset_to_str])

        cumulative_regret = np.array(
            list(map(lambda x: max(x, 0), player.cumulative_regret[iset_to_str]))
        )
        if sum(cumulative_regret) > 0:
            player.strategy[iset_to_str] = cumulative_regret / sum(cumulative_regret)
        else:
            player.strategy[iset_to_str] = np.repeat(
                1 / len(iset.legal_actions), len(iset.legal_actions)
            )

    player.update_memory()

    return cfv


def train_cfr(num_episodes: int):
    agent_1 = Agent(label=1)
    agent_2 = Agent(label=2)
    poker_dealer = KuhnPokerDealer(agent_1, agent_2)

    for t in tqdm(range(num_episodes)):
        poker_dealer.deal_cards()
        # initialise empty node with active player as player 1
        initial_iset_1 = InformationSet(
            holding_card=agent_1.card, active_player_label=1
        )
        initial_iset_2 = InformationSet(
            holding_card=agent_2.card, active_player_label=1
        )

        # we want cfr algorithm to save nodes in place inside players
        # like the players have memories which are represented by game nodes
        run_cfr(initial_iset_1, agent_1, agent_2, t, 1, 1, poker_dealer)
        run_cfr(initial_iset_2, agent_2, agent_1, t, 1, 1, poker_dealer)
        poker_dealer.reset_hand()

    return agent_1, agent_2

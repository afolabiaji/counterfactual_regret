from typing import Optional, List, Dict
import numpy as np
import dataclass
import random
from copy import deepcopy

from classes import Action, KuhnPokerDealer, Agent, InformationSet

def run_cfr(iset, player, episode, arrival_prob_1, arrival_prob_2):
    if iset.is_terminal == True:
        iset.current_episode += 1
        # return history.get_utility()
    
    cfv = 0
    cfv_action = np.repeat(0, len(iset.legal_actions))
    
    next_iset = deepcopy(iset)
    for index, current_action in enumerate(iset.legal_actions):
        #you can probability use numpy vectorisation to speed this up 
        #you might not even need to use a for loop
        next_iset.history += [action for action in ACTIONS if action == current_action]
        if iset.active_player_label == 1:
            cfv_action[index] = run_cfr(next_iset, player, episode, iset.strategy[episode][index]*arrival_prob_1, arrival_prob_2)
        elif iset.active_player_label == 2:
            cfv_action[index] = run_cfr(next_iset, player, episode, arrival_prob_1, iset.strategy[episode][index]*arrival_prob_2)
        
        cfv += iset.strategy[episode][index]*cfv_action[index]
    
    if iset.active_player_label == player.label:
        for index, current_action in enumerate(iset.legal_actions):
            #you can probability use numpy vectorisation to speed this up 
            #you might not even need to use a for loop
            if player.label == 1:
                iset.cumulative_regret[index] += arrival_prob_2 * (cfv_action[index] - cfv)
                iset.cumulative_strategy[index] += arrival_prob_1 * iset.strategy[episode][index]
            else:
                iset.cumulative_regret[index] += arrival_prob_1 * (cfv_action[index] - cfv)
                iset.cumulative_strategy[index] += arrival_prob_2 * iset.strategy[episode][index]
                
        if sum(iset.cumulative_regret) > 0:
            iset.strategy[episode+1] = iset.cumulative_regret / sum(iset.cumulative_regret)
        else:
            iset.strategy[episode+1] = np.repeat(1/len(legal_actions), len(legal_actions))
            
    return cfv


def train(num_episodes:int):
    agent_1 = Agent(label=1)
    agent_2 = Agent(label=2)
    poker_dealer = KuhnPokerDealer(agent_1, agent_2)
    
    for t in range(num_episodes):
        while poker_dealer.hand_terminated == False:
            poker_dealer.deal_cards()
            cfr(iset, agent_1, t, 1, 1)
            cfr(iset, agent_2, t, 1, 1)
            
            action = poker_dealer.get_action()
            poker_dealer.return_utility_to_players(self, action)
        poker_dealer.reset_hand()
    
        
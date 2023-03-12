from typing impoty List
import numpy as np

@dataclass
class Action
    name:str
    int_rep:int

ACTIONS = [
    Action("pass",0)
    Action("bet",1)
]
    
@dataclass
class InformationSet:
    """
        Information set for a given player and history in Kuhn Poker
    """
    holding_card:int
    history: List[Action]
    legal_actions: List[Action] = ACTIONS
    active_player_label:int
    is_terminal: bool
    current_episode = 0
    strategy:Dict[int,np.ndarray] = {0, np.repeat(1/len(legal_actions), len(legal_actions))}
    cumulative_strategy:np.ndarray = np.repeat(0, len(legal_actions))
    cumulative_regret:np.ndarray = np.repeat(0, len(legal_actions))
    
    
    def is_chance_node(self) -> bool:
        if len(history) == 0:
            return True
        else:
            return False
    
    
    

class Agent:
    def __init__(self):
        self.label:Optional[str] = None
        self.card:Optional[int] = None #card
        self.current_iset : Optional[InformationSet] = None
        cumulative_regret:Dict[InformationSet, np.ndarray] = dict()
        strategy:Dict[InformationSet, np.ndarray] = dict()
        cumulative_strategy:Dict[InformationSet, np.ndarray] = dict()
    
    def get_current_action(self, iset):
        action = np.random.choice(ACTIONS, p=self.current_iset.strategy)
        self.current_action = action
        return action
    
    def update_strategy(self, realisation_weight, iset):
        """
            Return strategy for node weighted by probability that iset is reached with current strategy profile
        """
        self.strategy[iset] = np.where(self.cumulative_regret[iset] > 0, self.cumulative_regret[iset], 0)

        if sum(self.strategy[iset]) > 0:
            self.strategy[iset] = self.strategy[iset] / sum(self.strategy[iset])
        else:
            self.strategy[iset] = 1 / len(iset.legal_actions)
        
        self.cumulative_strategy[iset] += realisation_weight * self.strategy[iset]
        
        return self.strategy[iset]
    
        
class KuhnPokerDealer:
    def __init__(self, agent_1:Type[Agent], agent_2:Type[Agent]):
        self.deck = [1,2,3]
        self.max_rounds = 3
        self.player_1 = agent_1
        self.player_2 = agent_2
        self.betting_round = 0
        self.pot = 2 #both players ante one chip
        self.hand_terminated = False
        self.action_history = list()
        
    def deal_cards(self):
        self.player_1.card = random.choice(self.deck)
        self.deck.remove(self.player_1.card)
        self.player_2.card = #get card from deck at random
    
    def return_higher_card_player(self) -> KuhnAgent:
        if self.player_1.card > self.player_2.card
            return self.player_1
        else:
            return self.player_2
            
    def get_action(self):
        termial_round = False
        
        if (self.betting_round % 2) == 1:
            self.active_player = self.player_1
            self.inactive_player = self.player_2
        else:
            self.active_player = self.player_2
            self.inactive_player = self.player_1
        
        
        iset = InformationSet(
            holding_card=self.active_player.card,
            history=self.action_history,
            legal_actions=ACTIONS,
            active_player_label=self.active_player.label
        )
        if iset not in active_player.strategy:
            r_weight = 1 #change in cfv algorithm
            active_player.current_iset = iset
            active_player.update_strategy(r_weight, iset)
            
        action = self.active_player.get_current_action()
        self.action_history += [action]
        
        #do recursive cfr call
        
        return action
    
    def return_utility_to_players(self, action):
        if (action.int_rep == 0)
            if (self.betting_round != 1):
                terminal_round = True
                if (inactive_player.current_action.int_rep == 1):
                    #inactive player wins and gets the pot
                    # self.inactive_player.
                else:
                    #the game is a tie and the pot is split
            else:
                #move to next betting round
                self.betting_round +=1
                
        elif (action.int_rep == 1):
            self.active_player.cumulative_bet += 1
            self.pot += 1
            if (inactive_player.current_action.int_rep == 0) and (self.betting_round != 3):
                self.betting_round += 1
                #move to next round
            elif (inactive_player.current_action.int_rep == 1):
                #split pot
            elif (inactive_player.current_action.int_rep == 0) and (self.betting_round == 3):
                #current player wins and takes the pot
        
        #check if this was terminal
        #if terminal give utility payouts to players
        #if not terminal increment betting round
        
    def reset_hand(self):
        self.deck = [1,2,3]
        self.betting_round = 0
        self.pot = 2 #both players ante one chip
        self.hand_terminated = False

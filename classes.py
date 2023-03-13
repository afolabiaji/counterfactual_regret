import random
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple, Type

import numpy as np


@dataclass(eq=True, frozen=True)
class Action:
    name: str
    int_rep: int


ACTIONS = (Action("pass", 0), Action("bet", 1))


@dataclass(eq=True, frozen=True)
class InformationSet:
    """
    Information set for a given player and history in Kuhn Poker.
    This represent all information available to a given player,
    in a given game state.
    """

    holding_card: int
    active_player_label: int
    history: Tuple[Type[Action]] = field(default_factory=tuple)
    legal_actions: Tuple = field(default_factory=lambda: ACTIONS)


# class GameNode:
#     """
#         Node that contains information set, represents full game state
#         including information hidden to given player at given time
#     """
#     def __init__(self, iset, active_player_label, opponent_card, current_episode):
#         self.iset = iset
#         self.legal_actions = ACTIONS
#         self.active_player_label = active_player_label
#         self.opponent_card = opponent_card
#         self.is_terminal: bool = False
#         # self.strategy = {0: np.repeat(1/len(self.legal_actions), len(self.legal_actions))}
#         # self.cumulative_strategy = np.repeat(0, len(legal_actions))
#         # self.cumulative_regret = np.repeat(0, len(legal_actions))


class Agent:
    def __init__(self, label):
        self.label: int = label
        self.card: Optional[int] = None  # card
        self.current_iset: Optional[Type[InformationSet]] = None

        self.strategy: Dict[Type[str], np.ndarray] = dict()
        self.cumulative_regret: Dict[Type[str], np.ndarray] = dict()
        self.cumulative_strategy: Dict[Type[str], np.ndarray] = dict()
        self.memory = {
            "strategy": self.strategy,
            "cumulative_regret": self.cumulative_regret,
            "cumulative_strategy": self.cumulative_strategy,
        }

    def get_current_action(self, iset):
        action = np.random.choice(ACTIONS, p=self.current_iset.strategy)
        self.current_action = action
        return action

    def update_memory(self) -> None:
        """
        Update memory when strategy/regret have been altered by external cfr call
        """
        self.memory = {
            "strategy": self.strategy,
            "cumulative_regret": self.cumulative_regret,
            "cumulative_strategy": self.cumulative_strategy,
        }


class KuhnPokerDealer:
    def __init__(self, agent_1: Type[Agent], agent_2: Type[Agent]):
        self.deck = [1, 2, 3]
        self.max_rounds = 3
        self.player_1 = agent_1
        self.player_2 = agent_2
        self.betting_round = 0
        self.pot = 2  # both players ante one chip
        self.hand_terminated = False
        self.action_history = list()

    def deal_cards(self):
        self.player_1.card = random.choice(self.deck)
        self.deck.remove(self.player_1.card)
        self.player_2.card = random.choice(self.deck)  # get card from deck at random

    def return_higher_card_player(self) -> Agent:
        if self.player_1.card > self.player_2.card:
            return self.player_1
        else:
            return self.player_2

    def get_action(self):
        if (self.betting_round % 2) == 1:
            self.active_player = self.player_1
            self.inactive_player = self.player_2
        else:
            self.active_player = self.player_2
            self.inactive_player = self.player_1

        action = self.active_player.get_current_action()
        self.action_history += [action]

        return action

    def reset_hand(self):
        self.deck = [1, 2, 3]
        self.betting_round = 0
        self.pot = 2  # both players ante one chip
        self.hand_terminated = True

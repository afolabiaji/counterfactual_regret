# this file is to allow a human player to play against
# approximate Nash equilibrium generated from CFR algorithm
import pickle
from pathlib import Path
from random import randint

from classes import Agent, KuhnPokerDealer

if __name__ == "__main__":
    # 1. allow player to select the play order (or random)
    print(
        "Welcome to the Kuhn Poker terminal game. You will be playing against a finely crafted AI trained to decieve you with it's bluffing skills."
    )
    play_order = None
    while (play_order != 1) and (play_order != 2):
        play_order_inpt = (
            str(
                input(
                    "Please select whether you would like to act first or second (leave blank for this to be selected at random): "
                )
            )
            .lower()
            .replace(" ", "")
        )
        if ("first" in play_order_inpt) or ("1st" in play_order_inpt):
            play_order = 1
        elif ("second" in play_order_inpt) or ("2nd" in play_order_inpt):
            play_order = 2
        elif not play_order_inpt:
            play_order = randint(1, 2)
            print(f"You will play {'first' if play_order == 1 else 'second'}")
        else:
            print("Your input was invalid, please enter again...")

    human_hero = Agent(label=play_order, is_human=True)
    ai_villain = Agent(label=(3 - play_order), is_human=False)

    # 2. load player 1 or 2 stratgy depending on play order
    def get_agent_memory(agent_play_order: int):
        mod_path = Path(__file__).parent
        src_path = (
            mod_path / f"./saved_data/agent_{agent_play_order}__memory.pkl"
        ).resolve()
        with open(src_path, "rb") as file:
            agent_memory = pickle.load(file)
        return agent_memory

    villain_memory = get_agent_memory(ai_villain.label)
    ai_villain.memory = villain_memory

    # 3. construct dealer from players
    if play_order == 1:
        dealer = KuhnPokerDealer(agent_1=human_hero, agent_2=ai_villain)
    else:
        dealer = KuhnPokerDealer(agent_1=ai_villain, agent_2=human_hero)

    # 4. Begin game by dealing cards
    dealer.deal_cards()
    print(f"Your card is: {human_hero.card}")

    # 5. Get action from first players
    while dealer.hand_terminated == False:
        # print history of betting actions
        action = dealer.get_action()
        if dealer.hand_terminated == False:
            if dealer.active_player == human_hero:
                pass
            else:
                print(f"Your opponent has opted to: {action.name}")

    # 6. Tell player game has ended and present result (along with opponents card)
    payout = dealer.end_hand_and_payout_players(human_hero)
    print("The game has ended...")
    if payout == 1 or payout == 2:
        print(
            f"You won, Your card was stronger than your opponent's! Your payout is {payout}. Your opponents card was {ai_villain.card}"
        )
    else:
        print(
            f"You lost! :(  Your payout is {payout}. Your opponents card was {ai_villain.card}"
        )

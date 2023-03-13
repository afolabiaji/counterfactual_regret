import pickle
from pathlib import Path

from cfr_algorithm import train_cfr
from constants import NUM_ITERATIONS

if __name__ == "__main__":
    print("Running algorithm...")
    iterations = int(
        eval(input("Please enter the number of iterations (enter 0 for default): "))
    )
    agent_1, agent_2 = train_cfr(iterations if iterations > 0 else int(NUM_ITERATIONS))
    print("Training complete.")

    mod_path = Path(__file__).parent
    src_path_1 = (mod_path / "./saved_data/agent_1__memory.pkl").resolve()
    src_path_2 = (mod_path / "./saved_data/agent_2__memory.pkl").resolve()

    with open(src_path_1, "wb") as file:
        pickle.dump(agent_1.memory, file)

    with open(src_path_2, "wb") as file:
        pickle.dump(agent_2.memory, file)

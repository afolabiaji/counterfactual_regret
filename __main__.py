from cfr_algorithm import train_cfr
from constants import NUM_ITERATIONS

if __name__ == "__main__":
    print("Running algorithm...")
    iterations = int(
        eval(input("Please enter the number of iterations (enter 0 for default): "))
    )
    agent_1, agent_2 = train_cfr(iterations if iterations > 0 else int(NUM_ITERATIONS))
    print("Training complete.")
    print(agent_1.memory)

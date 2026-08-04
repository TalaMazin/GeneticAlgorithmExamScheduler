# convergence_analysis.py


import matplotlib.pyplot as plt
from ga import genetic_algorithm

def run_experiment(pop_size, generations):

    print("\n===================================")
    print(f"Running with population = {pop_size}")
    print("===================================\n")

    best, best_history, avg_history = genetic_algorithm(
        pop_size=pop_size,
        generations=generations
    )

    return best_history, avg_history

if __name__ == "__main__":

    generations = 100

    # EXPERIMENT 1 : SMALL POPULATION
    best_30, avg_30 = run_experiment(
        pop_size=30,
        generations=generations
    )

    # EXPERIMENT 2 : MEDIUM POPULATION
    best_60, avg_60 = run_experiment(
        pop_size=60,
        generations=generations
    )

    # EXPERIMENT 3 : LARGE POPULATION
    best_100, avg_100 = run_experiment(
        pop_size=100,
        generations=generations
    )

    # PLOT BEST FITNESS
    plt.figure(figsize=(12, 6))

    plt.plot(
        range(generations),
        best_30,
        label="Population = 30",
        linewidth=2
    )

    plt.plot(
        range(generations),
        best_60,
        label="Population = 60",
        linewidth=2
    )

    plt.plot(
        range(generations),
        best_100,
        label="Population = 100",
        linewidth=2
    )

    plt.title("Convergence Rate for Different Population Sizes")

    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")

    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    # save graph
    plt.savefig("population_convergence.png")

    plt.show()

    plt.figure(figsize=(12, 6))

    plt.plot(
        range(generations),
        best_60,
        label="Best Fitness",
        linewidth=2
    )

    plt.plot(
        range(generations),
        avg_60,
        label="Average Fitness",
        linewidth=2
    )

    plt.title("Genetic Algorithm Convergence")

    plt.xlabel("Generation")
    plt.ylabel("Fitness")

    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    plt.savefig("ga_convergence.png")

    plt.show()

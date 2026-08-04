"""
FINAL GENETIC ALGORITHM FOR EXAM SCHEDULING
==========================================

Balanced version:
- stable convergence (elitism)
- controlled exploration (mutation + immigrants)
- tournament selection
- simple crossover
"""

import random
from dataset import COURSES, ALL_SLOT_IDS, ENROLLMENTS, get_day
from fitness import fitness


# =========================================================
# 1. CREATE RANDOM SCHEDULE (CHROMOSOME)
# =========================================================
def create_schedule():
    return {c: random.choice(ALL_SLOT_IDS) for c in COURSES}


# =========================================================
# 2. INITIAL POPULATION
# =========================================================
def create_population(size):
    return [create_schedule() for _ in range(size)]


# =========================================================
# 3. TOURNAMENT SELECTION (BEST BALANCE)
# =========================================================
def select(pop, scores, k=3):
    best = None
    best_score = float("-inf")

    for _ in range(k):
        i = random.randint(0, len(pop) - 1)
        if scores[i] > best_score:
            best_score = scores[i]
            best = pop[i]

    return best


# =========================================================
# 4. CROSSOVER (SAFE + SIMPLE)
# =========================================================
def crossover(p1, p2):
    child = {}

    for c in COURSES:
        child[c] = p1[c] if random.random() < 0.5 else p2[c]

    return child


# =========================================================
# 5. MUTATION (CONTROLLED + ADAPTIVE)
# =========================================================
def mutate(schedule, gen, max_gen):
    new = schedule.copy()

    # starts low, increases slightly later
    rate = 0.03 + (gen / max_gen) * 0.07   # 3% → 10%

    for c in new:
        if random.random() < rate:
            new[c] = random.choice(ALL_SLOT_IDS)

    return new


# =========================================================
# 6. RANDOM IMMIGRANTS (DIVERSITY CONTROL)
# =========================================================
def inject_diversity(pop, scores):
    worst = sorted(range(len(pop)), key=lambda i: scores[i])[:2]

    for i in worst:
        pop[i] = create_schedule()


# =========================================================
# 7. ELITISM (KEEP BEST SAFE)
# =========================================================
def get_best(pop, scores):
    return pop[scores.index(max(scores))].copy()


# =========================================================
# 8. MAIN GA LOOP
# =========================================================
def genetic_algorithm(pop_size=60, generations=100):

    pop = create_population(pop_size)

    best_history = []
    avg_history = []

    global_best = None
    global_score = float("-inf")

    for gen in range(generations):

        scores = [fitness(ind) for ind in pop]

        best_score = max(scores)
        avg_score = sum(scores) / len(scores)

        best_history.append(best_score)
        avg_history.append(avg_score)

        # update global best
        if best_score > global_score:
            global_score = best_score
            global_best = get_best(pop, scores)

        # NEW POPULATION
        new_pop = []

        # elitism (keep best 1)
        new_pop.append(get_best(pop, scores))

        # generate rest
        while len(new_pop) < pop_size:

            p1 = select(pop, scores)
            p2 = select(pop, scores)

            child = crossover(p1, p2)
            child = mutate(child, gen, generations)

            new_pop.append(child)

        pop = new_pop

        # diversity injection every 15 generations
        if gen % 15 == 0:
            inject_diversity(pop, scores)

        print(f"Gen {gen:3} | Best: {best_score:7} | Avg: {avg_score:7.2f}")

    return global_best, best_history, avg_history



if __name__ == "__main__":

    best, best_hist, avg_hist = genetic_algorithm()

    print("\n================ FINAL RESULT ================\n")
    print("BEST FITNESS:", max(best_hist))

    print("\nSAMPLE SCHEDULE (first 10):")
    for i, (c, s) in enumerate(best.items()):
        print(c, "->", s)
        if i == 9:
            break
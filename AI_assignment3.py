import random
import math

def fitness_function(x):
    return x * math.cos(5 * math.pi * x) + 1.0

# 일정 확률로 무작위의 한 지점에서 crossover연산 수행
def crossover(parent1, parent2, crossover_rate):
    if random.uniform(0, 1) < crossover_rate:
        crossover_point = random.uniform(0, 1)
        return parent1 * crossover_point + parent2 * (1 - crossover_point)
    else:
        return parent1

# 일정 확률로 무작위의 한 지점에서 mutation연산 수행
def mutate(child, mutation_rate):
    if random.uniform(0, 1) < mutation_rate:
        return child + random.uniform(-0.1, 0.1)
    else:
        return child

def generate_population(population_size):
    return [random.uniform(-10, 10) for _ in range(population_size)]

def main():
    population_size = 100 
    generations = 100
    crossover_rate = 0.8
    mutation_rate = 0.2

    #chromosome 100개
    population = generate_population(population_size)

    for generation in range(generations):
        # 적합도 평가
        fitness = [fitness_function(x) for x in population]

        # 가장 높은 적합도를 가진 상위 20개의 개체 선택
        parents = [pop for pop, fit in sorted(zip(population, fitness), key=lambda x: x[1], reverse=True)[:20]]

        # crossover, mutation 연산 수행
        new_population = []
        for _ in range(population_size // 2):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child = crossover(parent1, parent2, crossover_rate)
            new_population.extend([mutate(child, mutation_rate) for _ in range(2)])

        # 새로운 세대로 교체
        population = new_population

        
        best_individual = max(population, key=fitness_function)
        print(f"Generation {generation + 1}: Best = {best_individual}, Fitness = {fitness_function(best_individual)}")

if __name__ == "__main__":
    main()

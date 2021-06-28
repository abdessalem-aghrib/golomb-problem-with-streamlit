from math import log
import golomb as golomb
import random
import time
import streamlit as st
import pandas as pd

import strings


def generate_population(population_size: int, marks_count: int, max_bound: int):
    population = list()
    while len(population) < population_size:
        ruler = golomb.generate_golomb_ruler(marks_count, max_bound, max_generate_time=60)
        if ruler not in population:
            population.append(ruler)

    return population


def evaluation_function(individual: list[int]):
    return individual[len(individual) - 1] - individual[0]


def binary_list_to_integer(binary_list: list[int]):
    string_ints = [str(i) for i in binary_list]
    binary_str = "".join(string_ints)
    return int(binary_str, 2)


def integer_to_binary_list(integer: int, size_of_bits: int):
    b = str(format(integer, 'b'))
    l = len(b)
    if l > size_of_bits:
        return b

    binary = str("0" * (size_of_bits - l)) + b
    binary_list = [int(binary[i]) for i in range(len(binary))]

    return binary_list


def crossover(parent_ruler_1: list[int], parent_ruler_2: list[int], size_of_bits: int,
              max_trying_time_for_correct_ruler: float):
    l = len(parent_ruler_1)
    if l != len(parent_ruler_2):
        raise ValueError("Rules must be of same length")

    child_1 = parent_ruler_1.copy()
    child_2 = parent_ruler_2.copy()

    # the positions where the crossing must be made
    position_1 = random.randint(1, l - 1)
    position_2 = random.randint(1, l - 1)

    # get binary lists of positions chooses (gene)
    binary_list_1 = integer_to_binary_list(integer=parent_ruler_1[position_1], size_of_bits=size_of_bits)
    binary_list_2 = integer_to_binary_list(integer=parent_ruler_2[position_2], size_of_bits=size_of_bits)

    # made crossing between this two lists

    # choose crossing point
    x = min(parent_ruler_1[position_1], parent_ruler_2[position_2])
    p = random.randint(1, int(log(x + 1) / log(2)) + 1)

    # made binary lists of children
    child_binary_list_1 = binary_list_1[0:p] + binary_list_2[p:]
    child_binary_list_2 = binary_list_2[0:p] + binary_list_1[p:]

    # rebuild children
    child_1[position_1] = binary_list_to_integer(child_binary_list_1)
    child_2[position_2] = binary_list_to_integer(child_binary_list_2)

    # correct the children
    child_1 = golomb.correct_golomb_ruler(child_1, original_ruler=parent_ruler_1,
                                          max_trying_time=max_trying_time_for_correct_ruler)
    child_2 = golomb.correct_golomb_ruler(child_2, original_ruler=parent_ruler_2,
                                          max_trying_time=max_trying_time_for_correct_ruler)

    return [child_1, child_2]


def mutation(individual: list[int], size_of_bits: int, max_trying_time_for_correct_ruler: float):
    l = len(individual)
    original_individual = individual.copy()

    # the positions where the mutation must be made
    position = random.randint(1, l - 1)

    # get binary list of position chooses (gene)
    binary_list = integer_to_binary_list(integer=individual[position], size_of_bits=size_of_bits)

    # choose mutation point
    p = 0
    for i in range(len(binary_list)):
        if binary_list[i] == 1:
            p = i
            break
    # p = random.randint(p, size_of_bits-1)

    # made mutation
    binary_list[p] = 0

    # rebuild individual
    individual[position] = binary_list_to_integer(binary_list)

    # correct the individual
    individual = golomb.correct_golomb_ruler(individual, original_ruler=original_individual,
                                             max_trying_time=max_trying_time_for_correct_ruler)

    return individual


def evaluate(population: list[list[int]]):
    evaluation_table = []
    for individual in population:
        evaluation_table.append(evaluation_function(individual))

    return evaluation_table


def get_ranks(evaluation_table: list[int]):
    rank_tab = set()
    for ev in evaluation_table:
        rank_tab.add(ev)

    return list(sorted(rank_tab))


def get_probabilities(tab: list[int], of_ranks: bool):
    size = len(tab)
    probabilities = []

    if of_ranks:
        sum_ranks = size * (size + 1) / 2
        for i in range(size):
            probabilities.append((size - i) / sum_ranks)

    else:
        sum_tab = sum(tab)
        for i in range(size):
            probabilities.append(tab[i] / sum_tab)

    return probabilities


def rank_selection(population: list[list[int]], marks_count: int, ranks: list[int],
                   probabilities: list[float]):
    parent_1 = []
    parent_2 = []

    # select first parent
    size = len(probabilities)
    p = random.random()  # ]0-1]
    if p == 0:
        p = 0.1

    index = size - 1
    for i in range(size):
        if p >= probabilities[i]:
            index = i
            break

    fitness = ranks[index]
    for i in range(len(population)):
        if population[i][marks_count - 1] == fitness:
            parent_1 = population[i]
            break

    # select second parent
    second_population = population.copy()
    second_population.remove(parent_1)

    evaluation_table = evaluate(second_population)
    ranks = get_ranks(evaluation_table)
    probabilities = get_probabilities(ranks, of_ranks=True)

    size = len(probabilities)
    p = random.random()  # ]0-1]
    if p == 0:
        p = 0.1

    index = size - 1
    for i in range(size):
        if probabilities[i] >= p:
            index = i
            break

    fitness = ranks[index]
    for i in range(len(second_population)):
        if second_population[i][marks_count - 1] == fitness:
            parent_2 = second_population[i]
            break

    return [parent_1, parent_2]


def tournament_selection(population: list[list[int]], population_size: int, marks_count: int):

    k = random.randint(2, population_size)

    individuals_index = random.sample(range(0, population_size), k)

    parent_1 = population[individuals_index[0]]
    parent_2 = population[individuals_index[1]]

    for i in range(2, len(individuals_index)):
        current_individual = population[individuals_index[i]]
        if current_individual[marks_count - 1] < parent_1[marks_count - 1]:
            parent_1, parent_2 = current_individual, parent_1
        elif current_individual[marks_count - 1] < parent_2[marks_count - 1]:
            parent_2 = current_individual

    return [parent_1, parent_2]


def uniform_selection(population: list[list[int]], population_size: int):
    individuals_index = random.sample(range(0, population_size), 2)

    return [population[individuals_index[0]], population[individuals_index[1]]]


def get_best_individual(population: list[list[int]]):
    best_individual = population[0]
    for i in range(1, len(population)):
        if evaluation_function(population[i]) < evaluation_function(best_individual):
            best_individual = population[i]

    return best_individual


def genetic(population_size: int, generation_count: int, crossing_probability: float, mutation_probability: float,
            marks_count: int, max_bound: int, size_of_bits: int,
            max_trying_time_for_correct_ruler: float):
    start = time.time()
    record_best_individuals_from_all_generations = []

    population = generate_population(population_size, marks_count, max_bound)
    record_best_individuals_from_all_generations.append(get_best_individual(population))

    initial_population = population.copy()
    gen = 0
    new_pop = list()

    # draw line chart
    st.header(strings.genetic_graph_header)
    df = pd.DataFrame({
        'time': [(time.time() - start) for _ in range(len(initial_population))],
        'Fitness': evaluate(initial_population)
    }).rename(columns={'time': 'index'}).set_index('index')

    chart = st.line_chart(df)

    # write results
    results_container = st.beta_container()
    with results_container:
        st.header(strings.results_header)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.initial_generation_msg)
            col_value.markdown(f'<span style="color:#26ba1b">** {initial_population} **</span>', unsafe_allow_html=True)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.best_ruler_of_this_generation_msg)
            col_value.markdown(f'<span style="color:#26ba1b">** {get_best_individual(initial_population)} **</span>', unsafe_allow_html=True)

    while gen < generation_count:
        new_pop.clear()

        evaluation_table = evaluate(population)
        # print(f'Evaluate tab : \n{evaluation_table}')

        ranks = get_ranks(evaluation_table)
        # print(f'Rank_tab tab : \n{ranks}')

        probabilities = get_probabilities(ranks, of_ranks=True)
        # print(f'Probabilities tab : \n{probabilities}')

        while len(new_pop) < population_size:

            # choose selection methode
            r = random.random()
            if r >= 0.5:
                parents = rank_selection(population, marks_count, ranks, probabilities)
            else:
                parents = tournament_selection(population, population_size, marks_count)

            parent_1 = parents[0].copy()
            parent_2 = parents[1].copy()

            # crossover
            r = random.random()
            if r >= crossing_probability:
                parents = crossover(parent_1.copy(), parent_2.copy(), size_of_bits,
                                    max_trying_time_for_correct_ruler)

            # mutation
            r = random.random()
            if r >= mutation_probability:
                parent_1 = mutation(parents[0].copy(), size_of_bits, max_trying_time_for_correct_ruler)
                parent_2 = mutation(parents[1].copy(), size_of_bits, max_trying_time_for_correct_ruler)

            # add new children if not exists
            if not new_pop.__contains__(parent_1) and len(new_pop) < population_size:
                new_pop.append(parent_1.copy())

                # draw line chart
                new_df = pd.DataFrame({
                    'time': [time.time() - start],
                    'Fitness': [evaluation_function(parent_1)]
                }).rename(columns={'time': 'index'}).set_index('index')

                chart.add_rows(new_df)

            if not new_pop.__contains__(parent_2) and len(new_pop) < population_size:
                new_pop.append(parent_2.copy())

                # draw line chart
                new_df = pd.DataFrame({
                    'time': [time.time() - start + 0.2],
                    'Fitness': [evaluation_function(parent_2)]
                }).rename(columns={'time': 'index'}).set_index('index')

                chart.add_rows(new_df)

        # updates
        gen += 1
        population.clear()
        population = new_pop.copy()
        best_individual_for_this_generation = get_best_individual(population)
        record_best_individuals_from_all_generations.append(best_individual_for_this_generation)

        with results_container:
            st.markdown(body='<hr style="margin-top:0;border-top:0.5px solid '
                             '#bbb;border-radius:5px;color:#90939b;background-color:#90939b;" />',
                        unsafe_allow_html=True)

            with st.beta_container():
                col_title, col_value = st.beta_columns([2, 3])

                col_title.write(f'{strings.generation_msg} {gen} :\n ')
                col_value.markdown(f'<span style="color:#26ba1b">** {population} **</span>', unsafe_allow_html=True)

            with st.beta_container():
                col_title, col_value = st.beta_columns([2, 3])

                col_title.write(strings.best_ruler_of_this_generation_msg)
                col_value.markdown(f'<span style="color:#26ba1b">** {best_individual_for_this_generation} **</span>',
                               unsafe_allow_html=True)

    end = time.time() - start
    best_individual = get_best_individual(record_best_individuals_from_all_generations)

    # write results
    with results_container:
        st.markdown(body='<hr style="margin-top:2;border-top:2px solid '
                         '#bbb;border-radius:5px;color:#ef0741;background-color:#ef0741;" />',
                    unsafe_allow_html=True)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.best_ruler_of_all_generation_msg)
            col_value.markdown(f'<span style="color:#26ba1b">**{str(best_individual)}**</span>', unsafe_allow_html=True)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.best_fitness_msg)
            col_value.markdown(f'<span style="color:#26ba1b">**{evaluation_function(best_individual)}**</span>',
                               unsafe_allow_html=True)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.run_time_msg)
            col_value.markdown(f'<span style="color:#26ba1b">**{end} s**</span>', unsafe_allow_html=True)

    return {"initial_population": initial_population,
            "final_population": population,
            "best_individual": best_individual,
            "best_fitness": evaluation_function(best_individual),
            "runtime": end}

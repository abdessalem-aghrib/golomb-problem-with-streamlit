import random
import time
import streamlit as st
import strings as strings
import pandas as pd

# separator
separator_body = '<hr style="margin-top:40px;margin-bottom:50px;border-top:2px solid ' \
                 '#bbb;border-radius:5px;color:#90939b;background-color:#90939b;" />'


# Hill Climbing algorithm
def hill_climbing(problem_function, marks_count, max_bound, attempts_count=10):
    # best results
    best_params = {}
    best_result = [{}]

    # for results
    results_container = st.beta_container()
    results = [None]

    # start time
    start = time.time()

    # initial solution
    initial_temperature = 50.0  # initial temperature
    cooling_coeff = 0.1  # cooling coefficient
    computing_time = 0.1  # in seconds
    trials_number = 1  # number or trials to get neighborhood before use random one
    attempts_in_each_level_of_temperature = 1  # number of attempts in each level of temperature

    problem_function(marks_count, max_bound, initial_temperature, cooling_coeff,
                     computing_time, trials_number, attempts_in_each_level_of_temperature,
                     '', None, True, None, results, 0, False)

    current_result = results.copy()
    best_result = results.copy()

    best_params["initial_temperature"] = initial_temperature
    best_params["cooling_coeff"] = cooling_coeff
    best_params["computing_time"] = computing_time
    best_params["trials_number"] = trials_number
    best_params["attempts_in_each_level_of_temperature"] = attempts_in_each_level_of_temperature

    # draw params graphs

    # temperature graph
    st.header(strings.temperature_params_graph_header)
    temperature_chart = st.line_chart()

    new_df = pd.DataFrame({
        'trials': [0],
        'Température': [float(initial_temperature)]
    }).rename(columns={'trials': 'index'}).set_index('index')

    temperature_chart.add_rows(new_df)

    # cooling coeff graph
    st.header(strings.cooling_coeff_params_graph_header)
    cooling_coeff_chart = st.line_chart()

    new_df = pd.DataFrame({
        'trials': [0],
        'Refroidissement Coéff': [float(cooling_coeff)]
    }).rename(columns={'trials': 'index'}).set_index('index')

    cooling_coeff_chart.add_rows(new_df)

    # computing time graph
    st.header(strings.computing_time_params_graph_header)
    computing_time_chart = st.line_chart()
    new_df = pd.DataFrame({
        'trials': [0],
        'Temp de calcul': [float(computing_time)]
    }).rename(columns={'trials': 'index'}).set_index('index')

    computing_time_chart.add_rows(new_df)

    # trials neighbor graph
    st.header(strings.trials_neighbor_params_graph_header)
    neighbor_trials_chart = st.line_chart()
    new_df = pd.DataFrame({
        'trials': [0],
        'Tentatives voisin': [float(trials_number)]
    }).rename(columns={'trials': 'index'}).set_index('index')

    neighbor_trials_chart.add_rows(new_df)

    # trials temperature  graph
    st.header(strings.trials_temperature_params_graph_header)
    temperature_trials_chart = st.line_chart()
    new_df = pd.DataFrame({
        'trials': [0],
        'Tentatives température': [float(attempts_in_each_level_of_temperature)]
    }).rename(columns={'trials': 'index'}).set_index('index')

    temperature_trials_chart.add_rows(new_df)

    # draw fitness graph
    st.header(strings.fitness_graph_header)
    fitness_chart = st.line_chart()

    new_df = pd.DataFrame({
        'trials': [0],
        'Fitness': [float(current_result[0]['best_fitness'])]
    }).rename(columns={'trials': 'index'}).set_index('index')

    fitness_chart.add_rows(new_df)

    # draw results
    with st.beta_container():
        # separator
        st.markdown(body=separator_body, unsafe_allow_html=True)

        st.header(strings.initial_params_header)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.temperature_msg)
            col_value.markdown(f'<span style="color:#26ba1b">**{initial_temperature}**</span>',
                               unsafe_allow_html=True)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.cooling_coeff_msg)
            col_value.markdown(f'<span style="color:#26ba1b">**{cooling_coeff}**</span>',
                               unsafe_allow_html=True)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.computing_time_msg)
            col_value.markdown(
                f'<span style="color:#26ba1b">**{computing_time} s**</span>',
                unsafe_allow_html=True)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.trials_neighbor_msg)
            col_value.markdown(f'<span style="color:#26ba1b">**{trials_number}**</span>',
                               unsafe_allow_html=True)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.trials_temperature_msg)
            col_value.markdown(f'<span style="color:#26ba1b">**{attempts_in_each_level_of_temperature}**</span>',
                               unsafe_allow_html=True)

        st.header(strings.results_found_with_this_params)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.initial_ruler_msg)
            col_value.markdown(f'<span style="color:#26ba1b">**{str(current_result[0]["initial_ruler"])}**</span>',
                               unsafe_allow_html=True)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.best_ruler_founded_msg)
            col_value.markdown(f'<span style="color:#26ba1b">**{str(current_result[0]["best_ruler"])}**</span>',
                               unsafe_allow_html=True)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.best_fitness_msg)
            col_value.markdown(
                f'<span style="color:#26ba1b">**{str(current_result[0]["best_fitness"])}**</span>',
                unsafe_allow_html=True)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.run_time_msg)
            col_value.markdown(f'<span style="color:#26ba1b">**{current_result[0]["runtime"]} s**</span>',
                               unsafe_allow_html=True)

    for n in range(trials_number):
        # generate neighbor solution
        initial_temperature = random.uniform(50.0, 50000.0)  # initial temperature
        cooling_coeff = random.uniform(0.1, 0.99)  # cooling coefficient
        computing_time = random.uniform(0.1, 20.0)  # in seconds
        trials_number = random.randint(1, 50)  # number or trials to get neighborhood before use random one
        attempts_in_each_level_of_temperature = random.randint(1,
                                                               300)  # number of attempts in each level of temperature

        problem_function(marks_count, max_bound, initial_temperature, cooling_coeff,
                         computing_time, trials_number, attempts_in_each_level_of_temperature,
                         '', None, True, None, results, 0, False)

        neighbor_result = results.copy()

        # check if neighbor solution is better than the current one
        if neighbor_result[0]["best_fitness"] < current_result[0]["best_fitness"] or (neighbor_result[0]["best_fitness"]
                                                                                      == current_result[0][
                                                                                          "best_fitness"] and
                                                                                      neighbor_result[0]["runtime"] <
                                                                                      current_result[0]["runtime"]):
            # record best params
            best_params["initial_temperature"] = initial_temperature
            best_params["cooling_coeff"] = cooling_coeff
            best_params["computing_time"] = computing_time
            best_params["trials_number"] = trials_number
            best_params["attempts_in_each_level_of_temperature"] = attempts_in_each_level_of_temperature

            # record best results
            best_result[0]["initial_ruler"] = neighbor_result[0]["initial_ruler"]
            best_result[0]["best_ruler"] = neighbor_result[0]["best_ruler"]
            best_result[0]["best_fitness"] = neighbor_result[0]["best_fitness"]
            best_result[0]["runtime"] = neighbor_result[0]["runtime"]

        # params graph

        # temperature graph
        new_df = pd.DataFrame({
            'trials': [n + 1],
            'Température': [float(initial_temperature)]
        }).rename(columns={'trials': 'index'}).set_index('index')

        temperature_chart.add_rows(new_df)

        # cooling coeff graph
        new_df = pd.DataFrame({
            'trials': [n + 1],
            'Refroidissement Coéff': [float(cooling_coeff)]
        }).rename(columns={'trials': 'index'}).set_index('index')

        cooling_coeff_chart.add_rows(new_df)

        # computing time graph
        new_df = pd.DataFrame({
            'trials': [n + 1],
            'Temp de calcul': [float(computing_time)]
        }).rename(columns={'trials': 'index'}).set_index('index')

        computing_time_chart.add_rows(new_df)

        # trials neighbor graph
        new_df = pd.DataFrame({
            'trials': [n + 1],
            'Tentatives voisin': [float(trials_number)]
        }).rename(columns={'trials': 'index'}).set_index('index')

        neighbor_trials_chart.add_rows(new_df)

        # trials temperature  graph
        new_df = pd.DataFrame({
            'trials': [n + 1],
            'Tentatives température': [float(attempts_in_each_level_of_temperature)]
        }).rename(columns={'trials': 'index'}).set_index('index')

        temperature_trials_chart.add_rows(new_df)

        # fitness graph
        new_df = pd.DataFrame({
            'trials': [n + 1],
            'Fitness': [float(neighbor_result[0]['best_fitness'])]
        }).rename(columns={'trials': 'index'}).set_index('index')

        fitness_chart.add_rows(new_df)

    # draw results

    with st.beta_container():
        # separator
        st.markdown(body=separator_body, unsafe_allow_html=True)

        st.header(strings.best_params_header)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.temperature_msg)
            col_value.markdown(f'<span style="color:#26ba1b">**{str(best_params["initial_temperature"])}**</span>',
                               unsafe_allow_html=True)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.cooling_coeff_msg)
            col_value.markdown(f'<span style="color:#26ba1b">**{str(best_params["cooling_coeff"])}**</span>',
                               unsafe_allow_html=True)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.computing_time_msg)
            col_value.markdown(
                f'<span style="color:#26ba1b">**{str(best_params["computing_time"])} s**</span>',
                unsafe_allow_html=True)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.trials_neighbor_msg)
            col_value.markdown(f'<span style="color:#26ba1b">**{str(best_params["trials_number"])}**</span>',
                               unsafe_allow_html=True)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.trials_temperature_msg)
            col_value.markdown(
                f'<span style="color:#26ba1b">**{str(best_params["attempts_in_each_level_of_temperature"])}**</span>',
                unsafe_allow_html=True)

        st.header(strings.results_found_with_this_params)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.initial_ruler_msg)
            col_value.markdown(f'<span style="color:#26ba1b">**{str(best_result[0]["initial_ruler"])}**</span>',
                               unsafe_allow_html=True)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.best_ruler_founded_msg)
            col_value.markdown(f'<span style="color:#26ba1b">**{str(best_result[0]["best_ruler"])}**</span>',
                               unsafe_allow_html=True)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.best_fitness_msg)
            col_value.markdown(
                f'<span style="color:#26ba1b">**{str(best_result[0]["best_fitness"])}**</span>',
                unsafe_allow_html=True)

        with st.beta_container():
            col_title, col_value = st.beta_columns([2, 3])

            col_title.write(strings.run_time_msg)
            col_value.markdown(f'<span style="color:#26ba1b">**{best_result[0]["runtime"]} s**</span>',
                               unsafe_allow_html=True)


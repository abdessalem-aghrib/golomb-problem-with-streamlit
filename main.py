import random
import time

import streamlit as st
import simulated_annealing as sa
import genetic as genetic
import pandas as pd
import strings as strings
import threading

# separator
separator_body = '<hr style="margin-top:40px;margin-bottom:50px;border-top:2px solid ' \
                 '#bbb;border-radius:5px;color:#90939b;background-color:#90939b;" />'

genetic_id = 0
simulated_annealing_id = 1


def simulated_annealing_style(sidebar):
    st.title(strings.simulated_annealing_title)
    with sidebar:
        input_marks_count = st.number_input(strings.input_marks_count_header, min_value=3, max_value=500, value=4)
        input_max_bound = st.number_input(strings.input_max_bound_header, min_value=20, max_value=100000, value=100)
        input_temperature = st.number_input(strings.input_temperature_header, min_value=500.0, max_value=500000.0,
                                            value=1000.0)
        input_cooling_coeff = st.number_input(strings.input_cooling_coeff_header, min_value=0.1, max_value=0.99,
                                              value=0.7)
        input_computing_time = st.number_input(strings.input_computing_time_header, min_value=2.0, max_value=1000000.0,
                                               value=20.0)
        input_trials_number = st.number_input(strings.input_trials_number_header, min_value=5,
                                              max_value=1000, value=20)
        input_attempts_in_each_level_of_temperature = st.number_input(
            strings.input_attempts_in_each_level_of_temperature_header, min_value=10, max_value=10000, value=100)

        st.write('')
        start_bu = st.button(strings.start_bu_text)

    if start_bu:
        st.header(strings.simulated_annealing_graph_header)

        # draw line chart
        y_axis_title = 'Fitness'

        chart = st.line_chart()

        sa.simulated_annealing(marks_count=input_marks_count, max_bound=input_max_bound,
                               initial_temperature=input_temperature, cooling_coeff=input_cooling_coeff,
                               computing_time=input_computing_time, trials_number=input_trials_number,
                               attempts_in_each_level_of_temperature
                               =input_attempts_in_each_level_of_temperature,
                               y_axis_title=y_axis_title, chart=chart, with_lock=False, thread_lock=None,
                               result=None, index=simulated_annealing_id)


def genetic_style(sidebar):
    st.title(strings.genetic_title)
    with sidebar:
        input_marks_count = st.number_input(strings.input_marks_count_header, min_value=3, max_value=500, value=4)
        input_max_bound = st.number_input(strings.input_max_bound_header, min_value=20, max_value=100000, value=100)
        input_population_size = st.number_input(strings.input_population_size_header, min_value=2,
                                                max_value=1000, value=10)
        input_generation_count = st.number_input(strings.input_generation_count_header, min_value=2,
                                                 max_value=1000, value=5)
        input_crossing_probability = st.number_input(strings.input_crossing_probability_header, min_value=0.1,
                                                     max_value=1.0,
                                                     value=0.7)
        input_mutation_probability = st.number_input(strings.input_mutation_probability_header, min_value=0.1,
                                                     max_value=1.0,
                                                     value=0.2)
        input_size_of_bits = st.number_input(strings.input_population_size_header, min_value=4, max_value=20,
                                             value=10)
        input_max_trying_time_for_correct_ruler = st.number_input(
            strings.input_max_trying_time_for_correct_ruler_header,
            min_value=1.0, max_value=3600.0,
            value=10.0)

        st.write('')
        start_bu = st.button(strings.start_bu_text)

    if start_bu:
        st.header(strings.genetic_graph_header)

        # draw line chart
        y_axis_title = 'Fitness'

        chart = st.line_chart()

        genetic.genetic(population_size=input_population_size, generation_count=input_generation_count,
                        crossing_probability=input_crossing_probability,
                        mutation_probability=input_mutation_probability, marks_count=input_marks_count,
                        max_bound=input_max_bound, size_of_bits=input_size_of_bits,
                        max_trying_time_for_correct_ruler=input_max_trying_time_for_correct_ruler,
                        y_axis_title=y_axis_title, chart=chart, with_lock=False, thread_lock=None, result=None,
                        index=genetic_id)


def comparison_style(sidebar):
    st.title(strings.comparison_title)

    with sidebar:
        # common parameters inputs
        st.header(strings.common_parameters_header)

        input_marks_count = st.number_input(strings.input_marks_count_header, min_value=3, max_value=500, value=4)
        input_max_bound = st.number_input(strings.input_max_bound_header, min_value=20, max_value=100000, value=100)

        # separator
        st.markdown(body=separator_body, unsafe_allow_html=True)

        # simulated annealing parameters inputs
        st.header(strings.simulated_annealing_parameters_header)

        input_temperature = st.number_input(strings.input_temperature_header, min_value=500.0, max_value=500000.0,
                                            value=1000.0)
        input_cooling_coeff = st.number_input(strings.input_cooling_coeff_header, min_value=0.1, max_value=0.99,
                                              value=0.7)
        input_computing_time = st.number_input(strings.input_computing_time_header, min_value=2.0, max_value=1000000.0,
                                               value=20.0)
        input_trials_number = st.number_input(strings.input_trials_number_header, min_value=5,
                                              max_value=1000, value=20)
        input_attempts_in_each_level_of_temperature = st.number_input(
            strings.input_attempts_in_each_level_of_temperature_header, min_value=10, max_value=10000, value=100)

        # separator
        st.markdown(body=separator_body, unsafe_allow_html=True)

        # genetic parameters inputs
        st.header(strings.genetic_parameters_header)

        input_population_size = st.number_input(strings.input_population_size_header, min_value=2,
                                                max_value=1000, value=10)
        input_generation_count = st.number_input(strings.input_generation_count_header, min_value=2,
                                                 max_value=1000, value=5)
        input_crossing_probability = st.number_input(strings.input_crossing_probability_header, min_value=0.1,
                                                     max_value=1.0,
                                                     value=0.7)
        input_mutation_probability = st.number_input(strings.input_mutation_probability_header, min_value=0.1,
                                                     max_value=1.0,
                                                     value=0.2)
        input_size_of_bits = st.number_input(strings.input_population_size_header, min_value=4, max_value=20,
                                             value=10)
        input_max_trying_time_for_correct_ruler = st.number_input(
            strings.input_max_trying_time_for_correct_ruler_header,
            min_value=1.0, max_value=3600.0,
            value=10.0)

        st.write('')
        start_bu = st.button(strings.start_bu_text)

    if start_bu:
        st.header(strings.genetic_graph_header)

        # draw line chart
        chart = st.line_chart()

        thread_lock = threading.Lock()

        # 0 : for genetic results , 1 : for simulated annealing results
        results = [None] * 2

        t1 = threading.Thread(target=genetic.genetic, args=[
            input_population_size, input_generation_count, input_crossing_probability, input_mutation_probability,
            input_marks_count, input_max_bound, input_size_of_bits, input_max_trying_time_for_correct_ruler,
            'Génétique', chart, True, thread_lock, results, genetic_id
        ])
        st.report_thread.add_report_ctx(t1)

        t2 = threading.Thread(target=sa.simulated_annealing, args=[
            input_marks_count, input_max_bound, input_temperature, input_cooling_coeff,
            input_computing_time, input_trials_number, input_attempts_in_each_level_of_temperature,
            'Recuit simulé', chart, True, thread_lock, results, simulated_annealing_id
        ])
        st.report_thread.add_report_ctx(t2)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        # write results
        st.header(strings.results_header)
        st.write(results)


def main():
    sidebar = st.sidebar.beta_container()

    with sidebar:

        menu = [strings.simulated_annealing_menu, strings.genetic_menu, strings.comparison_menu, strings.test_menu]
        choice = st.selectbox(label=strings.input_algorithm_choice_header, options=menu)

        # separator
        st.markdown(body=separator_body, unsafe_allow_html=True)

    if choice == strings.simulated_annealing_menu:
        simulated_annealing_style(sidebar)

    elif choice == strings.genetic_menu:
        genetic_style(sidebar)

    elif choice == strings.comparison_menu:
        comparison_style(sidebar)

    elif choice == strings.test_menu:

        start_time = time.time()


if __name__ == '__main__':
    main()

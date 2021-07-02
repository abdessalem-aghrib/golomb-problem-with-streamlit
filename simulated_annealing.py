import time
import random
import math
import golomb as golomb
import streamlit as st
import pandas as pd
import strings as strings


# -----------------------------------


def objective_function(ruler: list[int]) -> int:
    return ruler[len(ruler) - 1] - ruler[0]


def neighborhood_function(current_ruler: list[int], marks_count: int, trials_number: int) -> list[int]:

    max_bound = current_ruler[marks_count - 1]

    interval = [k for k in range(1, max_bound, 1) if k not in current_ruler]

    # try to correct the current ruler
    stop = False
    for i in range(marks_count - 1, 0, -1):
        if not stop:
            for item in interval:
                temp_ruler = current_ruler.copy()
                temp_ruler[i] = item
                temp_ruler.sort()

                # check if golomb ruler
                if golomb.is_golomb_ruler(temp_ruler) and temp_ruler != current_ruler:
                    return temp_ruler

                trials_number -= 1

                if trials_number == 0:
                    stop = True
                    break

    '''
    # try to find best neighbor while trials > 0
    while trials_number > 0:
        random_position = random.randint(1, marks_count - 1)
        random_number = random.randint(1, current_ruler[random_position])

        # create a temp ruler
        temp_ruler = current_ruler.copy()

        temp_ruler[random_position] -= random_number

        temp_ruler.sort()

        # check if golomb ruler (correct ruler)
        if golomb.is_golomb_ruler(temp_ruler):
            return temp_ruler

        trials_number -= 1
    '''


    # if fail to find best neighbor, generate a random one
    return golomb.generate_golomb_ruler(marks_count, max_bound, max_generate_time=10.0)


def simulated_annealing(marks_count: int, max_bound: int,
                        initial_temperature: float, cooling_coeff: float, computing_time: float,
                        trials_number: int, attempts_in_each_level_of_temperature: int, y_axis_title: str,
                        chart, with_lock=False, thread_lock=None, result=None, index=1, draw_graph=True):
    # begin time
    start = time.time()
    initial_ruler = golomb.generate_golomb_ruler(marks_count, max_bound, max_generate_time=3600)

    current_ruler = initial_ruler.copy()
    best_ruler = initial_ruler.copy()
    best_ruler_saved = initial_ruler.copy()

    n = 1  # number of accepted rulers
    i = 1  # iteration number

    best_fitness = objective_function(best_ruler)
    current_temperature = initial_temperature  # current temperature
    # record_best_fitness = []

    # stop by computing time
    while (time.time() - start) < computing_time:
        for j in range(attempts_in_each_level_of_temperature):

            current_ruler = neighborhood_function(current_ruler, marks_count, trials_number)

            if len(current_ruler) == 0:
                current_ruler = best_ruler

            current_fitness = objective_function(current_ruler)

            if current_fitness > best_fitness:
                try:
                    p = math.exp((best_fitness - current_fitness) / current_temperature)
                except:
                    pass
                r = random.random()

                # make a decision to accept the worse ruler or not
                if r < p:
                    accept = True  # this worse ruler is accepted
                else:
                    accept = False  # this worse ruler is not accepted
            else:
                accept = True  # accept better ruler
                if objective_function(best_ruler_saved) > current_fitness:
                    best_ruler_saved = current_ruler.copy()

            if accept:
                best_ruler = current_ruler.copy()  # update the best ruler
                best_fitness = objective_function(best_ruler)
                n = n + 1  # count the rulers accepted

            if draw_graph:
                # draw line chart
                new_df = pd.DataFrame({
                    'time': [time.time() - start],
                    y_axis_title: [current_fitness]
                }).rename(columns={'time': 'index'}).set_index('index')

                if with_lock:
                    thread_lock.acquire()
                    chart.add_rows(new_df)
                    thread_lock.release()
                else:
                    chart.add_rows(new_df)

            if (time.time() - start) > computing_time:
                break
        # end For Loop

        i += 1  # increment iterations number
        # record_best_fitness.append(best_fitness)

        # cooling the temperature
        current_temperature = current_temperature * cooling_coeff

    # end While Loop

    # end time
    end = time.time() - start

    # write results
    if not with_lock:
        st.header(strings.results_header)

        col_title, col_value = st.beta_columns([2, 3])

        col_title.write(strings.initial_ruler_msg)
        col_value.markdown(f'<span style="color:#26ba1b">**{str(initial_ruler)}**</span>', unsafe_allow_html=True)

        col_title.write(strings.best_ruler_founded_msg)
        col_value.markdown(f'<span style="color:#26ba1b">**{str(best_ruler_saved)}**</span>', unsafe_allow_html=True)

        col_title.write(strings.best_fitness_msg)
        col_value.markdown(
            f'<span style="color:#26ba1b">**{str(best_ruler_saved[len(best_ruler_saved) - 1])}**</span>',
            unsafe_allow_html=True)

        col_title.write(strings.run_time_msg)
        col_value.markdown(f'<span style="color:#26ba1b">**{time.time() - start} s**</span>', unsafe_allow_html=True)

    else:
        result[index] = {"initial_ruler": initial_ruler,
                         "best_ruler": best_ruler_saved,
                         "best_fitness": best_ruler_saved[len(best_ruler_saved) - 1],
                         "runtime": end
                         }

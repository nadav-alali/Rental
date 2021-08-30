import constants
from algorithms.local_search import local_search
from algorithms.q_learner import get_vehicles
from environment.environment_factory import environment_factory
from helper_functions import *
import numpy as np
import matplotlib.pyplot as plt
from vehicle_assignment import vehicle_assignment
import sys


def extract_user_input(user_input: list):
    """
    checks if the given user's input is valid and extract's it
    :param user_input:
    :return: extracted user's input
    """
    if len(user_input) == 0:
        # default assignment
        return q_learneing_str, hill_climbing_str, default_costumers_num, default_vehicles_types,\
               default_vehicles_for_rental
    elif len(user_input) < arguments_num:
        print(invalid_arguments_num)
        exit(EXIT_ERR)

    purchase_algorithm, assignment_algorithm, costumers_num, vehicle_num_types, vehicles_num = user_input

    # check if the first algorithm was typed correctly
    if purchase_algorithm not in valid_purchase_algorithmm:
        print(invalid_purchase_error)
        exit(EXIT_ERR)

    # check if the second algorithm was typed correctly
    if assignment_algorithm not in valid_assignment_algorithmm:
        print(invalid_assignment_error)
        exit(EXIT_ERR)

    # check population validity
    if not costumers_num.isnumeric() or int(costumers_num) <= 0:
        print(invalid_population_size)
        exit(EXIT_ERR)

    # check vehicles variety validity
    if not vehicle_num_types.isnumeric() or int(vehicle_num_types) <= 0:
        print(invalid_vehicles_num_error)
        exit(EXIT_ERR)

    # check vehicles amount validity
    if not vehicles_num.isnumeric() or int(vehicles_num) <= 0:
        print(invalid_vehicles_amount_error)
        exit(EXIT_ERR)

    return purchase_algorithm, assignment_algorithm, int(costumers_num), int(vehicle_num_types), int(vehicles_num)


def get_vehicles_and_factory(excel_writer, buying_algorithm, num_of_costumers, num_of_vehicle_type, num_of_vehicles):
    """
    creates the environment and buys the vehicles
    :param excel_writer:
    :param buying_algorithm: buy vehicles according to this algorithms
    :param num_of_costumers: num of costumers in the environment
    :param num_of_vehicle_type: if this value is 'x' then in the catalog there will be 8*x vehicles
    :param num_of_vehicles: number of vehicles that we would like to buy
    :return:
    """
    factory = environment_factory(excel_writer, num_of_costumers, num_of_vehicle_type)
    v_ranks = factory.v_ranks
    v_ranks_size = len(v_ranks)
    if buying_algorithm == constants.q_learneing_str:
        vehicles = get_vehicles(v_ranks, num_of_vehicles)
    else:
        local_search_env = local_search(range(v_ranks_size), v_ranks, first_problem_evaluation)
        search_algorithm = local_search_env.get_algorithm(buying_algorithm)
        vehicles = np.zeros(v_ranks_size)
        for i in range(num_of_vehicles):
            r = search_algorithm()
            factory.v_ranks[r] += (1 / (loss_adder_const_factor * len(v_ranks)))
            vehicles[r] += 1

    plt.bar(range(v_ranks_size), vehicles, label=buying_algorithm)
    plt.title(f'{buying_algorithm} - Vehicles purchase')
    plt.xlabel("vehicle id")
    plt.ylabel("amount")
    plt.savefig(os.path.join(get_output_path(), vehicles_bought_figure_name), dpi=200)
    plt.close()

    # update excel file
    v_data = []
    for i in range(v_ranks_size):
        v_data.append([factory.vehicles[i].id, vehicles[i]])
    df_v = pd.DataFrame(v_data, columns=constants.bought_vehicles_cols)
    write_to_excel(excel_writer, constants.bought_vehicles_sheet, df_v)
    return vehicles, factory


def assign_vehicles(excel_writer, purchase_algo: q_learneing_str, assigning_algo: hill_climbing_str,
                    factory_, vehicles_):
    """
    handles the second section of the problem
    :param excel_writer:
    :param purchase_algo: buy vehicles according to this algorithms
    :param assigning_algo: algorithm for the assignment section(local search)
    :param factory_: environment - contains costumers and vehicles
    :param vehicles_: vehicles that were purchase in the previous section
    :return: nothing
    """
    num_of_vehicles_in_car_lot = int(np.sum(vehicles_))
    costumers_num = len(factory_.costumers)
    if costumers_num >= num_of_vehicles_in_car_lot:
        people_who_came = np.random.choice(range(num_of_vehicles_in_car_lot // 2, num_of_vehicles_in_car_lot + 1))
    else:
        people_who_came = np.random.choice(range((2 * costumers_num) // 3, costumers_num + 1))
    costumers = np.random.choice(factory_.costumers, people_who_came, replace=False)
    assignment = vehicle_assignment(costumers, vehicles_, factory_)
    assignment.assign_vehicles_to_costumers(purchase_algo, assigning_algo)
    assignment.update_excel(excel_writer)


if __name__ == '__main__':
    buy_algorithm, assign_algorithm, population_size, vehicles_types, vehicles_num = extract_user_input(sys.argv[1:])
    writer = initialize_writer()
    print(please_wait_str)
    vehicles, factory = get_vehicles_and_factory(writer, buy_algorithm, population_size, vehicles_types, vehicles_num)
    assign_vehicles(writer, buy_algorithm, assign_algorithm, factory, vehicles)
    writer.save()
    writer.close()
    print(finished_proccess_str)

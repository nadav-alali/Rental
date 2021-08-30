import random
import pandas as pd
from constants import *
import os


def get_output_path():
    """
    :return: output result path from curr dir
    """
    dir_path = os.path.abspath(os.curdir)
    output_path = os.path.join(dir_path, output_dir_name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    return output_path


def initialize_writer():
    """
    initializes the excel writer
    :return: excel writer
    """
    output_path = os.path.join(get_output_path(), output_file_name)
    return pd.ExcelWriter(output_path, engine='xlsxwriter')


def write_to_excel(writer: pd.ExcelWriter, sheet_name: str, data_frame: pd.DataFrame):
    """
    :param writer: excel writer
    :param sheet_name: write the data frame into this sheet
    :param data_frame: data to write into the given file into a new sheet
    :return: nothing
    """
    data_frame.to_excel(writer, sheet_name)


def flip(p, f1, f2):
    """
    a function that flips a coin and with a probability of p it will return f1 and otherwise f2
    :param p: 'f1' probability
    :param f1: feature 1
    :param f2:  feature 2
    :return: f1 with a probability of p, otherwise f2
    """
    return f1 if random.random() > p else f2


def generate_object_from_multi_distributions(distributions: np.array, group: np.array):
    """
    a function that returns a value from a given group by a given distribution
    :param distributions: distribution numpy array of size N
    :param group: values array of size N (same size as distribution)
    :return: a value from the given group by the given distribution
    """
    distributions = np.cumsum(distributions)
    distributions[distributions <= 0] = np.inf
    distributions -= random.random()
    idx = (np.abs(distributions)).argmin()
    return group[idx]


def generate_normal_distribution(_mean, _sd, lower_bound, upper_bound):
    """
    generates from normal distribuations with given bounds
    :param _mean: mean
    :param _sd: Standard Deviation
    :param lower_bound: don't return values which are lower than this bound - return this bound instead
    :param upper_bound: don't return values which are greater than this bound - return this bound instead
    :return: the distribution
    """
    dist = np.random.normal(_mean, _sd, 1)[0]
    if dist < lower_bound:
        dist = lower_bound
    elif dist > upper_bound:
        dist = upper_bound
    return dist


########################### evaluation functions ##########################
def first_problem_evaluation(index, losses):
    """
    evaluates the firs problem(vehicle purchase) for the local search algorithms
    :param index: index to checks it's loss
    :param losses: losses array
    :return: the loss of the given vehicle
    """
    return losses[index]


def second_problem_evaluation(costumers_pair, domain):
    """
    evaluates the firs problem(vehicle purchase) for the local search algorithms
    :param costumers_pair: evaluate the swap loss of the two costumers
    :param domain: problems domain
    :return: swap loss - positive means that we added loss and negative means that we reduced it.
    """
    placements, table = domain[0], domain[1]
    costumer1, costumer2 = costumers_pair[0], costumers_pair[1]
    # if the second index is greater than the costumer's number then the vehicle is in the rental,
    # meanning that it's loss is 0
    if costumer2 >= len(table):
        return table[costumer1][int(placements[costumer2])] - table[costumer1][int(placements[costumer1])]
    curr_loss = table[costumer1][int(placements[costumer1])] + table[costumer2][[int(placements[costumer2])]]
    new_loss = table[costumer1][int(placements[costumer2])] + table[costumer2][[int(placements[costumer1])]]
    result = (new_loss - curr_loss)[0]
    return result

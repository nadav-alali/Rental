import random
import numpy as np


def flip(p, f1, f2):
    """
    a function that flips a coin and with a probability of p it will return f1 and otherwise f2
    :param p: 'f1' probability
    :param f1: feature 1
    :param f2:  feature 2
    :return: f1 with a probability of p, otherwise f2
    """
    return f1 if random.random() < p else f2


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


def generate_age_array():
    # todo - maybe it should be placed in the costumer class (relevant only in there)
    return [random.choice(range(1, 11)), random.choice(range(11, 17)), random.choice(range(17, 28)),
            random.choice(range(28, 39)), random.choice(range(39, 40)), random.choice(range(40, 51)),
            random.choice(range(51, 62)), random.choice(range(62, 73)), random.choice(range(73, 80)),
            random.choice(range(80, 115))]

def generate_normal_distribution(_mean, _sd, lower_bound, upper_bound):
    dist = np.random.normal(_mean, _sd, 1)[0]
    if dist < lower_bound:
        dist = lower_bound
    elif dist > upper_bound:
        dist = upper_bound
    return dist

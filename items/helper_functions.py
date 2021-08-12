import random
import numpy as np

def flip(p, f1, f2):
    return f1 if random.random() < p else f2


def generate_object_from_multi_distributions(distributions: np.array, group: np.array):
    distributions = np.cumsum(distributions)
    r = random.random()
    idx = (np.abs(distributions - r)).argmin()
    return group[idx]


def generate_age_array():
    return [random.choice(range(1, 11)), random.choice(range(11, 17)), random.choice(range(17, 28)),
            random.choice(range(28, 39)), random.choice(range(39, 40)), random.choice(range(40, 51)),
            random.choice(range(51, 62)), random.choice(range(62, 73)), random.choice(range(73, 80)),
            random.choice(range(80, 115))]
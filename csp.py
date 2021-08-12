from scipy import stats
import random
import numpy as np

def flip(p):
    return 'male' if random.random() < p else 'female'

male_counter, female_counter = 0, 0
for i in range(10):
    x = flip(0.32)
    if x == 'male':
        male_counter += 1
    else:
        female_counter += 1

def _generate_object_from_multi_distributions(distributions: np.array, group):
    distributions = np.cumsum(distributions)
    r = random.random()
    idx = (np.abs(distributions - r)).argmin()
    return group[idx]

def generate_age_array():
    return [random.choice(range(1, 11)), random.choice(range(11, 17)), random.choice(range(17, 28)),
            random.choice(range(28, 39)), random.choice(range(39, 40)), random.choice(range(40, 51)),
            random.choice(range(51, 62)), random.choice(range(62, 73)), random.choice(range(73, 80)),
            random.choice(range(80, 115))]


x = np.array([0.22, 0.11, 0.18, 0.22, 0.1, 0.08, 0.065, 0.02, 0.005])
y = [random.choice(range(1, 11)), random.choice(range(11, 17)), random.choice(range(17, 28)),
     random.choice(range(28, 39)), random.choice(range(39, 40)), random.choice(range(40, 51)),
     random.choice(range(51, 62)), random.choice(range(62, 73)), random.choice(range(73, 80)), random.choice(range(80, 115))]

for i in range(10):
    print(_generate_object_from_multi_distributions(x, y))
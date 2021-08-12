import numpy as np

################ Costumer Constants #######################
age_distributions = np.array([0.22, 0.11, 0.18, 0.22, 0.1, 0.08, 0.065, 0.02, 0.005])
num_of_children_distributions = np.array([0.23, 0.15, 0.26, 0.19, 0.1, 0.07])
income_distributions = np.array([0.11, 0.24, 0.24, 0.14, 0.08, 0.06, 0.05, 0.04, 0.03, 0.01])
questions = ['Fuel saving is more important than performance?',
             'Num of children',
             'Income',
             'Environmental care is more important than performance?',
             'Smart features',
             'Home to work distance',
             'Compact vs spacious vehicle',
             'Urbanic vs nature',
             'Safety vs mobility',
             'age']

male_prob = 0.48
two_wheels_prob = 0.08



################ Vehicle Constants #######################
engine_types = ['electrical', 'hybrid', 'gas']
engine_type_distribution = [0.04, 0.2, 0.76]

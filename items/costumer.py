import random
import numpy as np
import pandas as pd
from constants import *
from helper_functions import *


class costumer:
    def __init__(self):
        # todo how should we number a costumer?
        self.id = 0
        # todo - how can we take advantage with the age and gender parameters?
        self.age = generate_object_from_multi_distributions(age_distributions, generate_age_array())
        self.gender = flip(male_prob, 'male', 'female')
        self.num_of_children = generate_object_from_multi_distributions(num_of_children_distributions,
                                                                         [0, 1, 2, 3, 4, random.choice(range(5, 8))])
        self.income = generate_object_from_multi_distributions(income_distributions, list(range(1, 11)))  # by decile

    def fill_questionnaire(self):
        # todo - fill the questions answer
        answers_arr = []
        # Q1: Fuel saving is more important than performance?
        answers_arr.append(np.random.normal(5, 2, 1)[0])

        # Q2: Num of children
        answers_arr.append(self.num_of_children)

        # Q3: Income
        answers_arr.append(self.income)

        # Q4: Environmental care is more important than performance?
        answers_arr.append(np.random.normal(5, 2.25, 1)[0])

        # Q5: Smart features
        answers_arr.append(np.random.normal(5, 2.55, 1)[0])

        # Q6: Home to work distance
        answers_arr.append(np.random.normal(5, 2.32, 1)[0])  # todo - poisson or normal?

        # Q7: Compact vs spacious vehicle
        answers_arr.append(np.random.normal(4, 2, 1)[0])  # todo - find a justification to the distribution

        # Q8: Urbanic vs nature
        answers_arr.append(np.random.normal(4, 2.15, 1)[0])  # todo - find a justification to the distribution

        # Q9: Safety vs mobility
        # there are ~8% two wheels vehicles compared to 4 wheels
        answers_arr.append(flip(two_wheels_prob, 'mobility', 'safety'))  # todo - find a justification to the distribution

        # Q10: age
        answers_arr.append(self.age)  # todo - find a justification to the distribution
        return pd.DataFrame({'Q': questions, 'A': answers_arr})



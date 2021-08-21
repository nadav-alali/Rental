import random
import numpy as np
import pandas as pd
from constants import *
from helper_functions import *
import itertools


class costumer:
    id_iter = itertools.count()
    def __init__(self):
        self.id = next(self.id_iter)
        # todo - how can we take advantage with the age and gender parameters?
        self.age = generate_object_from_multi_distributions(age_distributions, generate_age_array())
        self.gender = flip(male_prob, 'male', 'female')  # todo - should we even use it?
        self.num_of_children = generate_object_from_multi_distributions(num_of_children_distributions,
                                                                         [0, 1, 2, 3, 4, random.choice(range(5, 8))])
        self.income = generate_object_from_multi_distributions(income_distributions, list(range(1, 11)))  # by decile

    def fill_questionnaire(self):
        answers_arr = []
        # Q1: Fuel saving is more important than performance?
        answers_arr.append(generate_normal_distribution(5, 2.51, 1, 10))

        # Q2: Num of children
        answers_arr.append(self.num_of_children)

        # Q3: Income
        answers_arr.append(self.income)

        # Q4: Environmental care is more important than performance?
        answers_arr.append(generate_normal_distribution(5, 2.321, 1, 10))

        # Q5: Smart features
        answers_arr.append(generate_normal_distribution(5, 2.573, 1, 10))

        # Q6: Home to work distance
        answers_arr.append(generate_normal_distribution(5, 2.231, 1, 10))  # todo - poisson or normal?

        # Q7: Compact vs spacious vehicle
        answers_arr.append(generate_normal_distribution(4, 2.783, 1, 10))  # todo - find a justification to the distribution

        # Q8: Urbanic vs nature
        answers_arr.append(generate_normal_distribution(4, 2.51, 1, 10))  # todo - find a justification to the distribution

        # Q9: Safety vs mobility
        # there are ~8% two wheels vehicles compared to 4 wheels
        answers_arr.append(generate_normal_distribution(5, 3.16, 0, 10))  # todo - find a justification to the distribution

        # Q10: age
        answers_arr.append(self.age)  # todo - find a justification to the distribution
        return pd.DataFrame({QUESTION: questions, ANSWER: answers_arr})



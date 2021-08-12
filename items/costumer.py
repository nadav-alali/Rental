import random
import numpy as np
import pandas as pd
from constants import *
from helper_functions import *


class costumer:
    def __init__(self):
        # todo how should we number a costumer?
        self.id = 0
        self.age = _generate_object_from_multi_distributions(age_distributions, generate_age_array())
        self.gender = _flip()
        self.num_of_children = _generate_object_from_multi_distributions(num_of_children_distributions,
                                                                         [0, 1, 2, 3, 4, random.choice(range(5-8))])
        self.income = _generate_object_from_multi_distributions(income_distributions, list(range(1-11)))  # by decile
        self.hobbies = 0

    def fill_questionnaire(self):
        # todo - fill the questions answer
        questionnaire = pd.DataFrame({'Q': questions, 'A': []})

        # Q1 : Fuel saving is more important than performance?



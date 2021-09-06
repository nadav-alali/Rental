from helper_functions import *
import itertools

def generate_age_array():
    """
    :return: array for age distribution
    """
    return [random.choice(range(1, 11)), random.choice(range(11, 17)), random.choice(range(17, 28)),
            random.choice(range(28, 39)), random.choice(range(39, 40)), random.choice(range(40, 51)),
            random.choice(range(51, 62)), random.choice(range(62, 73)), random.choice(range(73, 80)),
            random.choice(range(80, 96))]


class costumer:
    """
    Costumer class that defines a costumer object by different parameters
    """
    id_iter = itertools.count()
    def __init__(self):
        self.id = next(self.id_iter)
        self.age = generate_object_from_multi_distributions(age_distributions, generate_age_array())
        self.num_of_children = generate_object_from_multi_distributions(num_of_children_distributions,
                                                                         [0, 1, 2, 3, 4, random.choice(range(5, 7))])
        self.income = generate_object_from_multi_distributions(income_distributions, list(range(1, 11)))  # by decile
        self._questionnaire = None

    def fill_questionnaire(self):
        """
        fills the costumer questionnaire by some defined distributions
        :return: costumer's questionnaire
        """
        if self._questionnaire is None:
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
            answers_arr.append(generate_normal_distribution(5, 2.231, 1, 10))

            # Q7: Compact vs spacious vehicle
            answers_arr.append(generate_normal_distribution(4, 2.783, 1, 10))

            # Q8: Urbanic vs nature
            answers_arr.append(generate_normal_distribution(4, 2.51, 1, 10))

            # Q9: Safety vs mobility
            # there are ~8% two wheels vehicles compared to 4 wheels
            answers_arr.append(generate_normal_distribution(5, 3.16, 1, 10))

            # Q10: age
            answers_arr.append(self.age)
            self._questionnaire = pd.DataFrame({QUESTION: questions, ANSWER: answers_arr})
        return self._questionnaire

    def get_data(self):
        """
        :return: costumer's data
        """
        return [self.id, self.age, self.num_of_children, self.income] + self.fill_questionnaire()[ANSWER][:-1].tolist()



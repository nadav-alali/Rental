import numpy as np

################ Costumer Constants #######################
# age_distributions = np.array([0.22, 0.11, 0.18, 0.22, 0.1, 0.08, 0.065, 0.02, 0.005])
age_distributions = np.array([0, 0, 0.18, 0.22, 0.1, 0.08, 0.065, 0.02, 0.005])
age_distributions[age_distributions > 0] += 0.33 / 7
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

QUESTION = 'Question'
ANSWER = 'Answer'

male_prob = 0.48
two_wheels_prob = 0.08

################ Vehicle Constants #######################
engine_type_distribution = [0.04, 0.2, 0.76]
electrical_score = 3
hybrid_score = 6
gas_score = 10
auto_gear_score = 8
handle_gear_score = 4
engine_types = [electrical_score, hybrid_score, gas_score]

################ Car-lot Constants #######################
engine_type_const = "engine_type"
engine_size_const = "engine_size"
trunk_size_const = "trunk_size"
hands_const = "hands_num"
gear_const = "gear"
smart_feat_const = "smart_features"
seats_num_const = "seats_num"
price_const = "price"
insurance_const = "insurance"

questions_match = {questions[0]: [engine_type_const, engine_size_const, gear_const],
                   questions[1]: [trunk_size_const, seats_num_const],
                   questions[2]: [hands_const, price_const],
                   questions[3]: [engine_type_const, engine_size_const],
                   questions[4]: [smart_feat_const],
                   questions[5]: [hands_const, gear_const, price_const, insurance_const],
                   questions[6]: [engine_size_const, trunk_size_const, seats_num_const],
                   questions[7]: [engine_size_const, gear_const],
                   questions[8]: [insurance_const],
                   questions[9]: [insurance_const, hands_const, price_const]}

age_index = 9

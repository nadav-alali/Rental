import numpy as np

output_dir_name = 'output'
output_file_name = 'results.xlsx'
population_sheet = 'Population'
population_col_names = ['ID', 'Age', '#Childrens', 'Income', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9']
vehicles_catalog_sheet = 'Vehicles Catalog'
vehicles_col_names = ['ID', 'Engine Type', 'Engine Size', 'Trunk_Size', '#Hands', 'Gear',
                      'Smart Features Rank', '#Seats', 'Price']
bought_vehicles_sheet = 'Bought Vehicles'
bought_vehicles_cols = ['ID', 'Amount']
vehicles_assignment_sheet = 'Assignment'
assignment_cols = ['Person ID', 'Vehicle ID']
vehicles_bought_figure_name = 'purchased_vehicles_histogram.png'
assignment_figure_name = 'loss_over_swaps.png'


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

two_wheels_prob = 0.08

################ Vehicle Constants #######################
engine_type_distribution = [0.04, 0.2, 0.76]
electrical_score = 3
hybrid_score = 6
gas_score = 10
auto_gear_score = 8
handle_gear_score = 4
engine_types = [electrical_score, hybrid_score, gas_score]

# vehicles names:
mini_str = 'mini'
private_str = 'private'
suv_str = 'suv'
manager_str = 'manager'
luxury_str = 'luxury'
family_str = 'family'
scooter_str = 'scooter'
motorcycle_str = 'motorcycle'


################ factory Constants #######################
engine_type_const = "engine_type"
engine_size_const = "engine_size"
trunk_size_const = "trunk_size"
hands_const = "hands_num"
gear_const = "gear"
smart_feat_const = "smart_features"
seats_num_const = "seats_num"
price_const = "price"
mobility_const = "mobility"

questions_match = {questions[0]: [engine_type_const, engine_size_const, gear_const],
                   questions[1]: [trunk_size_const, seats_num_const],
                   questions[2]: [hands_const, price_const],
                   questions[3]: [engine_type_const, engine_size_const],
                   questions[4]: [smart_feat_const],
                   questions[5]: [hands_const, gear_const, price_const],
                   questions[6]: [engine_size_const, trunk_size_const, seats_num_const],
                   questions[7]: [engine_size_const, gear_const],
                   questions[8]: [mobility_const],
                   questions[9]: [hands_const, price_const]}

age_index = 9

######################## Q-Learner Constants #######################
scale_constant = 2
default_training_num = 1000
q_learning_epsilon = 0.25
q_learning_epsilon_decay = 0.9993

######################## Local Search Constants #######################

hill_climbing_str = "hill_climbing"
stochastic_hill_climbing_str = "stochastic_hill_climbing"
first_choice_hill_climbing_str = "first_choice_hill_climbing"
random_restart_hill_climbing_str = "random_restart_hill_climbing"
local_beam_search_str = "local_beam_search"
stochastic_local_beam_search_str = "stochastic_local_beam_search"
simulated_annealing_str = "simulated_annealing"
iteration_limit = 100
random_restart_const = 4
loss_adder_const_factor = 100
default_steps = 3
default_beam_neighbors = 3
simulated_annealing_epsilon = 0.17
simulated_annealing_iters_bound = 10



######################## Vehicle purchase Constants #######################
q_learneing_str = "q_learing"
default_costumers_num = 1000
default_vehicles_types = 5
default_vehicles_for_rental = 800
arguments_num = 5


######################## Vehicle assignment Constants #######################
swaps_num = 500


######################## Main Constants #######################
valid_purchase_algorithmm = {q_learneing_str, hill_climbing_str, stochastic_hill_climbing_str,
                             first_choice_hill_climbing_str, random_restart_hill_climbing_str, local_beam_search_str,
                             stochastic_local_beam_search_str, simulated_annealing_str}

valid_assignment_algorithmm = valid_purchase_algorithmm - {q_learneing_str}

invalid_purchase_error = f"You typed an incorrect purchase algorithm!!!\nType one of the next algorithms:\n1) " \
                       f"{q_learneing_str}\n2) {hill_climbing_str}\n3) {stochastic_hill_climbing_str}\n4)" \
                       f" {first_choice_hill_climbing_str}\n5) {random_restart_hill_climbing_str}\n6) " \
                       f"{local_beam_search_str}\n7) {stochastic_local_beam_search_str}\n8) {simulated_annealing_str}"

invalid_assignment_error = f"You typed an incorrect purchase algorithm!!!\nType one of the next algorithms:\n1) " \
                                 f"{hill_climbing_str}\n2) {stochastic_hill_climbing_str}\n3) " \
                                 f"{first_choice_hill_climbing_str}\n4) {random_restart_hill_climbing_str}\n5) " \
                                 f"{local_beam_search_str}\n6) {stochastic_local_beam_search_str}\n7) " \
                                 f"{simulated_annealing_str}"

invalid_vehicles_num_error = "The number of vehicles variation number should be an integer larger than 0!!!"

invalid_vehicles_amount_error = "You need to buy at least one vehicle!!!"

invalid_arguments_num = "You are missing some arguments!!!\nReminder:\n<purchase_algorithm> <assignment_algorithm>" \
                        " <population_size> <vehicles_variety> <vehicles_amount>"

invalid_population_size = "Population size should be an integer larger than 0!!!"

please_wait_str = "please wait..."
finished_proccess_str = "Done :)"

EXIT_ERR = 1


import helper_functions
from environment.environment_factory import *


class q_learner:
    """
    Q-Learner class
    """
    def __init__(self, rewards):
        self._size = len(rewards)
        self.rewards = rewards
        self.q_values = np.zeros(self._size)
        self.q_counter = np.zeros(self._size)

    def step(self, action):
        """
        :param action: environment action
        :return: the given action reward with added noise
        """
        assert 0 <= action < self._size
        return np.random.normal(loc=self.rewards[action], scale=self.rewards[action] / constants.scale_constant)

    def epsilon_greedy(self, episodes_number, epsilon, epsilon_factor):
        """
        :param episodes_number: number of learning episodes
        :param epsilon:
        :param epsilon_factor: decay factor for epsilon
        :return: the q_values after learning
        """
        for i in range(episodes_number):
            if helper_functions.flip(epsilon, True, False):
                action = np.random.choice(np.flatnonzero(self.q_values == self.q_values.min()))
            else:
                action = np.random.randint(self._size)
            reward = self.step(action)
            self.q_counter[action] += 1
            alpha = 1 / self.q_counter[action]
            self.q_values[action] += alpha * (reward - self.q_values[action])  # Q(a) = Q(a) + alpha * (R(a) - Q(a))
            epsilon *= epsilon_factor  # epsilon decay
        return self.q_values


def get_vehicles(vehicles_ranks, num_of_vehicles_in_car_lot):
    """
    :param vehicles_ranks: ranks of vehicles to run the learning on
    :param num_of_vehicles_in_car_lot: the amount of vehciles to buy with the Q-Learning algorithm
    :return: amount of vehicles to buy from each veihcle type
    """
    learner = q_learner(vehicles_ranks)
    vehicles_to_buy = learner.epsilon_greedy(constants.default_training_num, constants.q_learning_epsilon,
                                             constants.q_learning_epsilon_decay)
    vehicles_to_buy[vehicles_to_buy < 0] = 0  # ignore negative values -> the car lot won't buy them
    # standardize [0, 1] and after that multuply by the num of vehicles
    vehicles_to_buy = np.round((vehicles_to_buy / vehicles_to_buy.sum()) * num_of_vehicles_in_car_lot)
    q_sum_diff = int(np.sum(vehicles_to_buy) - num_of_vehicles_in_car_lot)
    complete = -1 if q_sum_diff > 0 else 1
    q_sum_diff = abs(q_sum_diff)
    q_range = range(len(vehicles_to_buy)) if complete > 0 else np.where(vehicles_to_buy > q_sum_diff)[0]
    while q_sum_diff:
        vehicles_to_buy[np.random.choice(q_range)] += complete
        q_sum_diff -= 1
    return vehicles_to_buy



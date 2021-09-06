import random
from constants import *

class local_search:
    """
    a class that defines some local search algorithms
    """
    def __init__(self, environment, domain, evaluation_func, steps=default_steps):
        self._environment = environment
        self._steps = steps
        self._size = len(environment)
        self._domain = domain
        self._evaluate = evaluation_func
        self._searches_map = {hill_climbing_str: self._hill_climbing,
                              stochastic_hill_climbing_str: self._stochastic_hill_climbing,
                              first_choice_hill_climbing_str: self._first_choice_hill_climbing,
                              random_restart_hill_climbing_str: self._random_restart_hill_climbing,
                              local_beam_search_str: self._local_beam_search,
                              stochastic_local_beam_search_str: self._stochastic_local_beam_search,
                              simulated_annealing_str: self._simulated_annealing}

    def get_algorithm(self, algorithm_name):
        """
        :param algorithm_name: A local search algorithm name
        :return: a pointer for the algorithm's function
        """
        return self._searches_map[algorithm_name]

    def _get_neighbors(self, curr_position):
        """
        :param curr_position: curr index in the environment
        :return: the neighbors of the given index - k steps from its left and from its right
        """
        assert 0 <= curr_position < self._size
        left_bound, right_bound = curr_position - self._steps, curr_position + self._steps
        if left_bound < 0:
            left_bound = 0
        if right_bound > self._size:
            right_bound = self._size
        return list(range(left_bound, curr_position)) + list(range(curr_position + 1, right_bound))

    def _hill_climbing(self):
        """
        hill climbing implementation
        :return: minimum action (that found)
        """
        index_ = np.random.choice(range(self._size))
        solution = self._environment[index_]
        while True:
            next_eval = np.inf
            successor = -1
            index_succ = 0
            for s in self._get_neighbors(index_):
                evaluation = self._evaluate(self._environment[s], self._domain)
                if evaluation < next_eval:
                    successor = self._environment[s]
                    next_eval = evaluation
                    index_succ = s
            if next_eval >= self._evaluate(solution, self._domain):
                return solution
            solution = successor
            index_ = index_succ

    def _stochastic_hill_climbing(self):
        """
        stochastic hill climbing implementation
        :return: minimum action (that found)
        """
        index_ = np.random.choice(range(self._size))
        solution = self._environment[index_]
        solution_eval = self._evaluate(solution, self._domain)
        while True:
            possible_successors = []
            for s in self._get_neighbors(index_):
                evaluation = self._evaluate(self._environment[s], self._domain)
                # evaluation = 0 means that we neither improve nor worsen our general loss
                if evaluation < solution_eval:
                    possible_successors.append((self._environment[s], s, evaluation))
            if not possible_successors:
                return solution
            solution, index_, solution_eval = possible_successors[np.random.randint(0, len(possible_successors))]

    def _first_choice_hill_climbing(self):
        """
        first choice hill climbing implementation
        :return: minimum action (that found)
        """
        index_ = np.random.choice(range(self._size))
        solution = self._environment[index_]
        solution_eval = self._evaluate(solution, self._domain)
        while True:
            possible_successors = []
            for s in self._get_neighbors(index_):
                evaluation = self._evaluate(self._environment[s], self._domain)
                if evaluation < solution_eval:
                    if np.random.choice([True, False]):
                        possible_successors = [(self._environment[s], s, evaluation)]
                        break
                    possible_successors.append((self._environment[s], s, evaluation))
            if not possible_successors:
                return solution
            solution, index_, solution_eval = possible_successors[np.random.randint(0, len(possible_successors))]

    def _random_restart_hill_climbing(self, num_of_runs=random_restart_const):
        """
        random restart hill climbing implementation
        :param num_of_runs: The amount of times that hill climbing algorithm is about to repeat
        :return: minimum action (that found)
        """
        best_solution_index = -1
        best_solution_val = np.inf
        for i in range(num_of_runs):
            hill_result = self._hill_climbing()
            evaluation = self._evaluate(hill_result, self._domain)
            if best_solution_val > evaluation:
                best_solution_index = hill_result
                best_solution_val = evaluation
        return best_solution_index

    def _local_beam_search(self, k=default_beam_neighbors, iterations_limit=iteration_limit):
        """
        local beam search algorithm implementation
        :param k: number of nearest neighbors
        :param iterations_limit: for optimization set a bound for iterations
        :return: minimum action (that found)
        """
        def append_successors(indexes):
            s = indexes.copy()
            for i in indexes:
                s += self._get_neighbors(i)
            return s
        k_neighbors = list(np.random.choice(range(self._size), k, replace=False))
        curr_best = 0

        while iterations_limit > 0:
            successors = append_successors(k_neighbors)
            ordered = sorted(successors, key=lambda m: self._evaluate(self._environment[m], self._domain))
            k_neighbors = ordered[:k]
            iterations_limit -= 1
            if k_neighbors[0] == curr_best:
                break
            curr_best = k_neighbors[0]
        return self._environment[k_neighbors[0]]

    def _stochastic_local_beam_search(self, k=default_beam_neighbors, iterations_limit=iteration_limit):
        """
        stochastic local beam search algorithm implementation
        :param k: number of nearest neighbors
        :param iterations_limit: for optimization set a bound for iterations
        :return: minimum action (that found)
        """
        def append_successors(indexes):
            s = indexes.copy()
            for i in indexes:
                s += self._get_neighbors(i)
            return s

        k_neighbors = list(np.random.choice(range(self._size), k, replace=False))
        curr_best = k_neighbors[0]

        while iterations_limit > 0:
            successors = append_successors(k_neighbors)
            probs = np.array([self._evaluate(self._environment[s], self._domain) for s in successors])
            probs += np.abs(np.min(probs))
            probs /= np.max(probs)
            random_neighbors = [successors[i] for i in np.where(random.random() > probs)[0]]
            k_neighbors = sorted(random_neighbors[:k], key=lambda m: self._evaluate(self._environment[m], self._domain))
            iterations_limit -= 1
            if not k_neighbors or k_neighbors[0] == curr_best:
                break
            curr_best = k_neighbors[0]
        return self._environment[curr_best]

    def _simulated_annealing(self, epsilon=simulated_annealing_epsilon, iterations=simulated_annealing_iters_bound):
        """
        simulated annealing algorithm implementation
        :param epsilon:
        :param iterations: for optimization
        :return: minimum action (that found)
        """
        epsilon_decay = epsilon / iterations
        index_ = np.random.choice(range(self._size))
        solution = self._environment[index_]
        solution_eval = self._evaluate(solution, self._domain)
        for i in range(iterations):
            while True:
                next_eval = np.inf
                successor = -1
                neighbors = self._get_neighbors(index_)
                curr_index = 0
                if random.random() < epsilon:
                    curr_index = np.random.choice(neighbors)
                    successor = self._environment[curr_index]
                    next_eval = self._evaluate(successor, self._domain)
                else:
                    for s in neighbors:
                        evaluation = self._evaluate(self._environment[s], self._domain)
                        if evaluation < next_eval:
                            curr_index = s
                            successor = self._environment[curr_index]
                            next_eval = evaluation
                if next_eval >= solution_eval:
                    break
                solution, index_, solution_eval = successor, curr_index, next_eval
            epsilon -= epsilon_decay
        return solution

import itertools
from algorithms import local_search
from helper_functions import *
from constants import *
import matplotlib.pyplot as plt


class vehicle_assignment:
    """
    class that handles the second section of the problem - assigning vehicles to costumers
    """
    def __init__(self, costumers, vehicles, factory):
        self._factory = factory
        self._costumers = costumers
        self._vehicles = vehicles.copy()
        self.dynamic_table = self._create_loss_table()  # rows = costumers, cols = vehicles
        self._placement = np.zeros(int(sum(vehicles)))
        self._randomize_choices()
        self._environment = self._set_environment(len(costumers), int(sum(vehicles)))

    def _set_environment(self, costumer_num, vehicles_num):
        """
        sets the class environment - creates the pairs for the local search
        :param costumer_num: number of costumers that arrived
        :param vehicles_num: number of vehicles in the rental
        :return: the costumer to costumer pair
        """
        env = list(itertools.combinations(range(costumer_num), 2))
        # add vehicles that were not given to a costumer
        for i in range(costumer_num):
            for j in range(costumer_num, vehicles_num):
                env.append((i, j))
        return sorted(env, key=lambda m: m[0])

    def _create_loss_table(self):
        """
        creates the loss table between users that arrived and vehicles that are in the rental
        :return: loss table
        """
        table = np.ones((len(self._costumers), len(self._vehicles))) * np.inf
        not_in_stock = set(np.where(self._vehicles == 0)[0])
        for i in range(len(self._costumers)):
            c = self._costumers[i]
            for j in range(len(self._vehicles)):
                if j not in not_in_stock:
                    table[i][j] = self._factory.get_costumer_match(self._factory.vehicles[j], c.fill_questionnaire(), c.age)
        return table

    def _randomize_choices(self):
        """
        assign vehicles to costumers - first try the optimal assignment , otherwise randomize
        :return: nothing
        """
        in_stock = set(np.where(self._vehicles > 0)[0])
        for i in range(len(self._placement)):
            if i >= len(self._costumers):
                v = random.sample(in_stock, 1)[0]
            else:
                v = np.argmin(self.dynamic_table[i])
                if v not in in_stock:
                    v = random.sample(in_stock, 1)[0]
            self._placement[i] = v
            self._vehicles[v] -= 1
            if self._vehicles[v] <= 0:
                in_stock.remove(v)

    def _swap(self, action):
        """
        swaps vehicles between two costumers
        :param action: indexes of the two costumers
        :return: nothing
        """
        tmp = self._placement[action[0]]
        self._placement[action[0]] = self._placement[action[1]]
        self._placement[action[1]] = tmp

    def update_excel(self, writer):
        """
        updates the excel with the final results
        :param writer: excel writer
        :return: nothing
        """
        assignment_data = []
        for i in range(len(self._costumers)):
            assignment_data.append([self._costumers[i].id, self._factory.vehicles[int(self._placement[i])].id])
        df_assignment = pd.DataFrame(assignment_data, columns=assignment_cols)
        write_to_excel(writer, vehicles_assignment_sheet, df_assignment)

    def assign_vehicles_to_costumers(self, buy_algorithm, assign_algorithm):
        """
        perform the swap assignments
        :param buy_algorithm: algorithm that was used to purchase the vehciles
        :param assign_algorithm: local search algorithm
        :return: nothing
        """
        domain = tuple((self._placement, self.dynamic_table))
        local_search_env = local_search.local_search(self._environment, domain, second_problem_evaluation)
        search_algorithm = local_search_env.get_algorithm(assign_algorithm)

        losses = [np.sum([self.dynamic_table[i][int(self._placement[i])] for i in range(len(self._costumers))])]
        for i in range(swaps_num):
            action = search_algorithm()
            reward = second_problem_evaluation(action, domain)
            if reward >= 0:
                losses.append(losses[-1])
                continue
            losses.append(losses[-1] + reward)
            self._swap(action)
        plt.plot(losses, label=f"{buy_algorithm} + {assign_algorithm}")
        plt.title("Vehicle match loss over swaps")
        plt.xlabel("#swaps")
        plt.ylabel("loss")
        plt.legend()
        plt.savefig(os.path.join(get_output_path(), assignment_figure_name), dpi=200)
        plt.close()









import environment.costumer as costumer
import environment.vehicle as vehicle
import constants
import numpy as np
from helper_functions import write_to_excel
import pandas as pd


class environment_factory:
    """
    a factory that creates the costumers and vehicles.
    Also, contains some methods to handle data from costumers and vehicles.
    """
    def __init__(self, results_writer, num_of_costumers, num_of_vehicle_type):
        # create costumers
        self.costumers = []
        costumers_data_frame = []
        for i in range(num_of_costumers):
            costumer_ = costumer.costumer()
            self.costumers.append(costumer_)
            costumers_data_frame.append(costumer_.get_data())

        df_population = pd.DataFrame(costumers_data_frame, columns=constants.population_col_names)
        write_to_excel(results_writer, constants.population_sheet, df_population)

        # fill costumer service
        self.costumers_survey = self.costumers[0].fill_questionnaire().copy()
        for c in self.costumers[1:]:
            self.costumers_survey[constants.ANSWER] += c.fill_questionnaire()[constants.ANSWER].copy()
        self.costumers_survey[constants.ANSWER] /= num_of_costumers

        # create vehicle models options
        self.vehicles = []
        vehicles_data_frame = []
        for i in range(num_of_vehicle_type):
            mini, private, suv, manager, luxury, family, scooter, motorcycle = vehicle.mini(), vehicle.private(),\
                                                                               vehicle.suv(), vehicle.manager(),\
                                                                               vehicle.luxury(), vehicle.family(),\
                                                                               vehicle.scooter(), vehicle.motorcycle()
            self.vehicles.extend([mini, private, suv, manager, luxury, family, scooter, motorcycle])
            vehicles_data_frame.extend([mini.get_data(), private.get_data(), suv.get_data(), manager.get_data(),
                                        luxury.get_data(), family.get_data(), scooter.get_data(), motorcycle.get_data()])

        df_vehicles = pd.DataFrame(vehicles_data_frame, columns=constants.vehicles_col_names)
        write_to_excel(results_writer, constants.vehicles_catalog_sheet, df_vehicles)

        # create vehicle histogram
        self.avg_age = self.costumers_survey[constants.ANSWER][constants.age_index]
        self.vehicle_histogram = [0] * len(self.vehicles)
        self._update_vehicles_losses()

        # vehicles ranking
        self.v_ranks = self.get_vehicle_scores_by_survey(self.costumers_survey)

    def _update_vehicles_losses(self):
        """
        updates the vehicle losses - each cell contains the specific vehicle loss
        :return: nothing
        """
        for index, v in enumerate(self.vehicles):
            self.vehicle_histogram[index] = self.vehicle_loss(v, self.avg_age)

    def vehicle_loss(self, v: vehicle.vehicle, age):
        """
        calculates the vehicle's loss
        :param v: vehicle
        :param age: costumer age
        :return: the vehicle's losses
        """
        vehicle_losses = np.zeros(len(constants.questions))
        for i, q in enumerate(constants.questions):
            vehicle_losses[i] = self.extract_vehicle_features(v, constants.questions_match[q], age)
        return vehicle_losses


    def extract_vehicle_features(self, v: vehicle.vehicle, features, age):
        """
        The method that match a costumer survey section to a vehicle
        :param v: vehicle
        :param features: features to consider in the calculation
        :param age: costumer's age
        :return: loss by feature
        """
        result = 0
        for feature in features:
            if feature == constants.engine_type_const:
                result += v.engine_type
            elif feature == constants.engine_size_const:
                result += v.engine_size
            elif feature == constants.trunk_size_const:
                result += v.trunk_size
            elif feature == constants.hands_const:
                result += v.num_hand
            elif feature == constants.gear_const:
                result += v.gear
            elif feature == constants.smart_feat_const:
                result += v.smart_features
            elif feature == constants.seats_num_const:
                result += v.seats_num
            elif feature == constants.price_const:
                result += v.calc_renting_price(age)
            else:
                # scooter or motorcycle
                if v.seats_num == 1:
                    result += np.random.choice(range(7, 11))
                elif v.trunk_size < 5:  # mini
                    result += np.random.choice(range(5, 7))
                else:
                    result += np.random.choice(range(1, 5))
                pass
        return result / len(features)

    def get_costumer_match(self, v, survey, age):
        """
        gets the total loss between a costumer and a vehicle
        :param v: vehicle
        :param survey: costumer's survey
        :param age: costumer's age
        :return: total loss
        """
        v_score = self.vehicle_loss(v, age)
        return np.sum(np.abs(survey[constants.ANSWER][:-1] - v_score[:-1]))

    def get_vehicle_scores_by_survey(self, survey):
        """
        fits a survey to a vehicle
        :param survey:
        :return:
        """
        vehicle_scores = np.zeros(len(self.vehicles))
        survey_answers = np.array(survey[constants.ANSWER])

        for i, v in enumerate(self.vehicle_histogram):
            vehicle_scores[i] = np.sum(np.abs(survey_answers[:-1] - v[:-1]))
        return vehicle_scores / np.sum(vehicle_scores)







import costumer
import vehicle
import constants
import numpy as np

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class car_lot(object):
    __metaclass__ = Singleton
    def __init__(self, num_of_costumers=1000, num_of_vehicle_type=5):
        # create costumers
        self.costumers = []
        for i in range(num_of_costumers):
            self.costumers.append(costumer.costumer())

        # fill costumer service
        self.costumers_survey = self.costumers[0].fill_questionnaire()
        for c in self.costumers[1:]:
            self.costumers_survey[constants.ANSWER] += c.fill_questionnaire()[constants.ANSWER]
        self.costumers_survey[constants.ANSWER] /= num_of_costumers

        # create vehicle models options
        self.vehicles = []
        for i in range(num_of_vehicle_type):
            self.vehicles.extend([vehicle.mini(), vehicle.private(), vehicle.suv(), vehicle.manager(), vehicle.luxery(),
                                  vehicle.family(), vehicle.scooter(), vehicle.motorcycle()])

        # create vehicle histogram
        avge_age = self.costumers_survey[constants.ANSWER][constants.age_index]
        self.vehicle_histogram = [0] * len(self.vehicles)
        self.update_histogram(avge_age)

        # vehicles ranking
        self.v_ranks = self.get_vehicle_scores_by_survey(self.costumers_survey, avge_age)

    def update_histogram(self, age: int):
        for index, v in enumerate(self.vehicles):
            self.vehicle_histogram[index] = self.vehicle_score(v, age)

    def vehicle_score(self, v: vehicle.vehicle, age: int):
        vehicle_scores = np.zeros(len(constants.questions))
        for i, q in enumerate(constants.questions):
            vehicle_scores[i] = self.extract_vehicle_features(v, constants.questions_match[q], age)
        return vehicle_scores

    def extract_vehicle_features(self, v: vehicle.vehicle, features: list, age: int):
        result = 0
        for feature in features:
            # todo- check if there is a switch like method in python
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
                # result += v.calc_insurance(25)  # todo- check how to apply it to each person
                pass
        return result / len(features)

    def get_vehicle_scores_by_survey(self, survey, age: int):
        vehicle_scores = np.zeros(len(self.vehicles))
        survey_answers = np.array(survey[constants.ANSWER])

        for i, v in enumerate(self.vehicle_histogram):
            v[-1] = self.vehicles[i].calc_renting_price(age)
            vehicle_scores[i] = np.sum(np.abs(survey_answers[:-1] - v[:-1]))
        return vehicle_scores

    def choose_ideal_vehicle(self, c: costumer.costumer):
        return self.vehicles[np.argmin(self.get_vehicle_scores_by_survey(c.fill_questionnaire(), c.age))]


c = car_lot()
costumer_ = c.costumers[0]
v = c.choose_ideal_vehicle(costumer_)
print(1)





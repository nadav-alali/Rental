import random
from constants import *
from helper_functions import *

def generate_gear(p, engine_type: str):
    if engine_type == electrical_score:
        return auto_gear_score
    return flip(p, auto_gear_score, handle_gear_score)

class vehicle:
    def __init__(self):
        self.engine_type = 0  # electrical, hybrid, gas
        self.engine_size = 0

        #self.environmental_pollution = 0  # on a scale from 1 to 7 while the lower the more env friendly todo - should we even use it?
        self.trunk_size = 0
        self.num_hand = random.choice(list(range(1, 5)))  # first hand, second hand....
        self.gear = 0
        self.smart_features = 0  # rank
        self._mid_insurance_cost = 0  # on a scale from 1 to 10 while the lower the more env friendly
        self.seats_num = 0
        self.price = 0  # on a scale from 1 to 10

    def calc_insurance(self, age: int):
        # todo - avoid linearity
        age_score = (100 - age) / 10
        return round((age_score * 0.65) + (self._mid_insurance_cost * 0.35))

    def update_price(self):
        pass

    def calc_renting_price(self, age):
        return 0.7 * self.price + 0.3 * self.calc_insurance(age)


    # todo - how can we use private methods in inherited class?
    def set_default_insurance(self, price):
        self._mid_insurance_cost = price


class four_wheels(vehicle):
    def __init__(self):
        super().__init__()
        self.seats_num = 4
        self.smart_features = random.choice(list(range(1, 11)))
        self.gear = generate_gear(0.74, self.engine_type)
        self.engine_type = generate_object_from_multi_distributions(engine_type_distribution, engine_types)

class mini(four_wheels):
    def __init__(self):
        super().__init__()
        self.trunk_size = random.choice(list(range(3, 4)))
        self.engine_size = 2
        self.set_default_insurance(2)
        self.price = flip(0.5, 2, 3)


class private(four_wheels):
    def __init__(self):
        super().__init__()
        self.trunk_size = random.choice(list(range(4, 6)))
        self.engine_size = 3
        self.set_default_insurance(2.6)
        self.price = flip(0.5, 3, flip(0.5, 2, 4))

class suv(four_wheels):
    def __init__(self):
        super().__init__()
        self.trunk_size = random.choice(list(range(7, 10)))
        self.engine_size = flip(0.66, 6, 7)  # six is the green section and seven is the white
        self.set_default_insurance(5.5)
        self.price = flip(0.5, 6, flip(0.5, 5, 7))

class manager(four_wheels):
    def __init__(self):
        super().__init__()
        self.trunk_size = random.choice(list(range(4, 10)))
        self.engine_size = flip(0.7, 5, 4)
        self.set_default_insurance(7.5)
        self.price = flip(0.5, 7, flip(0.5, 6, 8))

class luxery(four_wheels):
    def __init__(self):
        super().__init__()
        self.trunk_size = random.choice(list(range(3, 8)))
        self.engine_size = flip(0.66, 6, 7)
        self.insurance_cost = flip(0.57, 6, 7)
        self.set_default_insurance(8)
        self.price = flip(0.5, 9, flip(0.5, 8, 10))

class family(four_wheels):
    def __init__(self):
        super().__init__()
        self.seats_num = 7
        self.trunk_size = random.choice(list(range(7, 10)))
        self.engine_size = 3
        self.set_default_insurance(2.5)
        self.price = flip(0.5, 5, flip(0.5, 4, 6))

class two_wheels(vehicle):
    def __init__(self):
        super().__init__()
        self.seats_num = 1
        self.trunk_size = random.choice(list(range(1, 2)))
        self.smart_features = random.choice(list(range(1, 3)))
        self.gear = generate_gear(0.93, self.engine_type)
        self.engine_size = 1
        self.engine_type = flip(0.02, electrical_score, gas_score)
        self.insurance_cost = flip(0.55, 6, 7)
        self.set_default_insurance(7.5)


class scooter(two_wheels):
    def __init__(self):
        super().__init__()
        self.price = flip(0.5, 2, flip(0.5, 1, 3))

class motorcycle(two_wheels):
    def __init__(self):
        super().__init__()
        self.gear = 1 - self.gear
        self.price = flip(0.5, 4, flip(0.5, 3, 5))



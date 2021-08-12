import random
from constants import *
from helper_functions import *

def generate_gear(p, engine_type: str):
    if engine_type == 'electrical':
        return 'auto'
    return flip(p, 'auto', 'handle')

class vehicle:
    def __init__(self):
        self.engine_type = ""  # electrical, hybrid, gas
        self.engine_size = 0
        self.environmental_pollution = 0  #                                X
        self.trunk_size = 0
        self.num_hand = random.choice(list(range(1, 5)))  # first hand, second hand....
        self.gear = 0
        self.smart_features = 0  # rank
        self.insurance_cost = 0  #                                        X
        self.seats_num = 0


class four_wheels(vehicle):
    def __init__(self):
        self.seats_num = 4
        self.smart_features = random.choice(list(range(1, 11)))
        self.gear = generate_gear(0.74, self.engine_type)
        self.engine_type = generate_object_from_multi_distributions(engine_type_distribution, engine_types)

class mini(four_wheels):
    def __init__(self):
        self.trunk_size = random.choice(list(range(3, 4)))
        self.engine_size = 2

class private(four_wheels):
    def __init__(self):
        self.trunk_size = random.choice(list(range(4, 6)))
        self.engine_size = 3

class suv(four_wheels):
    def __init__(self):
        self.trunk_size = random.choice(list(range(7, 10)))
        self.engine_size = flip(0.66, 6, 7)  # six is the green section and seven is the white

class manager(four_wheels):
    def __init__(self):
        self.trunk_size = random.choice(list(range(4, 10)))
        self.engine_size = flip(0.7, 5, 4)

class luxery(four_wheels):
    def __init__(self):
        self.trunk_size = random.choice(list(range(3, 8)))
        self.engine_size = flip(0.66, 6, 7)

class family(four_wheels):
    def __init__(self):
        self.seats_num = 7
        self.trunk_size = random.choice(list(range(7, 10)))
        self.engine_size = 3

class two_wheels(vehicle):
    def __init__(self):
        self.seats_num = 1
        self.trunk_size = random.choice(list(range(1, 2)))
        self.smart_features = random.choice(list(range(1, 3)))
        self.gear = generate_gear(0.93, self.engine_type)
        self.engine_size = 1
        self.engine_type = flip(0.02, 'electrical', 'gas')


class scooter(two_wheels):
    def __init__(self):
        pass

class motorcycle(two_wheels):
    def __init__(self):
        self.gear = 1 - self.gear



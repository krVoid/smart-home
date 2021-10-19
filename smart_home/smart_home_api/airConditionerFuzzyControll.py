import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from random import randrange
import time


import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def fuzzy_controller(x, y):
    temperature = ctrl.Antecedent(np.arange(-20, 50, 1), 'temperature')
    humidity = ctrl.Antecedent(np.arange(0, 25, 1), 'humidity')
    fan_speed = ctrl.Consequent(np.arange(0, 1601, 1), 'fan_speed')

    temperature['Too-cold'] = fuzz.trapmf(temperature.universe, [-20, -20, -5, 5])
    temperature['cold'] = fuzz.trapmf(temperature.universe, [-5, 7, 10, 18])
    temperature['warm'] = fuzz.trapmf(temperature.universe, [12, 19, 23, 27])
    temperature['hot'] = fuzz.trapmf(temperature.universe, [23, 28, 33, 37])
    temperature['Too-hot'] = fuzz.trapmf(temperature.universe, [33, 40, 50, 50])
    # temperature.automf(3)
    # humidity.automf(3)
    humidity['low'] = fuzz.trimf(humidity.universe, [0, 0, 10])
    humidity['medium'] = fuzz.trimf(humidity.universe, [5, 10, 15])
    humidity['high'] = fuzz.trimf(humidity.universe, [10, 15, 20])
    # print(fan_speed.universe)
    fan_speed['low'] = fuzz.trimf(fan_speed.universe, [0, 0, 800])
    fan_speed['medium'] = fuzz.trimf(fan_speed.universe, [400, 800, 1200])
    fan_speed['high'] = fuzz.trimf(fan_speed.universe, [800, 1200, 1600])

    # temperature.view()
    # x = input()
    # humidity.view()
    # y = input()
    # fan_speed.view()
    rule1a = ctrl.Rule(temperature['hot'] | humidity['low'], fan_speed['high'])
    rule1b = ctrl.Rule(temperature['hot'] | humidity['high'], fan_speed['medium'])

    rule2 = ctrl.Rule(humidity['medium'], fan_speed['medium'])

    rule3a = ctrl.Rule(temperature['Too-hot'] | humidity['low'], fan_speed['high'])
    rule3b = ctrl.Rule(temperature['Too-hot'] |
                    humidity['high'], fan_speed['medium'])

    rule4a = ctrl.Rule(temperature['cold'] | humidity['low'], fan_speed['low'])
    rule4b = ctrl.Rule(temperature['cold'] | humidity['high'], fan_speed['low'])

    rule5a = ctrl.Rule(temperature['warm'] | humidity['low'], fan_speed['medium'])
    rule5b = ctrl.Rule(temperature['warm'] | humidity['high'], fan_speed['low'])

    rule6a = ctrl.Rule(temperature['Too-cold'] | humidity['low'], fan_speed['low'])
    rule6b = ctrl.Rule(temperature['Too-cold'] |
                    humidity['high'], fan_speed['low'])

    fan_speed_ctrl = ctrl.ControlSystem(
        [rule1a, rule1b, rule2, rule3a, rule3b, rule4a, rule4b, rule5a, rule5b, rule6a, rule6b])
    speed = ctrl.ControlSystemSimulation(fan_speed_ctrl)

    speed.input['temperature'] = int(x)
    speed.input['humidity'] = int(y)

    speed.compute()
    fan_speed.view(sim=speed)
    print('Dane z czujnika temperatury: ', x, ', z czujnika wilgotności powietrza: ', y)
    print('Wynik Fuzzy Controller: ', speed.output['fan_speed'])

    return speed.output['fan_speed'] 

for i in range(10):
    humidity = randrange(25)
    temperature = randrange(46)
    fuzzy_controller(temperature, humidity);
    # time(5)
# https://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem.html#example-plot-tipping-problem-py
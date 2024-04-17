'''Representation of single battery or battery pack'''

import json
import math


class Battery:
    def __init__(self, type, power_w, capacity_wh,
                 dod, rte, duration, isbattery_pack=0, number=1):
        self.type = type
        self.power_w = power_w

        self.dod = dod
        self.rte = rte
        self.duration = duration

        self.nominal_capacity = capacity_wh
        self.max_capacity = self.nominal_capacity * self.dod
        self.min_capacity = self.nominal_capacity * (1-self.dod)
        self.capacity = self.min_capacity

        self.isbattery_pack = isbattery_pack
        self.number = number

    def __str__(self):
        if self.isbattery_pack == 0:
            return f'{self.nominal_capacity / 1000} kWh {self.type} battery.'
        else:
            return f'{self.nominal_capacity / 1_000_000} MWh {self.type} battery pack.'

    def batteriesNeeded(self, energy):
        return math.ceil(energy / self.max_capacity)

    def batteryPack(self, number, inSeries=1):
        assert number > 0, "Cannot be less than 1 battery in a pack!"
        assert inSeries > 0, "Cannot be less than 1 battery in series!"

        self.power_w *= number
        self.nominal_capacity *= number
        self.max_capacity *= number
        self.min_capacity *= number
        self.capacity = self.nominal_capacity

        self.number = number
        self.isbattery_pack = 1

    def charge(self, energy):
        potential_soc = (self.capacity + energy) / self.nominal_capacity
        if potential_soc > 1:
            energy = self.nominal_capacity - self.capacity
            self.capacity = self.nominal_capacity        
        else:
            self.capacity += energy
        return energy

    def discharge(self, energy):
        potential_soc = (self.capacity - energy) / self.nominal_capacity
        if potential_soc < 1-self.dod:
            discharge_energy = self.capacity - self.min_capacity
            self.capacity = self.min_capacity
        else:
            discharge_energy = energy
            self.capacity -= discharge_energy
            
        if discharge_energy > energy:
            discharge_energy = energy
        if discharge_energy < 0:
            discharge_energy = 0
        return discharge_energy

    def stateOfCharge(self):
        return self.capacity / self.nominal_capacity

    @classmethod
    def from_json(cls, json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)

        return cls(data['type'], data['power_w'], data['capacity_wh'],
                   data['dod'], data['rte'], data['duration'])

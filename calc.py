from constants import *


class calc:
    def __init__(self, inputs):
        self.parents = list()
        self.childrens = list()
        self.energy_range, self.duration = self.init_elems(inputs)

    @staticmethod
    def init_elems(inputs):
        energy_range = {}
        duration = {}
        for daughter, elems in inputs.items():
            energy_range[daughter] = {Constants.min: float(elems[Constants.min]),
                                      Constants.max: float(elems[Constants.max])}
            duration[daughter] = int(elems[Constants.time])
        return energy_range, duration

    def is_parent_candidate(self, data):
        return not (data.x == -1 or data.y == -1) and data.not_found_tdc_energies() and \
               (self.energy_range[Constants.D1][Constants.min] <= data.energy_x <=
                self.energy_range[Constants.D1][Constants.max] or
                self.energy_range[Constants.D1][Constants.min] <= data.energy_x + max(
                    data.side_energies) <= self.energy_range[Constants.D1][Constants.max])

    def is_daughter_candidate(self, parent, data, key):
        return self.in_time(parent, data, key) and (
            self.energy_range[key][Constants.min] <= data.energy_x <= self.energy_range[key][Constants.max] or
            self.energy_range[key][
                Constants.min] <= data.energy_x + max(
                data.side_energies) <= self.energy_range[key][Constants.max])

    def in_daughters_candidate(self, parent, data):
        return data.not_found_tdc_energies() and data.x == parent.x and data.y == parent.y and (
            self.is_daughter_candidate(parent, data, Constants.D2)
            or self.is_daughter_candidate(parent, data, Constants.D3)
            or self.is_daughter_candidate(parent, data, Constants.D4)
            or self.is_daughter_candidate(parent, data, Constants.D5))

    def in_time(self, parent, data, key):
        return data.time - parent.time <= self.duration[key]

    def classify(self, data):
        for index, parent in enumerate(self.parents):
            if self.in_daughters_candidate(parent, data):
                self.childrens[index].append(data)

        if self.is_parent_candidate(data):
            self.parents.append(data)
            self.childrens.append([])

    def same_point(self, data):
        if self.is_parent_candidate(data):
            self.parents.append(data)
            self.childrens.append([])
        else:
            for index, parent in enumerate(self.parents):
                if self.in_daughters_candidate(parent, data):
                    self.childrens[index].append(data)

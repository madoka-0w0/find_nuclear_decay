class data_set:
    def __init__(self, data):
        self.event_num = int(data[0])
        self.x = int(data[2])
        self.energy_x = float(data[3])
        self.y = int(data[4])
        self.energy_y = float(data[5])
        self.side_energies = [0 for _ in range(16)]
        self.tdc_energies = [0 for _ in range(5)]

        size = len(data)

        for i in range(6, size - 1, 2):
            num = int(data[i])
            if 1000 <= num < 2100:
                index = num - 2000
                self.side_energies[index] = float(data[i + 1])
            elif 3000 <= num < 3005:
                index = num - 3000
                self.tdc_energies[index] = float(data[i + 1])
        self.time = int(data[size - 1])

    def __str__(self, regex=', '):
        list = [self.event_num, 0, self.x, self.energy_x, self.y, self.energy_y]
        line = regex.join(str(e) for e in list)
        for index, se in enumerate(self.side_energies):
            if se > 0:
                line += regex + str(2000 + index) + regex + str(se)
        for index, te in enumerate(self.tdc_energies):
            if te > 0:
                line += regex + str(3000 + index) + regex + str(te)
        line += regex + str(self.time)
        return line

    def not_found_tdc_energies(self):
        for energy in self.tdc_energies:
            if not energy == 0:
                return False
        return True

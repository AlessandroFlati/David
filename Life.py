class Life:
    def __init__(self, states):
        self.years = states
        self.probability = 1

    def add_next_year(self, state):
        return Life(self.years + [state])

    def get_last_year(self):
        return self.years[-1]

    def __str__(self):
        s = ""
        for k in range(0, len(self.years)):
            s += str(self.years[k]) + \
                 ("-[p={:.10f}]->".format(self.years[k + 1].probability) if k < len(self.years) - 1 else "")
        return s

    def get_until_year(self, n):
        if len(self.years) >= n:
            return Life(self.years[:n + 1])
        else:
            return self

    def calculate_probability_of_this_life(self):
        p = 1
        for y in self.years:
            p *= y.probability
        self.probability = p
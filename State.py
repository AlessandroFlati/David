class State:
    def __init__(self, person, probability):
        self.person = person
        self.probability = probability

    def __str__(self):
        return "({:d},{},{})".format(self.person.age,
                                     "ALIVE" if self.person.alive else "DEAD",
                                     "AUTONOMOUS" if self.person.autonomous else "NOT AUTONOMOUS")

from Life import Life
from State import State


class LifeTime:
    def __init__(self, person):
        self.person = person
        self.lives = [Life([State(person, 1)])]

    def calculate_lives_for_next_year(self):
        new_lives = []
        for life in self.lives:
            last_year = life.get_last_year()
            new_states = last_year.person.get_states_for_next_year()
            for new_state in new_states:
                new_lives.append(life.add_next_year(new_state))
        self.lives = new_lives
        for l in self.lives:
            l.calculate_probability_of_this_life()

    # def calculate_lives_for_next_n_years(self, n):
    #     for y in range(0, n):
    #         self.calculate_lives_for_next_year()
    #     for l in self.lives:
    #         l.calculate_probability_of_this_life()

    # def calculate_lives(self):
    #     if any(life.get_last_year().person.alive and life.get_last_year().person.age < 100 for life in self.lives):
    #         self.calculate_lives_for_next_year()
    #         self.calculate_lives()
    #     else:
    #         for l in self.lives:
    #             l.calculate_probability_of_this_life()

    # def get_lives_until_year(self, n):
    #     truncated_lives = []
    #     for life in self.lives:
    #         truncated_lives.append(life.get_until_year(n))
    #     return truncated_lives

    def get_probability_of_fundamental_states(self):
        alive_and_autonomous_probability = 0
        alive_and_not_autonomous_probability = 0
        dead_and_autonomous_probability = 0
        dead_and_not_autonomous_probability = 0

        for life in self.lives:
            final_state = life.get_last_year()
            person = final_state.person
            if person.alive and person.autonomous:
                alive_and_autonomous_probability += life.probability
            elif person.alive and not person.autonomous:
                alive_and_not_autonomous_probability += life.probability
            elif not person.alive and person.autonomous:
                dead_and_autonomous_probability += life.probability
            elif not person.alive and not person.autonomous:
                dead_and_not_autonomous_probability += life.probability

        return {
            'Alive and autonomous': alive_and_autonomous_probability,
            'Alive and not autonomous': alive_and_not_autonomous_probability,
            'Dead and autonomous': dead_and_autonomous_probability,
            'Dead and not autonomous': dead_and_not_autonomous_probability,
            'Dead': dead_and_autonomous_probability + dead_and_not_autonomous_probability,
            'Dead or not autonomous': dead_and_autonomous_probability + dead_and_not_autonomous_probability + alive_and_not_autonomous_probability,
            'Checksum': alive_and_autonomous_probability + alive_and_not_autonomous_probability + dead_and_autonomous_probability + dead_and_not_autonomous_probability
        }

    def __str__(self):
        s = ""
        for y, life in enumerate(self.lives):
            s += "\nLife #" + str(y + 1) + "\n" + str(life) + "\n"
        return s

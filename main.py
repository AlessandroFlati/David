import pandas as pd

pd.options.display.float_format = '{:.9f}'.format

qx = pd.read_excel('data/data.xlsx', sheet_name=1, index_col=0, usecols='F:G')  # morire
px = pd.DataFrame(1 - qx.values, columns=['px'], index=qx.index)  # non morire
ix = pd.read_excel('data/data.xlsx', sheet_name=1, index_col=0, usecols='C:D')  # entrare in non autonomia
ax = pd.DataFrame(1 - ix.values, columns=['ax'], index=ix.index)  # rimanere in autonomia
px_ax = pd.DataFrame(px.values * ax.values, columns=['px_ax'], index=ix.index)
px_ix = pd.DataFrame(px.values * ix.values, columns=['px_ix'], index=ix.index)
qx_ax = pd.DataFrame(qx.values * ax.values, columns=['qx_ax'], index=ix.index)
qx_ix = pd.DataFrame(qx.values * ix.values, columns=['qx_ix'], index=ix.index)


# distribution = pd.read_excel('data/data.xlsx', sheet_name=1, usecols='A',
#                              dtype={'a': np.int32})  # distribuzione per anno
# distribution.index.name = 'Età'
# distribution.index = distribution.index + 18


class Person:

    def __init__(self, age, alive, autonomous):
        self.age = age
        self.alive = alive
        self.autonomous = autonomous
        self.p_live = px.loc[age]['px']
        self.p_die = qx.loc[age]['qx']
        self.p_remain_autonomous = ax.loc[age]['ax']
        self.p_become_not_autonomous = ix.loc[age]['ix']
        self.p_live_and_remain_autonomous = px_ax.loc[age]['px_ax']
        self.p_live_and_become_not_autonomous = px_ix.loc[age]['px_ix']
        self.p_die_and_remain_autonomous = qx_ax.loc[age]['qx_ax']
        self.p_die_and_become_not_autonomous = qx_ix.loc[age]['qx_ix']

    def get_states_for_next_year(self):
        if not self.alive or self.age > 99:
            return [State(self, 1)]
        else:
            if not self.autonomous:
                return [
                    State(Person(self.age + 1, True, False), self.p_live),
                    State(Person(self.age + 1, False, False), self.p_die)
                ]
            else:
                return [
                    State(Person(self.age + 1, True, True), self.p_live_and_remain_autonomous),
                    State(Person(self.age + 1, True, False), self.p_live_and_become_not_autonomous),
                    State(Person(self.age + 1, False, True), self.p_die_and_remain_autonomous),
                    State(Person(self.age + 1, False, False), self.p_die_and_become_not_autonomous)
                ]


class State:

    def __init__(self, person, probability):
        self.person = person
        self.probability = probability

    def __str__(self):
        return "({:d},{},{})".format(self.person.age,
                                     "ALIVE" if self.person.alive else "DEAD",
                                     "AUTONOMOUS" if self.person.autonomous else "NOT AUTONOMOUS")


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

    def calculate_lives_for_next_n_years(self, n):
        for y in range(0, n):
            self.calculate_lives_for_next_year()
        for l in self.lives:
            l.calculate_probability_of_this_life()

    def calculate_lives(self):
        if any(life.get_last_year().person.alive and life.get_last_year().person.age < 100 for life in self.lives):
            self.calculate_lives_for_next_year()
            self.calculate_lives()
        else:
            for l in self.lives:
                l.calculate_probability_of_this_life()

    def get_lives(self):
        return self.lives

    def get_lives_until_year(self, n):
        truncated_lives = []
        for life in self.lives:
            truncated_lives.append(life.get_until_year(n))
        return truncated_lives

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


alive_and_autonomous = pd.DataFrame(columns=range(1, 101 - 18), index=range(18, 101))
alive_and_not_autonomous = pd.DataFrame(columns=range(1, 101 - 18), index=range(18, 101))
dead_and_autonomous = pd.DataFrame(columns=range(1, 101 - 18), index=range(18, 101))
dead_and_not_autonomous = pd.DataFrame(columns=range(1, 101 - 18), index=range(18, 101))
dead = pd.DataFrame(columns=range(1, 101 - 18), index=range(18, 101))
dead_or_not_autonomous = pd.DataFrame(columns=range(1, 101 - 18), index=range(18, 101))

people = []
for a in range(18, 101):
    lifetime = LifeTime(Person(a, True, True))
    for b in range(1, 102 - a):
        lifetime.calculate_lives_for_next_year()
        probabilities = lifetime.get_probability_of_fundamental_states()
        # print("Checksum per un individuo di età {:d} invecchiato di {:d} anni: {:.20f} ".format(a,b,probabilities['Checksum']))
        alive_and_autonomous.loc[a][b] = probabilities['Alive and autonomous']
        alive_and_not_autonomous.loc[a][b] = probabilities['Alive and not autonomous']
        dead_and_autonomous.loc[a][b] = probabilities['Dead and autonomous']
        dead_and_not_autonomous.loc[a][b] = probabilities['Dead and not autonomous']
        dead.loc[a][b] = probabilities['Dead']
        dead_or_not_autonomous.loc[a][b] = probabilities['Dead or not autonomous']

writer = pd.ExcelWriter('newData.xlsx')
alive_and_autonomous.to_excel(writer, 'Vivi e autonomi')
alive_and_not_autonomous.to_excel(writer, 'Vivi e non autonomi')
dead_and_autonomous.to_excel(writer, 'Morti da autonomi')
dead_and_not_autonomous.to_excel(writer, 'Morti da non autonomi')
dead.to_excel(writer, 'Morti')
dead_or_not_autonomous.to_excel(writer, 'Morti o non autonomi')
writer.save()

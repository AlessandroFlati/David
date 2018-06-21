from State import State
from base_probabilities import *


class Person:
    def __init__(self, age, alive, autonomous):
        self.age = age
        self.alive = alive
        self.autonomous = autonomous

        if self.age <= 100:
            self.p_live = px.loc[age]['px']
            self.p_die = qx.loc[age]['qx']
            self.p_remain_autonomous = ax.loc[age]['ax']
            self.p_become_not_autonomous = ix.loc[age]['ix']
            self.p_live_and_remain_autonomous = px_ax.loc[age]['px_ax']
            self.p_live_and_become_not_autonomous = px_ix.loc[age]['px_ix']
            self.p_die_and_remain_autonomous = qx_ax.loc[age]['qx_ax']
            self.p_die_and_become_not_autonomous = qx_ix.loc[age]['qx_ix']

    def get_states_for_next_year(self):
        if not self.alive:
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

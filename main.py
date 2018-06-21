import pandas as pd
from Person import Person
from LifeTime import LifeTime
from base_probabilities import *
from scipy.stats import chisquare

pd.options.display.float_format = '{:.9f}'.format

alive_and_autonomous_df = pd.DataFrame(columns=range(1, 101 - 18), index=range(18, 101))
alive_and_not_autonomous_df = pd.DataFrame(columns=range(1, 101 - 18), index=range(18, 101))
dead_and_autonomous_df = pd.DataFrame(columns=range(1, 101 - 18), index=range(18, 101))
dead_and_not_autonomous_df = pd.DataFrame(columns=range(1, 101 - 18), index=range(18, 101))
dead_df = pd.DataFrame(columns=range(1, 101 - 18), index=range(18, 101))
dead_or_not_autonomous_df = pd.DataFrame(columns=range(1, 101 - 18), index=range(18, 101))

for a in range(18, 101):
    lifetime = LifeTime(Person(a, True, True))
    print("*** Generazione {:d} ***".format(a))
    for b in range(1, 102-a):
        lifetime.calculate_lives_for_next_year()
        probabilities = lifetime.get_probability_of_fundamental_states()
        if "{:.10f}".format(probabilities['Checksum']) != "1.0000000000":
            print("Checksum per un individuo di età {:d} invecchiato di {:d} anni: {:.10f} ".format(a, b, probabilities['Checksum']))
        alive_and_autonomous_df.loc[a][b] = probabilities['Alive and autonomous']
        alive_and_not_autonomous_df.loc[a][b] = probabilities['Alive and not autonomous']
        dead_and_autonomous_df.loc[a][b] = probabilities['Dead and autonomous']
        dead_and_not_autonomous_df.loc[a][b] = probabilities['Dead and not autonomous']
        dead_df.loc[a][b] = probabilities['Dead']
        dead_or_not_autonomous_df.loc[a][b] = probabilities['Dead or not autonomous']

writer = pd.ExcelWriter(destination_file_url)
alive_and_autonomous_df.to_excel(writer, 'Vivi e autonomi')
alive_and_not_autonomous_df.to_excel(writer, 'Vivi e non autonomi')
dead_and_autonomous_df.to_excel(writer, 'Morti da autonomi')
dead_and_not_autonomous_df.to_excel(writer, 'Morti da non autonomi')
dead_df.to_excel(writer, 'Morti')
dead_or_not_autonomous_df.to_excel(writer, 'Morti o non autonomi')
writer.save()

print(chisquare(alive_and_autonomous_df.loc[28]))

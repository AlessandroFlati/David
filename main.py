from openpyxl import load_workbook

from LifeTime import LifeTime
from Person import Person
from base_probabilities import *
from matplotlib import pyplot as plt

pd.options.display.float_format = '{:.9f}'.format
destination_url = 'observedData.xlsx'


def xlsCreation():
    aa = pd.DataFrame(columns=range(0, 71), index=range(18, 77))
    ana = pd.DataFrame(columns=range(0, 71), index=range(18, 77))
    da = pd.DataFrame(columns=range(0, 71), index=range(18, 77))
    dna = pd.DataFrame(columns=range(0, 71), index=range(18, 77))
    sxe = pd.DataFrame(columns=range(0, 71), index=range(18, 77))
    esd = pd.DataFrame(columns=range(0, 71), index=range(18, 77))

    for a in range(18, 77):
        lifetime = LifeTime(Person(a, True, True))
        print("*** Generazione {:d} ***".format(a))
        for b in range(0, 89 - a):
            probabilities = lifetime.get_probability_of_fundamental_states()
            # if "{:.8f}".format(probabilities['Checksum']) != "1.00000000":
            #     print("Checksum per un individuo di età {:d} invecchiato di {:d} anni: {:.10f} ".format(a, b, probabilities['Checksum']))
            aa.loc[a][b] = round(probabilities['Alive and autonomous'] * population.loc[a]['population'])
            ana.loc[a][b] = round(probabilities['Alive and not autonomous'] * population.loc[a]['population'])
            da.loc[a][b] = round(probabilities['Dead and autonomous'] * population.loc[a]['population'])
            dna.loc[a][b] = round(probabilities['Dead and not autonomous'] * population.loc[a]['population'])
            sxe.loc[a][b] = aa.loc[a][b] * ix.loc[a + b]['ix']
            esd.loc[a][b] = sxe.loc[a][b] * years_in_LTC.loc[a + b]['years_in_LTC']
            lifetime.calculate_lives_for_next_year()

    sum_of_sx_expected = sxe.sum(axis=0)
    sum_of_expected_sx_duration = esd.sum(axis=0)
    sum_of_alive_and_autonomous = alive_and_autonomous.sum(axis=0)

    rate = 12000

    total_cost_for_community = sum_of_expected_sx_duration * rate
    cost_for_aa_community = total_cost_for_community.divide(sum_of_alive_and_autonomous)
    cost_for_aa_community = cost_for_aa_community.apply(lambda x: round(x, 2))
    total_cost_for_community = total_cost_for_community.apply(lambda x: round(x, 2))

    final_df = pd.DataFrame({'Costi totali': total_cost_for_community, 'Premi': cost_for_aa_community},
                            index=range(0, 71))
    final_df.index.name = 'Invecchiamento'

    w = pd.ExcelWriter(destination_url)
    aa.to_excel(w, 'Vivi e autonomi')
    ana.to_excel(w, 'Vivi e non autonomi')
    da.to_excel(w, 'Morti da autonomi')
    dna.to_excel(w, 'Morti da non autonomi')
    sxe.to_excel(w, 'Sinistri attesi')
    esd.to_excel(w, 'Sinistri attesi per durata')
    final_df.to_excel(w, 'Costi e Premi')
    w.save()
    w.close()


xlsCreation()

alive_and_autonomous = pd.read_excel(destination_url, sheet_name='Vivi e autonomi', index_col=0)
alive_and_not_autonomous = pd.read_excel(destination_url, sheet_name='Vivi e non autonomi', index_col=0)
dead_and_autonomous = pd.read_excel(destination_url, sheet_name='Morti da autonomi', index_col=0)
dead_and_not_autonomous = pd.read_excel(destination_url, sheet_name='Morti da non autonomi', index_col=0)
sx_expected = pd.read_excel(destination_url, sheet_name='Sinistri attesi', index_col=0)
expected_sx_duration = pd.read_excel(destination_url, sheet_name='Sinistri attesi per durata', index_col=0)
costs_and_premiums = pd.read_excel(destination_url, sheet_name='Costi e Premi', index_col=0)


import pandas as pd
import numpy as np

source_file_url = 'data/observedData.xlsx'

ix = pd.read_excel(source_file_url, index_col=0, usecols='A,E')  # entrare in non autonomia
ax = pd.DataFrame(1 - ix.values, columns=['ax'], index=ix.index)  # rimanere in autonomia
qx = pd.read_excel(source_file_url, index_col=0, usecols='A,F')  # morire
px = pd.DataFrame(1 - qx.values, columns=['px'], index=ix.index)  # non morire
years_in_LTC = pd.read_excel(source_file_url, index_col=0, usecols='A,G')  # anni in LTC
population = pd.read_excel(source_file_url, index_col=0, usecols='A, D')  # popolazione
px_ax = pd.DataFrame(px.values * ax.values, columns=['px_ax'], index=ix.index)
px_ix = pd.DataFrame(px.values * ix.values, columns=['px_ix'], index=ix.index)
qx_ax = pd.DataFrame(qx.values * ax.values, columns=['qx_ax'], index=ix.index)
qx_ix = pd.DataFrame(qx.values * ix.values, columns=['qx_ix'], index=ix.index)

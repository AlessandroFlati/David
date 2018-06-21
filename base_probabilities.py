import pandas as pd

source_file_url = 'data/pessimisticData.xlsx'
destination_file_url = 'newPessimisticData.xlsx'

qx = pd.read_excel(source_file_url, sheet_name=1, index_col=0, usecols='F:G')  # morire
px = pd.DataFrame(1 - qx.values, columns=['px'], index=qx.index)  # non morire
ix = pd.read_excel(source_file_url, sheet_name=1, index_col=0, usecols='C:D')  # entrare in non autonomia
ax = pd.DataFrame(1 - ix.values, columns=['ax'], index=ix.index)  # rimanere in autonomia
px_ax = pd.DataFrame(px.values * ax.values, columns=['px_ax'], index=ix.index)
px_ix = pd.DataFrame(px.values * ix.values, columns=['px_ix'], index=ix.index)
qx_ax = pd.DataFrame(qx.values * ax.values, columns=['qx_ax'], index=ix.index)
qx_ix = pd.DataFrame(qx.values * ix.values, columns=['qx_ix'], index=ix.index)
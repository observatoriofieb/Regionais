import pandas as pd
from sql.env import pega_engine_sfieb
from sqlalchemy import text

engine = pega_engine_sfieb()

with engine.begin() as conn:
    df = pd.read_sql('select * from [DB_OBSERVATORIO_SFIEB].[dbo].[dimensao_territorio_identidade_fieb]', conn)

regionais_novas = pd.read_excel('proposta mudanças e nova regional.xlsx', dtype=str)
regionais_novas = regionais_novas[['NO_TERRITORIO', 'NO_MUNICIPIO', 'Regionais FIEB antes da mudança',
       'Regionais pós mudança', 'Regionais pós nova regional']]

regionais_novas.loc[regionais_novas['Regionais pós nova regional'] == 'NOVA REGIONAL (NORDESTE)', 'Regionais pós nova regional'] = 'RMS/LITORAL NORTE'
regionais_novas.loc[regionais_novas['Regionais pós nova regional'] == 'RMS', 'Regionais pós nova regional'] = 'RMS/LITORAL NORTE'

regionais_novas = regionais_novas[['NO_MUNICIPIO', 'Regionais pós nova regional']] 
regionais_novas.columns = ['NO_MUNICIPIO', 'REGIONAIS_SA3_nova']
regionais_novas = regionais_novas.drop_duplicates()

df = df.merge(regionais_novas, on='NO_MUNICIPIO', how='left')
df = df.drop(columns='REGIONAIS_SA3')
df = df.rename(columns={'REGIONAIS_SA3_nova': 'REGIONAIS_SA3'})

with engine.begin() as conn:
    conn.execute(text('truncate table [DB_OBSERVATORIO_SFIEB].[dbo].[dimensao_territorio_identidade_fieb]'))
    df.to_sql('dimensao_territorio_identidade_fieb', conn, schema='dbo', if_exists='append', index=False)
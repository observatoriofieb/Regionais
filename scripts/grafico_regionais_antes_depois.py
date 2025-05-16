import pandas as pd
import geopandas as gpd
from geobr import read_municipality
import plotly.express as px
import plotly.graph_objects as go

gdf_regionais = gpd.read_file('gdf_regionais.gpkg')
regionais_senai_sesi = gdf_regionais[['SENAI', 'Municipio', 'SESI', 'FIEB', 'IEL', 'geometry']].copy()

regionais_senai_sesi['Regionais Pós Mudança'] = regionais_senai_sesi['FIEB'].copy()

municipios_metropolitana = ['CAMACARI', 'CANDEIAS', "DIAS D'AVILA", 'ITAPARICA', 'LAURO DE FREITAS', 
                            'MADRE DE DEUS', 'MATA DE SAO JOAO', 'POJUCA', 'SALVADOR', 
                            'SAO FRANCISCO DO CONDE', 'SAO SEBASTIAO DO PASSE', 'SIMOES FILHO',
                            'VERA CRUZ']

regionais_senai_sesi.loc[regionais_senai_sesi['Municipio'].isin(municipios_metropolitana), 'Regionais Pós Mudança'] = 'RMS'
regionais_senai_sesi['Regionais Pós Mudança'] = regionais_senai_sesi['Regionais Pós Mudança'].str.replace('LITORAL NORTE/RMS', 'LITORAL NORTE')
regionais_senai_sesi['Regionais Pós Mudança'] = regionais_senai_sesi['Regionais Pós Mudança'].str.replace('CENTRO', 'CENTRAL')
municipios_central = ['ALAGOINHAS', 'OURICANGAS', 'ARAMARI', 'PEDRAO']
regionais_senai_sesi.loc[regionais_senai_sesi['Municipio'].isin(municipios_central), 'Regionais Pós Mudança'] = 'CENTRAL'
municipios_sil = ['ITAGIBA', 'ITAMARI', 'IPIAU', 'SANTA CRUZ DA VITORIA', 'NOVA IBIA', 'IBIRATAIA', 'UBATA',
                  'BARRA DO ROCHA', 'GONGOGI']
regionais_senai_sesi.loc[regionais_senai_sesi['Municipio'].isin(municipios_sil), 'Regionais Pós Mudança'] = 'SUL'
municipios_norte = ['MONTE SANTO', 'ITIUBA', 'VARZEA DO POCO', 'CAPIM GROSSO']
regionais_senai_sesi.loc[regionais_senai_sesi['Municipio'].isin(municipios_norte), 'Regionais Pós Mudança'] = 'NORTE'

# Normalizar nomes para comparação correta
def normalizar_regiao(nome):
    if pd.isna(nome):
        return nome
    nome = nome.upper().strip()
    if nome in ['CENTRO', 'CENTRAL']:
        return 'CENTRAL'
    if nome == 'LITORAL NORTE/RMS':
        return 'LITORAL NORTE/RMS'
    if nome == 'LITORAL NORTE':
        return 'LITORAL NORTE'
    if nome == 'RMS':
        return 'RMS'
    return nome

regionais_senai_sesi['FIEB_norm'] = regionais_senai_sesi['FIEB'].apply(normalizar_regiao)
regionais_senai_sesi['Regionais Pós Mudança_norm'] = regionais_senai_sesi['Regionais Pós Mudança'].apply(normalizar_regiao)
regionais_senai_sesi

def mudou_regional(row):
    fieb = row['FIEB_norm']
    pos = row['Regionais Pós Mudança_norm']
    if fieb == pos:
        return 'Não'
    if fieb == 'LITORAL NORTE/RMS' and pos in ['LITORAL NORTE', 'RMS']:
        return 'Não'
    if pos == 'LITORAL NORTE/RMS' and fieb in ['LITORAL NORTE', 'RMS']:
        return 'Não'
    return 'Sim'

regionais_senai_sesi['Mudou Regional'] = regionais_senai_sesi.apply(mudou_regional, axis=1)

# Definir tons de azuis para as regionais e vermelho para as diferenças
color_map = {
    'CENTRAL': '#B0E0E6',        # Azul claro (PowderBlue)
    'NORTE': '#87CEEB',          # Azul céu (SkyBlue)
    'RMS': '#00BFFF', # Azul aço (SteelBlue)
    'LITORAL NORTE': 'DarkSlateGrey',  # Cinza escuro (DarkSlateGrey)
    'SUDOESTE': '#1E90FF',       # Azul Dodge (DodgerBlue)
    'EXTREMO SUL': '#000080',    # Azul marinho (Navy)
    'SUL': '#4169E1',            # Azul real (RoyalBlue)
    'OESTE': '#4682B4',         # Azul profundo (DeepSkyBlue)
    'REGIONAIS DIFERENTES': '#FF0000'  # Vermelho
}

# Criar o gráfico base
fig = px.choropleth_map(
    regionais_senai_sesi,
    geojson=regionais_senai_sesi.geometry,
    locations=regionais_senai_sesi.index,
    color='Regionais Pós Mudança',
    hover_name='Municipio',
    hover_data={
        'SENAI': True,
        'SESI': True,
        'FIEB': True,
        'IEL': True
    },
    color_discrete_map=color_map,
    category_orders={"Regionais Pós Mudança": list(color_map.keys())},
    center={"lat": -12.9, "lon": -38.5},
    zoom=5.5,
    opacity=0.7
)

# Ajustar layout final
fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    legend=dict(
        title="Legenda",
        title_font_size=12,
        font=dict(size=10),
        x=0.01,
        y=0.99,
        bgcolor='rgba(255,255,255,0.8)',
        itemsizing='constant'
    )
)

fig.show()

# Salvar o gráfico como HTML
fig.write_html('proposta_regionais_mudancas.html', include_plotlyjs='cdn')

regionais_senai_sesi[['SENAI', 'Municipio', 'SESI', 'FIEB', 'IEL', 'Regionais Pós Mudança', 'Mudou Regional']].to_excel('proposta_regionais_mudança.xlsx', index=False)
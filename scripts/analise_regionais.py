import pandas as pd
import geopandas as gpd
from geobr import read_municipality
import plotly.express as px
import plotly.graph_objects as go


regionais_senai = pd.read_excel('raw/MUNICIPIOS POR REGIONAL_050525.xlsx', dtype=str)
caminho_dimensao_municipios = r"C:\Users\jorge.sm\OneDrive - Sistema FIEB\Documentos\Observatorio\Dimensoes\Municipios\dados\dimensao_territorios_municipios.csv"
dimensao_municipios = pd.read_csv(caminho_dimensao_municipios, dtype=str)
regionais_senai = regionais_senai.merge(dimensao_municipios[['CO_MUN_IBGE_7', 'CO_MUN_RFB']], how='left', left_on='Cod_Municipio', right_on='CO_MUN_IBGE_7')
regionais_senai = regionais_senai.rename(columns={'REGIONAL': 'REGIONAL_SENAI'})
regionais_senai = regionais_senai[['REGIONAL_SENAI', 'CO_MUN_RFB', 'CO_MUN_IBGE_7']]
regionais_senai['SENAI'] = regionais_senai['REGIONAL_SENAI'].copy()
regionais_senai['REGIONAL_SENAI'] = regionais_senai['REGIONAL_SENAI'].replace('DENDEZEIROS', 'LITORAL NORTE/RMS')
regionais_senai['REGIONAL_SENAI'] = regionais_senai['REGIONAL_SENAI'].replace('METROPOLITANA', 'LITORAL NORTE/RMS')

regionais_sesi = pd.read_excel('raw/Zoneamento 2024 Atualizado _ versao validada_ SESI _BA.xlsx', dtype=str, sheet_name='Relação Municípios')
regionais_sesi = regionais_sesi.rename(columns={'Zoneamento NOVO SESI': 'REGIONAL_SESI', 'Código Município': 'CO_MUN_RFB', 'Nome do Município': 'Municipio'})
regionais_sesi = regionais_sesi[['REGIONAL_SESI', 'CO_MUN_RFB', 'Municipio']]
regionais_sesi['SESI'] = regionais_sesi['REGIONAL_SESI'].copy()
regionais_sesi['REGIONAL_SESI'] = regionais_sesi['REGIONAL_SESI'].str.upper()
regionais_sesi['REGIONAL_SESI'] = regionais_sesi['REGIONAL_SESI'].replace('LESTE', 'LITORAL NORTE/RMS')

regionais_fieb = pd.read_csv(r"C:\Users\jorge.sm\OneDrive - Sistema FIEB\Documentos\Observatorio\Dimensoes\Territorio_Identidade\dados\dimensao_territorio_territorio_identidade.csv", dtype=str)
regionais_fieb = regionais_fieb.rename(columns={'NO_REGIAO_FIEB': 'REGIONAL_FIEB'})
regionais_fieb['REGIONAL_FIEB'] = regionais_fieb['REGIONAL_FIEB'].replace('RMS', 'LITORAL NORTE/RMS')
regionais_fieb['FIEB'] = regionais_fieb['REGIONAL_FIEB'].copy()
regionais_fieb['REGIONAL_FIEB'] = regionais_fieb['REGIONAL_FIEB'].replace('CENTRO', 'CENTRAL')

regionais = regionais_senai.merge(regionais_sesi, how='outer', on='CO_MUN_RFB')
regionais = regionais.merge(regionais_fieb[['CO_MUN_RFB', 'REGIONAL_FIEB', 'FIEB']], how='left', on='CO_MUN_RFB')

def define_flag(row):
    sesi = row['REGIONAL_SESI']
    senai = row['REGIONAL_SENAI']
    fieb = row['REGIONAL_FIEB']
    
    if sesi != fieb and senai != fieb and sesi != senai:
        return 'TODAS'
    elif sesi != fieb and senai == fieb:
        return 'SESI'
    elif senai != fieb and sesi == fieb:
        return 'SENAI'
    elif sesi == senai and sesi != fieb:
        return 'FIEB'
    else:
        return None

regionais['FLAG_DIFERENTE'] = regionais.apply(define_flag, axis=1)

regionais[regionais['FLAG_DIFERENTE'].notnull()]


# Carregar geometria dos municípios do Brasil
gdf_municipios = read_municipality(year=2020, simplified=True)
gdf_municipios = gdf_municipios[gdf_municipios['abbrev_state'] == 'BA']

# Ajustes nos dados
regionais = regionais.rename(columns={'CO_MUN_IBGE_7': 'code_muni'})
regionais['code_muni'] = pd.to_numeric(regionais['code_muni'])

# Unir sua tabela com a geometria via CO_MUN_IBGE_7 (code_muni)
gdf_regionais = gdf_municipios.merge(regionais, on='code_muni', how='inner')

# Criar uma coluna nova com valor de REGIONAL_FIEB e onde FALG_DIFERENTE não é nulo mudar o valor para "Regionais Diferentes"
gdf_regionais['REGIONAL'] = gdf_regionais.apply(
    lambda x: 'REGIONAIS DIFERENTES' if pd.notnull(x['FLAG_DIFERENTE']) else x['REGIONAL_FIEB'],
    axis=1
)

# Definir tons de azuis para as regionais e vermelho para as diferenças
color_map = {
    'CENTRAL': '#B0E0E6',        # Azul claro (PowderBlue)
    'NORTE': '#87CEEB',          # Azul céu (SkyBlue)
    'LITORAL NORTE/RMS': '#4682B4', # Azul aço (SteelBlue)
    'SUDOESTE': '#1E90FF',       # Azul Dodge (DodgerBlue)
    'EXTREMO SUL': '#000080',    # Azul marinho (Navy)
    'SUL': '#4169E1',            # Azul real (RoyalBlue)
    'OESTE': '#00BFFF',          # Azul profundo (DeepSkyBlue)
    'REGIONAIS DIFERENTES': '#FF0000'  # Vermelho
}

# Criar o gráfico base
fig = px.choropleth_map(
    gdf_regionais,
    geojson=gdf_regionais.geometry,
    locations=gdf_regionais.index,
    color='REGIONAL',
    hover_name='Municipio',
    hover_data={
        'SENAI': True,
        'SESI': True,
        'FIEB': True
    },
    color_discrete_map=color_map,
    category_orders={"REGIONAL_FIEB": list(color_map.keys())},
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

fig.write_html("index.html", full_html=True, include_plotlyjs='cdn')
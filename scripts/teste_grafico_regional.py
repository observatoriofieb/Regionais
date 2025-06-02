import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go

# Substitua por seu token pessoal do Mapbox
mapbox_token = 'SEU_MAPBOX_TOKEN_AQUI'
import plotly.io as pio
pio.templates.default = "plotly_white"

# Carregar dados
gdf_regionais = gpd.read_file('gdf_regionais.gpkg')
regionais_senai_sesi = gdf_regionais[['SENAI', 'Municipio', 'SESI', 'FIEB', 'IEL', 'geometry']].copy()
regionais_senai_sesi['Regionais Pós Mudança'] = regionais_senai_sesi['FIEB'].copy()

# Reclassificar
municipios_metropolitana = ['CAMACARI', 'CANDEIAS', "DIAS D'AVILA", 'ITAPARICA', 'LAURO DE FREITAS', 
                            'MADRE DE DEUS', 'MATA DE SAO JOAO', 'POJUCA', 'SALVADOR', 
                            'SAO FRANCISCO DO CONDE', 'SAO SEBASTIAO DO PASSE', 'SIMOES FILHO',
                            'VERA CRUZ']
regionais_senai_sesi.loc[regionais_senai_sesi['Municipio'].isin(municipios_metropolitana), 'Regionais Pós Mudança'] = 'RMS'
regionais_senai_sesi['Regionais Pós Mudança'] = regionais_senai_sesi['Regionais Pós Mudança'].str.replace('LITORAL NORTE/RMS', 'NOVA_REGIONAL')
regionais_senai_sesi['Regionais Pós Mudança'] = regionais_senai_sesi['Regionais Pós Mudança'].str.replace('CENTRO', 'CENTRAL')

municipios_regional_alagoinhas = ['ALAGOINHAS', 'OURICANGAS', 'ARAMARI', 'PEDRAO']
regionais_senai_sesi.loc[regionais_senai_sesi['Municipio'].isin(municipios_regional_alagoinhas), 'Regionais Pós Mudança'] = 'NOVA_REGIONAL'

municipios_sil = ['ITAGIBA', 'ITAMARI', 'IPIAU', 'SANTA CRUZ DA VITORIA', 'NOVA IBIA', 'IBIRATAIA', 'UBATA',
                  'BARRA DO ROCHA', 'GONGOGI']
regionais_senai_sesi.loc[regionais_senai_sesi['Municipio'].isin(municipios_sil), 'Regionais Pós Mudança'] = 'SUL'

municipios_norte = ['MONTE SANTO', 'ITIUBA', 'VARZEA DO POCO', 'CAPIM GROSSO']
regionais_senai_sesi.loc[regionais_senai_sesi['Municipio'].isin(municipios_norte), 'Regionais Pós Mudança'] = 'NORTE'

# Cores
color_map = {
    'CENTRAL': '#B0E0E6',
    'NORTE': '#87CEEB',
    'RMS': '#00BFFF',
    'NOVA_REGIONAL': 'DarkSlateGrey',
    'SUDOESTE': '#1E90FF',
    'EXTREMO SUL': '#000080',
    'SUL': '#4169E1',
    'OESTE': '#4682B4',
    'REGIONAIS DIFERENTES': '#FF0000'
}

# Convert to GeoJSON for use in mapbox
geojson_data = regionais_senai_sesi.__geo_interface__

# Criar o mapa base
fig = go.Figure(go.Choroplethmapbox(
    geojson=geojson_data,
    locations=regionais_senai_sesi.index,
    z=regionais_senai_sesi['Regionais Pós Mudança'].astype(str),
    colorscale=[ [0, color_map.get(k, "#ffffff")] for k in regionais_senai_sesi['Regionais Pós Mudança'].unique()],
    showscale=False,
    marker_opacity=0.7,
    marker_line_width=0
))

# Adicionar contornos nos municípios de Alagoinhas
alagoinhas_gdf = regionais_senai_sesi[regionais_senai_sesi['Municipio'].isin(municipios_regional_alagoinhas)]

for _, row in alagoinhas_gdf.iterrows():
    geom = row['geometry']
    if geom.geom_type == 'Polygon':
        x, y = list(geom.exterior.xy[0]), list(geom.exterior.xy[1])
        fig.add_trace(go.Scattermapbox(
            lon=x,
            lat=y,
            mode='lines',
            line=dict(color=color_map['CENTRAL'], width=3),
            hoverinfo='skip',
            showlegend=False
        ))
    elif geom.geom_type == 'MultiPolygon':
        for poly in geom.geoms:
            x, y = list(geom.exterior.xy[0]), list(geom.exterior.xy[1])
            fig.add_trace(go.Scattermapbox(
                lon=x,
                lat=y,
                mode='lines',
                line=dict(color=color_map['CENTRAL'], width=3),
                hoverinfo='skip',
                showlegend=False
            ))

# Configurar layout do mapa
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_accesstoken=mapbox_token,
    mapbox_zoom=5.5,
    mapbox_center={"lat": -12.9, "lon": -38.5},
    margin={"r": 0, "t": 0, "l": 0, "b": 0}
)

fig.show()

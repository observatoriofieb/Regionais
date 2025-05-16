import geopandas as gpd
from geobr import read_municipality, read_state
import matplotlib.pyplot as plt

# Baixar os municípios da Bahia
bahia_mun = read_municipality()
bahia_mun = bahia_mun[bahia_mun['abbrev_state'] == 'BA']
bahia = read_state(code_state='BA', year=2020)


# Lista de cidades desejadas
cidades = [
    "Salvador", "Feira de Santana", "Eunápolis", "Ilhéus",
    "Brumado", "Luís Eduardo Magalhães", "Juazeiro"
]

# Converter para lowercase para facilitar comparação
bahia_mun['nome_muni_lower'] = bahia_mun['name_muni'].str.lower()
cidades_lower = [c.lower() for c in cidades]

# Filtrar os municípios desejados
alvo = bahia_mun[bahia_mun['nome_muni_lower'].isin(cidades_lower)].copy()

alvo.loc[alvo['name_muni'] == 'Feira De Santana', 'name_muni'] = 'Feira de Santana'

# Calcular centroides para localização dos textos
alvo['centroid'] = alvo.geometry.centroid

# Plotar
fig, ax = plt.subplots(figsize=(10, 10))
bahia.plot(ax=ax, color='skyblue', edgecolor='white')
alvo.set_geometry('centroid').plot(ax=ax, color='black', markersize=20)  # Apenas pontos

# Adicionar rótulos
for _, row in alvo.iterrows():
    x, y = row['centroid'].x, row['centroid'].y
    ax.text(x + 0.1, y, row['name_muni'], fontsize=9, ha='left', va='center')

# ax.set_title('Municípios Selecionados na Bahia', fontsize=14)
ax.axis('off')
plt.tight_layout()
plt.show()

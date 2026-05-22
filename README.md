<<<<<<< HEAD
# 💧 Patagônia Water Quality Monitor

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://patagonia-water-quality.streamlit.app/)

Dashboard interativo de monitoramento da qualidade da água nos principais rios da Patagônia chilena e argentina.

## 🗺️ Sobre o projeto

A Patagônia abriga alguns dos rios mais preservados do planeta. Este projeto aplica técnicas de **ciência de dados** e **visualização geoespacial** para monitorar e analisar a qualidade da água em 18 estações distribuídas pelos principais sistemas fluviais da região.

## 🛠️ Tecnologias utilizadas

- Python 3.10+
- Streamlit — dashboard interativo
- Folium — mapas geoespaciais
- Plotly — gráficos e visualizações
- Pandas — manipulação de dados

## 📊 Funcionalidades

- Mapa interativo com 18 estações de monitoramento
- Tendência histórica do IQA (2019–2024) por rio
- Análise de parâmetros: pH, oxigênio dissolvido, turbidez e temperatura
- Comparativo entre bacias do Chile e Argentina
- Download dos dados em CSV

## 🏗️ Como executar localmente

```bash
git clone https://github.com/seu-usuario/patagonia-water-quality.git
cd patagonia-water-quality
pip install -r requirements.txt
streamlit run app.py
```

## 📚 Fontes científicas

- PatagoniaMet — Dataset hidrometeorológico (2023). *Scientific Data, Nature*
- Miserendino et al. (2008) — Water Quality in Andean Patagonian Rivers. *Water, Air & Soil Pollution*
- Red Ecofluvial Patagonia — Monitoramento Rio Gallegos (2019). INTA / Secretaria de Ambiente

## 👤 Autor

**Amauri Almeida**
Análise e Desenvolvimento de Sistemas
Pós-graduação em Inteligência Artificial, Machine Learning & Ciência de Dados

[![LinkedIn](https://img.shields.io/badge/LinkedIn-perfil-blue)](https://www.linkedin.com/in/amauri-almeida26/)
=======
# 🌬️ Energia Eólica — Patagônia

**005 · CHILE & ARGENTINA · PATAGÔNIA SUL**

Análise comparativa do potencial eólico de **Punta Arenas**, **Puerto Natales** e **Rio Gallegos** — três das cidades mais ventosas do mundo. Dados históricos 2020–2024.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://patagonia-wind-energy.streamlit.app)

---

## 📋 Sobre o Projeto

Este projeto faz parte do [Portfólio de Pesquisa Ambiental](https://amaurialmeida.github.io/environmental-portfolio/) de Amauri Almeida e explora o imenso potencial de geração de energia eólica nas cidades mais ventosas da Patagônia.

Durante visitas a **Punta Arenas** (2024) e **Puerto Natales / Puerto Williams** (2025), o pesquisador vivenciou pessoalmente a força dos ventos patagônicos — incluindo um terremoto de magnitude 7+ em Puerto Williams em 02 de maio de 2025 — e decidiu quantificar cientificamente esse recurso natural extraordinário.

### Por que a Patagônia?

As três cidades estudadas estão localizadas na zona dos **Westerlies** — ventos do Oeste que circulam quase sem obstáculos no Hemisfério Sul entre as latitudes 40°S e 60°S. Essa faixa é conhecida historicamente pelos marinheiros como:

- 🌊 *Roaring Forties* — Quarenta Rugidores (40°S)
- 🌊 *Furious Fifties* — Cinquenta Furiosos (50°S)  
- 🌊 *Screaming Sixties* — Sessenta Uivantes (60°S)

---

## 🗺️ Cidades Analisadas

| Cidade | País | Vel. Média | Rajada Máx. | Potencial |
|--------|------|-----------|-------------|-----------|
| 🇨🇱 Punta Arenas | Chile | 30.2 km/h | 130 km/h | 4.200 MW |
| 🇨🇱 Puerto Natales | Chile | 26.8 km/h | 104 km/h | 1.800 MW |
| 🇦🇷 Rio Gallegos | Argentina | 27.1 km/h | 100 km/h | 3.500 MW |

---

## 📊 Funcionalidades

- **🗺️ Mapa Interativo** — Folium com marcadores clicáveis, círculos proporcionais à velocidade e corredor de ventos
- **💨 Análise do Vento** — Velocidade mensal, rajadas, rosa dos ventos interativa
- **⚡ Potencial Energético** — Simulador com turbinas configuráveis, GWh/ano, domicílios atendidos, CO₂ evitado
- **📊 Comparativo Anual** — Evolução 2020–2024, tabela comparativa, gauges de fator de capacidade
- **🔬 Curiosidades** — Contexto científico, comparação global, fenômenos meteorológicos

---

## ⚙️ Instalação Local

```bash
git clone https://github.com/amaurialmeida/patagonia-wind-energy.git
cd patagonia-wind-energy
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## 🔌 Fontes de Dados

| Fonte | Uso | Tipo |
|-------|-----|------|
| [Open-Meteo Historical API](https://archive-api.open-meteo.com) | Dados horários ERA5 | API REST gratuita |
| [Climates to Travel](https://www.climatestotravel.com) | Médias mensais Rio Gallegos | Web scraping |
| [Weather Spark](https://weatherspark.com) | Perfil climático Punta Arenas | Referência |
| [Global Wind Atlas](https://globalwindatlas.info) | Densidade de potência eólica | Download GIS |
| [MDPI Sustainability 2024](https://doi.org/10.3390/su16146082) | Potencial regional Patagônia | Paper científico |
| [BNP Paribas CIB](https://cib.bnpparibas) | Fator de capacidade Argentina | Relatório técnico |

---

## 🧮 Metodologia

### Densidade de Potência Eólica

```
P/A = ½ × ρ × v³
```

Onde:
- `ρ` = densidade do ar (~1.2 kg/m³)
- `v` = velocidade do vento em m/s
- A velocidade entra ao **cubo** — dobrar o vento = 8× mais energia

### Estimativa de Geração

```
GWh/ano = P_turbina × N_turbinas × Fator_Capacidade × 8760h
```

### Fator de Capacidade

A Patagônia argentina registra fatores de capacidade acima de **60%** (média global: ~35%), tornando-a uma das melhores regiões do mundo para geração eólica.

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|-----------|-----|
| Python 3.10+ | Linguagem principal |
| Streamlit | Interface web interativa |
| Folium + streamlit-folium | Mapa geoespacial |
| Plotly | Gráficos interativos |
| Pandas / NumPy | Processamento de dados |
| Open-Meteo API | Dados climáticos históricos |

---

## 🔭 Próximos Projetos

| # | Projeto | Status |
|---|---------|--------|
| 001 | Qualidade da Água — Patagônia | ✅ Online |
| 002 | Síndrome do Colapso das Abelhas — Brasil | ✅ Online |
| 003 | Observatório Rio Santa Rita | ✅ Online |
| **004** | **Energia Eólica — Patagônia** | **✅ Este projeto** |
| 005 | Terremotos — Patagônia Chilena e Argentina | 📋 Planejado |
| 006 | Abelhas Sem Ferrão — Brasil | 📋 Planejado |
| 007 | Moringa — Tratamento de Água no Brasil | 📋 Planejado |

---

## 👨‍🔬 Pesquisador

**Amauri Almeida de Souza Junior**

Técnico e tecnólogo em Gestão Ambiental, com formação em Análise e Desenvolvimento de Sistemas e pós-graduações em IA, Machine Learning e Ciência de Dados.

- 🌐 [Portfólio](https://amaurialmeida.github.io/environmental-portfolio/)
- 💼 [LinkedIn](https://www.linkedin.com/in/amauri-almeida26/)
- 🐙 [GitHub](https://github.com/amaurialmeida)
- 📍 São Paulo · SP · Brasil

---

*Elaborado com dados públicos de fontes científicas e meteorológicas. Para uso não-comercial e fins educacionais.*
>>>>>>> 7365cd7 (water patagonia is fully)

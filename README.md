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
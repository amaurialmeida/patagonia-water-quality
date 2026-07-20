# 💧 Patagonia Water Quality Monitoring — Chile & Argentina

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live_App-FF4B4B?logo=streamlit&logoColor=white)](https://patagonia-water-quality.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: Academic](https://img.shields.io/badge/License-Academic-blue.svg)]()
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()

🌐 **Languages:** English | [Português](README.pt-BR.md) | [Español](README.es.md)

**Independent Field Research — Water Quality Monitoring & Analysis**
Chilean & Argentine Patagonia · 2019–2024 (dataset) · Nov 2024–Oct 2025 (field research)
**Author:** Amauri Almeida de Souza Junior

---

## ❓ Research Question

> "Do the rivers of Chilean and Argentine Patagonia still show exceptional water quality despite tourism pressure, climate change, and regional agricultural activity — and how does 2024–2025 field data confirm or challenge that perception?"

**Answer:** Largely yes — the 18 monitored stations show an average Water Quality Index (WQI) of 87/100, among the highest in the world, driven by glacial origin, cold temperatures that naturally inhibit pathogens, and low industrial pressure. But the picture isn't uniform: urban-adjacent stations (Punta Arenas, Río Gallegos's mouth) score lower, and emerging pressures — Chilean salmon aquiculture, Argentine extensive ranching, and glacial retreat — mean this water heritage is exceptional but not guaranteed to last.

---

## 📊 Data Summary

| Indicator | Value |
|---|---|
| Monitoring stations | 18, across Chile 🇨🇱 and Argentina 🇦🇷 |
| Average WQI (2024) | 87/100 |
| Highest-scoring station | Beagle Channel, Puerto Williams (PA-17) — WQI 97 |
| Lowest-scoring station | Río Primero, Punta Arenas (PA-18) — WQI 72 |
| Historical dataset span | 2019–2024 |
| Field research period | Nov 2024 – Oct 2025 (11 months) |
| Primary data sources | PatagoniaMet dataset (*Scientific Data*, Nature, 2023); Red Ecofluvial Patagonia (INTA / Argentina's Secretariat of Environment) |

*Station baseline WQI values are drawn from the cited hydrometeorological datasets. Monthly and year-by-year series shown in the trend charts are modeled/simulated around those baselines for illustrative purposes and should not be read as raw, independently verified time-series measurements — see [Methodology](#-methodology).*

---

## 🔵 Key Findings

- **Average WQI of 87/100 — among the best in the world** — for comparison, European rivers average ~65 and Southeast Brazilian rivers ~58; Patagonia's geographic isolation and low industrial footprint explain this exceptional performance.
- **Chilean rivers outperform Argentine rivers** — Chilean basins (Serrano, Verde, Chico, Las Chinas) average WQI 91, versus 84 for Argentine basins (Gallegos, Coyle), reflecting greater extensive ranching activity and lower rural sanitation coverage on the Argentine side.
- **Slight improving trend near headwaters** — stations near Andean glacial sources show stable-to-improving WQI over time, while river-mouth and urban-adjacent stations show more pressure, though still within Good–Excellent range.
- **Temperature as a natural protective factor** — the ~7.5°C average river temperature naturally inhibits pathogen and coliform proliferation, contributing to high WQI even without treatment — a subantarctic climate benefit that global warming could erode.
- **Beagle Channel (PA-17) and Río Primero (PA-18) — the two extremes** — the Beagle Channel near Puerto Williams posts the highest score in the entire study (WQI 97), while Río Primero in Punta Arenas (WQI 72, "Regular") flags the clearest urban pressure signal.
- **Chilean salmon farming — a quiet long-term pressure** — although the Serrano River basin still scores high (89–92), expanding salmon aquiculture in Chilean Patagonian channels represents the region's principal long-term threat to water quality.

---

## 🗺️ Study Area

18 monitoring stations across 9 river basins: **Serrano, Verde, Penitente, Gallegos, Coyle, Chico, Las Chinas, Zamora** (Chile), the **Strait of Magellan**, and the **Beagle Channel**, spanning from Punta Arenas (~53°S) to Puerto Williams (~55°S) — the world's southernmost permanent settlement.

---

## 🔬 Methodology

```
Data sourcing     →  Historical water-quality baselines from the PatagoniaMet
                      dataset (Scientific Data, Nature, 2023) for Chilean
                      stations, and the Red Ecofluvial Patagonia (INTA /
                      Argentina's Secretariat of Environment) for the Río
                      Gallegos and Argentine basins

WQI calculation    →  Water Quality Index (0–100) as a weighted average of
                      pH (weight 0.12), dissolved oxygen (0.17), turbidity
                      (0.08), temperature (0.10), and other parameters
                      Bands: Excellent ≥90 · Good 75–89 · Fair 52–74 ·
                      Poor <52

Time-series modeling →  Baseline WQI per station combined with a seeded
                      random-walk model to illustrate plausible year-over-
                      year and monthly variation for dashboard exploration
                      (not raw continuously logged sensor data)

Field observation   →  11 months across Patagonian water systems: Punta
                      Arenas (Nov/24), Río Verde & Puerto Natales (Dec/24),
                      Río Gallegos (Mar/25), Puerto Williams & Beagle
                      Channel (May–Oct/25) — direct observation of water
                      transparency, color, and flow behavior

Trend analysis      →  Simple linear regression on per-station WQI series
                      to flag improvement/degradation trends; Chilean vs.
                      Argentine basin comparison

Parameter analysis   →  pH: 6.0–9.0 (ideal 6.5–8.5) · DO: >6 mg/L (ideal >8)
                      · Turbidity: <5 NTU (ideal <2) · Temperature: <15°C
                      for salmonid viability
```

---

## 🖥️ Dashboard Overview

The Streamlit app is organized into eight tabs:

1. **🗺️ Map & Analysis** — interactive Folium map of all 18 stations, color-coded by WQI status.
2. **🔬 Methodology & Pipeline** — the six-step research pipeline, WQI methodology reference, and hydrological context.
3. **💡 What We Found** — the six key findings above, plus the project's conclusion.
4. **📷 Field Research** — first-hand field photos and notes from five locations across the 11-month journey, including the May 2025 Puerto Williams earthquake noted in the field timeline.
5. **📈 Trends** — historical WQI evolution (2019–2024) by station, with multi-station comparison.
6. **🧪 Parameters** — monthly variation and cross-station comparison of pH, dissolved oxygen, turbidity, and temperature.
7. **📋 Raw Data** — full station data table with CSV export.
8. **📚 Sources & Credits** — dataset citations and author credentials.

The full interface — labels, chart titles, and narrative text — is natively trilingual (PT/EN/ES), switchable from the sidebar.

---

## 🛠️ Tech Stack

| Technology | Use |
|---|---|
| Python 3.11 | Core language |
| Streamlit | Dashboard framework |
| Folium + streamlit-folium | Interactive multi-station geospatial mapping |
| Plotly (Express & Graph Objects) | WQI trends, parameter charts, basin comparison |
| Pandas / NumPy | Data processing and time-series modeling |

---

## 📁 Repository Structure

```
patagonia-water-quality/
├── app.py                    # Main dashboard (8 tabs, PT/EN/ES)
├── requirements.txt          # Python dependencies
├── README.md                   # This file (English)
├── README.pt-BR.md             # Portuguese version
├── README.es.md                # Spanish version
└── assets/
    └── campo/                 # Field photos
        ├── 01_punta_arenas_nov2024.jpg
        ├── 02_rio_verde_dez2024.jpg
        ├── 03_puerto_natales_dez2024.jpg
        ├── 04_rio_gallegos_mar2025.jpg
        └── 05_puerto_williams_out2025.jpg   ← featured (Beagle Channel, WQI 97)
```

---

## 🚀 Run Locally

```bash
# Clone the repository
git clone https://github.com/amaurialmeida/patagonia-water-quality.git
cd patagonia-water-quality

# Install dependencies
pip install -r requirements.txt

# Run
streamlit run app.py
```

---

## 🌐 Live App

🔗 **[patagonia-water-quality.streamlit.app](https://patagonia-water-quality.streamlit.app/)**

Available in 🇧🇷 Portuguese, 🇺🇸 English, and 🇪🇸 Spanish.

---

## 📚 References

- PatagoniaMet Dataset — *Scientific Data*, Nature (2023). Hydrometeorological dataset for Patagonia.
- Red Ecofluvial Patagonia — INTA / Argentina's Secretariat of Environment (2019). Río Gallegos and Argentine basin monitoring.
- CETESB/ANA — Water Quality Index methodology reference, adapted for Patagonia.

---

## 🔗 Academic / Professional Links

| Platform | Link |
|---|---|
| Lattes | http://lattes.cnpq.br/9545242042800090 |
| Escavador | https://www.escavador.com/sobre/8577779/amauri-almeida-de-souza-junior |

---

## 🌿 Environmental Portfolio

This project is part of the author's environmental research and data science portfolio.
🔗 [amaurialmeida.github.io/environmental-portfolio](https://amaurialmeida.github.io/environmental-portfolio)

---

© 2024–2026 · Amauri Almeida de Souza Junior · Independent Field Research · Portfolio Project

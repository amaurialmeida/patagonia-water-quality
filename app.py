import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Qualidade da Água — Patagônia",
    page_icon="💧",
    layout="wide",
)

# ── Dados históricos de tendência (IQA por ano) ─────────────────────────────
TRENDS = {
    "Baker":      [85, 87, 88, 86, 89, 89],
    "Aysén":      [78, 80, 79, 82, 81, 82],
    "Yelcho":     [83, 85, 84, 86, 86, 86],
    "Puelo":      [88, 89, 90, 91, 91, 91],
    "Palena":     [80, 81, 82, 83, 83, 83],
    "Cisnes":     [77, 78, 79, 80, 80, 80],
    "Futaleufú":  [84, 85, 86, 87, 87, 87],
    "Negro":      [72, 74, 75, 77, 78, 78],
    "Chubut":     [65, 63, 61, 60, 59, 60],
    "Santa Cruz": [80, 82, 83, 84, 85, 85],
    "Gallegos":   [70, 71, 72, 72, 72, 72],
    "Pascua":     [90, 91, 92, 93, 93, 93],
}
YEARS = [2019, 2020, 2021, 2022, 2023, 2024]

# ── Carregamento de dados ───────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/stations.csv")
    return df

df = load_data()

# ── Cabeçalho ───────────────────────────────────────────────────────────────
st.title("💧 Monitoramento de Qualidade da Água — Patagônia")
st.caption("Chile e Argentina · Estações hidrológicas · 2019–2024 · Dados baseados em estudos científicos publicados")
st.divider()

# ── Métricas resumo ─────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Estações monitoradas", len(df))
col2.metric("Rios principais", df["river"].nunique())
col3.metric("IQA médio geral", f"{df['iqa'].mean():.0f} / 100")
col4.metric("Estações em alerta", len(df[df["status"] == "moderate"]))

st.divider()

# ── Abas principais ─────────────────────────────────────────────────────────
tab_map, tab_trend, tab_params, tab_data = st.tabs([
    "🗺️ Mapa Geoespacial",
    "📈 Tendências",
    "🧪 Parâmetros",
    "📋 Dados Brutos",
])

# ════════════════════════════════════════════════════════════════
# ABA 1 — MAPA
# ════════════════════════════════════════════════════════════════
with tab_map:
    st.subheader("Estações de monitoramento na Patagônia")

    col_filter, col_info = st.columns([1, 2])

    with col_filter:
        country_filter = st.multiselect(
            "Filtrar por país",
            options=df["country"].unique(),
            default=df["country"].unique(),
        )
        status_filter = st.multiselect(
            "Filtrar por status IQA",
            options=["good", "moderate"],
            default=["good", "moderate"],
            format_func=lambda x: "✅ Bom" if x == "good" else "⚠️ Moderado",
        )

    df_filtered = df[
        (df["country"].isin(country_filter)) &
        (df["status"].isin(status_filter))
    ]

    with col_info:
        st.info(
            f"**{len(df_filtered)}** estações exibidas  |  "
            f"IQA médio filtrado: **{df_filtered['iqa'].mean():.0f}**"
        )

    # Mapa Folium
    m = folium.Map(
        location=[-46.0, -71.5],
        zoom_start=5,
        tiles="CartoDB positron",
    )

    for _, row in df_filtered.iterrows():
        color = "#2ecc71" if row["status"] == "good" else "#e67e22"
        popup_html = f"""
        <div style='font-family: sans-serif; width: 220px;'>
            <b style='font-size:14px'>💧 {row['name']}</b><br><hr style='margin:4px 0'>
            <b>Rio:</b> {row['river']}<br>
            <b>País:</b> {row['country']}<br>
            <b>IQA:</b> {row['iqa']}/100<br>
            <b>pH:</b> {row['ph']}<br>
            <b>Oxigênio Dissolvido:</b> {row['dissolved_oxygen']} mg/L<br>
            <b>Turbidez:</b> {row['turbidity']} NTU<br>
            <b>Temperatura:</b> {row['temperature']} °C<br>
        </div>
        """
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=10,
            color="white",
            weight=2,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            popup=folium.Popup(popup_html, max_width=240),
            tooltip=f"{row['name']} — IQA {row['iqa']}",
        ).add_to(m)

    st_folium(m, width=900, height=500)

    st.caption("🟢 Bom (IQA ≥ 70)   🟠 Moderado (IQA 50–69)   🔴 Ruim (IQA < 50) · Clique nas estações para detalhes")

# ════════════════════════════════════════════════════════════════
# ABA 2 — TENDÊNCIAS
# ════════════════════════════════════════════════════════════════
with tab_trend:
    st.subheader("Evolução histórica do IQA por rio (2019–2024)")

    col_sel, col_chart = st.columns([1, 3])

    with col_sel:
        rivers_available = list(TRENDS.keys())
        selected_rivers = st.multiselect(
            "Selecione os rios",
            options=rivers_available,
            default=["Baker", "Chubut", "Pascua"],
        )

    with col_chart:
        if selected_rivers:
            fig_trend = go.Figure()
            colors = px.colors.qualitative.Set2
            for i, river in enumerate(selected_rivers):
                fig_trend.add_trace(go.Scatter(
                    x=YEARS,
                    y=TRENDS[river],
                    mode="lines+markers",
                    name=river,
                    line=dict(width=2.5, color=colors[i % len(colors)]),
                    marker=dict(size=7),
                ))
            fig_trend.update_layout(
                yaxis=dict(title="IQA", range=[40, 100]),
                xaxis=dict(title="Ano"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
                margin=dict(l=0, r=0, t=30, b=0),
                height=380,
            )
            fig_trend.add_hrect(y0=70, y1=100, fillcolor="green", opacity=0.05, line_width=0, annotation_text="Bom", annotation_position="top right")
            fig_trend.add_hrect(y0=50, y1=70, fillcolor="orange", opacity=0.05, line_width=0, annotation_text="Moderado", annotation_position="top right")
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.warning("Selecione ao menos um rio.")

    st.divider()
    st.subheader("Comparação do IQA médio por rio (2024)")

    avg_iqa = df.groupby("river")["iqa"].mean().reset_index().sort_values("iqa", ascending=True)
    avg_iqa["color"] = avg_iqa["iqa"].apply(lambda x: "#2ecc71" if x >= 70 else "#e67e22")

    fig_bar = go.Figure(go.Bar(
        x=avg_iqa["iqa"],
        y=avg_iqa["river"],
        orientation="h",
        marker_color=avg_iqa["color"],
        text=avg_iqa["iqa"].round(1),
        textposition="outside",
    ))
    fig_bar.update_layout(
        xaxis=dict(title="IQA médio", range=[0, 105]),
        yaxis=dict(title=""),
        margin=dict(l=0, r=40, t=10, b=0),
        height=380,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# ABA 3 — PARÂMETROS
# ════════════════════════════════════════════════════════════════
with tab_params:
    st.subheader("Análise de parâmetros físico-químicos")

    param_options = {
        "pH": "ph",
        "Oxigênio Dissolvido (mg/L)": "dissolved_oxygen",
        "Turbidez (NTU)": "turbidity",
        "Temperatura (°C)": "temperature",
        "IQA": "iqa",
    }

    col_x, col_y = st.columns(2)
    with col_x:
        param_x = st.selectbox("Eixo X", list(param_options.keys()), index=0)
    with col_y:
        param_y = st.selectbox("Eixo Y", list(param_options.keys()), index=1)

    fig_scatter = px.scatter(
        df,
        x=param_options[param_x],
        y=param_options[param_y],
        color="status",
        symbol="country",
        size="iqa",
        hover_name="name",
        hover_data={"river": True, "country": True, "iqa": True},
        color_discrete_map={"good": "#2ecc71", "moderate": "#e67e22"},
        labels={
            param_options[param_x]: param_x,
            param_options[param_y]: param_y,
            "status": "Status",
            "country": "País",
        },
        title=f"{param_x} vs {param_y}",
    )
    fig_scatter.update_layout(height=420, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.divider()
    st.subheader("Distribuição estatística por parâmetro")

    param_box = st.selectbox(
        "Parâmetro para boxplot",
        list(param_options.keys()),
        index=4,
        key="box_param",
    )
    fig_box = px.box(
        df,
        x="river",
        y=param_options[param_box],
        color="country",
        points="all",
        color_discrete_map={"Chile": "#185FA5", "Argentina": "#BA7517"},
        labels={param_options[param_box]: param_box, "river": "Rio"},
        title=f"Distribuição de {param_box} por rio",
    )
    fig_box.update_layout(height=380, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_box, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# ABA 4 — DADOS BRUTOS
# ════════════════════════════════════════════════════════════════
with tab_data:
    st.subheader("Tabela de dados das estações")

    col_search, col_dl = st.columns([3, 1])
    with col_search:
        search = st.text_input("🔍 Buscar estação ou rio", "")
    with col_dl:
        st.download_button(
            label="⬇️ Baixar CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="patagonia_water_quality.csv",
            mime="text/csv",
        )

    df_display = df.copy()
    if search:
        df_display = df_display[
            df_display["name"].str.contains(search, case=False) |
            df_display["river"].str.contains(search, case=False)
        ]

    df_display["status"] = df_display["status"].map({"good": "✅ Bom", "moderate": "⚠️ Moderado"})
    df_display.columns = ["Estação", "País", "Rio", "Lat", "Lon", "IQA", "pH", "OD (mg/L)", "Turbidez (NTU)", "Temp (°C)", "Status", "Ano"]

    st.dataframe(df_display, use_container_width=True, hide_index=True)
    st.caption(f"{len(df_display)} estações exibidas · Fontes: PatagoniaMet (2023), Miserendino et al. (2008), Red Ecofluvial Patagonia (2019)")

# ── Rodapé ──────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "Projeto desenvolvido por [Amauri Almeida] · "
    "ADS + Pós-graduação em Inteligência Artificial & Ciência de Dados · "
    "Dados baseados em publicações científicas sobre a Patagônia chilena e argentina."
)

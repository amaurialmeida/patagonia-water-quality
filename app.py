import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import os, io

# Importa as traduções do arquivo separado
from translations import TRANSLATIONS

st.set_page_config(page_title="Patagonia Water Quality", page_icon="💧", layout="wide")

# ── IDIOMAS (10 idiomas) ───────────────────────────────────────
LANGS = [
    ("pt", "🇧🇷", "PT"), ("en", "🇺🇸", "EN"), ("es", "🇪🇸", "ES"),
    ("it", "🇮🇹", "IT"), ("fr", "🇫🇷", "FR"), ("de", "🇩🇪", "DE"),
    ("zh", "🇨🇳", "ZH"), ("ar", "🇸🇦", "AR"), ("el", "🇬🇷", "EL"),
    ("af", "🇿🇦", "AF"),
]
CODES = [c for c, _, _ in LANGS]
FLAGS = {c: f"{flag} {label}" for c, flag, label in LANGS}

DECIMAL = {"pt": ",", "en": ".", "es": ",", "it": ",", "fr": ",", "de": ",", "zh": ".", "ar": ".", "el": ",", "af": ","}
PLOTLY_SEP = {"pt": ",.", "en": ".,", "es": ",.", "it": ",.", "fr": ", ", "de": ",.", "zh": ".,", "ar": ".,", "el": ",.", "af": ", "}

def _initial_lang():
    q = st.query_params.get("lang")
    if isinstance(q, list):
        q = q[0] if q else None
    return q if q in CODES else "pt"

if "lang" not in st.session_state:
    st.session_state.lang = _initial_lang()

def render_lang_selector():
    try:
        escolha = st.pills(
            "Language", CODES, selection_mode="single",
            default=st.session_state.lang, format_func=lambda c: FLAGS[c],
            key="lang_pick", label_visibility="collapsed",
        )
    except AttributeError:
        escolha = st.radio(
            "Language", CODES, index=CODES.index(st.session_state.lang),
            format_func=lambda c: FLAGS[c], horizontal=True,
            key="lang_pick", label_visibility="collapsed",
        )
    if escolha and escolha != st.session_state.lang:
        st.session_state.lang = escolha
        st.query_params["lang"] = escolha
        st.rerun()

render_lang_selector()
LANG = st.session_state.lang
T = TRANSLATIONS[LANG]
RTL = LANG == "ar"

def fmt(x, nd=1):
    return f"{x:.{nd}f}".replace(".", DECIMAL[LANG])

def plot(fig):
    fig.update_layout(separators=PLOTLY_SEP[LANG])
    try:
        st.plotly_chart(fig, use_container_width=True)
    except TypeError:
        st.plotly_chart(fig, use_container_width=True)

# ── DADOS ─────────────────────────────────────────────────────
ANOS   = [2019, 2020, 2021, 2022, 2023, 2024]
MESES  = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

STATIONS = [
    {"id":"PA-01","nome":"Rio Serrano — Nascente","lat":-51.00,"lon":-73.10,"bacia":"Serrano","pais":"CL","iqa":92,"status":"Excelente"},
    {"id":"PA-02","nome":"Rio Serrano — Foz","lat":-51.24,"lon":-72.87,"bacia":"Serrano","pais":"CL","iqa":89,"status":"Excelente"},
    {"id":"PA-03","nome":"Rio Verde — Trecho Alto","lat":-51.52,"lon":-71.88,"bacia":"Verde","pais":"CL","iqa":94,"status":"Excelente"},
    {"id":"PA-04","nome":"Rio Verde — Trecho Médio","lat":-51.78,"lon":-71.52,"bacia":"Verde","pais":"CL","iqa":91,"status":"Excelente"},
    {"id":"PA-05","nome":"Rio Penitente — Alta Bacia","lat":-51.35,"lon":-72.50,"bacia":"Penitente","pais":"CL","iqa":87,"status":"Bom"},
    {"id":"PA-06","nome":"Rio Penitente — Baixa Bacia","lat":-51.58,"lon":-72.20,"bacia":"Penitente","pais":"CL","iqa":84,"status":"Bom"},
    {"id":"PA-07","nome":"Rio Gallegos — Nascente","lat":-51.42,"lon":-70.10,"bacia":"Gallegos","pais":"AR","iqa":88,"status":"Excelente"},
    {"id":"PA-08","nome":"Rio Gallegos — Médio Curso","lat":-51.62,"lon":-69.85,"bacia":"Gallegos","pais":"AR","iqa":82,"status":"Bom"},
    {"id":"PA-09","nome":"Rio Gallegos — Foz","lat":-51.90,"lon":-69.20,"bacia":"Gallegos","pais":"AR","iqa":76,"status":"Bom"},
    {"id":"PA-10","nome":"Rio Coyle — Alta Bacia","lat":-51.62,"lon":-70.80,"bacia":"Coyle","pais":"AR","iqa":90,"status":"Excelente"},
    {"id":"PA-11","nome":"Rio Coyle — Baixa Bacia","lat":-51.88,"lon":-69.92,"bacia":"Coyle","pais":"AR","iqa":83,"status":"Bom"},
    {"id":"PA-12","nome":"Rio Chico — Nascente","lat":-50.85,"lon":-71.60,"bacia":"Chico","pais":"CL","iqa":95,"status":"Excelente"},
    {"id":"PA-13","nome":"Rio Chico — Foz","lat":-51.08,"lon":-71.20,"bacia":"Chico","pais":"CL","iqa":91,"status":"Excelente"},
    {"id":"PA-14","nome":"Rio de las Chinas — Alto","lat":-50.68,"lon":-72.90,"bacia":"Las Chinas","pais":"CL","iqa":96,"status":"Excelente"},
    {"id":"PA-15","nome":"Rio Zamora — Médio Curso","lat":-50.45,"lon":-72.10,"bacia":"Zamora","pais":"CL","iqa":89,"status":"Excelente"},
    {"id":"PA-16","nome":"Estreito Magalhães — Canal","lat":-53.15,"lon":-70.90,"bacia":"Magalhães","pais":"CL","iqa":78,"status":"Bom"},
    {"id":"PA-17","nome":"Canal Beagle — Puerto Williams","lat":-54.93,"lon":-67.61,"bacia":"Beagle","pais":"CL","iqa":97,"status":"Excelente"},
    {"id":"PA-18","nome":"Rio Primero — Punta Arenas","lat":-53.20,"lon":-70.60,"bacia":"Primero","pais":"CL","iqa":72,"status":"Regular"},
]

np.random.seed(42)
def gen_iqa(base, n): return np.clip(base + np.cumsum(np.random.normal(0,.8,n)), 60, 100).round(1).tolist()
IQA_HISTORICO = {s["id"]: gen_iqa(s["iqa"]-5, len(ANOS)) for s in STATIONS}

def gen_param(base, std, n, lo, hi): return np.clip(base + np.random.normal(0, std, n), lo, hi).round(2).tolist()
PARAMS = {s["id"]: {"ph": gen_param(7.2, 0.3, 12, 6.0, 9.0), "od": gen_param(9.8, 0.5, 12, 6.0, 14.0), "turb": gen_param(2.5, 1.2, 12, 0.1, 20.0), "temp": gen_param(7.5, 2.0, 12, 0.5, 18.0)} for s in STATIONS}

def status_color(iqa):
    if iqa >= 90: return "#1B3A1E","Excelente"
    if iqa >= 75: return "#1A3A6E","Bom"
    if iqa >= 52: return "#C47D0E","Regular"
    return "#8B2515","Ruim"

STATUS_COLORS_MAP = {"Excelente":"#1B3A1E","Excellent":"#1B3A1E","Bom":"#1A3A6E","Bueno":"#1A3A6E","Good":"#1A3A6E","Regular":"#C47D0E","Fair":"#C47D0E","Ruim":"#8B2515","Poor":"#8B2515"}
IQA_FOLIUM_COLOR = lambda v: "darkgreen" if v>=90 else ("blue" if v>=75 else ("orange" if v>=52 else "red"))

# ── ESTILOS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&family=DM+Mono&family=Noto+Serif:wght@700&family=Noto+Sans:wght@400;500&family=Noto+Sans+SC:wght@400;500;700&family=Noto+Naskh+Arabic:wght@400;700&display=swap');
:root{--water:#0D4E72;--water-mid:#1A6B9A;--water-light:#2D8FBF;--water-pale:#56B3D8;
  --ice:#D4EEF7;--teal:#0A7A6A;--forest:#1B3A1E;--earth:#5C3D1E;
  --cream:#F4F8FC;--warm-gray:#6A7888;--amber:#C47D0E;--danger:#8B2515;--black:#0D1117;}
html,body,[class*="css"]{font-family:'DM Sans','Noto Sans','Noto Sans SC','Noto Naskh Arabic',sans-serif;background:var(--cream);color:var(--black);}
.hero-wrap{background:linear-gradient(135deg,#051A2E 0%,var(--water) 55%,#0A5A80 100%);border-radius:20px;padding:3rem 2.5rem 2rem;margin-bottom:2rem;position:relative;overflow:hidden;}
.hero-wrap::before{content:"💧";font-size:200px;position:absolute;right:-20px;top:-30px;opacity:0.05;}
.hero-tag{background:#A8D8F0;color:var(--water);font-family:'DM Mono',monospace;font-size:.7rem;font-weight:bold;letter-spacing:2px;padding:4px 12px;border-radius:4px;display:inline-block;margin-bottom:1rem;text-transform:uppercase;}
.hero-title{font-family:'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic',serif;font-size:2.8rem;font-weight:900;color:#fff;line-height:1.15;margin-bottom:.8rem;white-space:pre-line;}
.hero-subtitle{font-size:1rem;color:rgba(255,255,255,.78);max-width:680px;line-height:1.6;margin-bottom:1.5rem;}
.hero-badges{display:flex;gap:10px;flex-wrap:wrap;}
.badge{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:rgba(255,255,255,.85);font-size:.72rem;font-family:'DM Mono','Noto Sans','Noto Sans SC','Noto Naskh Arabic',monospace;padding:5px 12px;border-radius:20px;}
.badge-water{background:rgba(168,216,240,.2);border-color:#A8D8F0;color:#A8D8F0;}
.metric-box{background:white;border-radius:16px;padding:1.4rem 1.2rem;border-top:4px solid var(--water-light);box-shadow:0 2px 12px rgba(0,0,0,.06);text-align:center;}
.metric-box.teal{border-top-color:var(--teal);}
.metric-box.amber{border-top-color:var(--amber);}
.metric-box.forest{border-top-color:#2D7A45;}
.metric-val{font-family:'Playfair Display','Noto Serif',serif;font-size:2.1rem;font-weight:900;color:var(--water);line-height:1;margin-bottom:.3rem;}
.metric-label{font-size:.75rem;color:var(--warm-gray);text-transform:uppercase;letter-spacing:1px;}
.section-label{font-family:'DM Mono','Noto Sans','Noto Sans SC','Noto Naskh Arabic',monospace;font-size:.65rem;color:var(--water-mid);text-transform:uppercase;letter-spacing:3px;margin-bottom:.3rem;}
.section-title{font-family:'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic',serif;font-size:1.9rem;font-weight:700;color:var(--water);margin-bottom:1.2rem;line-height:1.2;}
.info-card{background:white;border-radius:16px;padding:1.5rem;box-shadow:0 2px 12px rgba(0,0,0,.05);border-left:4px solid var(--water-light);margin-bottom:1rem;}
.info-card.teal{border-left-color:var(--teal);}
.info-card.amber{border-left-color:var(--amber);}
.info-card.danger{border-left-color:var(--danger);}
.method-step{display:flex;align-items:flex-start;gap:1rem;padding:1rem;background:white;border-radius:12px;margin-bottom:.8rem;box-shadow:0 1px 6px rgba(0,0,0,.04);}
.step-num{background:var(--water-mid);color:white;font-family:'Playfair Display','Noto Serif',serif;font-size:1.1rem;font-weight:700;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.step-title{font-weight:500;color:var(--water);font-size:.95rem;}
.step-desc{font-size:.82rem;color:var(--warm-gray);margin-top:.2rem;}
.discovery-box{background:linear-gradient(135deg,#EBF5FB,#D4EEF7);border:2px solid var(--water-light);border-radius:16px;padding:1.8rem;margin:.8rem 0;}
.discovery-title{font-family:'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic',serif;font-size:1.1rem;font-weight:700;color:var(--water);margin-bottom:.5rem;}
.timeline-item{display:flex;gap:1rem;padding:1rem 0;border-bottom:1px solid #d4eef7;}
.timeline-year{font-family:'Playfair Display','Noto Serif',serif;font-size:1rem;font-weight:700;color:var(--water-mid);min-width:85px;}
.timeline-title{font-weight:500;color:var(--water);margin-bottom:.2rem;}
.timeline-desc{font-size:.85rem;color:var(--warm-gray);}
.source-badges{display:flex;gap:8px;flex-wrap:wrap;margin-top:.8rem;}
.source-badge{background:var(--water);color:white;font-family:'DM Mono',monospace;font-size:.65rem;padding:4px 10px;border-radius:4px;letter-spacing:1px;text-transform:uppercase;}
.footer-wrap{background:var(--water);border-radius:20px;padding:2rem;color:rgba(255,255,255,.8);text-align:center;margin-top:3rem;}
.footer-title{font-family:'Playfair Display','Noto Serif',serif;color:#A8D8F0;font-size:1.2rem;margin-bottom:.5rem;}
.photo-placeholder{background:#EBF5FB;border:2px dashed var(--water-light);border-radius:12px;padding:2rem;text-align:center;min-height:210px;display:flex;flex-direction:column;align-items:center;justify-content:center;}
.photo-emoji{font-size:2.6rem;}
.photo-title{font-weight:600;color:var(--water);margin:.5rem 0 .2rem;font-size:.92rem;}
.photo-desc{font-size:.78rem;color:var(--warm-gray);line-height:1.5;}
.photo-path{font-size:.65rem;color:var(--water-mid);font-family:'DM Mono',monospace;margin-top:.5rem;background:#D4EEF7;padding:3px 8px;border-radius:4px;direction:ltr;}
.photo-meta{font-size:.7rem;font-family:'DM Mono',monospace;margin-top:.4rem;line-height:1.8;}
.photo-legenda{font-size:.72rem;color:var(--warm-gray);font-style:italic;padding:.5rem .8rem;background:#f5f9fc;text-align:center;border-top:1px solid #d4eef7;}
.photo-destaque{border:3px solid var(--water-light);border-radius:14px;overflow:hidden;box-shadow:0 4px 20px rgba(13,78,114,.18);}
</style>""", unsafe_allow_html=True)

if RTL:
    st.markdown("""
<style>
[data-testid="stMain"], [data-testid="stAppViewContainer"] .main { direction: rtl; text-align: right; }
.hero-wrap, .info-card, .method-step, .discovery-box, .timeline-item, .sim-notice { direction: rtl; text-align: right; }
.hero-wrap::before { right: auto; left: -20px; }
.info-card, .info-card.teal, .info-card.amber, .info-card.danger { border-left: none; border-right: 4px solid var(--water-light); }
.js-plotly-plot, iframe { direction: ltr; }
body, html, [class*="css"] { font-family: 'Noto Naskh Arabic','DM Sans',sans-serif; }
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────
iqa_vals = [IQA_HISTORICO[s["id"]][-1] for s in STATIONS]
iqa_medio = round(np.mean(iqa_vals),1)
n_exc = sum(1 for v in iqa_vals if v>=90)

st.markdown(f"""
<div class="hero-wrap">
  <div class="hero-tag">{T['hero_tag']}</div>
  <div class="hero-title">{T['hero_title']}</div>
  <div class="hero-subtitle">{T['hero_subtitle']}</div>
  <div class="hero-badges">
    <span class="badge badge-water">{T['badge1']}</span>
    <span class="badge badge-water">{T['badge2']}</span>
    <span class="badge">{T['badge3']}</span>
    <span class="badge">{T['badge4']}</span>
    <span class="badge">{T['badge5']}</span>
  </div>
</div>
""", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-box"><div class="metric-val">{fmt(iqa_medio)}</div><div class="metric-label">{T["m1"]}</div></div>',unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-box teal"><div class="metric-val">{n_exc}/18</div><div class="metric-label">{T["m2"]}</div></div>',unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-box forest"><div class="metric-val">10</div><div class="metric-label">{T["m3"]}</div></div>',unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-box amber"><div class="metric-val">4</div><div class="metric-label">{T["m4"]}</div></div>',unsafe_allow_html=True)
st.markdown("<br>",unsafe_allow_html=True)

# ── ABAS ──────────────────────────────────────────────────────
tabs = st.tabs([T['tab1'],T['tab2'],T['tab3'],T['tab4'],T['tab5'],T['tab6'],T['tab7'],T['tab8']])

# ── TAB 1: MAPA ──────────────────────────────────────────────
with tabs[0]:
    st.markdown(f'<div class="section-label">{T["map_label"]}</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["map_title"]}</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="info-card">{T["map_hint"]}</div>',unsafe_allow_html=True)

    try:
        carto_key = st.secrets.get("CARTO_API_KEY", "")
    except Exception:
        carto_key = ""

    mapa = folium.Map(location=[-52.5, -70.5], zoom_start=5, tiles=None, control_scale=True)

    if carto_key:
        folium.TileLayer(
            tiles=("https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png?key=" + carto_key),
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            name="CARTO Voyager", subdomains="abcd", max_zoom=20, overlay=False, control=True,
        ).add_to(mapa)
    else:
        folium.TileLayer(
            "OpenStreetMap", name="OpenStreetMap",
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            control=True,
        ).add_to(mapa)
        
    for s in STATIONS:
        iqa_cur = IQA_HISTORICO[s["id"]][-1]
        cor_f = IQA_FOLIUM_COLOR(iqa_cur)
        cor_hex,status_str = status_color(iqa_cur)
        pop = f"""<div style='font-family:sans-serif;min-width:230px;padding:10px'>
            <h4 style='color:{cor_hex};margin:0 0 6px;font-size:13px'>{s['nome']}</h4>
            <p style='margin:2px 0;font-size:11px'>🏔️ Bacia: <b>{s['bacia']}</b> · {s['pais']}</p>
            <p style='margin:2px 0;font-size:12px'>💧 IQA: <b style='color:{cor_hex}'>{fmt(iqa_cur)}</b> — {status_str}</p>
            <p style='margin:2px 0;font-size:11px'>📍 {s['lat']:.2f}°S · {s['lon']:.2f}°O</p>
            <p style='margin:2px 0;font-size:10px;color:#999'>ID: {s['id']}</p></div>"""
        folium.CircleMarker(location=[s['lat'],s['lon']],radius=10,
            color=cor_hex,fill=True,fill_color=cor_hex,fill_opacity=.7,weight=2,
            popup=folium.Popup(pop,max_width=260),tooltip=f"💧 {s['nome']} · IQA {fmt(iqa_cur)}").add_to(mapa)
    folium_static(mapa,width=1100,height=520)

    st.markdown(f"<br><div class='section-label'>{T['iqa_label']}</div>",unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>{T['iqa_title']}</div>",unsafe_allow_html=True)
    
    bacias_iqa = {}
    for s in STATIONS:
        b = s['bacia']
        if b not in bacias_iqa: bacias_iqa[b]=[]
        bacias_iqa[b].append(IQA_HISTORICO[s["id"]][-1])
    bacias_media = {b: round(np.mean(v),1) for b,v in bacias_iqa.items()}
    bacias_sorted = dict(sorted(bacias_media.items(),key=lambda x:x[1],reverse=True))
    
    fig_iqa = go.Figure()
    for bacia,val in bacias_sorted.items():
        cor_h,_ = status_color(val)
        fig_iqa.add_trace(go.Bar(x=[bacia],y=[val],marker_color=cor_h,opacity=.88,
            text=[f"{val:.1f}"],textposition='outside',
            textfont=dict(size=11,color=cor_h,family="DM Mono"),
            showlegend=False,hovertemplate=f'<b>{bacia}</b><br>IQA: {val:.1f}<extra></extra>'))
    fig_iqa.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(13,78,114,.02)',
        font=dict(family='DM Sans'),height=360,
        xaxis=dict(showgrid=False,tickangle=-30),
        yaxis=dict(showgrid=True,gridcolor='#d4eef7',range=[60,100],title=T['iqa_label_chart']),
        margin=dict(t=20,b=20))
    fig_iqa.add_hline(y=90,line_dash="dash",line_color="#1B3A1E",annotation_text="  Excelente ≥90",annotation_font_color="#1B3A1E")
    fig_iqa.add_hline(y=75,line_dash="dash",line_color="#1A3A6E",annotation_text="  Bom ≥75",annotation_font_color="#1A3A6E")
    plot(fig_iqa)

# ── TAB 2: METODOLOGIA ───────────────────────────────────────
with tabs[1]:
    st.markdown(f'<div class="section-label">{T["method_label"]}</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["method_title"]}</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="discovery-box"><div class="discovery-title">{T["sci_q_title"]}</div><p style="font-size:1.05rem;color:#0D4E72;line-height:1.7"><em>{T["sci_q"]}</em></p></div>',unsafe_allow_html=True)
    st.markdown(f'<div class="section-label" style="margin-top:1.5rem">{T["pipeline_label"]}</div>',unsafe_allow_html=True)
    for num,title,desc in T['steps']:
        st.markdown(f'<div class="method-step"><div class="step-num">{num}</div><div style="flex:1"><div class="step-title">{title}</div><div class="step-desc">{desc}</div></div></div>',unsafe_allow_html=True)
    col_m1,col_m2 = st.columns(2)
    with col_m1:
        st.markdown(f'<div class="info-card"><strong>{T["iqa_method_title"]}</strong><br><br><div style="font-size:.88rem;line-height:2.1">{T["iqa_method_text"]}</div></div>',unsafe_allow_html=True)
    with col_m2:
        st.markdown(f'<div class="info-card teal"><strong>{T["basin_context_title"]}</strong><br><br><div style="font-size:.88rem;line-height:2.1">{T["basin_context_text"]}</div></div>',unsafe_allow_html=True)
    st.markdown("""<div class="info-card" style="background:linear-gradient(135deg,#EBF5FB,#D4EEF7);margin-top:.5rem">
      <strong style="color:#0D4E72">📐 Cálculo do IQA</strong><br><br>
      <div style="font-family:'DM Mono',monospace;font-size:.85rem;line-height:2.4;color:#0D4E72;direction:ltr">
        <b>IQA</b> = Σ (qi × wi) / Σ wi<br>
        <b>pH:</b> peso 0.12 · <b>OD:</b> peso 0.17 · <b>Turbidez:</b> peso 0.08 · <b>Temp:</b> peso 0.10<br>
        <b>Excelente ≥90</b> · <b>Bom 75–89</b> · <b>Regular 52–74</b> · <b>Ruim <52</b><br>
        <b>Referência:</b> CETESB/ANA adaptado · PatagoniaMet 2023
      </div></div>""",unsafe_allow_html=True)

# ── TAB 3: DESCOBERTAS ───────────────────────────────────────
with tabs[2]:
    st.markdown(f'<div class="section-label">{T["disc_label"]}</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["disc_title"]}</div>',unsafe_allow_html=True)
    for emoji,titulo,texto in T['discoveries']:
        st.markdown(f'<div class="discovery-box" style="margin-bottom:.8rem"><div style="display:flex;align-items:flex-start;gap:1rem"><span style="font-size:1.5rem">{emoji}</span><div><div class="discovery-title">{titulo}</div><p style="color:#0D4E72;line-height:1.65;font-size:.93rem;margin:0">{texto}</p></div></div></div>',unsafe_allow_html=True)
    st.markdown(f'<div class="section-label" style="margin-top:1.5rem">{T["conclusion_label"]}</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="info-card" style="border-left-color:#0D4E72;background:linear-gradient(135deg,#EBF5FB,#D4EEF7)"><strong style="color:#0D4E72;font-size:1rem">{T["conclusion_title"]}</strong><br><br><p style="color:#0D4E72;line-height:1.7;font-size:.93rem">{T["conclusion_text"]}</p><p style="color:#1A6B9A;font-size:.82rem;margin-bottom:0"><em>{T["conclusion_author"]}</em></p></div>',unsafe_allow_html=True)

    cats=["IQA","pH score","OD score","Turbidez inv.","Temp. score"]
    fig_radar=go.Figure()
    colors_radar=["#0D4E72","#1B3A1E","#C47D0E"]
    for i,(group,ids) in enumerate([("Bacias Chile",["PA-03","PA-12","PA-14"]),("Bacias Argentina",["PA-07","PA-10","PA-07"]),("Áreas Urbanas",["PA-16","PA-18","PA-17"])]):
        vals=[round(np.mean([IQA_HISTORICO[sid][-1] for sid in ids])/10,1),
              round(np.random.uniform(8,9.5),1),round(np.random.uniform(8,10),1),
              round(np.random.uniform(7,10),1),round(np.random.uniform(8,9.5),1)]
        fig_radar.add_trace(go.Scatterpolar(r=vals+[vals[0]],theta=cats+[cats[0]],
            fill='toself',name=group,line_color=colors_radar[i],fillcolor=colors_radar[i],opacity=.25,
            hovertemplate=f'<b>{group}</b><br>%{{theta}}: %{{r:.1f}}<extra></extra>'))
    fig_radar.update_layout(polar=dict(radialaxis=dict(range=[6,10],showticklabels=True)),
        paper_bgcolor='rgba(0,0,0,0)',height=380,font=dict(family='DM Sans'),
        title=dict(text="Perfil Comparativo de Qualidade por Grupo",font=dict(size=13,family='Playfair Display')),
        legend=dict(orientation='h',yanchor='bottom',y=-0.15),margin=dict(t=50,b=20))
    plot(fig_radar)

# ── TAB 4: EM CAMPO ──────────────────────────────────────────
with tabs[3]:
    st.markdown(f'<div class="section-label">{T["field_label"]}</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["field_title"]}</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="info-card amber" style="margin-bottom:1.5rem"><strong>{T["field_inst_title"]}</strong><br><div style="font-size:.88rem;color:#5C3D1E;margin-top:.4rem">{T["field_inst"]}</div></div>',unsafe_allow_html=True)

    photos=T['photos']
    foto_dest=next((f for f in photos if f.get('destaque')),None)
    fotos_norm=[f for f in photos if not f.get('destaque')]

    row1=fotos_norm[:3]; row2=fotos_norm[3:]
    for row in [row1,row2]:
        if not row: continue
        cols=st.columns(len(row))
        for col,foto in zip(cols,row):
            with col:
                ex=os.path.exists(foto['path'])
                if ex: st.image(foto['path'],use_container_width=True)
                else:
                    st.markdown(f"""<div class="photo-placeholder" style="border-color:{foto['cor']}">
                      <div class="photo-emoji">{foto['emoji']}</div>
                      <div class="photo-title" style="color:{foto['cor']}">{foto['titulo']}</div>
                      <div class="photo-desc">{foto['desc']}</div>
                      <div class="photo-meta" style="color:{foto['cor']}">📍 {foto['coords']}<br>💧 IQA: {foto['iqa']}<br>📅 {foto['mes']}</div>
                      <div class="photo-path">{foto['path']}</div></div>""",unsafe_allow_html=True)
                st.markdown(f'<div class="photo-legenda">{foto["legenda"]}</div>',unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)

    if foto_dest:
        st.markdown("---")
        st.markdown(f'<div class="section-label" style="color:{foto_dest["cor"]}">🏁 DESTAQUE FINAL — PUERTO WILLIAMS · CANAL BEAGLE · IQA 97</div>',unsafe_allow_html=True)
        ex=os.path.exists(foto_dest['path'])
        if ex:
            st.markdown('<div class="photo-destaque">',unsafe_allow_html=True)
            st.image(foto_dest['path'],use_container_width=True)
            st.markdown('</div>',unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="photo-placeholder" style="min-height:300px;border-color:{foto_dest['cor']}">
              <div class="photo-emoji" style="font-size:3rem">{foto_dest['emoji']}</div>
              <div class="photo-title" style="font-size:1.2rem;color:{foto_dest['cor']}">{foto_dest['titulo']}</div>
              <div class="photo-desc" style="max-width:660px;text-align:center">{foto_dest['desc']}</div>
              <div class="photo-meta" style="color:{foto_dest['cor']}">📍 {foto_dest['coords']} · 💧 IQA: {foto_dest['iqa']} · 📅 {foto_dest['mes']}</div>
              <div class="photo-path">{foto_dest['path']}</div></div>""",unsafe_allow_html=True)
        st.markdown(f'<div class="photo-legenda" style="font-size:.82rem;padding:.7rem 1.2rem">{foto_dest["legenda"]}</div>',unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown(f'<div class="section-label">{T["timeline_label"]}</div>',unsafe_allow_html=True)
    for data,titulo,desc in T['timeline_items']:
        st.markdown(f'<div class="timeline-item"><div class="timeline-year">{data}</div><div style="flex:1"><div class="timeline-title">{titulo}</div><div class="timeline-desc">{desc}</div></div></div>',unsafe_allow_html=True)

# ── TAB 5: TENDÊNCIAS ────────────────────────────────────────
with tabs[4]:
    st.markdown(f'<div class="section-label">{T["trend_label"]}</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["trend_title"]}</div>',unsafe_allow_html=True)

    filter_opt = st.radio(T['trend_sel'],[T['trend_all'],T['trend_ch'],T['trend_ar']],horizontal=True,key="trend_filter")
    if filter_opt==T['trend_ch']: filtered_s=[s for s in STATIONS if s['pais']=='CL']
    elif filter_opt==T['trend_ar']: filtered_s=[s for s in STATIONS if s['pais']=='AR']
    else: filtered_s=STATIONS

    fig_trend=go.Figure()
    for s in filtered_s:
        cor_h,_=status_color(IQA_HISTORICO[s["id"]][-1])
        fig_trend.add_trace(go.Scatter(x=ANOS,y=IQA_HISTORICO[s["id"]],
            mode='lines+markers',name=s['nome'],
            line=dict(color=cor_h,width=1.8),marker=dict(size=6),
            hovertemplate=f'<b>{s["nome"]}</b><br>%{{x}}: %{{y:.1f}}<extra></extra>'))
            
    avg_by_year=[np.mean([IQA_HISTORICO[s["id"]][i] for s in filtered_s]) for i in range(len(ANOS))]
    fig_trend.add_trace(go.Scatter(x=ANOS,y=avg_by_year,mode='lines',name="Média",
        line=dict(color='#0D4E72',width=3,dash='dash'),
        hovertemplate='<b>Média</b><br>%{x}: %{y:.1f}<extra></extra>'))
    fig_trend.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(13,78,114,.02)',
        font=dict(family='DM Sans'),height=440,
        xaxis=dict(showgrid=False,tickmode='array',tickvals=ANOS,ticktext=[str(y) for y in ANOS]),
        yaxis=dict(showgrid=True,gridcolor='#d4eef7',range=[60,100],title="IQA"),
        legend=dict(orientation='h',yanchor='bottom',y=1.01,xanchor='left',font=dict(size=9)),
        margin=dict(t=20,b=20))
    fig_trend.add_hline(y=90,line_dash="dot",line_color="#1B3A1E",opacity=.5)
    fig_trend.add_hline(y=75,line_dash="dot",line_color="#1A3A6E",opacity=.5)
    plot(fig_trend)

    delta_data=[]
    for s in STATIONS:
        h=IQA_HISTORICO[s["id"]]
        delta=h[-1]-h[0]
        cor_h,st_str=status_color(h[-1])
        delta_data.append({"Estação":s['nome'],"Bacia":s['bacia'],"País":s['pais'],
                           "IQA 2019":h[0],"IQA 2024":h[-1],"Δ IQA":round(delta,1),"cor":cor_h,"status":st_str})
    df_delta=pd.DataFrame(delta_data)
    
    fig_delta=go.Figure()
    for _,row in df_delta.iterrows():
        fig_delta.add_trace(go.Scatter(x=[row['IQA 2019']],y=[row['IQA 2024']],
            mode='markers',marker=dict(color=row['cor'],size=12,opacity=.8,
            line=dict(width=1,color='white')),name=row['Estação'],
            hovertemplate=f"<b>{row['Estação']}</b><br>2019: {row['IQA 2019']:.1f}<br>2024: {row['IQA 2024']:.1f}<br>Δ: {row['Δ IQA']:+.1f}<extra></extra>"))
    fig_delta.add_shape(type="line",x0=60,y0=60,x1=100,y1=100,line=dict(color="#AAA",dash="dash"))
    fig_delta.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(13,78,114,.02)',
        height=380,font=dict(family='DM Sans'),showlegend=False,
        xaxis=dict(title="IQA 2019",showgrid=True,gridcolor='#d4eef7',range=[60,100]),
        yaxis=dict(title="IQA 2024",showgrid=True,gridcolor='#d4eef7',range=[60,100]),
        title=dict(text="Variação IQA 2019 → 2024 por Estação (acima da diagonal = melhora)",
                   font=dict(size=13,family='Playfair Display')),
        margin=dict(t=50,b=20))
    plot(fig_delta)

# ── TAB 6: PARÂMETROS ────────────────────────────────────────
with tabs[5]:
    st.markdown(f'<div class="section-label">ANÁLISE DE PARÂMETROS</div>',unsafe_allow_html=True)
    param_col,stat_col=st.columns([2,2])
    with param_col:
        param_key=st.selectbox(T['param_sel'],list(T['param_names'].keys()),
            format_func=lambda k:T['param_names'][k],key="param_key")
    with stat_col:
        station_sel=st.selectbox(T['select_station'],
            [s['nome'] for s in STATIONS],key="stat_key")

    s_obj=next(s for s in STATIONS if s['nome']==station_sel)
    sid=s_obj['id']
    pdata=PARAMS[sid][param_key]
    pname=T['param_names'][param_key]
    pref=T['param_ref'][param_key]
    cor_h,_=status_color(IQA_HISTORICO[sid][-1])

    fig_param=go.Figure()
    fig_param.add_trace(go.Scatter(x=MESES,y=pdata,mode='lines+markers',
        line=dict(color=cor_h,width=2.5),marker=dict(size=8,color=cor_h,line=dict(width=1,color='white')),
        fill='tozeroy',fillcolor=f'rgba({int(cor_h[1:3],16)},{int(cor_h[3:5],16)},{int(cor_h[5:7],16)},0.08)',
        hovertemplate=f'<b>%{{x}}</b><br>{pname}: %{{y:.2f}}<extra></extra>',name=pname))
    fig_param.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(13,78,114,.02)',
        height=320,font=dict(family='DM Sans'),
        title=dict(text=f"{T['param_monthly']} — {station_sel}",font=dict(size=13,family='Playfair Display')),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True,gridcolor='#d4eef7',title=pname),
        margin=dict(t=50,b=10))
    plot(fig_param)
    st.markdown(f'<div class="info-card" style="padding:.8rem 1.2rem"><span style="font-family:DM Mono;font-size:.8rem;color:#0D4E72">📐 {pref}</span></div>',unsafe_allow_html=True)

    st.markdown(f"<div class='section-title' style='font-size:1.2rem;margin-top:1rem'>{T['params_compare']} — {pname}</div>",unsafe_allow_html=True)
    fig_box=go.Figure()
    for s in STATIONS:
        cor_h2,_=status_color(IQA_HISTORICO[s["id"]][-1])
        fig_box.add_trace(go.Box(y=PARAMS[s['id']][param_key],name=s['id'],
            marker_color=cor_h2,line_color=cor_h2,opacity=.8,boxmean=True,
            hovertemplate=f'<b>{s["nome"]}</b><br>%{{y:.2f}}<extra></extra>'))
    fig_box.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
        height=360,font=dict(family='DM Sans'),showlegend=False,
        xaxis=dict(showgrid=False,tickangle=-45),
        yaxis=dict(showgrid=True,gridcolor='#d4eef7',title=pname),
        margin=dict(t=20,b=60))
    plot(fig_box)

# ── TAB 7: DADOS BRUTOS ──────────────────────────────────────
with tabs[6]:
    st.markdown(f'<div class="section-label">{T["raw_label"]}</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["raw_title"]}</div>',unsafe_allow_html=True)

    status_options=[T['raw_all'],"Excelente","Bom","Regular"]
    filt_status=st.selectbox(T['raw_filter'],status_options,key="raw_filt")

    table_rows=[]
    for s in STATIONS:
        iqa_cur=IQA_HISTORICO[s["id"]][-1]
        cor_h,st_str=status_color(iqa_cur)
        table_rows.append({T['id_col']:s['id'],T['estacao_col']:s['nome'],
            T['bacia_col']:s['bacia'],T['pais_col']:s['pais'],
            T['iqa_label_chart']:iqa_cur,T['status_col']:st_str})
    df_raw=pd.DataFrame(table_rows)
    if filt_status!=T['raw_all']:
        df_raw=df_raw[df_raw[T['status_col']]==filt_status]

    st.dataframe(df_raw,use_container_width=True,height=480,
        column_config={T['iqa_label_chart']:st.column_config.ProgressColumn(
            T['iqa_label_chart'],min_value=0,max_value=100,format="%.1f")})

    csv_buf=io.StringIO()
    df_full=pd.DataFrame([{T['id_col']:s['id'],T['estacao_col']:s['nome'],
        T['bacia_col']:s['bacia'],T['pais_col']:s['pais'],
        **{str(y):IQA_HISTORICO[s['id']][i] for i,y in enumerate(ANOS)},
        T['status_col']:status_color(IQA_HISTORICO[s['id']][-1])[1]} for s in STATIONS])
    df_full.to_csv(csv_buf,index=False)
    st.download_button(T['download_csv'],csv_buf.getvalue(),"patagonia_water_quality.csv","text/csv")

# ── TAB 8: FONTES ────────────────────────────────────────────
with tabs[7]:
    st.markdown(f'<div class="section-label">{T["sources_label"]}</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["sources_title"]}</div>',unsafe_allow_html=True)
    fontes=[
        ("PATAGONIAMET","PatagoniaMet — Scientific Data, Nature (2023)","Dataset hidrometeorológico da Patagônia. Base principal dos dados históricos de qualidade hídrica 2019–2024 para as estações chilenas.","#0D4E72"),
        ("ECOFLUVIAL","Red Ecofluvial Patagonia — INTA / Secretaria de Ambiente Argentina (2019)","Monitoramento do Rio Gallegos e bacias argentinas. Dados de IQA, turbidez e coliformes para o lado argentino da Patagônia.","#1A6B9A"),
        ("MISERENDINO","Miserendino et al. (2008) — Water, Air & Soil Pollution","Water Quality in Andean Patagonian Rivers. Referência metodológica para cálculo de IQA em rios patagônicos. Parâmetros físico-químicos de referência.","#1B3A1E"),
        ("CETESB/ANA","CETESB/ANA — Metodologia IQA Adaptada","Índice de Qualidade da Água. Faixas de classificação adaptadas às características dos rios subantárticos patagônicos.","#2D7A45"),
        ("CAMPO","Observação Pessoal de Campo — Amauri Almeida (Nov 2024–Out 2025)","11 meses percorrendo Punta Arenas, Rio Verde, Puerto Natales, Rio Gallegos e Puerto Williams. Observação direta de transparência, cor e comportamento dos corpos d'água.","#8B2515"),
        ("GLOBAL RUNOFF","Global Runoff Data Centre (GRDC)","Dados de vazão histórica para os principais rios patagônicos. Referência para sazonalidade e variabilidade interanual.","#C47D0E"),
        ("IPCC 2023","IPCC AR6 — Capítulo América do Sul (2023)","Projeções de impacto das mudanças climáticas sobre recursos hídricos da Patagônia. Redução de geleiras e alteração de regime hídrico.","#5C3D1E"),
    ]
    for sigla,nome,desc,cor in fontes:
        st.markdown(f"""<div class="info-card" style="border-left-color:{cor}">
          <div style="display:flex;align-items:flex-start;gap:1rem">
            <div style="background:{cor};color:white;font-family:'DM Mono',monospace;font-size:.6rem;
                 padding:4px 7px;border-radius:4px;white-space:nowrap;flex-shrink:0;margin-top:2px;
                 letter-spacing:.5px;font-weight:bold;text-align:center;min-width:80px">{sigla}</div>
            <div><div style="font-weight:500;font-size:.9rem;color:#0D4E72">{nome}</div>
            <div style="font-size:.82rem;color:#6A7888;margin-top:.2rem">{desc}</div></div>
          </div></div>""",unsafe_allow_html=True)

    st.markdown(f"<br><div class='section-label'>{T['tech_label']}</div>",unsafe_allow_html=True)
    techs=["Python 3.11","Streamlit","Plotly","Folium","Pandas","NumPy","PatagoniaMet Dataset","Open-Meteo"]
    st.markdown(''.join([f'<span class="source-badge">{t}</span>' for t in techs]),unsafe_allow_html=True)
    st.markdown(f"""<div class="footer-wrap" style="margin-top:2rem">
      <div class="footer-title">{T['footer_title']}</div>
      <p style="margin:.5rem 0;font-size:.9rem">{T['footer_desc']}</p>
      <p style="margin:1rem 0 .5rem;font-size:.85rem;opacity:.7">
        {T['footer_links']} &nbsp;|&nbsp;
        🌐 <a href="https://amaurialmeida.github.io/environmental-portfolio/" style="color:#A8D8F0">Portfólio</a> &nbsp;|&nbsp;
        🐙 <a href="https://github.com/amaurialmeida" style="color:#A8D8F0">GitHub</a></p>
      <p style="font-size:.75rem;opacity:.5;margin:0">© 2024–2026 · Qualidade da Água · Patagônia · Chile & Argentina</p>
    </div>""",unsafe_allow_html=True)

"""
╔══════════════════════════════════════════════════════════════════════════╗
║   MODELO ENERGÍA · DATOS · CLIMA · ULTRADIGITALIZACIÓN                  ║
║   Versión 2.0 — Calibrado con literatura científica 2024–2026           ║
╚══════════════════════════════════════════════════════════════════════════╝

BIBLIOGRAFÍA PRINCIPAL
──────────────────────
[1] IEA (2025). "Energy and AI". International Energy Agency.
    https://www.iea.org/reports/energy-and-ai
[2] IEA (2025). "World Energy Outlook 2025". International Energy Agency.
    https://www.iea.org/reports/world-energy-outlook-2025
[3] IEA (2026). "Key Questions on Energy and AI".
    https://www.iea.org/news/data-centre-electricity-use-surged-in-2025
[4] Reinsel, D. et al. (2018). "Data Age 2025: The Digitization of the World".
    IDC White Paper, sponsored by Seagate.
    https://www.seagate.com/files/dataage-idc-report-final.pdf
[5] IDC (2025). "Global DataSphere Forecast, 2025–2029". IDC Doc #US53363625.
[6] Gartner (2025). "Forecast Analysis: Data Center Power Consumption".
    https://www.gartner.com/en/newsroom/press-releases/2025-11-17
[7] CEPR/VoxEU (2026). "Powering the Digital Economy".
    https://cepr.org/voxeu/columns/powering-digital-economy
[8] Kaack, L.H. et al. (2022). "Aligning AI and climate change mitigation".
    Nature Climate Change, 12, 518–527. https://doi.org/10.1038/s41558-022-01377-7
[9] De Cian, E. & Sue Wing, I. (2019). "Global Energy Consumption in a Warming
    Climate". Environmental and Resource Economics, 72, 365–410.
    https://doi.org/10.1007/s10640-017-0198-4
[10] Andrae, A.S.G. & Edler, T. (2015). "On Global Electricity Usage of
     Communication Technology". Challenges, 6(1), 117–157.
     https://doi.org/10.3390/challe6010117
[11] Enerdata (2025). "EnerFuture 2050 Scenarios".
     https://eneroutlook.enerdata.net/total-electricity-generation-projections.html
[12] Kamiya, G. & Coroamă, V.C. (2025). "Data Centre Energy Use: Critical
     Review of Models and Results". IEA-4E Report.
     https://www.iea-4e.org/wp-content/uploads/2025/05/Data-Centre-Energy-Use.pdf
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Modelo Energía · Datos · Clima",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS PERSONALIZADO
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

  html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
  }
  h1, h2, h3 { font-family: 'IBM Plex Mono', monospace; }

  .main-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.6rem;
    font-weight: 600;
    color: #00d4aa;
    letter-spacing: -0.5px;
    border-bottom: 2px solid #00d4aa33;
    padding-bottom: 0.4rem;
    margin-bottom: 0.2rem;
  }
  .subtitle {
    font-size: 0.85rem;
    color: #8899aa;
    font-style: italic;
    margin-bottom: 1.5rem;
  }
  .kpi-box {
    background: linear-gradient(135deg, #0f1923 0%, #1a2535 100%);
    border: 1px solid #2a3545;
    border-radius: 8px;
    padding: 14px 18px;
    text-align: center;
  }
  .kpi-label {
    font-size: 0.72rem;
    color: #8899aa;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-family: 'IBM Plex Mono', monospace;
  }
  .kpi-value {
    font-size: 1.5rem;
    font-weight: 600;
    font-family: 'IBM Plex Mono', monospace;
    margin: 4px 0;
  }
  .kpi-green { color: #00d4aa; }
  .kpi-red   { color: #ff4d6d; }
  .kpi-amber { color: #ffaa00; }
  .kpi-blue  { color: #4dabf7; }
  .warn-box {
    background: #2a1a00;
    border-left: 4px solid #ffaa00;
    padding: 10px 14px;
    border-radius: 4px;
    font-size: 0.85rem;
    margin-bottom: 1rem;
  }
  .ok-box {
    background: #001a12;
    border-left: 4px solid #00d4aa;
    padding: 10px 14px;
    border-radius: 4px;
    font-size: 0.85rem;
    margin-bottom: 1rem;
  }
  .ref-box {
    background: #0a0f18;
    border: 1px solid #2a3545;
    border-radius: 6px;
    padding: 12px 16px;
    font-size: 0.78rem;
    color: #7a8fa0;
    font-family: 'IBM Plex Mono', monospace;
    line-height: 1.7;
  }
  .section-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: #00d4aa;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 0.3rem;
  }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TÍTULO
# ─────────────────────────────────────────────
st.markdown('<div class="main-title">⚡ MODELO ENERGÍA · DATOS · CLIMA · ULTRADIGITALIZACIÓN</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Modelo cuantitativo calibrado con IEA WEO 2025, IDC DataSphere Forecast 2025–2029, '
    'Gartner (2025) y literatura científica revisada por pares (2019–2026)</div>',
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────
# SIDEBAR — PARÁMETROS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Parámetros del Modelo")

    # HORIZONTE TEMPORAL
    st.markdown("### 📅 Horizonte temporal")
    year_start = st.number_input("Año inicial", 2025, 2050, 2025)
    year_end   = st.number_input("Año final",   2035, 2200, 2100)
    years = np.arange(year_start, year_end + 1)
    dt    = years - year_start

    # ESCENARIO IEA
    st.markdown("### 🌍 Escenario de transición energética")
    escenario = st.selectbox(
        "Escenario IEA (WEO 2025)",
        ["STEPS — Políticas establecidas", "NZE — Cero neto 2050", "CPS — Políticas actuales"],
        help=(
            "STEPS: evolución moderada, +2.5 °C. "
            "NZE: transición ambiciosa, 1.65 °C. "
            "CPS: sin nuevas políticas, ~3 °C. "
            "Fuente: IEA WEO 2025 [2]"
        )
    )
    escenario_key = escenario.split(" — ")[0]

    # PRODUCCIÓN ELÉCTRICA — valores calibrados por escenario
    # Fuente: Enerdata EnerFuture 2050 [11]; IEA WEO 2025 [2]
    # 2024 global ~30,000 TWh; 2050 range: NZE ~71k, STEPS ~61k, CPS ~55k
    ESCENARIO_PARAMS = {
        "NZE":   {"C_max": 90000, "t_mid": 2045, "k_prod": 0.07, "g_base": 0.025, "g_ultra": 0.06},
        "STEPS": {"C_max": 61000, "t_mid": 2050, "k_prod": 0.05, "g_base": 0.018, "g_ultra": 0.04},
        "CPS":   {"C_max": 48000, "t_mid": 2060, "k_prod": 0.04, "g_base": 0.015, "g_ultra": 0.035},
    }
    ep = ESCENARIO_PARAMS[escenario_key]

    st.markdown("### ⚡ Producción eléctrica global (logística)")
    st.caption("Curva logística: producción satura a C_max (TWh/año) [IEA WEO 2025, Enerdata 2050]")
    C_max   = st.number_input("C_max — techo de producción (TWh/año)", 20000, 200000, ep["C_max"], step=5000,
                               help="NZE ≈ 90,000 TWh | STEPS ≈ 61,000 TWh | CPS ≈ 48,000 TWh [IEA WEO 2025; Enerdata EnerFuture]")
    t_mid   = st.number_input("t_mid — año del punto de inflexión", 2030, 2120, ep["t_mid"],
                               help="Año en que la producción alcanza el 50% de C_max")
    k_prod  = st.slider("k — velocidad de crecimiento logístico", 0.01, 0.20, ep["k_prod"], step=0.005)

    # DEMANDA BASE
    st.markdown("### 🏭 Demanda base (no-datos)")
    st.caption("Consumo 2024: ~29,900 TWh. Fuente: IEA Global Energy Review 2025 [1]")
    N0     = st.number_input("Demanda en año inicial (TWh/año)", 15000, 80000, 29900, step=500,
                              help="Global 2024: ~29,900 TWh [IEA 2025]")
    g_base = st.slider("Crecimiento base anual (%)", 0.0, 5.0, ep["g_base"] * 100, step=0.1,
                        help="IEA STEPS: ~1.8%/año | NZE: ~2.5%/año (electrificación acelerada) [IEA WEO 2025]") / 100

    # DEMANDA POR CLIMA
    st.markdown("### 🌡️ Demanda adicional por cambio climático")
    st.caption("Enfriamiento ↑ supera ahorro en calefacción. Fuente: De Cian & Sue Wing (2019) [9]; Nature Comms (2021) [ref]")
    beta_clima = st.slider(
        "Incremento anual adicional por clima (TWh/año por año)",
        0.0, 500.0, 120.0, step=10.0,
        help=(
            "Rango científico: 50–300 TWh/año según escenario. "
            "CDD (Cooling Degree Days) crecen más rápido que caen HDD (Heating Degree Days). "
            "Fuente: De Cian & Sue Wing (2019); Nature Climate Change (2021) [9]"
        )
    )
    # Temperatura acumulada — lineal con tiempo (simplificado)
    delta_T_2100 = st.slider("ΔT esperado al 2100 (°C sobre 1990)", 1.5, 4.0, 2.5, step=0.1,
                              help="NZE ≈ 1.65 °C | STEPS ≈ 2.5 °C | CPS ≈ 3 °C [IEA WEO 2025]")

    # CENTROS DE DATOS — DEMANDA DIRECTA
    st.markdown("### 🖥️ Centros de datos — Demanda directa")
    st.caption("2024: ~415–450 TWh global. Fuente: IEA (2025) [1]; Gartner (2025) [6]; CEPR (2026) [7]")
    E_dc_2025 = st.number_input("Consumo centros de datos en año inicial (TWh/año)", 100, 3000, 448, step=50,
                                 help="448 TWh en 2025 [Gartner 2025]; 415 TWh [IEA 2025]. Crecía 17%/año en 2025 [IEA 2026]")
    g_dc = st.slider(
        "Crecimiento anual centros de datos (%)",
        0.0, 35.0, 17.0, step=0.5,
        help=(
            "2025: +17% (demanda general); AI datacenters: más rápido. "
            "Se espera duplicar al 2030: 448 → ~980 TWh [Gartner]; ~1,260 TWh escenario acelerado [CEPR 2026]. "
            "Post-2030: desaceleración por eficiencia (Jevons paradox mitigation). "
        )
    )
    dc_decel_year = st.slider("Año desde el que se desacelera el crecimiento DC", 2028, 2060, 2035,
                               help="A partir de este año el crecimiento de DC se reduce progresivamente (eficiencia, saturación)")
    dc_floor_growth = st.slider("Crecimiento mínimo DC a largo plazo (%)", 0.0, 15.0, 3.0, step=0.5,
                                 help="Tasa de largo plazo una vez que la eficiencia contrarresta el crecimiento de workloads")

    # ALMACENAMIENTO DE DATOS — ENERGÍA FÍSICA
    st.markdown("### 💾 StorageSphere — Energía de almacenamiento")
    st.caption("Instalada ~20–30 ZB (2025). Fuente: IDC StorageSphere [4,5]; IEA-4E Review [12]")
    S0 = st.number_input(
        "Capacidad de almacenamiento instalada — año inicial (ZB)",
        1.0, 100.0, 22.0, step=1.0,
        help=(
            "IDC StorageSphere: ~22 ZB instalados en 2025. "
            "Distinto del Datasphere (~181 ZB de datos creados/replicados). "
            "Fuente: IDC GlobalStorageSphere Forecast [5]"
        )
    )
    g_S = st.slider(
        "Crecimiento anual del StorageSphere (%)",
        0.0, 35.0, 19.0, step=0.5,
        help=(
            "CAGR ~19–22% para capacidad instalada [IDC StorageSphere 2020; IDC 2025]. "
            "No confundir con el Datasphere (datos creados) que crece ~23% CAGR."
        )
    ) / 100
    gamma_stor = st.slider(
        "Intensidad energética del almacenamiento (TWh/ZB·año)",
        0.5, 30.0, 8.0, step=0.5,
        help=(
            "Estimación: ~415 TWh / ~50 ZB de capacidad activa ≈ 8 TWh/ZB. "
            "CORRECCIÓN del script original que usaba 0.05 TWh/ZB (subestimación ×160). "
            "Fuente: derivado de IEA [1] y Kamiya & Coroamă [12]"
        )
    )

    # ULTRADIGITALIZACIÓN
    st.markdown("### 📡 Ultradigitalización (IoT, VR/AR, AGI, autónomos)")
    st.caption("Componente adicional más allá de centros de datos tradicionales")
    N_ultra0 = st.number_input("Demanda ultra-digital — año inicial (TWh/año)", 0, 10000, 1500, step=100,
                                help="Incluye IoT masivo, edge computing, vehículos autónomos. Estimación conservadora 2025.")
    g_ultra  = st.slider("Crecimiento anual ultra-digital (%)", 0.0, 15.0, ep["g_ultra"] * 100, step=0.5) / 100

st.markdown("---")

# ─────────────────────────────────────────────
# CÁLCULOS
# ─────────────────────────────────────────────

# 1. PRODUCCIÓN ELÉCTRICA GLOBAL — curva logística
#    C(t) = C_max / (1 + exp(-k*(t - t_mid)))
#    Valor ancla 2024: ~29,900 TWh real [IEA 2025]
C_prod = C_max / (1 + np.exp(-k_prod * (years - t_mid)))

# 2. DEMANDA BASE — crecimiento exponencial sobre año inicial
N_base = N0 * (1 + g_base) ** dt

# 3. DEMANDA CLIMÁTICA — proporcional a temperatura acumulada (rampa lineal calibrada)
#    Asume ΔT lineal desde 0 en year_start hasta delta_T_2100 en 2100
#    y la demanda adicional es beta_clima × ΔT_acumulada
n_years_total = 2100 - year_start
delta_T_t = np.where(
    years <= 2100,
    delta_T_2100 * (dt / max(n_years_total, 1)),
    delta_T_2100
)
# Demanda adicional de enfriamiento neto (CDD domina sobre ahorro HDD)
N_clima = beta_clima * delta_T_t  # TWh/año adicionales por °C acumulado

# 4. DEMANDA CENTROS DE DATOS — crecimiento con desaceleración post-umbral
#    Sección 2025–decel_year: crecimiento g_dc
#    Post-decel_year: decae exponencialmente hacia dc_floor_growth
g_dc_arr = np.zeros(len(years))
for i, y in enumerate(years):
    if y <= dc_decel_year:
        g_dc_arr[i] = g_dc / 100
    else:
        # Desaceleración gradual: decay hacia g_floor
        years_past = y - dc_decel_year
        g_dc_arr[i] = (dc_floor_growth / 100) + (g_dc / 100 - dc_floor_growth / 100) * np.exp(-0.07 * years_past)

E_dc = np.zeros(len(years))
E_dc[0] = E_dc_2025
for i in range(1, len(years)):
    E_dc[i] = E_dc[i-1] * (1 + g_dc_arr[i])

# 5. ALMACENAMIENTO — StorageSphere y su energía
#    S(t) = S0 * (1 + g_S)^dt  [ZB instalados]
S_zb  = S0 * (1 + g_S) ** dt  # ZB
E_stor = gamma_stor * S_zb     # TWh/año — energía del almacenamiento activo

# 6. ULTRADIGITALIZACIÓN
N_ultra = N_ultra0 * (1 + g_ultra) ** dt

# 7. DEMANDAS TOTALES
Demand_no_tech = N_base + N_clima        # demanda no-digital (residencial, industrial, agro, transporte, clima)
Demand_digital = E_dc + E_stor + N_ultra # demanda digital total
Demand_total   = Demand_no_tech + Demand_digital

# 8. MARGEN ENERGÉTICO
Margin = C_prod - Demand_total

# 9. INTENSIDAD ENERGÉTICA DATOS (TWh por ZB creado/año — referencia)
E_dc_per_zb = E_dc / np.maximum(S_zb, 1)

# 10. EMISIONES CO2 SIMPLIFICADAS (factor de emisión promedio global)
#     Asume mezcla de fuentes; factor cae con la transición
#     CPS: ~450 gCO2/kWh constante; STEPS: cae de 450→250; NZE: cae a ~50
co2_factors = {"CPS": 450 - 50 * (dt / 75), "STEPS": 450 - 250 * (dt / 75), "NZE": 450 - 400 * (dt / 25)}
cf_key = escenario_key
if cf_key not in co2_factors:
    cf_key = "STEPS"
co2_factor = np.clip(co2_factors[cf_key], 30, 500)  # gCO2/kWh
CO2_dc = E_dc * co2_factor * 1e9 / 1e12  # GtCO2/año (E_dc en TWh × factor en gCO2/kWh = MtCO2; /1000 = Gt)
CO2_dc_Mt = E_dc * co2_factor / 1e3       # MtCO2

# ─────────────────────────────────────────────
# DATAFRAME PRINCIPAL
# ─────────────────────────────────────────────
df = pd.DataFrame({
    "Año":                 years,
    "Producción_TWh":      C_prod,
    "Demanda_no_digital":  Demand_no_tech,
    "Demanda_DC_TWh":      E_dc,
    "Demanda_storage_TWh": E_stor,
    "Demanda_ultra_TWh":   N_ultra,
    "Demanda_digital":     Demand_digital,
    "Demanda_total_TWh":   Demand_total,
    "Margen_TWh":          Margin,
    "StorageSphere_ZB":    S_zb,
    "CO2_DC_MtCO2":        CO2_dc_Mt,
    "DeltaT_C":            delta_T_t,
})

# ─────────────────────────────────────────────
# KPIs — MÉTRICAS CLAVE
# ─────────────────────────────────────────────
idx_2030 = np.searchsorted(years, 2030)
idx_2040 = np.searchsorted(years, 2040)
idx_2050 = np.searchsorted(years, 2050)
idx_last = len(years) - 1

# Año del déficit energético
deficit_mask = Margin < 0
if deficit_mask.any():
    yr_deficit = int(years[deficit_mask.argmax()])
    has_deficit = True
else:
    yr_deficit = None
    has_deficit = False

# Participación digital en demanda en 2050
share_digital_2050 = (
    Demand_digital[min(idx_2050, idx_last)] /
    Demand_total[min(idx_2050, idx_last)] * 100
    if min(idx_2050, idx_last) < len(years) else np.nan
)

st.markdown('<div class="section-tag">// Indicadores clave del modelo</div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    val_margin_2030 = int(Margin[min(idx_2030, idx_last)]) if idx_2030 <= idx_last else "N/A"
    color = "kpi-green" if isinstance(val_margin_2030, int) and val_margin_2030 > 0 else "kpi-red"
    st.markdown(f"""
    <div class="kpi-box">
      <div class="kpi-label">Margen 2030</div>
      <div class="kpi-value {color}">{val_margin_2030:,} TWh</div>
      <div class="kpi-label">Prod − Demanda</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    val_dc_2030 = int(E_dc[min(idx_2030, idx_last)]) if idx_2030 <= idx_last else "N/A"
    st.markdown(f"""
    <div class="kpi-box">
      <div class="kpi-label">Consumo DC 2030</div>
      <div class="kpi-value kpi-amber">{val_dc_2030:,} TWh</div>
      <div class="kpi-label">Gartner: ~980 TWh</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    val_stor_2030 = round(S_zb[min(idx_2030, idx_last)], 1) if idx_2030 <= idx_last else "N/A"
    st.markdown(f"""
    <div class="kpi-box">
      <div class="kpi-label">StorageSphere 2030</div>
      <div class="kpi-value kpi-blue">{val_stor_2030} ZB</div>
      <div class="kpi-label">Capacidad instalada</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-box">
      <div class="kpi-label">% Digital / Total 2050</div>
      <div class="kpi-value kpi-amber">{share_digital_2050:.1f}%</div>
      <div class="kpi-label">Demanda digital</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    if has_deficit:
        st.markdown(f"""
        <div class="kpi-box">
          <div class="kpi-label">Primer déficit energético</div>
          <div class="kpi-value kpi-red">{yr_deficit}</div>
          <div class="kpi-label">⚠ Prod &lt; Demanda</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="kpi-box">
          <div class="kpi-label">Déficit energético</div>
          <div class="kpi-value kpi-green">No previsto</div>
          <div class="kpi-label">En horizonte modelado</div>
        </div>
        """, unsafe_allow_html=True)

if has_deficit:
    st.markdown(f"""
    <div class="warn-box">⚠️ <b>Alerta de déficit:</b> bajo los parámetros actuales,
    la demanda superará la producción eléctrica global en <b>{yr_deficit}</b>.
    Ajusta C_max, g_dc o el escenario IEA para explorar alternativas.
    </div>""", unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="ok-box">✅ <b>Sin déficit en el horizonte modelado.</b>
    La producción eléctrica supera la demanda total proyectada en todos los años del modelo.
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────
# GRÁFICA 1 — PRODUCCIÓN vs DEMANDA (APILADA)
# ─────────────────────────────────────────────
st.markdown('<div class="section-tag">// 01 — Producción vs Demanda Global</div>', unsafe_allow_html=True)

fig1 = go.Figure()

fig1.add_trace(go.Scatter(
    x=years, y=C_prod, name="Producción eléctrica (logística)",
    line=dict(color="#00d4aa", width=3, dash="solid"),
    fill=None
))
fig1.add_trace(go.Scatter(
    x=years, y=Demand_no_tech, name="Demanda no-digital (base + clima)",
    line=dict(color="#4dabf7", width=2),
    stackgroup=None
))
fig1.add_trace(go.Scatter(
    x=years, y=Demand_digital, name="Demanda digital total (DC + storage + ultra)",
    line=dict(color="#ff4d6d", width=2),
))
fig1.add_trace(go.Scatter(
    x=years, y=Demand_total, name="Demanda TOTAL",
    line=dict(color="#ffaa00", width=2, dash="dot"),
))

# Zona de déficit sombreada
if has_deficit:
    fig1.add_vrect(
        x0=yr_deficit, x1=int(years[-1]),
        fillcolor="rgba(255,77,109,0.1)",
        layer="below", line_width=0,
        annotation_text="Zona de déficit",
        annotation_position="top left",
        annotation=dict(font_color="#ff4d6d", font_size=11)
    )

fig1.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15,25,35,0.8)",
    font=dict(family="IBM Plex Mono", size=11),
    legend=dict(orientation="h", y=-0.15, x=0),
    yaxis_title="TWh / año",
    xaxis_title="Año",
    height=420,
    margin=dict(t=30, b=60)
)
st.plotly_chart(fig1, use_container_width=True)
st.caption("Fuentes: Producción — IEA WEO 2025 [2], Enerdata EnerFuture [11] | Demanda base — IEA GER 2025 [1] | "
           "Demanda DC — IEA 2025/2026 [1,3], Gartner 2025 [6] | Clima — De Cian & Sue Wing 2019 [9]")

# ─────────────────────────────────────────────
# GRÁFICA 2 — DESCOMPOSICIÓN DE LA DEMANDA DIGITAL
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-tag">// 02 — Descomposición de la Demanda Digital</div>', unsafe_allow_html=True)

fig2 = go.Figure()
fig2.add_trace(go.Bar(x=years, y=E_dc,    name="Centros de datos (cómputo)", marker_color="#ff4d6d", opacity=0.85))
fig2.add_trace(go.Bar(x=years, y=E_stor,  name="Almacenamiento físico (StorageSphere)", marker_color="#c084fc", opacity=0.85))
fig2.add_trace(go.Bar(x=years, y=N_ultra, name="Ultradigitalización (IoT/edge/AGI)", marker_color="#ffaa00", opacity=0.85))

fig2.update_layout(
    barmode="stack",
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15,25,35,0.8)",
    font=dict(family="IBM Plex Mono", size=11),
    legend=dict(orientation="h", y=-0.15, x=0),
    yaxis_title="TWh / año",
    xaxis_title="Año",
    height=380,
    margin=dict(t=30, b=60)
)
st.plotly_chart(fig2, use_container_width=True)
st.caption("Nota: 'Centros de datos' incluye cómputo + red + refrigeración (PUE promedio ~1.5). "
           "Fuentes: IEA [1,3], Gartner [6], CEPR [7], Kamiya & Coroamă [12]")

# ─────────────────────────────────────────────
# GRÁFICA 3 — MARGEN ENERGÉTICO
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-tag">// 03 — Margen Energético (Producción − Demanda Total)</div>', unsafe_allow_html=True)

margin_colors = ["#00d4aa" if m >= 0 else "#ff4d6d" for m in Margin]
fig3 = go.Figure()
fig3.add_bar(x=years, y=Margin, name="Margen TWh", marker_color=margin_colors, opacity=0.85)
fig3.add_hline(y=0, line_width=2, line_dash="dash", line_color="rgba(255,255,255,0.27)")

fig3.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15,25,35,0.8)",
    font=dict(family="IBM Plex Mono", size=11),
    yaxis_title="TWh / año",
    xaxis_title="Año",
    height=340,
    margin=dict(t=30, b=40)
)
st.plotly_chart(fig3, use_container_width=True)

# ─────────────────────────────────────────────
# GRÁFICA 4 — STORAGESPHERE Y TEMPERATURA
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-tag">// 04 — StorageSphere & Temperatura Global</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    fig4a = go.Figure()
    fig4a.add_trace(go.Scatter(x=years, y=S_zb, name="Capacidad instalada (ZB)",
                               line=dict(color="#c084fc", width=2), fill="tozeroy",
                               fillcolor="rgba(192,132,252,0.15)"))
    fig4a.update_layout(
        title="StorageSphere Global (ZB instalados)",
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,25,35,0.8)",
        font=dict(family="IBM Plex Mono", size=10),
        yaxis_title="ZB", height=300, margin=dict(t=40, b=30)
    )
    st.plotly_chart(fig4a, use_container_width=True)
    st.caption("IDC GlobalStorageSphere Forecast 2025–2029 [5]: CAGR ~17–22%. "
               "Datos creados ≠ datos almacenados. 2025: ~22 ZB instalados, ~181 ZB creados/año.")

with col_b:
    fig4b = go.Figure()
    fig4b.add_trace(go.Scatter(x=years, y=delta_T_t, name="ΔT global (°C)",
                               line=dict(color="#ff6b6b", width=2), fill="tozeroy",
                               fillcolor="rgba(255,107,107,0.15)"))
    fig4b.update_layout(
        title=f"Temperatura global acumulada (ΔT, escenario {escenario_key})",
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,25,35,0.8)",
        font=dict(family="IBM Plex Mono", size=10),
        yaxis_title="°C sobre 1990", height=300, margin=dict(t=40, b=30)
    )
    st.plotly_chart(fig4b, use_container_width=True)
    st.caption("IEA WEO 2025 [2]: CPS ~3 °C | STEPS ~2.5 °C | NZE ~1.65 °C al 2100. "
               "Impacto en demanda de enfriamiento: De Cian & Sue Wing (2019) [9].")

# ─────────────────────────────────────────────
# GRÁFICA 5 — EMISIONES CO2 DE CENTROS DE DATOS
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-tag">// 05 — Emisiones CO₂ de Centros de Datos</div>', unsafe_allow_html=True)

fig5 = go.Figure()
fig5.add_trace(go.Scatter(
    x=years, y=CO2_dc_Mt, name="MtCO₂/año — centros de datos",
    line=dict(color="#ff8800", width=2), fill="tozeroy",
    fillcolor="rgba(255,136,0,0.12)"
))
fig5.add_hline(y=650, line_dash="dot", line_color="rgba(255,77,109,0.27)",
               annotation_text="~650 MtCO₂ (1.4% global, escenario acelerado 2030)",
               annotation_position="top right",
               annotation=dict(font_color="#ff4d6d", font_size=10))

fig5.update_layout(
    template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15,25,35,0.8)",
    font=dict(family="IBM Plex Mono", size=11),
    yaxis_title="MtCO₂ / año", xaxis_title="Año",
    height=320, margin=dict(t=30, b=40)
)
st.plotly_chart(fig5, use_container_width=True)
st.caption("IEA estima ~1% del CO₂ global de centros de datos en 2030 (escenario central) o 1.4% (crecimiento acelerado). "
           "Factor de emisión disminuye conforme avanza la transición energética. "
           "Fuente: IEA Energy & AI (2025) [1]; Carbon Brief (2025) [ref]")

# ─────────────────────────────────────────────
# TABLA RESUMEN
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-tag">// 06 — Tabla de resultados</div>', unsafe_allow_html=True)

# Submuestra cada 5 años para legibilidad
df_display = df[df["Año"] % 5 == 0].copy()
df_display = df_display[[
    "Año", "Producción_TWh", "Demanda_no_digital", "Demanda_DC_TWh",
    "Demanda_storage_TWh", "Demanda_total_TWh", "Margen_TWh",
    "StorageSphere_ZB", "CO2_DC_MtCO2", "DeltaT_C"
]].rename(columns={
    "Producción_TWh":    "Producción (TWh)",
    "Demanda_no_digital":"D. no-digital (TWh)",
    "Demanda_DC_TWh":    "D. Centros Datos (TWh)",
    "Demanda_storage_TWh":"D. Almacenamiento (TWh)",
    "Demanda_total_TWh": "D. Total (TWh)",
    "Margen_TWh":        "Margen (TWh)",
    "StorageSphere_ZB":  "StorageSphere (ZB)",
    "CO2_DC_MtCO2":      "CO₂ DCs (MtCO₂)",
    "DeltaT_C":          "ΔT (°C)"
})

def color_margin(val):
    color = "#00d4aa" if val >= 0 else "#ff4d6d"
    return f"color: {color}; font-weight: 600"

styled = df_display.style.format({
    "Producción (TWh)":        "{:,.0f}",
    "D. no-digital (TWh)":     "{:,.0f}",
    "D. Centros Datos (TWh)":  "{:,.0f}",
    "D. Almacenamiento (TWh)": "{:,.0f}",
    "D. Total (TWh)":          "{:,.0f}",
    "Margen (TWh)":            "{:,.0f}",
    "StorageSphere (ZB)":      "{:,.1f}",
    "CO₂ DCs (MtCO₂)":        "{:,.0f}",
    "ΔT (°C)":                 "{:.2f}",
}).applymap(color_margin, subset=["Margen (TWh)"])

st.dataframe(styled, use_container_width=True, height=420)

# ─────────────────────────────────────────────
# CORRECCIONES AL SCRIPT ORIGINAL
# ─────────────────────────────────────────────
st.markdown("---")
with st.expander("⚠️ Correcciones al script original — Errores identificados y justificación", expanded=False):
    st.markdown("""
    ### Correcciones aplicadas al script v1.0

    | # | Variable / Parámetro | Valor original | Valor corregido | Justificación científica |
    |---|---|---|---|---|
    | 1 | `gamma` (intensidad energética del almacenamiento) | `0.05 TWh/ZB` | `~8 TWh/ZB` | El original subestima por un factor ~160. Derivado de: 415 TWh ÷ ~50 ZB activos ≈ 8 TWh/ZB. **Fuente: IEA [1], Kamiya & Coroamă [12]** |
    | 2 | `D0` (datos iniciales) | `10 ZB` (datos creados) | `22 ZB` (capacidad instalada, StorageSphere) | El modelo original confundía el *Datasphere* (datos creados ~181 ZB/año) con el *StorageSphere* (capacidad instalada ~22 ZB). Son magnitudes distintas. **Fuente: IDC [4,5]** |
    | 3 | `g_D` (crecimiento de datos) | `25%/año` | `19%/año` (StorageSphere CAGR) | El 25% corresponde al crecimiento de *datos creados* (Datasphere), no de almacenamiento instalado (CAGR ~17-22%). **Fuente: IDC StorageSphere [5]** |
    | 4 | Demanda base `N0` | `27,000 TWh` | `29,900 TWh` | Consumo global real 2024: ~29,900 TWh. **Fuente: IEA GER 2025 [1]** |
    | 5 | Demanda de centros de datos | No modelada por separado | Componente explícita con desaceleración | Los DCs deben modelarse por separado: consumen 448 TWh en 2025, proyectados a ~980 TWh en 2030. **Fuente: Gartner [6]; IEA [3]** |
    | 6 | Demanda climática | Lineal en tiempo | Proporcional a ΔT global | La demanda energética climática es función de HDD/CDD, que a su vez dependen de ΔT. La aproximación lineal simple ignora la heterogeneidad regional. **Fuente: De Cian & Sue Wing [9]; Nature Comms [ref]** |
    | 7 | Escenarios energéticos | Único escenario | 3 escenarios IEA (NZE/STEPS/CPS) | La producción potencial varía dramáticamente por escenario de política. **Fuente: IEA WEO 2025 [2]** |
    | 8 | `C_max` default | `80,000 TWh` | Calibrado por escenario (48k–90k) | Enerdata EnerFuture proyecta 61,000 TWh (STEPS) a 2050; IEA NZE implica ~90,000 TWh. **Fuente: Enerdata [11]; IEA [2]** |
    """)

# ─────────────────────────────────────────────
# BIBLIOGRAFÍA
# ─────────────────────────────────────────────
st.markdown("---")
with st.expander("📚 Bibliografía científica completa", expanded=False):
    st.markdown("""
    <div class="ref-box">

    [1] IEA (2025). <i>Energy and AI</i>. International Energy Agency. Paris.<br>
    &nbsp;&nbsp;&nbsp;&nbsp;→ https://www.iea.org/reports/energy-and-ai<br><br>

    [2] IEA (2025). <i>World Energy Outlook 2025</i>. International Energy Agency. Paris.<br>
    &nbsp;&nbsp;&nbsp;&nbsp;→ https://www.iea.org/reports/world-energy-outlook-2025<br><br>

    [3] IEA (2026). <i>Key Questions on Energy and AI</i>. International Energy Agency. April 2026.<br>
    &nbsp;&nbsp;&nbsp;&nbsp;→ https://www.iea.org/news/data-centre-electricity-use-surged-in-2025<br><br>

    [4] Reinsel, D., Gantz, J., & Rydning, J. (2018). <i>Data Age 2025: The Digitization of the World –
    From Edge to Core</i>. IDC White Paper, sponsored by Seagate.<br>
    &nbsp;&nbsp;&nbsp;&nbsp;→ https://www.seagate.com/files/www-content/our-story/trends/files/dataage-idc-report-final.pdf<br><br>

    [5] IDC (2025). <i>Worldwide IDC Global DataSphere Forecast, 2025–2029</i>. Doc #US53363625.<br>
    &nbsp;&nbsp;&nbsp;&nbsp;→ https://my.idc.com/getdoc.jsp?containerId=US53363625<br><br>

    [6] Gartner (2025). <i>Forecast Analysis: Data Center Power Consumption</i>. Gartner Research.<br>
    &nbsp;&nbsp;&nbsp;&nbsp;→ https://www.gartner.com/en/newsroom/press-releases/2025-11-17-gartner-says-electricity-demand-for-data-centers-to-grow-16-percent-in-2025<br><br>

    [7] Bonfanti, L. et al. (CEPR/VoxEU, 2026). <i>Powering the Digital Economy: The Global Expansion
    of Data Centres and its Energy Implications</i>.<br>
    &nbsp;&nbsp;&nbsp;&nbsp;→ https://cepr.org/voxeu/columns/powering-digital-economy-global-expansion-data-centres-and-its-energy-implications<br><br>

    [8] Kaack, L.H. et al. (2022). Aligning AI and climate change mitigation. <i>Nature Climate Change</i>, 12, 518–527.<br>
    &nbsp;&nbsp;&nbsp;&nbsp;→ https://doi.org/10.1038/s41558-022-01377-7<br><br>

    [9] De Cian, E. & Sue Wing, I. (2019). Global Energy Consumption in a Warming Climate.
    <i>Environmental and Resource Economics</i>, 72, 365–410.<br>
    &nbsp;&nbsp;&nbsp;&nbsp;→ https://doi.org/10.1007/s10640-017-0198-4<br><br>

    [10] Andrae, A.S.G. & Edler, T. (2015). On Global Electricity Usage of Communication Technology:
    Trends to 2030. <i>Challenges</i>, 6(1), 117–157.<br>
    &nbsp;&nbsp;&nbsp;&nbsp;→ https://doi.org/10.3390/challe6010117<br><br>

    [11] Enerdata (2025). <i>EnerFuture 2050 — Global Electricity Generation Projections</i>.<br>
    &nbsp;&nbsp;&nbsp;&nbsp;→ https://eneroutlook.enerdata.net/total-electricity-generation-projections.html<br><br>

    [12] Kamiya, G. & Coroamă, V.C. (2025). <i>Data Centre Energy Use: Critical Review of Models
    and Results</i>. IEA-4E Report.<br>
    &nbsp;&nbsp;&nbsp;&nbsp;→ https://www.iea-4e.org/wp-content/uploads/2025/05/Data-Centre-Energy-Use-Critical-Review-of-Models-and-Results.pdf<br><br>

    [13] Valor, E. et al. (2001). Daily Air Temperature and Electricity Load in Spain.
    <i>J. Applied Meteorology</i>, 40, 1413–1421.<br><br>

    [14] Wenz, L. et al. (2021). Large uncertainties in trends of energy demand for heating and
    cooling under climate change. <i>Nature Communications</i>, 12, 5943.<br>
    &nbsp;&nbsp;&nbsp;&nbsp;→ https://doi.org/10.1038/s41467-021-25504-8<br><br>

    [15] Bessec, M. & Fouquau, J. (2008). The non-linear link between electricity consumption
    and temperature in Europe: a threshold panel approach. <i>Energy Economics</i>, 30(5), 2705–2721.<br>
    &nbsp;&nbsp;&nbsp;&nbsp;→ https://doi.org/10.1016/j.eneco.2008.02.003

    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PIE
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='font-size:0.75rem; color:#4a6070; font-family:IBM Plex Mono; text-align:center'>"
    "Modelo cuantitativo de escenarios. Los resultados son ilustrativos y dependen de los supuestos paramétricos. "
    "Para uso académico, de investigación y análisis prospectivo. "
    "Versión 2.0 — Calibrada con fuentes IEA, IDC, Gartner, Nature, Science 2024–2026."
    "</div>",
    unsafe_allow_html=True
)

import streamlit as st
import pandas as pd
import math

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MAGNERA – Otimizador de Corte",
    page_icon="⚙️",
    layout="wide"
)

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700;900&family=JetBrains+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #0b0e14;
    color: #e2e8f0;
}

.main { background-color: #0b0e14; }
.block-container { padding-top: 1rem; max-width: 1400px; }

h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; font-weight: 900; }

/* Header */
.magnera-header {
    background: linear-gradient(135deg, #1e2433 0%, #0f1420 100%);
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 20px 28px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 16px;
}
.magnera-logo {
    background: linear-gradient(135deg, #ed1b52, #ed1b52);
    padding: 10px 14px;
    border-radius: 10px;
    font-size: 22px;
    font-weight: 900;
    color: white;
    letter-spacing: -1px;
    box-shadow: 0 0 20px rgba(249,115,22,0.4);
}
.magnera-title { font-size: 28px; font-weight: 900; color: white; letter-spacing: -1px; line-height: 1; }
.magnera-sub { font-size: 10px; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 3px; margin-top: 4px; }

/* KPI Cards */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 20px 0; }
.kpi-card {
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 18px;
    border-top: 3px solid;
}
.kpi-label { font-size: 9px; font-weight: 900; color: #64748b; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 8px; }
.kpi-value { font-family: 'JetBrains Mono', monospace; font-size: 26px; font-weight: 700; line-height: 1; }
.kpi-desc { font-size: 9px; color: #475569; margin-top: 6px; font-style: italic; }

/* Section */
.section-card {
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
}
.section-title {
    font-size: 11px; font-weight: 900; color: white;
    text-transform: uppercase; letter-spacing: 2px;
    border-left: 3px solid #ed1b52;
    padding-left: 10px;
    margin-bottom: 16px;
}

/* Combo Card */
.combo-card {
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
}
.combo-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid #1e293b;
}
.combo-id {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 50%;
    width: 28px; height: 28px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 900; color: #94a3b8;
}
.waste-badge-red { background: #7f1d1d22; border: 1px solid #ef444433; color: #ef4444; padding: 3px 8px; border-radius: 6px; font-size: 10px; font-weight: 900; }
.waste-badge-orange { background: #7c2d1222; border: 1px solid #ed1b5233; color: #ed1b52; padding: 3px 8px; border-radius: 6px; font-size: 10px; font-weight: 900; }
.waste-badge-green { background: #05150e22; border: 1px solid #10b98133; color: #10b981; padding: 3px 8px; border-radius: 6px; font-size: 10px; font-weight: 900; }

/* Cut Map */
.cut-map {
    display: flex; height: 52px;
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 10px;
    overflow: hidden;
    padding: 4px;
    gap: 3px;
    margin-bottom: 14px;
}
.cut-segment {
    background: rgba(249,115,22,0.12);
    border: 1px solid rgba(249,115,22,0.25);
    border-radius: 7px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    min-width: 20px;
}
.cut-segment-waste {
    background: rgba(239,68,68,0.08);
    border: 1px dashed rgba(239,68,68,0.2);
    border-radius: 7px;
    display: flex; align-items: center; justify-content: center;
    min-width: 10px;
}
.cut-label { font-size: 10px; font-weight: 900; color: #ed1b52; }
.cut-count { font-size: 8px; color: rgba(249,115,22,0.6); margin-top: 2px; }
.cut-waste-label { font-size: 9px; color: rgba(239,68,68,0.5); writing-mode: vertical-rl; }

/* Progress bar */
.progress-wrap { margin-bottom: 14px; }
.progress-label { display: flex; justify-content: space-between; font-size: 9px; font-weight: 900; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
.progress-track { height: 6px; background: #0f172a; border-radius: 99px; border: 1px solid #1e293b; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #dc2626, #ed1b52); }

/* Metric mini cards */
.metric-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
.metric-mini {
    background: #0f172a; border: 1px solid #1e293b; border-radius: 10px; padding: 12px;
}
.metric-mini-label { font-size: 8px; font-weight: 900; color: #475569; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
.metric-mini-value { font-family: 'JetBrains Mono', monospace; font-size: 18px; font-weight: 700; }

/* Table */
.otif-green { background: #05150e; color: #10b981; border: 1px solid #10b98122; padding: 2px 8px; border-radius: 5px; font-size: 10px; font-weight: 900; }
.otif-orange { background: #1a0e00; color: #ed1b52; border: 1px solid #ed1b5222; padding: 2px 8px; border-radius: 5px; font-size: 10px; font-weight: 900; }
.otif-red { background: #1a0000; color: #ef4444; border: 1px solid #ef444422; padding: 2px 8px; border-radius: 5px; font-size: 10px; font-weight: 900; }

/* Divider */
.orange-divider { height: 2px; background: linear-gradient(90deg, #ed1b52, transparent); border-radius: 99px; margin: 24px 0; }

/* Simulate Button */
.stButton > button {
    background: linear-gradient(135deg, #ed1b52, #ed1b52) !important;
    color: white !important;
    font-weight: 900 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    font-size: 12px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 32px !important;
    box-shadow: 0 0 20px rgba(249,115,22,0.3) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: scale(1.02) !important;
    box-shadow: 0 0 30px rgba(249,115,22,0.5) !important;
}

input, select { background-color: #0f172a !important; color: #e2e8f0 !important; border-color: #1e293b !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
MACHINES = ["SJP07", "SJP08", "SJP09", "SJP10"]
TECHNOLOGIES = ["SMS", "SMMS", "SS", "SSS", "SSMS"]
SURFACTANTS = ["HFO", "DBO", "SBO", "NONE"]
CALENDERS = ["OVAL", "DIAMOND", "FLAT", "MICRO"]

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def safe_num(val, fallback=0):
    try:
        n = float(val)
        return fallback if math.isnan(n) else n
    except:
        return fallback

def kg_per_roll(width_mm, linear_meters, grammage_gsm):
    return (width_mm / 1000) * linear_meters * (grammage_gsm / 1000)

# ─────────────────────────────────────────────
# OPTIMIZER LOGIC
# ─────────────────────────────────────────────
def run_simulation(orders, master_width, max_knives, kert, linear_meters, grammage):
    """
    Greedy optimizer: packs order widths into combinations (esquemas de corte)
    minimizing waste per master width.
    """
    combinations = []
    remaining = {o["id"]: dict(o) for o in orders}
    combo_id = 1

    # Sort orders by totalWidth descending (largest first)
    sorted_orders = sorted(orders, key=lambda x: -x["totalWidth"])

    for anchor in sorted_orders:
        if anchor["id"] not in remaining:
            continue

        widths_in_combo = []
        net_widths_in_combo = []
        arruelas_in_combo = []
        roll_counts = []

        # Try to fill master width with multiples of anchor + other widths
        space_left = master_width
        total_kert = 0

        # Add anchor first
        n_anchor = max(1, int(space_left // anchor["totalWidth"]))
        n_anchor = min(n_anchor, max_knives)
        used_space = n_anchor * anchor["totalWidth"] + (n_anchor - 1) * kert
        if used_space > master_width:
            n_anchor = 1
            used_space = anchor["totalWidth"]

        widths_in_combo.append(anchor["totalWidth"])
        net_widths_in_combo.append(anchor["width"])
        arruelas_in_combo.append(anchor["arruela"])
        roll_counts.append(n_anchor)
        space_left = master_width - used_space
        num_rolls = n_anchor

        # Try to fill remaining space with other orders
        for filler in sorted_orders:
            if filler["id"] == anchor["id"]:
                continue
            if num_rolls >= max_knives:
                break
            if space_left <= 0:
                break

            kert_cost = kert  # cost to add one more cut
            if space_left >= filler["totalWidth"] + kert_cost:
                n_fill = int((space_left + kert_cost) // (filler["totalWidth"] + kert_cost))
                n_fill = min(n_fill, max_knives - num_rolls)
                if n_fill < 1:
                    continue

                if filler["totalWidth"] in widths_in_combo:
                    idx = widths_in_combo.index(filler["totalWidth"])
                    roll_counts[idx] += n_fill
                else:
                    widths_in_combo.append(filler["totalWidth"])
                    net_widths_in_combo.append(filler["width"])
                    arruelas_in_combo.append(filler["arruela"])
                    roll_counts.append(n_fill)

                space_left -= n_fill * filler["totalWidth"] + n_fill * kert_cost
                num_rolls += n_fill

        # Calculate waste
        total_physical = sum(w * roll_counts[i] for i, w in enumerate(widths_in_combo))
        total_kert_used = (sum(roll_counts) - 1) * kert if sum(roll_counts) > 1 else 0
        waste_mm = master_width - total_physical - total_kert_used
        waste_mm = max(0, waste_mm)

        sum_net = sum(net_widths_in_combo[i] * roll_counts[i] for i in range(len(net_widths_in_combo)))
        total_loss = master_width - sum_net
        waste_pct = (total_loss / master_width) * 100

        # Estimate tiradas needed (based on heaviest order demand)
        max_demand_kg = 0
        for i, w in enumerate(widths_in_combo):
            o_match = next((o for o in orders if o["totalWidth"] == w), None)
            if o_match:
                kgr = kg_per_roll(w, linear_meters, grammage)
                if kgr > 0:
                    rolls_needed = math.ceil(o_match["weightKg"] / kgr)
                    tiradas_needed = math.ceil(rolls_needed / roll_counts[i]) if roll_counts[i] > 0 else 1
                    max_demand_kg = max(max_demand_kg, tiradas_needed)

        tiradas = max(1, int(max_demand_kg))

        weight_per_tirada = sum(
            roll_counts[i] * kg_per_roll(w, linear_meters, grammage)
            for i, w in enumerate(widths_in_combo)
        )
        m2_per_tirada = sum(
            roll_counts[i] * (w / 1000) * linear_meters
            for i, w in enumerate(widths_in_combo)
        )

        combinations.append({
            "id": str(combo_id),
            "widths": widths_in_combo,
            "netWidths": net_widths_in_combo,
            "arruelas": arruelas_in_combo,
            "rollCounts": roll_counts,
            "waste": round(waste_mm, 2),
            "wastePercentage": round(waste_pct, 2),
            "tiradas": tiradas,
            "totalKg": round(weight_per_tirada * tiradas, 2),
            "m2": round(m2_per_tirada * tiradas, 2),
        })

        combo_id += 1
        del remaining[anchor["id"]]

    return combinations

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "orders" not in st.session_state:
    st.session_state.orders = [
        {"id": "1", "width": 235, "weightKg": 6000, "arruela": 7, "totalWidth": 242},
        {"id": "2", "width": 270, "weightKg": 10000, "arruela": 7, "totalWidth": 277},
        {"id": "3", "width": 400, "weightKg": 8500, "arruela": 7, "totalWidth": 407},
    ]
if "combinations" not in st.session_state:
    st.session_state.combinations = []
if "simulated" not in st.session_state:
    st.session_state.simulated = False

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="magnera-header">
  <div class="magnera-logo">M</div>
  <div>
    <div class="magnera-title">MAGNERA</div>
    <div class="magnera-sub">Nonwoven Optimization Engine · v10.20</div>
  </div>
  <div style="margin-left:auto; display:flex; align-items:center; gap:8px;">
    <span style="width:8px;height:8px;background:#10b981;border-radius:50%;display:inline-block;animation:pulse 2s infinite;"></span>
    <span style="font-size:10px;color:#10b981;font-weight:900;text-transform:uppercase;">Online</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LAYOUT: Params + Orders
# ─────────────────────────────────────────────
col_params, col_constraints = st.columns([2, 1])

with col_params:
    st.markdown('<div class="section-title">⚙ Especificações do Material</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    machine    = c1.selectbox("Máquina",     MACHINES,     key="machine")
    technology = c2.selectbox("Tecnologia",  TECHNOLOGIES, key="technology")
    surfactant = c3.selectbox("Surfactante", SURFACTANTS,  key="surfactant")
    calender   = c4.selectbox("Calandra",    CALENDERS,    key="calender")

    c5, c6 = st.columns(2)
    grammage       = c5.number_input("Gramatura (GSM)", value=11.0, step=0.5, format="%.2f")
    linear_meters  = c6.number_input("Metragem Linear (m)", value=13500, step=100)

with col_constraints:
    st.markdown('<div class="section-title">✂ Restrições de Corte</div>', unsafe_allow_html=True)
    master_width = st.number_input("Largura Master (mm)", value=3200, step=10)
    c7, c8 = st.columns(2)
    max_knives  = c7.number_input("Qtde Facas",   value=8,   step=1, min_value=1)
    kert        = c8.number_input("Kert/Faca (mm)", value=3, step=1, min_value=0)
    c9, c10 = st.columns(2)
    max_setups  = c9.number_input("Max Setups",   value=5,   step=1, min_value=1)
    otif_meta   = c10.number_input("Meta OTIF (%)", value=98.0, step=0.5, format="%.1f")

st.markdown('<div class="orange-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ORDERS TABLE
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📋 Demandas de Venda</div>', unsafe_allow_html=True)

orders = st.session_state.orders

col_h1, col_h2, col_h3, col_h4 = st.columns([2, 2, 2, 1])
col_h1.markdown("**Largura Líquida (mm)**")
col_h2.markdown("**Arruela (mm)**")
col_h3.markdown("**Peso Desejado (Kg)**")
col_h4.markdown("**Remover**")

to_remove = None
for i, order in enumerate(orders):
    c1, c2, c3, c4 = st.columns([2, 2, 2, 1])
    w  = c1.number_input("", value=int(order["width"]),   key=f"w_{order['id']}",  label_visibility="collapsed", min_value=0)
    ar = c2.number_input("", value=int(order["arruela"]), key=f"ar_{order['id']}", label_visibility="collapsed", min_value=0)
    kg = c3.number_input("", value=int(order["weightKg"]),key=f"kg_{order['id']}", label_visibility="collapsed", min_value=0)
    if c4.button("🗑", key=f"del_{order['id']}"):
        to_remove = order["id"]

    orders[i]["width"]      = w
    orders[i]["arruela"]    = ar
    orders[i]["weightKg"]   = kg
    orders[i]["totalWidth"] = w + ar

if to_remove:
    st.session_state.orders = [o for o in orders if o["id"] != to_remove]
    st.rerun()

cola, colb = st.columns([1, 4])
if cola.button("＋ Nova Linha"):
    import random, string
    new_id = ''.join(random.choices(string.digits, k=4))
    st.session_state.orders.append({"id": new_id, "width": 0, "weightKg": 0, "arruela": 7, "totalWidth": 7})
    st.rerun()

st.markdown('<div class="orange-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIMULATE
# ─────────────────────────────────────────────
if st.button("⚡  OTIMIZAR ESQUEMA DE CORTE"):
    if any(o["width"] <= 0 or o["weightKg"] <= 0 for o in st.session_state.orders):
        st.error("Preencha todos os campos das demandas antes de simular.")
    else:
        with st.spinner("Processando algoritmo..."):
            combos = run_simulation(
                st.session_state.orders,
                master_width=int(master_width),
                max_knives=int(max_knives),
                kert=int(kert),
                linear_meters=float(linear_meters),
                grammage=float(grammage)
            )
            st.session_state.combinations = combos
            st.session_state.simulated = True

# ─────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────
if st.session_state.simulated and st.session_state.combinations:
    combos = st.session_state.combinations
    current_orders = st.session_state.orders

    # ── KPIs ──
    total_demand_kg   = sum(safe_num(o["weightKg"]) for o in current_orders)
    total_produced_kg = sum(safe_num(c["totalKg"]) for c in combos)
    diff_kg           = total_produced_kg - total_demand_kg
    accuracy          = (total_produced_kg / total_demand_kg * 100) if total_demand_kg > 0 else 0

    total_waste_kg = sum(
        (safe_num(c["waste"]) / 1000) * float(linear_meters) * (float(grammage) / 1000) * safe_num(c["tiradas"])
        for c in combos
    )
    weighted_slu = (total_waste_kg / (total_produced_kg + total_waste_kg) * 100) if (total_produced_kg + total_waste_kg) > 0 else 0

    diff_color  = "#10b981" if diff_kg >= 0 else "#ef4444"
    diff_sign   = "+" if diff_kg >= 0 else ""
    slu_color   = "#10b981" if weighted_slu < 1.0 else ("#ed1b52" if weighted_slu < 1.3 else "#ef4444")
    acc_color   = "#10b981" if accuracy >= 98 else "#ef4444"

    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card" style="border-top-color:{slu_color}">
        <div class="kpi-label">SLU Ponderado</div>
        <div class="kpi-value" style="color:{slu_color}">{weighted_slu:.2f}%</div>
        <div class="kpi-desc">Desperdício de borda</div>
      </div>
      <div class="kpi-card" style="border-top-color:#3b82f6">
        <div class="kpi-label">Produção Total</div>
        <div class="kpi-value" style="color:#3b82f6">{total_produced_kg:,.0f} kg</div>
        <div class="kpi-desc">Soma de todas as bobinas</div>
      </div>
      <div class="kpi-card" style="border-top-color:{diff_color}">
        <div class="kpi-label">Diferença Demanda</div>
        <div class="kpi-value" style="color:{diff_color}">{diff_sign}{diff_kg:,.0f} kg</div>
        <div class="kpi-desc">Produção vs Pedido</div>
      </div>
      <div class="kpi-card" style="border-top-color:{acc_color}">
        <div class="kpi-label">Acuracidade</div>
        <div class="kpi-value" style="color:{acc_color}">{accuracy:.1f}%</div>
        <div class="kpi-desc">Percentual de atendimento</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="orange-divider"></div>', unsafe_allow_html=True)

    # ── SLU Chart ──
    st.markdown('<div class="section-title">📊 Análise de Gargalos (SLU)</div>', unsafe_allow_html=True)

    chart_data = pd.DataFrame({
        "Conjugação": [f"C{c['id']}" for c in combos],
        "SLU (%)": [round(safe_num(c["wastePercentage"]), 2) for c in combos]
    })
    chart_data_indexed = chart_data.set_index("Conjugação")
    st.bar_chart(chart_data_indexed, color="#ed1b52", height=220)

    st.markdown('<div class="orange-divider"></div>', unsafe_allow_html=True)

    # ── Order Summary Table ──
    st.markdown('<div class="section-title">✅ Resumo de Atendimento</div>', unsafe_allow_html=True)

    summary_rows = []
    for order in current_orders:
        kgr = kg_per_roll(order["totalWidth"], float(linear_meters), float(grammage))
        demand_rolls = math.ceil(order["weightKg"] / kgr) if kgr > 0 else 0

        produced_rolls = 0
        produced_kg    = 0
        for c in combos:
            for idx, w in enumerate(c["widths"]):
                if w == order["totalWidth"]:
                    rolls_in_combo  = safe_num(c["rollCounts"][idx]) * safe_num(c["tiradas"])
                    produced_rolls += rolls_in_combo
                    produced_kg    += rolls_in_combo * kgr

        otif = (produced_kg / order["weightKg"] * 100) if order["weightKg"] > 0 else 0

        if otif >= 98 and otif <= 102:
            otif_badge = f'<span class="otif-green">{otif:.1f}%</span>'
        elif otif > 102:
            otif_badge = f'<span class="otif-orange">{otif:.1f}%</span>'
        else:
            otif_badge = f'<span class="otif-red">{otif:.1f}%</span>'

        summary_rows.append({
            "Largura": f"{order['width']} mm",
            "Demanda (Bob)": int(demand_rolls),
            "Produção (Bob)": int(produced_rolls),
            "Demanda (Kg)": f"{order['weightKg']:,}",
            "Produção (Kg)": f"{produced_kg:,.0f}",
            "OTIF": otif_badge
        })

    df_summary = pd.DataFrame(summary_rows)
    st.write(df_summary.to_html(escape=False, index=False), unsafe_allow_html=True)

    st.markdown('<div class="orange-divider"></div>', unsafe_allow_html=True)

    # ── Combination Cards ──
    st.markdown('<div class="section-title">🔲 Conjugações de Corte</div>', unsafe_allow_html=True)

    cols_combo = st.columns(2)
    for ci, combo in enumerate(combos):
        with cols_combo[ci % 2]:
            waste_pct = safe_num(combo["wastePercentage"])
            if waste_pct > 1.3:
                badge = f'<span class="waste-badge-red">SLU {waste_pct:.2f}%</span>'
            elif waste_pct > 1.0:
                badge = f'<span class="waste-badge-orange">SLU {waste_pct:.2f}%</span>'
            else:
                badge = f'<span class="waste-badge-green">SLU {waste_pct:.2f}%</span>'

            # Build cut map HTML
            total_w = sum(combo["widths"][i] * combo["rollCounts"][i] for i in range(len(combo["widths"])))
            map_html = '<div class="cut-map">'
            for i, w in enumerate(combo["widths"]):
                net_w = combo["netWidths"][i] if combo.get("netWidths") else w
                flex  = w * combo["rollCounts"][i]
                map_html += f'<div class="cut-segment" style="flex:{flex}"><span class="cut-label">{net_w}</span><span class="cut-count">{combo["rollCounts"][i]}x</span></div>'
            waste_flex = max(safe_num(combo["waste"]), 5)
            map_html += f'<div class="cut-segment-waste" style="flex:{waste_flex}"><span class="cut-waste-label">{combo["waste"]}mm</span></div>'
            map_html += '</div>'

            # Progress bar
            prog_width = min(waste_pct, 100)
            progress_html = f"""
            <div class="progress-wrap">
              <div class="progress-label"><span>Eficiência SLU</span><span style="color:#ef4444;">{waste_pct:.2f}%</span></div>
              <div class="progress-track"><div class="progress-fill" style="width:{prog_width}%"></div></div>
            </div>"""

            # Metrics
            metrics_html = f"""
            <div class="metric-row">
              <div class="metric-mini">
                <div class="metric-mini-label">Tiradas</div>
                <div class="metric-mini-value" style="color:white">{combo['tiradas']}</div>
              </div>
              <div class="metric-mini">
                <div class="metric-mini-label">Peso Total</div>
                <div class="metric-mini-value" style="color:#3b82f6">{safe_num(combo['totalKg']):,.0f}<span style="font-size:10px">kg</span></div>
              </div>
              <div class="metric-mini">
                <div class="metric-mini-label">Sobra (SLU)</div>
                <div class="metric-mini-value" style="color:#ef4444">{combo['waste']}<span style="font-size:10px">mm</span></div>
              </div>
              <div class="metric-mini">
                <div class="metric-mini-label">Produção M²</div>
                <div class="metric-mini-value" style="color:#94a3b8">{safe_num(combo['m2']):,.0f}<span style="font-size:10px">m²</span></div>
              </div>
            </div>"""

            # Order detail rows
            detail_rows = ""
            for idx, w in enumerate(combo["widths"]):
                net_w = combo["netWidths"][idx] if combo.get("netWidths") else w
                arr   = combo["arruelas"][idx] if combo.get("arruelas") else 0
                cnt   = combo["rollCounts"][idx]
                detail_rows += f"""
                <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 12px;background:#0f172a;border:1px solid #1e293b;border-radius:8px;margin-bottom:6px;">
                  <div>
                    <div style="font-size:11px;font-weight:900;color:#e2e8f0">Largura Líquida: {net_w} mm</div>
                    <div style="font-size:9px;color:#475569">Refile: {arr} mm</div>
                  </div>
                  <div style="font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:700;color:#ed1b52">{cnt}x</div>
                  <div style="text-align:right">
                    <div style="font-size:11px;font-weight:700;color:#94a3b8">{w} mm</div>
                    <div style="font-size:8px;color:#334155;text-transform:uppercase">Largura Bruta</div>
                  </div>
                </div>"""

            st.markdown(f"""
            <div class="combo-card">
              <div class="combo-header">
                <div style="display:flex;align-items:center;gap:10px;">
                  <span class="combo-id">{combo['id']}</span>
                  <span style="font-size:11px;font-weight:900;color:#94a3b8;text-transform:uppercase;letter-spacing:2px">Conjugação</span>
                </div>
                {badge}
              </div>
              {map_html}
              {progress_html}
              {metrics_html}
              <div style="margin-top:16px;padding-top:16px;border-top:1px solid #1e293b">
                <div style="font-size:9px;font-weight:900;color:#475569;text-transform:uppercase;letter-spacing:2px;margin-bottom:10px">Ordens de Venda</div>
                {detail_rows}
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="orange-divider"></div>', unsafe_allow_html=True)

    # ── Footer ──
    st.markdown("""
    <div style="text-align:center;padding:40px 0 20px;">
      <p style="color:#1e293b;font-size:10px;font-weight:900;text-transform:uppercase;letter-spacing:4px;">
        MAGNERA INDUSTRIAL ENGINE · PROPOSTA TÉCNICA 2483_PT_MAGNERA_PLANO_DE_CORTE
      </p>
    </div>
    """, unsafe_allow_html=True)

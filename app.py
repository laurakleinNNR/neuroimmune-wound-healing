
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="WoundSignal | Neuroimmune Atlas",
    page_icon="W",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# WOUNDSIGNAL — VISUAL DESIGN SYSTEM
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #142640;
    --blue: #6689E8;
    --ice: #EAF4FF;
    --cyan: #BCEAF3;
    --lavender: #DDD9FA;
    --mint: #D5F0E8;
    --pink: #F5DCE9;
    --ink: #1B2B44;
    --muted: #7D8BA1;
    --line: #E4EBF5;
    --canvas: #F6F9FD;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
}

.stApp { background: var(--canvas); }

header[data-testid="stHeader"] {
    background: rgba(246,249,253,.8);
}

.block-container {
    max-width: 1500px;
    padding: 2rem 3rem 4rem;
}

h1, h2, h3 {
    font-family: 'Manrope', sans-serif !important;
    color: var(--navy);
    letter-spacing: -0.8px;
}

.brand {
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
    font-size: 23px;
    letter-spacing: -1px;
    color: #172A46;
}
.brand span { color: #7699ED; }

.kicker {
    color: #718BD1;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2.3px;
    text-transform: uppercase;
}

.hero {
    background: linear-gradient(125deg,#E7F3FF 0%,#EEF0FF 48%,#E1F5F3 100%);
    border: 1px solid #DFE9F7;
    border-radius: 23px;
    padding: 42px 38px;
    margin: 18px 0 26px;
}

.hero h1 {
    font-size: clamp(34px,4vw,52px);
    line-height: 1.1;
    margin: 12px 0 15px;
    letter-spacing: -2.1px;
}

.hero p {
    color: #657893;
    font-size: 15px;
    line-height: 1.85;
    max-width: 700px;
}

.page-title {
    font-size: 35px;
    font-weight: 800;
    letter-spacing: -1.5px;
    margin: 5px 0;
}
.page-subtitle {
    font-size: 14px;
    color: #7A899F;
    line-height: 1.8;
    margin-bottom: 23px;
}

.module-card {
    background: white;
    border: 1px solid #E3EAF4;
    border-radius: 15px;
    padding: 22px;
    min-height: 190px;
    box-shadow: 0 5px 20px rgba(31,60,100,.035);
}
.module-number {
    font-size: 10px;
    color: #7A91D6;
    letter-spacing: 1.5px;
    font-weight: 700;
}
.module-title {
    font-family: 'Manrope', sans-serif;
    font-size: 17px;
    color: #1A2B45;
    font-weight: 800;
    margin: 15px 0 8px;
}
.module-desc {
    font-size: 12px;
    color: #8290A4;
    line-height: 1.8;
}
.module-accent {
    height: 4px;
    width: 37px;
    border-radius: 4px;
    margin-bottom: 16px;
}

.panel {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 15px;
    padding: 23px;
    box-shadow: 0 4px 18px rgba(31,60,100,.025);
    margin-bottom: 16px;
}
.panel-title {
    font-family: 'Manrope', sans-serif;
    font-size: 17px;
    font-weight: 800;
    color: #192B45;
}
.panel-sub {
    color: #8390A4;
    font-size: 12px;
    line-height: 1.8;
    margin: 5px 0 17px;
}
.metric {
    background: white;
    border: 1px solid var(--line);
    border-radius: 13px;
    padding: 20px;
    min-height: 115px;
}
.metric-label {
    color: #8190A6;
    font-size: 10px;
    letter-spacing: 1.2px;
    font-weight: 700;
}
.metric-value {
    font-family: 'Manrope', sans-serif;
    color: #1A2B45;
    font-size: 30px;
    font-weight: 800;
    margin-top: 10px;
}
.metric-note {
    color: #8B98AA;
    font-size: 11px;
    margin-top: 3px;
}
.note {
    background: #EDF4FF;
    border-left: 3px solid #8BA6ED;
    border-radius: 0 8px 8px 0;
    padding: 15px 18px;
    font-size: 12px;
    line-height: 1.9;
    color: #4F6584;
    margin: 14px 0 20px;
}
.tag {
    display: inline-block;
    background: #EDF2FF;
    color: #526DB7;
    padding: 6px 10px;
    border-radius: 5px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .8px;
}
.stButton > button {
    border-radius: 8px;
    border: 1px solid #DCE5F2;
    min-height: 40px;
    font-weight: 600;
    background: white;
    color: #263B59;
    transition: all .2s ease;
}
.stButton > button:hover {
    border-color: #91A9EB;
    color: #4267C9;
    background: #F5F8FF;
}
div[data-testid="stPlotlyChart"] {
    border-radius: 10px;
}
hr { border-color: #E5EBF4; margin: 25px 0; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# APP STATE AND NAVIGATION
# ============================================================

MODULES = {
    "Research Overview": {
        "number": "01",
        "description": "The research question, data status, and current analytical workflow.",
        "color": "#DDEAFF",
        "accent": "#7596E9",
    },
    "Expression Atlas": {
        "number": "02",
        "description": "Explore gene expression across conditions and cell populations.",
        "color": "#D8F1F1",
        "accent": "#76C9CF",
    },
    "Brain & Neural Signaling": {
        "number": "03",
        "description": "Explore a conceptual neural map and the biology of CGRP signaling.",
        "color": "#E7E0FC",
        "accent": "#A69AE9",
    },
    "Cell Populations": {
        "number": "04",
        "description": "Investigate immune, stromal, and vascular cell contexts.",
        "color": "#DDF2E8",
        "accent": "#83C6A8",
    },
    "Target Prioritization": {
        "number": "05",
        "description": "Review candidate genes and the evidence needed to assess them.",
        "color": "#F6E4ED",
        "accent": "#D8A0BD",
    },
    "Knowledge Center": {
        "number": "06",
        "description": "Understand the biology, data, terminology, and methods.",
        "color": "#E2EBFC",
        "accent": "#8EADE8",
    },
}

if "page" not in st.session_state:
    st.session_state.page = "Home"

def go_to(name):
    st.session_state.page = name

def header():
    a, b = st.columns([3, 2], vertical_alignment="center")
    with a:
        st.markdown(
            '<div class="brand">Wound<span>Signal</span></div>'
            '<div style="font-size:10px;color:#8A98AD;'
            'letter-spacing:1.8px;margin-top:3px;">'
            'COMPUTATIONAL NEUROIMMUNE ATLAS</div>',
            unsafe_allow_html=True,
        )
    with b:
        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("Home", use_container_width=True):
                go_to("Home")
                st.rerun()
        with c2:
            if st.button("Research data", use_container_width=True):
                go_to("Data & Methods")
                st.rerun()

def page_heading(title, subtitle):
    st.markdown(f'<div class="kicker">WOUNDSIGNAL / RESEARCH WORKSPACE</div>',
                unsafe_allow_html=True)
    st.markdown(f'<div class="page-title">{title}</div>',
                unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{subtitle}</div>',
                unsafe_allow_html=True)

def panel_heading(title, subtitle=""):
    st.markdown(
        f'<div class="panel-title">{title}</div>'
        f'<div class="panel-sub">{subtitle}</div>',
        unsafe_allow_html=True,
    )

header()
st.markdown("<hr>", unsafe_allow_html=True)


# ============================================================
# DEMONSTRATION DATA
# Synthetic values are not biological findings.
# ============================================================

GENES = [
    "CALCRL", "RAMP1", "THBS1", "IL1B",
    "TNF", "VEGFA", "MRC1", "CD68"
]

CELLS = [
    "Macrophages", "Fibroblasts",
    "Endothelial cells", "Neutrophils"
]

@st.cache_data
def demo_data():
    rng = np.random.default_rng(42)

    baseline = {
        "Macrophages": [4.1, 4.3, 5.1, 7.0, 5.9, 4.4, 5.4, 7.2],
        "Fibroblasts": [3.0, 3.4, 6.0, 2.2, 2.0, 4.8, 1.5, 1.2],
        "Endothelial cells": [3.6, 3.2, 4.0, 2.5, 2.2, 7.0, 1.4, 1.3],
        "Neutrophils": [2.8, 2.5, 3.1, 7.4, 5.6, 3.1, 1.1, 5.8],
    }

    rows = []
    for condition in ["Healing", "Non-healing"]:
        for cell in CELLS:
            for sample in range(1, 7):
                for gene, base in zip(GENES, baseline[cell]):
                    value = base
                    if condition == "Non-healing":
                        if gene in ["IL1B", "TNF"] and cell in [
                            "Macrophages", "Neutrophils"
                        ]:
                            value += 1.0
                        if gene == "VEGFA" and cell == "Endothelial cells":
                            value -= 0.8
                        if gene == "THBS1" and cell == "Fibroblasts":
                            value += 0.5

                    rows.append({
                        "sample_id": f"{condition[:2].upper()}_{sample:02d}",
                        "condition": condition,
                        "cell_type": cell,
                        "gene": gene,
                        "expression": round(max(0, rng.normal(value, .65)), 3)
                    })
    return pd.DataFrame(rows)


with st.expander("DATA SOURCE SETTINGS", expanded=False):
    source = st.radio(
        "Choose data source",
        ["Synthetic demonstration data", "Upload expression CSV"],
        horizontal=True,
    )
    uploaded = None
    if source == "Upload expression CSV":
        uploaded = st.file_uploader("Upload a CSV", type=["csv"])

required = {"sample_id", "condition", "cell_type", "gene", "expression"}

if source == "Synthetic demonstration data":
    df = demo_data()
    synthetic = True
elif uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
        missing = required - set(df.columns)
        if missing:
            st.error("Missing columns: " + ", ".join(sorted(missing)))
            st.stop()

        df = df[list(required)].copy()
        df["expression"] = pd.to_numeric(df["expression"], errors="coerce")
        df = df.dropna(subset=list(required))

        if df.empty or (df["expression"] < 0).any():
            st.error("The file has no valid rows or contains negative expression.")
            st.stop()
        synthetic = False
    except Exception as exc:
        st.error(f"Could not read the file: {exc}")
        st.stop()
else:
    st.info("Upload an expression CSV, or select synthetic demonstration data.")
    st.stop()

if synthetic:
    st.markdown(
        '<div class="note"><strong>Demonstration mode:</strong> '
        'All current expression values are synthetic. They are invented '
        'for interface testing, not patient data or scientific evidence.</div>',
        unsafe_allow_html=True,
    )

conditions = sorted(df["condition"].astype(str).unique())
cells = sorted(df["cell_type"].astype(str).unique())
genes = sorted(df["gene"].astype(str).unique())

if len(conditions) < 2:
    st.error("The dataset must contain at least two conditions.")
    st.stop()

with st.expander("ANALYSIS FILTERS", expanded=False):
    default_conditions = ["Healing", "Non-healing"]
    defaults = [x for x in default_conditions if x in conditions]
    if len(defaults) != 2:
        defaults = conditions[:2]

    chosen_conditions = st.multiselect(
        "Conditions", conditions, default=defaults
    )
    chosen_cells = st.multiselect("Cell populations", cells, default=cells)
    chosen_genes = st.multiselect("Genes", genes, default=genes)

if len(chosen_conditions) < 2:
    st.warning("Select at least two conditions.")
    st.stop()
if not chosen_cells or not chosen_genes:
    st.warning("Select at least one gene and cell population.")
    st.stop()

data = df[
    df["condition"].isin(chosen_conditions)
    & df["cell_type"].isin(chosen_cells)
    & df["gene"].isin(chosen_genes)
].copy()

if data.empty:
    st.warning("No data match these filters.")
    st.stop()


# ============================================================
# HOME — LANDING PAGE
# ============================================================

if st.session_state.page == "Home":

    st.markdown("""
    <div class="hero">
        <div class="kicker">AN EXPLORATORY RESEARCH PLATFORM</div>
        <h1>Understanding the signals<br>behind wound repair.</h1>
        <p>
        WoundSignal is a computational research workspace for exploring
        the relationship between neural signaling, immune activity, and
        chronic wound healing. Move from biological concepts to expression
        patterns and testable research questions.
        </p>
        <span class="tag">NEUROIMMUNOLOGY</span>
        &nbsp;
        <span class="tag">GENE EXPRESSION</span>
        &nbsp;
        <span class="tag">COMPUTATIONAL BIOLOGY</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Explore the research workspace")
    st.markdown(
        '<div class="page-subtitle">Choose a module to begin exploring.</div>',
        unsafe_allow_html=True,
    )

    items = list(MODULES.items())
    for start in range(0, len(items), 3):
        cols = st.columns(3, gap="medium")
        for col, (name, info) in zip(cols, items[start:start + 3]):
            with col:
                st.markdown(
                    f'<div class="module-card">'
                    f'<div class="module-accent" style="background:{info["accent"]};"></div>'
                    f'<div class="module-number">MODULE {info["number"]}</div>'
                    f'<div class="module-title">{name}</div>'
                    f'<div class="module-desc">{info["description"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                if st.button(
                    f"Open {name}  →",
                    key=f"open_{name}",
                    use_container_width=True,
                ):
                    go_to(name)
                    st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    left, right = st.columns([1.4, 1], gap="large")

    with left:
        st.markdown("### The central question")
        st.markdown(
            "Can human gene-expression data help identify cell populations "
            "and pathways worth investigating in CGRP-associated "
            "neuroimmune signaling and chronic wound repair?"
        )
        st.markdown(
            '<div class="note">The platform is designed to generate and '
            'evaluate hypotheses. Gene expression alone cannot demonstrate '
            'causality, receptor activation, or treatment effectiveness.</div>',
            unsafe_allow_html=True,
        )

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_heading("Research framework", "A transparent path from data to hypotheses.")
        for number, title, desc in [
            ("01", "Verify", "Confirm source, metadata, and sample structure."),
            ("02", "Explore", "Inspect patterns across genes and cell types."),
            ("03", "Validate", "Test findings in suitable independent data."),
        ]:
            st.markdown(
                f'<div style="display:flex;gap:13px;margin:16px 0;">'
                f'<div style="color:#7995E3;font-weight:800;font-size:12px;">{number}</div>'
                f'<div><strong>{title}</strong><div style="font-size:12px;'
                f'color:#8491A4;line-height:1.7;">{desc}</div></div></div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# RESEARCH OVERVIEW
# ============================================================

elif st.session_state.page == "Research Overview":

    page_heading(
        "Research Overview",
        "A high-level view of the selected dataset and the project's scientific scope.",
    )

    cols = st.columns(4)
    metrics = [
        ("OBSERVATIONS", f"{len(data):,}", "Filtered rows"),
        ("GENES", str(data["gene"].nunique()), "Selected panel"),
        ("CELL POPULATIONS", str(data["cell_type"].nunique()), "Included types"),
        ("CONDITIONS", str(data["condition"].nunique()), "Comparison groups"),
    ]

    for col, (label, value, note) in zip(cols, metrics):
        with col:
            st.markdown(
                f'<div class="metric"><div class="metric-label">{label}</div>'
                f'<div class="metric-value">{value}</div>'
                f'<div class="metric-note">{note}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("### Expression landscape")
    gene = st.selectbox("Gene to visualize", chosen_genes, key="overview_gene")
    subset = data[data["gene"] == gene]
    summary = (
        subset.groupby(["condition", "cell_type"], as_index=False)
        ["expression"].mean()
    )

    fig = px.bar(
        summary, x="cell_type", y="expression", color="condition",
        barmode="group",
        color_discrete_sequence=["#7B9BEA", "#8ED6DD"],
        labels={"expression": "Mean expression", "cell_type": "Cell population"},
    )
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="DM Sans", color="#687A92"),
        margin=dict(l=15, r=15, t=25, b=15),
        height=390,
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#EEF2F8"),
        legend=dict(orientation="h", y=1.12),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Workflow")
    workflow = st.columns(3)
    for col, n, title, desc in zip(
        workflow,
        ["01", "02", "03"],
        ["Data validation", "Expression analysis", "Independent validation"],
        [
            "Check provenance and clinical metadata.",
            "Compare patterns with appropriate biological replication.",
            "Test reproducibility in a separate compatible dataset.",
        ],
    ):
        with col:
            st.markdown(
                f'<div class="panel"><div class="kicker">STAGE {n}</div>'
                f'<h3 style="font-size:18px;margin-top:12px;">{title}</h3>'
                f'<div class="module-desc">{desc}</div></div>',
                unsafe_allow_html=True,
            )


# ============================================================
# EXPRESSION ATLAS
# ============================================================

elif st.session_state.page == "Expression Atlas":

    page_heading(
        "Expression Atlas",
        "Compare expression patterns across genes, cell populations, and conditions.",
    )

    gene = st.selectbox("Choose a gene", chosen_genes, key="atlas_gene")
    subset = data[data["gene"] == gene]

    summary = (
        subset.groupby(["condition", "cell_type"], as_index=False)
        ["expression"].agg(["mean", "std", "count"]).reset_index()
    )
    summary["std"] = summary["std"].fillna(0)

    fig = px.bar(
        summary, x="cell_type", y="mean", color="condition",
        barmode="group", error_y="std",
        color_discrete_sequence=["#7B9BEA", "#8ED6DD"],
        labels={"mean": "Mean expression", "cell_type": "Cell population"},
    )
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white", height=440,
        font=dict(family="DM Sans", color="#687A92"),
        margin=dict(l=15, r=15, t=20, b=15),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#EEF2F8"),
        legend=dict(orientation="h", y=1.12),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Summary")
    st.dataframe(summary, use_container_width=True, hide_index=True)
    st.download_button(
        "Download summary CSV",
        summary.to_csv(index=False).encode("utf-8"),
        file_name=f"{gene}_summary.csv",
        mime="text/csv",
    )
    st.caption(
        "Error bars represent standard deviation across rows, not confidence "
        "intervals. Interpretation depends on the uploaded data structure."
    )


# ============================================================
# BRAIN & NEURAL SIGNALING
# ============================================================

elif st.session_state.page == "Brain & Neural Signaling":

    page_heading(
        "Brain & Neural Signaling",
        "A conceptual map for exploring the nervous system and the biology of CGRP.",
    )

    st.markdown(
        '<div class="note">This is an educational schematic, not a brain scan, '
        'anatomical segmentation, or measured dataset. Chronic wound healing '
        'also involves peripheral sensory nerves and local tissue signaling; '
        'the brain is not the only relevant site.</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.4, 1], gap="large")

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_heading(
            "Neural signaling map",
            "Select a region or system to learn how it relates to neural biology.",
        )

        regions = {
            "Peripheral sensory neurons": {
                "color": "#A9DCD7",
                "description": (
                    "Sensory neurons detect tissue conditions and can release "
                    "neuropeptides, including CGRP, from peripheral nerve endings."
                ),
                "genes": "CALCRL, RAMP1",
            },
            "Brainstem": {
                "color": "#B9C7F4",
                "description": (
                    "Brainstem circuits participate in sensory processing and "
                    "autonomic regulation. Their role depends on the biological "
                    "question and experimental context."
                ),
                "genes": "Context-dependent",
            },
            "Thalamus": {
                "color": "#D9C9F3",
                "description": (
                    "The thalamus relays and modulates many sensory signals. "
                    "It is included here as an educational landmark, not as a "
                    "demonstrated driver of wound repair."
                ),
                "genes": "Not inferred by this dataset",
            },
            "Cortical networks": {
                "color": "#F0CDE0",
                "description": (
                    "Cortical networks contribute to perception, cognition, "
                    "and the interpretation of sensory experience. A wound "
                    "gene-expression table does not directly measure these processes."
                ),
                "genes": "Not inferred by this dataset",
            },
        }

        region = st.selectbox("Explore a system", list(regions.keys()))
        selected = regions[region]

        # Stylized bilateral brain-like schematic made from Plotly shapes.
        fig = go.Figure()

        # Left and right hemispheres: abstract rounded lobes.
        fig.add_shape(
            type="circle", x0=-2.1, y0=-1.45, x1=-0.05, y1=1.45,
            fillcolor="#DDE7FC", line=dict(color="#AABBEA", width=2)
        )
        fig.add_shape(
            type="circle", x0=0.05, y0=-1.45, x1=2.1, y1=1.45,
            fillcolor="#E8E2FB", line=dict(color="#BEB3EA", width=2)
        )

        # Conceptual regions, intentionally not anatomical boundaries.
        fig.add_shape(
            type="circle", x0=-1.65, y0=.25, x1=-.75, y1=1.0,
            fillcolor="#A9DCD7", line=dict(color="white", width=2)
        )
        fig.add_shape(
            type="circle", x0=.75, y0=.25, x1=1.65, y1=1.0,
            fillcolor="#F0CDE0", line=dict(color="white", width=2)
        )
        fig.add_shape(
            type="circle", x0=-.62, y0=-.25, x1=.0, y1=.35,
            fillcolor="#B9C7F4", line=dict(color="white", width=2)
        )
        fig.add_shape(
            type="circle", x0=.0, y0=-.25, x1=.62, y1=.35,
            fillcolor="#D9C9F3", line=dict(color="white", width=2)
        )

        fig.add_trace(go.Scatter(
            x=[-1.2, 1.2, -.3, .3],
            y=[.62, .62, .05, .05],
            mode="markers+text",
            text=["Sensory", "Cortical", "Brainstem", "Thalamus"],
            textposition="bottom center",
            marker=dict(size=12, color=[
                "#5DAFA8", "#D28BB4", "#718ED9", "#A58BD9"
            ], line=dict(color="white", width=2)),
            hovertemplate="%{text}<extra></extra>",
            showlegend=False,
        ))

        fig.update_layout(
            height=430,
            paper_bgcolor="white",
            plot_bgcolor="white",
            margin=dict(l=15, r=15, t=10, b=15),
            xaxis=dict(visible=False, range=[-2.5, 2.5]),
            yaxis=dict(visible=False, range=[-1.8, 1.8], scaleanchor="x"),
            showlegend=False,
        )

        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "Pastel shapes are conceptual landmarks. They do not represent "
            "validated anatomical outlines or spatial gene-expression measurements."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_heading("Selected system", "Biological context")
        st.markdown(
            f'<div style="height:5px;width:42px;border-radius:5px;'
            f'background:{selected["color"]};margin:16px 0;"></div>'
            f'<h3 style="font-size:22px;">{region}</h3>'
            f'<div style="font-size:13px;color:#74849A;line-height:1.9;">'
            f'{selected["description"]}</div>'
            f'<hr>'
            f'<div class="kicker">GENE CONTEXT</div>'
            f'<div style="font-size:14px;margin-top:10px;">'
            f'{selected["genes"]}</div>',
            unsafe_allow_html=True,
        )

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_heading("CGRP receptor components")
        st.markdown(
            "**CALCRL** encodes the calcitonin receptor-like receptor. "
            "**RAMP1** is a receptor activity-modifying protein. Together "
            "they are components of the canonical CGRP receptor complex."
        )
        st.markdown(
            "Expression of these genes alone does not prove that CGRP is "
            "being released, that the receptor is activated, or that the "
            "pathway changes wound outcomes."
        )
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# CELL POPULATIONS
# ============================================================

elif st.session_state.page == "Cell Populations":

    page_heading(
        "Cell Populations",
        "Explore the different cellular contexts that contribute to wound biology.",
    )

    descriptions = {
        "Macrophages": "Immune regulation, inflammation, and tissue remodeling.",
        "Fibroblasts": "Extracellular matrix production and tissue repair.",
        "Endothelial cells": "Vascular biology and blood vessel formation.",
        "Neutrophils": "Innate immune responses and inflammatory signaling.",
    }

    cols = st.columns(2)
    for i, cell in enumerate(CELLS):
        with cols[i % 2]:
            st.markdown(
                f'<div class="panel"><div class="kicker">CELL TYPE {i+1:02d}</div>'
                f'<h3 style="font-size:20px;margin-top:12px;">{cell}</h3>'
                f'<div class="module-desc">{descriptions[cell]}</div></div>',
                unsafe_allow_html=True,
            )

    selected_cell = st.selectbox("Analyze a population", chosen_cells)
    subset = data[data["cell_type"] == selected_cell]
    summary = (
        subset.groupby(["gene", "condition"], as_index=False)["expression"]
        .mean()
    )

    fig = px.bar(
        summary, x="gene", y="expression", color="condition",
        barmode="group",
        color_discrete_sequence=["#7B9BEA", "#8ED6DD"],
        labels={"expression": "Mean expression", "gene": "Gene"},
    )
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white", height=400,
        font=dict(family="DM Sans", color="#687A92"),
        margin=dict(l=15, r=15, t=20, b=15),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#EEF2F8"),
        legend=dict(orientation="h", y=1.12),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(summary, use_container_width=True, hide_index=True)


# ============================================================
# TARGET PRIORITIZATION
# ============================================================

elif st.session_state.page == "Target Prioritization":

    page_heading(
        "Target Prioritization",
        "Review descriptive expression differences without confusing them with therapeutic evidence.",
    )

    st.markdown(
        '<div class="note">This module ranks differences in mean expression '
        'only. It does not establish statistical significance, causality, '
        'druggability, or therapeutic value.</div>',
        unsafe_allow_html=True,
    )

    cell = st.selectbox("Cell population", chosen_cells)
    subset = data[data["cell_type"] == cell]

    means = subset.groupby(["gene", "condition"])["expression"].mean().unstack()
    a, b = chosen_conditions[0], chosen_conditions[1]

    if a in means.columns and b in means.columns:
        ranking = means[[a, b]].dropna().copy()
        ranking["Difference"] = ranking[b] - ranking[a]
        ranking["Absolute difference"] = ranking["Difference"].abs()
        ranking = ranking.sort_values(
            "Absolute difference", ascending=False
        ).reset_index()
        ranking.insert(0, "Descriptive rank", range(1, len(ranking) + 1))

        fig = px.bar(
            ranking.sort_values("Difference"),
            x="Difference", y="gene", orientation="h",
            color="Difference",
            color_continuous_scale=["#A6DDE4", "#EEF2FB", "#829CE8"],
            labels={"Difference": f"Mean difference ({b} − {a})"},
        )
        fig.update_layout(
            paper_bgcolor="white", plot_bgcolor="white", height=390,
            font=dict(family="DM Sans", color="#687A92"),
            margin=dict(l=15, r=15, t=20, b=15),
            yaxis=dict(showgrid=False),
            xaxis=dict(gridcolor="#EEF2F8"),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(ranking, use_container_width=True, hide_index=True)
        st.download_button(
            "Download descriptive ranking",
            ranking.to_csv(index=False).encode("utf-8"),
            file_name="woundsignal_descriptive_ranking.csv",
            mime="text/csv",
        )
    else:
        st.warning("The selected conditions cannot be compared in this data.")


# ============================================================
# KNOWLEDGE CENTER
# ============================================================

elif st.session_state.page == "Knowledge Center":

    page_heading(
        "Knowledge Center",
        "Background concepts and practical guidance for interpreting the research.",
    )

    topics = {
        "What is CGRP?": (
            "Calcitonin gene-related peptide (CGRP) is a neuropeptide "
            "involved in sensory signaling and vascular biology. Its effects "
            "depend on tissue context, receptor availability, and the "
            "experimental setting. Its presence alone does not imply a "
            "specific outcome in wound repair."
        ),
        "What are CALCRL and RAMP1?": (
            "CALCRL encodes the calcitonin receptor-like receptor, while "
            "RAMP1 encodes receptor activity-modifying protein 1. These "
            "proteins form key components of the canonical CGRP receptor. "
            "Transcript abundance is not a direct measurement of receptor "
            "protein, signaling activity, or functional response."
        ),
        "Why do chronic wounds matter?": (
            "Chronic wounds can involve persistent inflammation, impaired "
            "tissue repair, vascular dysfunction, altered immune responses, "
            "and changes in the wound microenvironment. No single pathway "
            "explains every chronic wound."
        ),
        "What is single-cell RNA sequencing?": (
            "Single-cell RNA sequencing measures RNA transcripts in "
            "individual cells. It can help characterize cell populations "
            "and expression patterns, but results are affected by sampling, "
            "technical noise, cell recovery, normalization, and annotation."
        ),
        "Why are biological replicates important?": (
            "Thousands of cells from one person do not equal thousands of "
            "independent people. Statistical analyses should account for "
            "the patient or biological sample as the unit of replication, "
            "where appropriate."
        ),
        "What is independent validation?": (
            "Independent validation tests a finding in a separate dataset "
            "that is sufficiently comparable in tissue, clinical definition, "
            "measurement, and processing. A second dataset is not automatically "
            "a valid replication dataset."
        ),
        "What can expression differences tell us?": (
            "Differences can generate hypotheses about which genes or cell "
            "populations warrant further study. They do not independently "
            "prove mechanism, causation, clinical relevance, or treatment benefit."
        ),
    }

    for title, explanation in topics.items():
        with st.expander(title):
            st.write(explanation)

    st.markdown("### Gene reference panel")

    gene_notes = pd.DataFrame([
        ["CALCRL", "CGRP receptor component", "Neural and vascular signaling"],
        ["RAMP1", "CGRP receptor component", "Neural and vascular signaling"],
        ["THBS1", "Thrombospondin 1", "Extracellular matrix and vascular context"],
        ["IL1B", "Inflammatory cytokine", "Inflammation"],
        ["TNF", "Tumor necrosis factor", "Inflammation"],
        ["VEGFA", "Vascular endothelial growth factor A", "Angiogenesis"],
        ["MRC1", "Mannose receptor C-type 1", "Immune-cell context"],
        ["CD68", "Lysosomal glycoprotein marker", "Often used in macrophage studies"],
    ], columns=["Gene", "Description", "Research context"])

    st.dataframe(gene_notes, use_container_width=True, hide_index=True)

    st.markdown(
        '<div class="note">This gene panel is an exploratory starting point, '
        'not a validated signature of wound healing or CGRP activity. '
        'Verify each gene\'s role against reliable primary literature and '
        'the specific dataset being analyzed.</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# DATA & METHODS
# ============================================================

elif st.session_state.page == "Data & Methods":

    page_heading(
        "Data & Methods",
        "Review the selected data, required fields, and key analytical limitations.",
    )

    if synthetic:
        st.markdown(
            '<div class="note"><strong>Synthetic demonstration data active.</strong> '
            'These data are invented for interface testing and are not clinical '
            'or experimental observations.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.warning(
            "A CSV is loaded, but this application has not independently "
            "verified its provenance or scientific validity."
        )

    overview = pd.DataFrame({
        "Property": [
            "Rows in filtered data", "Unique sample identifiers",
            "Conditions", "Cell populations", "Genes", "Missing values"
        ],
        "Value": [
            len(data), data["sample_id"].nunique(),
            data["condition"].nunique(), data["cell_type"].nunique(),
            data["gene"].nunique(), int(data.isna().sum().sum())
        ],
    })
    st.dataframe(overview, use_container_width=True, hide_index=True)

    with st.expander("Sample-level replication"):
        st.write(
            "Cells from the same patient are not independent biological "
            "replicates. For single-cell studies, consider sample-level "
            "aggregation or appropriate statistical models."
        )

    with st.expander("Clinical metadata"):
        st.write(
            "Diabetes status is not equivalent to healing outcome. Confirm "
            "whether the source data actually contain healing status, "
            "follow-up, and relevant clinical variables."
        )

    with st.expander("Normalization and comparability"):
        st.write(
            "Verify gene identifiers, normalization, assay technology, "
            "and preprocessing before comparing values between datasets."
        )

    with st.expander("Statistical inference"):
        st.write(
            "Mean differences are descriptive. A rigorous analysis should "
            "address uncertainty, biological replication, confounding, "
            "and multiple testing."
        )

    st.markdown("### Filtered data preview")
    st.dataframe(data.head(100), use_container_width=True)
    st.download_button(
        "Download filtered data",
        data.to_csv(index=False).encode("utf-8"),
        file_name="woundsignal_filtered_data.csv",
        mime="text/csv",
    )


# ============================================================
# FOOTER AND NAVIGATION
# ============================================================

st.markdown("<hr>", unsafe_allow_html=True)

foot_left, foot_right = st.columns([2, 1])
with foot_left:
    st.markdown(
        '<div style="font-size:11px;color:#8A97AA;">'
        'WoundSignal · Computational neuroimmune research</div>',
        unsafe_allow_html=True,
    )
with foot_right:
    st.markdown(
        '<div style="font-size:11px;color:#8A97AA;text-align:right;">'
        'Exploratory platform · Interpret results with caution</div>',
        unsafe_allow_html=True,
    )

if st.session_state.page != "Home":
    if st.button("← Return to module home"):
        go_to("Home")
        st.rerun()

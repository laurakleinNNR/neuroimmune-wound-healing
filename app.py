
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="WoundSignal | Research Workspace",
    page_icon="W",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# DESIGN SYSTEM
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #101D35;
    --blue: #4269E1;
    --cyan: #71C9E8;
    --ink: #18263D;
    --muted: #718096;
    --line: #E4EAF3;
    --surface: #FFFFFF;
    --background: #F5F8FC;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
}

.stApp {
    background: var(--background);
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1500px;
    padding: 2rem 2.8rem 4rem 2.8rem;
}

[data-testid="stSidebar"] {
    background: #101D35;
    border-right: 1px solid #24334D;
}

[data-testid="stSidebar"] * {
    color: #E6EDF8;
}

[data-testid="stSidebar"] .stRadio label {
    font-size: 14px;
    padding-top: 5px;
    padding-bottom: 5px;
}

.brand {
    font-family: 'Manrope', sans-serif;
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -1.1px;
    color: #FFFFFF;
    margin: 5px 0 0 0;
}

.brand-sub {
    font-size: 10px;
    letter-spacing: 2.5px;
    color: #8EA8D0;
    margin-top: 5px;
    margin-bottom: 30px;
}

.sidebar-caption {
    color: #8497B6;
    font-size: 10px;
    letter-spacing: 1.8px;
    font-weight: 700;
    margin: 26px 0 10px 0;
}

.main-title {
    font-family: 'Manrope', sans-serif;
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: #14233D;
    margin-bottom: 4px;
}

.subtitle {
    font-size: 14px;
    color: #728097;
    line-height: 1.7;
}

.eyebrow {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #496DE0;
    margin-bottom: 10px;
}

.status-pill {
    display: inline-block;
    border: 1px solid #D8E4F8;
    background: #EDF3FF;
    color: #3157B7;
    padding: 7px 11px;
    border-radius: 5px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
}

.metric-card {
    background: white;
    border: 1px solid #E3EAF4;
    border-radius: 12px;
    padding: 20px 21px;
    min-height: 126px;
    box-shadow: 0 3px 12px rgba(27, 49, 86, 0.025);
}

.metric-label {
    color: #738198;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 13px;
}

.metric-value {
    font-family: 'Manrope', sans-serif;
    color: #162641;
    font-size: 31px;
    font-weight: 800;
    letter-spacing: -1px;
}

.metric-note {
    font-size: 11px;
    color: #8B98AC;
    margin-top: 4px;
}

.panel {
    background: white;
    border: 1px solid #E3EAF4;
    border-radius: 12px;
    padding: 22px 23px;
    box-shadow: 0 3px 12px rgba(27, 49, 86, 0.025);
    height: 100%;
}

.panel-title {
    font-family: 'Manrope', sans-serif;
    color: #172740;
    font-size: 17px;
    font-weight: 800;
    letter-spacing: -0.4px;
}

.panel-description {
    font-size: 12px;
    color: #8390A4;
    margin-top: 4px;
    margin-bottom: 18px;
    line-height: 1.6;
}

.section-heading {
    font-family: 'Manrope', sans-serif;
    font-size: 21px;
    font-weight: 800;
    letter-spacing: -0.6px;
    color: #182740;
    margin-top: 28px;
    margin-bottom: 5px;
}

.section-description {
    font-size: 13px;
    color: #7D8AA0;
    margin-bottom: 17px;
}

.cell-card {
    background: white;
    border: 1px solid #E2E9F3;
    border-radius: 10px;
    padding: 17px;
    min-height: 116px;
}

.cell-name {
    color: #243651;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 8px;
}

.cell-description {
    color: #8390A4;
    font-size: 11px;
    line-height: 1.6;
}

.info-strip {
    border-left: 3px solid #5277E6;
    background: #EDF3FC;
    padding: 14px 17px;
    border-radius: 0 7px 7px 0;
    color: #425673;
    font-size: 12px;
    line-height: 1.8;
    margin: 12px 0;
}

hr {
    border-color: #E4EAF3;
    margin: 25px 0;
}

.stButton > button {
    border-radius: 7px;
    font-weight: 600;
}

.stDownloadButton > button {
    border-radius: 7px;
}

div[data-testid="stPlotlyChart"] {
    border-radius: 8px;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# DEMONSTRATION DATA
# These values are synthetic, not biological findings.
# --------------------------------------------------

GENES = [
    "CALCRL", "RAMP1", "THBS1", "IL1B",
    "TNF", "VEGFA", "MRC1", "CD68"
]

CELL_TYPES = [
    "Macrophages",
    "Fibroblasts",
    "Endothelial cells",
    "Neutrophils"
]

CONDITIONS = ["Healing", "Non-healing"]

CELL_DESCRIPTIONS = {
    "Macrophages": "Immune regulation and tissue remodeling",
    "Fibroblasts": "Extracellular matrix and tissue repair",
    "Endothelial cells": "Vascular biology and angiogenesis",
    "Neutrophils": "Innate immunity and inflammation"
}


@st.cache_data
def make_demo_data():
    rng = np.random.default_rng(42)

    baseline = {
        "Macrophages": {
            "CALCRL": 4.1, "RAMP1": 4.3, "THBS1": 5.1,
            "IL1B": 7.0, "TNF": 5.9, "VEGFA": 4.4,
            "MRC1": 5.4, "CD68": 7.2
        },
        "Fibroblasts": {
            "CALCRL": 3.0, "RAMP1": 3.4, "THBS1": 6.0,
            "IL1B": 2.2, "TNF": 2.0, "VEGFA": 4.8,
            "MRC1": 1.5, "CD68": 1.2
        },
        "Endothelial cells": {
            "CALCRL": 3.6, "RAMP1": 3.2, "THBS1": 4.0,
            "IL1B": 2.5, "TNF": 2.2, "VEGFA": 7.0,
            "MRC1": 1.4, "CD68": 1.3
        },
        "Neutrophils": {
            "CALCRL": 2.8, "RAMP1": 2.5, "THBS1": 3.1,
            "IL1B": 7.4, "TNF": 5.6, "VEGFA": 3.1,
            "MRC1": 1.1, "CD68": 5.8
        }
    }

    records = []

    for condition in CONDITIONS:
        for cell in CELL_TYPES:
            for sample_num in range(1, 7):
                sample_id = f"{condition[:2].upper()}_{sample_num:02d}"

                for gene in GENES:
                    mean = baseline[cell][gene]

                    # Illustrative differences only; not real findings.
                    if condition == "Non-healing":
                        if gene in ["IL1B", "TNF"] and cell in [
                            "Macrophages", "Neutrophils"
                        ]:
                            mean += 1.0
                        elif gene == "VEGFA" and cell == "Endothelial cells":
                            mean -= 0.8
                        elif gene == "THBS1" and cell == "Fibroblasts":
                            mean += 0.5

                    value = max(0, rng.normal(mean, 0.65))

                    records.append({
                        "sample_id": sample_id,
                        "condition": condition,
                        "cell_type": cell,
                        "gene": gene,
                        "expression": round(value, 3)
                    })

    return pd.DataFrame(records)


def style_chart(fig, height=340):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="DM Sans, sans-serif",
            size=11,
            color="#61718A"
        ),
        margin=dict(l=10, r=15, t=15, b=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=10)
        ),
        xaxis=dict(
            showgrid=False,
            linecolor="#E5EAF2",
            zeroline=False
        ),
        yaxis=dict(
            gridcolor="#EDF1F7",
            zeroline=False,
            linecolor="rgba(0,0,0,0)"
        )
    )
    return fig


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown(
        '<div class="brand">WoundSignal</div>'
        '<div class="brand-sub">NEUROIMMUNE RESEARCH</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="sidebar-caption">WORKSPACE</div>',
                unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Expression Atlas",
            "Cell Populations",
            "Target Prioritization",
            "Data & Methods"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown('<div class="sidebar-caption">RESEARCH QUESTION</div>',
                unsafe_allow_html=True)

    st.markdown(
        "<div style='font-size:13px;line-height:1.8;color:#D5E0F1;'>"
        "How can human gene-expression data help identify cellular "
        "pathways relevant to CGRP-associated neuroimmune signaling "
        "and chronic wound repair?</div>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div style="border:1px solid #30415E;border-radius:8px;'
        'padding:13px;background:#172641;">'
        '<div style="font-size:10px;letter-spacing:1.5px;'
        'color:#90A7CB;font-weight:700;">PROJECT STATUS</div>'
        '<div style="font-size:13px;color:#FFFFFF;margin-top:9px;">'
        'Exploratory research platform</div>'
        '<div style="font-size:11px;color:#91A3BF;margin-top:5px;">'
        'Dataset verification required</div></div>',
        unsafe_allow_html=True
    )


# --------------------------------------------------
# DATA SOURCE
# --------------------------------------------------

st.markdown(
    '<div class="eyebrow">COMPUTATIONAL BIOLOGY / RESEARCH WORKSPACE</div>',
    unsafe_allow_html=True
)

with st.expander("DATA SOURCE AND ANALYSIS SETTINGS", expanded=False):
    source_mode = st.radio(
        "Select data source",
        [
            "Synthetic demonstration data",
            "Upload expression CSV"
        ],
        horizontal=True
    )

    uploaded_file = None
    if source_mode == "Upload expression CSV":
        uploaded_file = st.file_uploader(
            "Upload expression data",
            type=["csv"],
            help=(
                "Required columns: sample_id, condition, cell_type, "
                "gene, expression"
            )
        )

required_columns = {
    "sample_id", "condition", "cell_type", "gene", "expression"
}

if source_mode == "Synthetic demonstration data":
    df = make_demo_data()
    data_is_synthetic = True

elif uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        missing = required_columns - set(df.columns)

        if missing:
            st.error(
                "Missing required columns: " + ", ".join(sorted(missing))
            )
            st.stop()

        df = df[list(required_columns)].copy()
        df["expression"] = pd.to_numeric(
            df["expression"], errors="coerce"
        )
        df = df.dropna(subset=list(required_columns))

        if df.empty:
            st.error("No valid rows were found in this file.")
            st.stop()

        if (df["expression"] < 0).any():
            st.error("Expression values must be non-negative.")
            st.stop()

        if df["condition"].nunique() < 2:
            st.warning(
                "At least two conditions are needed for a comparison."
            )

        data_is_synthetic = False

    except Exception as exc:
        st.error(f"Could not read the CSV: {exc}")
        st.stop()

else:
    st.info("Upload a CSV above, or switch to synthetic demonstration data.")
    st.stop()


# --------------------------------------------------
# GLOBAL FILTERS
# --------------------------------------------------

all_conditions = sorted(df["condition"].astype(str).unique())
all_cells = sorted(df["cell_type"].astype(str).unique())
all_genes = sorted(df["gene"].astype(str).unique())

if len(all_conditions) < 2:
    st.error("The dataset must contain at least two conditions.")
    st.stop()

default_conditions = [
    c for c in ["Healing", "Non-healing"] if c in all_conditions
]

if len(default_conditions) != 2:
    default_conditions = all_conditions[:2]

with st.expander("FILTER DATA", expanded=False):
    selected_conditions = st.multiselect(
        "Conditions to compare",
        all_conditions,
        default=default_conditions
    )

    selected_cells = st.multiselect(
        "Cell populations",
        all_cells,
        default=all_cells
    )

    selected_genes = st.multiselect(
        "Genes",
        all_genes,
        default=all_genes
    )

if len(selected_conditions) < 2:
    st.warning("Select at least two conditions to compare.")
    st.stop()

if not selected_cells or not selected_genes:
    st.warning("Select at least one cell population and one gene.")
    st.stop()

filtered = df[
    df["condition"].isin(selected_conditions)
    & df["cell_type"].isin(selected_cells)
    & df["gene"].isin(selected_genes)
].copy()

if filtered.empty:
    st.warning("No observations match the selected filters.")
    st.stop()


# --------------------------------------------------
# PAGE: OVERVIEW
# --------------------------------------------------

if page == "Overview":

    left, right = st.columns([4, 1.3], vertical_alignment="center")

    with left:
        st.markdown(
            '<div class="main-title">Neuroimmune Wound Atlas</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="subtitle">Explore cellular signals, gene '
            'expression patterns, and candidate pathways in chronic '
            'wound repair.</div>',
            unsafe_allow_html=True
        )

    with right:
        st.markdown(
            '<div style="text-align:right;">'
            '<span class="status-pill">RESEARCH PREVIEW</span></div>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    metric_cols = st.columns(4)

    metrics = [
        ("DATASET ROWS", f"{len(filtered):,}", "Filtered observations"),
        ("GENES", str(filtered["gene"].nunique()), "Selected gene panel"),
        ("CELL POPULATIONS", str(filtered["cell_type"].nunique()),
         "Selected cell types"),
        ("CONDITIONS", str(filtered["condition"].nunique()),
         "Groups available for comparison")
    ]

    for col, (label, value, note) in zip(metric_cols, metrics):
        with col:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-label">{label}</div>'
                f'<div class="metric-value">{value}</div>'
                f'<div class="metric-note">{note}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    if data_is_synthetic:
        st.markdown(
            '<div class="info-strip"><strong>Demonstration mode.</strong> '
            'The current values are synthetic and were generated for '
            'interface testing. They are not patient measurements, '
            'experimental results, or evidence of biological effects. '
            'No scientific conclusion should be drawn from these charts.'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="section-heading">Expression landscape</div>'
        '<div class="section-description">Explore average expression '
        'across selected genes and cell populations.</div>',
        unsafe_allow_html=True
    )

    chart_col, focus_col = st.columns([2.2, 1], gap="large")

    with chart_col:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(
            '<div class="panel-title">Gene expression profile</div>'
            '<div class="panel-description">Mean expression by gene '
            'and condition, across the selected populations.</div>',
            unsafe_allow_html=True
        )

        overview_gene = st.selectbox(
            "Gene displayed",
            selected_genes,
            key="overview_gene"
        )

        gene_df = filtered[filtered["gene"] == overview_gene]

        summary = (
            gene_df.groupby(["condition", "cell_type"], as_index=False)
            ["expression"].mean()
        )

        fig = px.bar(
            summary,
            x="cell_type",
            y="expression",
            color="condition",
            barmode="group",
            color_discrete_sequence=["#4269E1", "#70C6E5"],
            labels={
                "cell_type": "Cell population",
                "expression": "Mean expression",
                "condition": "Condition"
            }
        )

        fig = style_chart(fig, 350)
        fig.update_layout(xaxis_tickangle=-15)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with focus_col:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(
            '<div class="panel-title">Research focus</div>'
            '<div class="panel-description">The biological framework '
            'guiding this project.</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div style="font-size:11px;color:#5475D6;font-weight:700;'
            'letter-spacing:1px;margin-top:8px;">01 / NEURAL SIGNALING</div>'
            '<div style="font-family:Manrope;font-size:17px;'
            'font-weight:800;margin:7px 0;color:#1A2B46;">'
            'CGRP signaling</div>'
            '<div style="font-size:12px;line-height:1.8;color:#77859A;">'
            'CALCRL and RAMP1 encode components of the canonical '
            'CGRP receptor complex.</div>'
            '<hr>'
            '<div style="font-size:11px;color:#5475D6;font-weight:700;'
            'letter-spacing:1px;">02 / TISSUE REPAIR</div>'
            '<div style="font-family:Manrope;font-size:17px;'
            'font-weight:800;margin:7px 0;color:#1A2B46;">'
            'Wound microenvironment</div>'
            '<div style="font-size:12px;line-height:1.8;color:#77859A;">'
            'Immune cells, fibroblasts, and endothelial cells contribute '
            'to different aspects of wound biology.</div>'
            '<hr>'
            '<div style="font-size:11px;color:#5475D6;font-weight:700;'
            'letter-spacing:1px;">03 / EVIDENCE</div>'
            '<div style="font-size:12px;line-height:1.8;color:#77859A;">'
            'Expression patterns generate hypotheses. They do not '
            'establish receptor activation, causality, or treatment '
            'effectiveness.</div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">Cellular context</div>'
        '<div class="section-description">Four populations included in '
        'the initial exploratory gene panel.</div>',
        unsafe_allow_html=True
    )

    cell_cols = st.columns(4)

    for col, cell in zip(cell_cols, CELL_TYPES):
        with col:
            st.markdown(
                f'<div class="cell-card">'
                f'<div style="height:3px;width:30px;background:#5276E2;'
                f'border-radius:3px;margin-bottom:15px;"></div>'
                f'<div class="cell-name">{cell}</div>'
                f'<div class="cell-description">'
                f'{CELL_DESCRIPTIONS[cell]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown(
        '<div class="section-heading">Analysis workflow</div>',
        unsafe_allow_html=True
    )

    workflow_cols = st.columns(3)

    workflow = [
        ("01", "Data validation",
         "Confirm dataset provenance, sample metadata, and data quality."),
        ("02", "Expression analysis",
         "Compare expression patterns while respecting biological replicates."),
        ("03", "Independent validation",
         "Test whether patterns persist in a separate, appropriate dataset.")
    ]

    for col, (num, title, description) in zip(workflow_cols, workflow):
        with col:
            st.markdown(
                f'<div class="panel">'
                f'<div style="font-size:11px;font-weight:700;'
                f'color:#5578DF;letter-spacing:1px;">STAGE {num}</div>'
                f'<div class="panel-title" style="margin-top:12px;">'
                f'{title}</div>'
                f'<div class="cell-description" '
                f'style="margin-top:10px;">{description}</div>'
                f'</div>',
                unsafe_allow_html=True
            )


# --------------------------------------------------
# PAGE: EXPRESSION ATLAS
# --------------------------------------------------

elif page == "Expression Atlas":

    st.markdown(
        '<div class="main-title">Expression Atlas</div>'
        '<div class="subtitle">Inspect gene-level expression patterns '
        'and compare groups within the selected dataset.</div>',
        unsafe_allow_html=True
    )

    gene = st.selectbox("Select gene", selected_genes, key="atlas_gene")

    gene_data = filtered[filtered["gene"] == gene]

    summary = (
        gene_data.groupby(["condition", "cell_type"], as_index=False)
        ["expression"].agg(["mean", "std", "count"])
        .reset_index()
    )

    summary["std"] = summary["std"].fillna(0)

    fig = px.bar(
        summary,
        x="cell_type",
        y="mean",
        color="condition",
        barmode="group",
        error_y="std",
        color_discrete_sequence=["#4269E1", "#70C6E5"],
        labels={
            "cell_type": "Cell population",
            "mean": "Mean expression",
            "condition": "Condition"
        }
    )

    fig = style_chart(fig, 440)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Summary table")
    st.dataframe(summary, use_container_width=True, hide_index=True)

    st.download_button(
        "Download expression summary",
        summary.to_csv(index=False).encode("utf-8"),
        file_name=f"{gene}_expression_summary.csv",
        mime="text/csv"
    )

    st.caption(
        "Error bars show standard deviation across rows in the selected "
        "data. They are not confidence intervals. The meaning of a row "
        "depends on the uploaded dataset's structure."
    )


# --------------------------------------------------
# PAGE: CELL POPULATIONS
# --------------------------------------------------

elif page == "Cell Populations":

    st.markdown(
        '<div class="main-title">Cell Populations</div>'
        '<div class="subtitle">Compare gene expression across cellular '
        'contexts in the selected data.</div>',
        unsafe_allow_html=True
    )

    cell = st.selectbox("Cell population", selected_cells)

    cell_df = filtered[filtered["cell_type"] == cell]

    cell_summary = (
        cell_df.groupby(["gene", "condition"], as_index=False)
        ["expression"].mean()
    )

    fig = px.bar(
        cell_summary,
        x="gene",
        y="expression",
        color="condition",
        barmode="group",
        color_discrete_sequence=["#4269E1", "#70C6E5"],
        labels={
            "gene": "Gene",
            "expression": "Mean expression",
            "condition": "Condition"
        }
    )

    fig = style_chart(fig, 430)
    fig.update_layout(xaxis_tickangle=-25)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Population summary")

    pivot = cell_summary.pivot(
        index="gene", columns="condition", values="expression"
    ).reset_index()

    st.dataframe(pivot, use_container_width=True, hide_index=True)

    st.download_button(
        "Download population summary",
        pivot.to_csv(index=False).encode("utf-8"),
        file_name="cell_population_summary.csv",
        mime="text/csv"
    )


# --------------------------------------------------
# PAGE: TARGET PRIORITIZATION
# --------------------------------------------------

elif page == "Target Prioritization":

    st.markdown(
        '<div class="main-title">Target Prioritization</div>'
        '<div class="subtitle">Generate an exploratory ranking of '
        'expression differences. This is not a validated therapeutic '
        'target ranking.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="info-strip">Ranking is based only on absolute '
        'differences in group mean expression. It does not account for '
        'statistical significance, confounding, biological replication, '
        'causality, druggability, or external evidence. Treat it as a '
        'descriptive screening aid.</div>',
        unsafe_allow_html=True
    )

    rank_cell = st.selectbox(
        "Cell population",
        selected_cells,
        key="rank_cell"
    )

    rank_df = filtered[filtered["cell_type"] == rank_cell]

    means = (
        rank_df.groupby(["gene", "condition"])["expression"]
        .mean().unstack()
    )

    if all(c in means.columns for c in selected_conditions):
        a, b = selected_conditions[0], selected_conditions[1]

        ranking = means[[a, b]].dropna().copy()
        ranking["Mean difference"] = ranking[b] - ranking[a]
        ranking["Absolute difference"] = ranking["Mean difference"].abs()

        ranking = ranking.sort_values(
            "Absolute difference", ascending=False
        ).reset_index()

        ranking.insert(0, "Exploratory rank", range(1, len(ranking) + 1))

        fig = px.bar(
            ranking.sort_values("Mean difference"),
            x="Mean difference",
            y="gene",
            orientation="h",
            color="Mean difference",
            color_continuous_scale=["#75CBE5", "#EAF0FA", "#4269E1"],
            labels={
                "Mean difference": f"Mean difference ({b} − {a})",
                "gene": "Gene"
            }
        )

        fig = style_chart(fig, 380)
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Descriptive ranking")
        st.dataframe(ranking, use_container_width=True, hide_index=True)

        st.download_button(
            "Download ranking",
            ranking.to_csv(index=False).encode("utf-8"),
            file_name="exploratory_gene_ranking.csv",
            mime="text/csv"
        )

    else:
        st.warning("Could not calculate a comparison for these conditions.")


# --------------------------------------------------
# PAGE: DATA & METHODS
# --------------------------------------------------

elif page == "Data & Methods":

    st.markdown(
        '<div class="main-title">Data & Methods</div>'
        '<div class="subtitle">Document data provenance, analytical '
        'assumptions, and the limitations of the current platform.</div>',
        unsafe_allow_html=True
    )

    st.markdown("### Current data source")

    if data_is_synthetic:
        st.error(
            "Synthetic demonstration data are active. These values are "
            "invented for interface testing and must not be presented "
            "as experimental or clinical results."
        )
    else:
        st.success(
            "A user-uploaded CSV is active. Its scientific validity "
            "has not been independently verified by this application."
        )

    st.markdown("### Dataset overview")

    overview = pd.DataFrame({
        "Property": [
            "Rows in current filtered data",
            "Unique sample identifiers",
            "Conditions",
            "Cell populations",
            "Genes",
            "Missing values in displayed data"
        ],
        "Value": [
            len(filtered),
            filtered["sample_id"].nunique(),
            filtered["condition"].nunique(),
            filtered["cell_type"].nunique(),
            filtered["gene"].nunique(),
            int(filtered.isna().sum().sum())
        ]
    })

    st.dataframe(overview, use_container_width=True, hide_index=True)

    st.markdown("### Required analytical safeguards")

    safeguards = [
        (
            "Sample-level replication",
            "Cells from the same patient are not independent biological "
            "replicates. Single-cell analyses generally need appropriate "
            "sample-level aggregation or statistical models."
        ),
        (
            "Clinical metadata",
            "A dataset containing diabetic and non-diabetic wounds does "
            "not automatically contain healing outcomes. Group labels "
            "must reflect the actual metadata."
        ),
        (
            "Normalization",
            "Expression values from different technologies or processing "
            "pipelines may not be directly comparable. Verify units, "
            "normalization, and gene identifiers."
        ),
        (
            "CGRP interpretation",
            "CALCRL and RAMP1 are associated with the canonical CGRP "
            "receptor. Their expression alone does not prove that CGRP "
            "signaling is active or that it causes a wound outcome."
        ),
        (
            "Independent validation",
            "A separate dataset should be assessed for compatible tissue, "
            "cell annotations, clinical definitions, and measurement "
            "methods before testing replication."
        ),
        (
            "Statistical inference",
            "Differences in group means are descriptive. A robust study "
            "should address uncertainty, multiple testing, confounders, "
            "and appropriate statistical models."
        )
    ]

    for title, description in safeguards:
        with st.expander(title):
            st.write(description)

    st.markdown("### Data preview")
    st.dataframe(filtered.head(100), use_container_width=True)

    st.download_button(
        "Download filtered data",
        filtered.to_csv(index=False).encode("utf-8"),
        file_name="woundsignal_filtered_data.csv",
        mime="text/csv"
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")
st.markdown(
    '<div style="display:flex;justify-content:space-between;'
    'gap:20px;flex-wrap:wrap;color:#8995A8;font-size:11px;">'
    '<span>WoundSignal · Computational neuroimmune research</span>'
    '<span>Exploratory analysis · Interpret results with caution</span>'
    '</div>',
    unsafe_allow_html=True
)

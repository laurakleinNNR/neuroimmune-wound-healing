import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="WoundSignal",
    page_icon="🧬",
    layout="wide"
)

# ---------- Demo data: explicitly synthetic ----------
def make_demo_data():
    rng = np.random.default_rng(42)

    genes = [
        "CALCRL", "RAMP1", "THBS1", "IL1B",
        "TNF", "VEGFA", "MRC1", "CD68"
    ]

    cell_types = [
        "Macrophages",
        "Fibroblasts",
        "Endothelial cells",
        "Neutrophils"
    ]

    # Synthetic values are for testing the app only.
    # They are NOT measurements from patients or published data.
    base = {
        "CALCRL": 2.0,
        "RAMP1": 1.8,
        "THBS1": 2.5,
        "IL1B": 3.0,
        "TNF": 2.4,
        "VEGFA": 2.2,
        "MRC1": 2.8,
        "CD68": 3.2
    }

    rows = []

    for condition in ["Healing", "Non-healing"]:
        for patient_num in range(1, 7):
            sample_id = f"{condition[:1]}{patient_num:02d}"

            for cell_type in cell_types:
                for gene in genes:
                    value = base[gene] + rng.normal(0, 0.35)

                    # Illustrative differences only.
                    if condition == "Non-healing":
                        if gene in ["IL1B", "TNF"]:
                            value += 0.7
                        if gene in ["VEGFA", "MRC1"]:
                            value -= 0.5

                    if cell_type == "Macrophages" and gene in [
                        "IL1B", "TNF", "MRC1", "CD68"
                    ]:
                        value += 0.5

                    rows.append({
                        "sample_id": sample_id,
                        "condition": condition,
                        "cell_type": cell_type,
                        "gene": gene,
                        "expression": max(0, value)
                    })

    return pd.DataFrame(rows)


# ---------- Header ----------
st.title("🧬 WoundSignal")
st.subheader(
    "Exploring neuroimmune signaling in chronic wound repair"
)

st.write(
    "A computational research platform for investigating "
    "gene-expression patterns associated with tissue repair."
)

st.warning(
    "DEMO MODE: The built-in data are synthetic and invented "
    "to test this website. They are not patient data, "
    "published results, or evidence for a treatment."
)

# ---------- Sidebar ----------
st.sidebar.title("Research workspace")

data_source = st.sidebar.radio(
    "Choose data source",
    ["Synthetic demo", "Upload expression CSV"]
)

# ---------- Load data ----------
if data_source == "Synthetic demo":
    df = make_demo_data()
    st.info("Using synthetic demonstration data.")

else:
    uploaded_file = st.sidebar.file_uploader(
        "Upload a CSV file",
        type=["csv"]
    )

    if uploaded_file is None:
        st.info(
            "Upload a CSV with columns: sample_id, condition, "
            "cell_type, gene, expression."
        )
        st.stop()

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as exc:
        st.error(f"Could not read the CSV: {exc}")
        st.stop()

required_columns = {
    "sample_id", "condition", "cell_type", "gene", "expression"
}

missing_columns = required_columns - set(df.columns)

if missing_columns:
    st.error(
        "Missing required columns: "
        + ", ".join(sorted(missing_columns))
    )
    st.stop()

df = df[list(required_columns)].copy()

df["expression"] = pd.to_numeric(
    df["expression"], errors="coerce"
)

df = df.dropna(
    subset=[
        "sample_id", "condition", "cell_type",
        "gene", "expression"
    ]
)

if df.empty:
    st.error("No valid data rows were found.")
    st.stop()

if (df["expression"] < 0).any():
    st.error(
        "Negative expression values were found. "
        "Check the data format before continuing."
    )
    st.stop()

if df["condition"].nunique() < 2:
    st.error(
        "At least two condition groups are required "
        "for a comparison."
    )
    st.stop()

# ---------- Dataset overview ----------
st.header("1. Dataset overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Rows", f"{len(df):,}")
col2.metric("Samples", df["sample_id"].nunique())
col3.metric("Cell types", df["cell_type"].nunique())
col4.metric("Genes", df["gene"].nunique())

with st.expander("Inspect the data"):
    st.dataframe(df.head(30), use_container_width=True)

    st.write("Available conditions:")
    st.write(sorted(df["condition"].astype(str).unique()))

    st.write("Available cell types:")
    st.write(sorted(df["cell_type"].astype(str).unique()))

# ---------- Comparison controls ----------
st.header("2. Compare gene expression")

conditions = sorted(df["condition"].astype(str).unique())
cell_types = sorted(df["cell_type"].astype(str).unique())
genes = sorted(df["gene"].astype(str).unique())

left, right = st.columns(2)

with left:
    condition_a = st.selectbox(
        "Reference group",
        conditions,
        index=0
    )

with right:
    condition_b = st.selectbox(
        "Comparison group",
        conditions,
        index=1
    )

selected_cell = st.selectbox(
    "Cell population",
    cell_types
)

selected_genes = st.multiselect(
    "Genes to investigate",
    genes,
    default=[
        gene for gene in ["CALCRL", "RAMP1", "THBS1"]
        if gene in genes
    ]
)

if condition_a == condition_b:
    st.warning("Choose two different conditions.")
    st.stop()

if not selected_genes:
    st.info("Select at least one gene.")
    st.stop()

# Average expression within each biological sample first.
# This avoids treating every cell as an independent patient.
subset = df[
    (df["cell_type"].astype(str) == selected_cell)
    & (df["gene"].astype(str).isin(selected_genes))
    & (df["condition"].astype(str).isin(
        [condition_a, condition_b]
    ))
].copy()

sample_means = (
    subset.groupby(
        ["sample_id", "condition", "gene"],
        as_index=False
    )["expression"]
    .mean()
)

group_means = (
    sample_means.groupby(
        ["condition", "gene"],
        as_index=False
    )["expression"]
    .mean()
)

wide = group_means.pivot(
    index="gene",
    columns="condition",
    values="expression"
)

for condition in [condition_a, condition_b]:
    if condition not in wide.columns:
        wide[condition] = np.nan

results = wide.reset_index()
results["mean_difference"] = (
    results[condition_b] - results[condition_a]
)
results["absolute_difference"] = (
    results["mean_difference"].abs()
)

results = results.sort_values(
    "absolute_difference",
    ascending=False
)

# ---------- Results ----------
st.header("3. Exploratory results")

st.caption(
    f"Cell population: {selected_cell}. "
    f"Difference = mean({condition_b}) − mean({condition_a})."
)

fig = px.bar(
    group_means,
    x="gene",
    y="expression",
    color="condition",
    barmode="group",
    title="Mean expression by gene and condition",
    labels={
        "gene": "Gene",
        "expression": "Mean expression",
        "condition": "Condition"
    }
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Exploratory candidate ranking")

st.write(
    "Genes are ordered by the absolute difference in mean "
    "expression between the selected groups. This is a "
    "screening metric, not a measure of therapeutic benefit."
)

st.dataframe(
    results[
        [
            "gene", condition_a,
            condition_b, "mean_difference"
        ]
    ].round(4),
    use_container_width=True,
    hide_index=True
)

csv = results.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download comparison table",
    data=csv,
    file_name="woundsignal_comparison.csv",
    mime="text/csv"
)

# ---------- Scientific limitations ----------
st.header("4. Interpretation and limitations")

st.markdown("""
- Expression differences do not prove that a gene causes healing.
- Receptor-gene expression alone does not establish a functional
  response to CGRP.
- Uploaded data must have appropriate, documented expression
  values and meaningful sample labels.
- The comparison above does not calculate statistical
  significance or adjust for confounding variables.
- Independent validation and biological literature review
  are required before prioritizing research targets.
""")

st.success(
    "Initial interface loaded. The next research stage is to "
    "connect verified public biological data and implement "
    "statistical analysis and independent validation."
)

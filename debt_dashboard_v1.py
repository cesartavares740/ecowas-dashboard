import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="ECOWAS Debt Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("ECOWAS Debt Dashboard")

st.subheader(
    "Debt, Growth and Macroeconomic Vulnerability in Selected ECOWAS Economies (2015–2024)"
)

st.markdown("""
This dashboard compares external debt, GDP growth and inflation trends
across selected ECOWAS economies using World Bank Open Data.
""")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

debt = pd.read_csv("external_debt.csv")
gdp = pd.read_csv("gdp_growth.csv")
inflation = pd.read_csv("inflation.csv")

# ---------------------------------------------------
# CLEAN DATA
# ---------------------------------------------------

for df in [debt, gdp, inflation]:

    df.dropna(subset=["Country Name"], inplace=True)

    df.drop(
        df[df["Country Name"].str.contains(
            "Data from database",
            na=False
        )].index,
        inplace=True
    )

    df.drop(
        df[df["Country Name"].str.contains(
            "Last Updated",
            na=False
        )].index,
        inplace=True
    )

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("Dashboard Filters")

countries = sorted(debt["Country Name"].unique())

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    countries,
    default=countries
)

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------

debt = debt[debt["Country Name"].isin(selected_countries)]
gdp = gdp[gdp["Country Name"].isin(selected_countries)]
inflation = inflation[inflation["Country Name"].isin(selected_countries)]

# ---------------------------------------------------
# SUMMARY METRICS
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Countries Selected",
        len(selected_countries)
    )

with col2:
    st.metric(
        "Period Covered",
        "2015-2024"
    )

with col3:
    st.metric(
        "Indicators",
        3
    )

with col4:
    debt["2024 [YR2024]"] = pd.to_numeric(
        debt["2024 [YR2024]"],
        errors="coerce"
    )

    highest_country = debt.loc[
        debt["2024 [YR2024]"].idxmax(),
        "Country Name"
    ]

    st.metric(
        "Highest Debt (2024)",
        highest_country
    )

# ---------------------------------------------------
# RESHAPE FUNCTION
# ---------------------------------------------------

def reshape_data(df):

    years = [
        f"{year} [YR{year}]"
        for year in range(2015, 2025)
    ]

    long_df = df.melt(
        id_vars=["Country Name"],
        value_vars=years,
        var_name="Year",
        value_name="Value"
    )

    long_df["Year"] = long_df["Year"].str.extract(r'(\d{4})')

    long_df["Value"] = pd.to_numeric(
        long_df["Value"],
        errors="coerce"
    )

    return long_df


debt_long = reshape_data(debt)
gdp_long = reshape_data(gdp)
inflation_long = reshape_data(inflation)

# ---------------------------------------------------
# DEBT CHART
# ---------------------------------------------------

st.header("External Debt Stocks (% of GNI)")

st.markdown(
    "Comparison of external debt trends across selected countries."
)

fig_debt = px.line(
    debt_long,
    x="Year",
    y="Value",
    color="Country Name",
    markers=True
)

fig_debt.update_layout(
    height=600
)

st.plotly_chart(
    fig_debt,
    width="stretch"
)

# ---------------------------------------------------
# GDP CHART
# ---------------------------------------------------

st.header("GDP Growth (Annual %)")

st.markdown(
    "Comparison of economic growth performance."
)

fig_gdp = px.line(
    gdp_long,
    x="Year",
    y="Value",
    color="Country Name",
    markers=True
)

fig_gdp.update_layout(
    height=600
)

st.plotly_chart(
    fig_gdp,
    width="stretch"
)

# ---------------------------------------------------
# INFLATION CHART
# ---------------------------------------------------

st.header("Inflation (Annual %)")

st.markdown(
    "Comparison of inflation dynamics."
)

fig_inflation = px.line(
    inflation_long,
    x="Year",
    y="Value",
    color="Country Name",
    markers=True
)

fig_inflation.update_layout(
    height=600
)

st.plotly_chart(
    fig_inflation,
    width="stretch"
)

# ==========================
# COUNTRY RANKING TABLE
# ==========================

st.header("2024 Country Ranking")

ranking = pd.DataFrame({
    "Country": debt["Country Name"],
    "External Debt (% of GNI)": debt["2024 [YR2024]"],
    "GDP Growth (%)": gdp["2024 [YR2024]"],
    "Inflation (%)": inflation["2024 [YR2024]"]
})

ranking["External Debt (% of GNI)"] = pd.to_numeric(
    ranking["External Debt (% of GNI)"],
    errors="coerce"
)

ranking["GDP Growth (%)"] = pd.to_numeric(
    ranking["GDP Growth (%)"],
    errors="coerce"
)

ranking["Inflation (%)"] = pd.to_numeric(
    ranking["Inflation (%)"],
    errors="coerce"
)

ranking = ranking.sort_values(
    by="External Debt (% of GNI)",
    ascending=False
)
ranking = ranking.reset_index(drop=True)
ranking.insert(
    0,
    "Rank",
    range(1, len(ranking) + 1)
)
ranking["External Debt (% of GNI)"] = ranking["External Debt (% of GNI)"].round(1)
ranking["GDP Growth (%)"] = ranking["GDP Growth (%)"].round(1)
ranking["Inflation (%)"] = ranking["Inflation (%)"].round(1)

st.dataframe(
    ranking,
    hide_index=True,
    width="stretch"
)


# INSIGHTS
st.header("Key Economic Insights")
# ---------------------------------------------------
# INSIGHTS
# ---------------------------------------------------


st.markdown("""
- Senegal experienced the largest increase in external debt over the period.
- Nigeria's debt burden increased significantly after 2020.
- Ghana recorded persistently high inflation compared with WAEMU economies.
- Côte d'Ivoire maintained strong GDP growth while keeping inflation relatively moderate.
- Macroeconomic outcomes diverged considerably across ECOWAS economies.
""")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "Source: World Bank Open Data | Author: Cesar Tavares"
)
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="ECOWAS Exchange Rate Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

inflation_data = pd.read_csv(
    "worldbank_data.csv",
    skiprows=4
)

exchange_data = pd.read_csv(
    "exchange_rate_data.csv",
    skiprows=4
)

# ---------------------------------------------------
# SELECT COUNTRIES
# ---------------------------------------------------

selected_countries = [
    "Ghana",
    "Nigeria",
    "Senegal",
    "Cote d'Ivoire"
]

# ---------------------------------------------------
# SELECT YEARS
# ---------------------------------------------------

years = [str(year) for year in range(2015, 2025)]

# ---------------------------------------------------
# FILTER INFLATION DATA
# ---------------------------------------------------

inflation_filtered = inflation_data[
    inflation_data["Country Name"].isin(selected_countries)
]

inflation_long = inflation_filtered.melt(
    id_vars=["Country Name"],
    value_vars=years,
    var_name="Year",
    value_name="Inflation"
)

inflation_long["Inflation"] = pd.to_numeric(
    inflation_long["Inflation"],
    errors="coerce"
)

# ---------------------------------------------------
# FILTER EXCHANGE RATE DATA
# ---------------------------------------------------

exchange_filtered = exchange_data[
    exchange_data["Country Name"].isin(selected_countries)
]

exchange_long = exchange_filtered.melt(
    id_vars=["Country Name"],
    value_vars=years,
    var_name="Year",
    value_name="Exchange Rate"
)

exchange_long["Exchange Rate"] = pd.to_numeric(
    exchange_long["Exchange Rate"],
    errors="coerce"
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("Dashboard Filters")

st.sidebar.markdown("""
### Dashboard Overview

This dashboard compares exchange rate stability and inflation divergence across selected ECOWAS economies using official macroeconomic indicators.

### Data Sources
- World Bank Open Data
- BCEAO Statistical Publications

### Author
Cesar Tavares
""")
st.markdown("""
<style>

[data-baseweb="tag"] {
    background-color: #1f2937 !important;
    color: white !important;
    border-radius: 8px !important;
    border: 1px solid #374151 !important;
}

[data-baseweb="select"] {
    background-color: #111827 !important;
}

</style>
""", unsafe_allow_html=True)
selected_countries_sidebar = st.sidebar.multiselect(
    "Select Countries",
    selected_countries,
    default=selected_countries
)

# ---------------------------------------------------
# FILTER BASED ON SIDEBAR
# ---------------------------------------------------

inflation_long = inflation_long[
    inflation_long["Country Name"].isin(selected_countries_sidebar)
]

exchange_long = exchange_long[
    exchange_long["Country Name"].isin(selected_countries_sidebar)
]

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title(
    "ECOWAS Exchange Rate and Inflation Dashboard (2015–2024)"
)

st.markdown("""
Interactive macroeconomic dashboard using World Bank Open Data and BCEAO statistical sources 
to compare exchange rate stability and inflation dynamics across selected ECOWAS economies.
""")

# ---------------------------------------------------
# METRIC CARDS
# ---------------------------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Countries Selected",
    len(selected_countries_sidebar)
)

col2.metric(
    "Period Covered",
    "2015–2024"
)

col3.metric(
    "Data Sources",
    "World Bank + BCEAO"
)

# ---------------------------------------------------
# EXCHANGE RATE CHART
# ---------------------------------------------------

st.markdown("---")

st.header("Exchange Rate Trends (2015–2024)")

fig_exchange = px.line(
    exchange_long,
    x="Year",
    y="Exchange Rate",
    color="Country Name",
    markers=True,
    template="plotly_dark"
)

fig_exchange.update_layout(
    height=600,
    xaxis_title="Year",
    yaxis_title="Exchange Rate",
    legend_title="Country"
)

st.plotly_chart(fig_exchange, use_container_width=True)

st.caption(
    "Source: World Bank Open Data (Indicator: PA.NUS.FCRF). "
    "Author calculations and visualisations based on annual exchange rate data (2015–2024)."
)

# ---------------------------------------------------
# INFLATION CHART
# ---------------------------------------------------

st.markdown("---")

st.header("Inflation Trends (2015–2024)")

fig_inflation = px.line(
    inflation_long,
    x="Year",
    y="Inflation",
    color="Country Name",
    markers=True,
    template="plotly_dark"
)

fig_inflation.update_layout(
    height=600,
    xaxis_title="Year",
    yaxis_title="Inflation (%)",
    legend_title="Country"
)

st.plotly_chart(fig_inflation, use_container_width=True)

st.caption(
    "Source: World Bank Open Data (Indicator: FP.CPI.TOTL.ZG). "
    "Author calculations and visualisations based on annual inflation data (2015–2024)."
)

# ---------------------------------------------------
# KEY INSIGHTS
# ---------------------------------------------------

st.markdown("---")

st.header("Key Economic Insights")

st.markdown("""

- Nigeria experienced the sharpest currency depreciation after the 2022 exchange rate liberalisation period.

- Ghana faced elevated inflationary pressures linked to currency instability and external financing challenges.

- WAEMU economies such as Senegal and Côte d’Ivoire maintained relatively greater exchange rate stability due to the CFA franc monetary framework.

- Inflation divergence across ECOWAS widened significantly after the COVID-19 pandemic and global commodity price shocks.

- Exchange rate stability appears closely associated with inflation containment across the region.

""")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.markdown("""
<div style='text-align: center; color: gray; font-size: 14px;'>

Created by <b>Cesar Tavares</b><br>
ECOWAS Economic Insights | Data Analysis & Regional Macroeconomic Research<br><br>

Sources: World Bank Open Data, BCEAO Statistical Bulletins

</div>
""", unsafe_allow_html=True)

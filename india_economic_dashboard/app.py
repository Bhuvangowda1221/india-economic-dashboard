# ============================================================
# app.py
# India Economic Dashboard — Interactive Web Application
# Run with: streamlit run app.py
# ============================================================

# ── Import Libraries ─────────────────────────────────────────
import streamlit as st      # Creates the web dashboard
import pandas as pd         # Handles data
import plotly.express as px # Creates interactive charts
import plotly.graph_objects as go  # For advanced chart customization
from PIL import Image       # Opens saved PNG images
import os                   # Checks if files exist
import warnings

warnings.filterwarnings("ignore")

# ── PAGE CONFIGURATION ────────────────────────────────────────
# This MUST be the very first Streamlit command
# Sets the browser tab title, icon, and layout

st.set_page_config(
    page_title="India Economic Dashboard",  # Browser tab title                       
    layout="wide",                          # Use full width of screen
    initial_sidebar_state="expanded"        # Sidebar open by default
)

# ── CUSTOM CSS STYLING ────────────────────────────────────────
# This adds custom colors and styles to make dashboard look professional
# You don't need to understand CSS — just paste it as is

st.markdown("""
    <style>
    /* Main background color */
    .main {
        background-color: #0f1117;
    }

    /* KPI Card Style */
    .kpi-card {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin: 8px 0;
    }

    .kpi-title {
        color: #90CAF9;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    .kpi-value {
        color: #FFFFFF;
        font-size: 32px;
        font-weight: 800;
    }

    .kpi-subtitle {
        color: #B0BEC5;
        font-size: 12px;
        margin-top: 4px;
    }

    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #1565C0, #0D47A1);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        font-size: 18px;
        font-weight: bold;
        margin: 20px 0 15px 0;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #78909C;
        font-size: 13px;
        border-top: 1px solid #263238;
        margin-top: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────
# @st.cache_data tells Streamlit to save the data in memory
# So it doesn't reload the file every time you interact with dashboard

@st.cache_data
def load_data():
    try:
      df = pd.read_csv("india_economic_dashboard/india_economic_data.csv")
        # ✅ Clean column names (important)
        df.columns = df.columns.str.strip()

        # ✅ Convert all columns to numeric
        for col in df.columns:
            if col != "Year":
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # ✅ Fill missing values
        df = df.fillna(0)

        return df
    except FileNotFoundError:
        st.error("❌ ERROR: 'india_economic_data.csv' not found!")
        st.info("📁 Please make sure the CSV file is in the same folder as app.py")
        st.stop()  # Stop the app here

# Load the data
df = load_data()

# ── DASHBOARD HEADER ──────────────────────────────────────────
# st.markdown lets us write HTML inside Streamlit
# unsafe_allow_html=True allows HTML tags

st.markdown("""
    <div style="text-align:center; padding: 30px 0 10px 0;">
        <h1 style="color:#42A5F5; font-size:42px; font-weight:900; margin:0;">
            India Economic Dashboard
        </h1>
        <p style="color:#90CAF9; font-size:18px; margin-top:8px;">
            Comprehensive Analysis of India's Economic Indicators
        </p>
        <p style="color:#546E7A; font-size:13px;">
            Data Source: india_economic_data.csv
        </p>
    </div>
    <hr style="border:1px solid #1E3A5F; margin-bottom:20px;">
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────
# Sidebar appears on the LEFT side of the dashboard
# It contains filters that control what data is shown

with st.sidebar:
    # Sidebar header with flag
    st.markdown("""
        <div style="text-align:center; padding:15px 0;">
            <h2 style="color:#42A5F5;"> Dashboard Controls</h2>
            <p style="color:#78909C; font-size:13px;">Use filters to explore data</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")  # Horizontal divider line

    # ── YEAR RANGE SLIDER ──
    # st.slider creates a draggable slider
    # min_value = first year in dataset
    # max_value = last year in dataset

    st.markdown("### 📅 Select Year Range")

    min_year = 2015  # Get earliest year from data
    max_year = 2025  # Get latest year from data

    # Slider returns a tuple: (start_year, end_year)
    year_range = st.slider(
        label="Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),  # Default: show all years
        step=1
    )

    st.markdown("---")

    # ── INDICATOR SELECTOR ──
    # Multiselect lets user choose which indicators to compare

    st.markdown("### 📊 Select Indicators to Compare")

    # List of columns user can choose from
    all_indicators = [
        "GDP_Growth_Rate",
        "Inflation_Rate",
        "Unemployment_Rate",
        "Exports_Billion_USD",
        "Imports_Billion_USD",
        "Agriculture_Contribution",
        "Industry_Contribution",
        "Population_Millions"
    ]

    selected_indicators = st.multiselect(
        label="Choose indicators:",
        options=all_indicators,
        default=["GDP_Growth_Rate", "Inflation_Rate"]  # Selected by default
    )

    st.markdown("---")

    # ── CHART TYPE SELECTOR ──
    st.markdown("### 📈 Chart Style")
    chart_type = st.radio(
        label="Select chart type for comparison:",
        options=["Line Chart", "Bar Chart", "Area Chart"]
    )

    st.markdown("---")

    # Show total years in dataset
    st.info(f"📌 Dataset: {min_year} to {max_year}\n\n"
            f"📊 Total Years: {df.shape[0]}\n\n"
            f"📋 Total Columns: {df.shape[1]}")

# ── FILTER DATA BASED ON YEAR RANGE ───────────────────────────
# This filters the dataframe to only show selected years
# Boolean indexing: keep rows where Year is between start and end

filtered_df = df[
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
].reset_index(drop=True)

# ── KPI CARDS ROW ─────────────────────────────────────────────
# KPI = Key Performance Indicators
# These are the big number cards at the top of the dashboard

st.markdown('<div class="section-header">📌 Key Performance Indicators (Latest Year Data)</div>',
            unsafe_allow_html=True)

# Get the LAST row of FILTERED data (most recent year in selection)
latest = filtered_df.iloc[-1]

# Create 4 columns — each column gets one KPI card
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">📈 GDP Growth Rate</div>
            <div class="kpi-value">{latest['GDP_Growth_Rate']:.1f}%</div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">💰 Inflation Rate</div>
            <div class="kpi-value">{latest['Inflation_Rate']:.1f}%</div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">📦 Exports (USD B)</div>
             <div class="kpi-value">${float(latest['Exports_Billion_USD']):.0f}B</div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">👥 Population</div>
          <div class="kpi-value">{float(latest['Population_Millions']):.0f}M</div>
    """, unsafe_allow_html=True)

# Add space between sections
st.markdown("<br>", unsafe_allow_html=True)

# Second row of KPI cards
col5, col6, col7, col8 = st.columns(4)

with col5:
    # Average GDP Growth across selected years
    avg_gdp = filtered_df["GDP_Growth_Rate"].mean()
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">📊 Avg GDP Growth</div>
            <div class="kpi-value">{avg_gdp:.1f}%</div>
            <div class="kpi-subtitle">Selected Period</div>
        </div>
    """, unsafe_allow_html=True)

with col6:
    # Trade Deficit = Imports - Exports
    trade_deficit = latest["Imports_Billion_USD"] - latest["Exports_Billion_USD"]
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">⚖️ Trade Deficit</div>
            <div class="kpi-value">${trade_deficit:.0f}B</div>
            <div class="kpi-subtitle">Year {int(latest['Year'])}</div>
        </div>
    """, unsafe_allow_html=True)

with col7:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">🌾 Agriculture %</div>
            <div class="kpi-value">{latest['Agriculture_Contribution']:.1f}%</div>
            <div class="kpi-subtitle">GDP Contribution</div>
        </div>
    """, unsafe_allow_html=True)

with col8:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">🏭 Industry %</div>
            <div class="kpi-value">{latest['Industry_Contribution']:.1f}%</div>
            <div class="kpi-subtitle">GDP Contribution</div>
        </div>
    """, unsafe_allow_html=True)

# ── SECTION: INTERACTIVE COMPARISON CHART ─────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">📈 Interactive Indicator Comparison</div>',
            unsafe_allow_html=True)

# Only show chart if user selected at least one indicator
if selected_indicators:
    if chart_type == "Line Chart":
        # px.line creates an interactive line chart
        # x = X-axis column
        # y = list of Y-axis columns (one line per indicator)
        fig = px.line(
            filtered_df,
            x="Year",
            y=selected_indicators,
            title=f"Selected Economic Indicators ({year_range[0]}–{year_range[1]})",
            markers=True,           # Show dots at each data point
            color_discrete_sequence=px.colors.qualitative.Set2  # Color palette
        )

    elif chart_type == "Bar Chart":
        fig = px.bar(
            filtered_df,
            x="Year",
            y=selected_indicators,
            title=f"Selected Economic Indicators ({year_range[0]}–{year_range[1]})",
            barmode="group",        # Side by side bars
            color_discrete_sequence=px.colors.qualitative.Set2
        )

    else:  # Area Chart
        fig = px.area(
            filtered_df,
            x="Year",
            y=selected_indicators,
            title=f"Selected Economic Indicators ({year_range[0]}–{year_range[1]})",
            color_discrete_sequence=px.colors.qualitative.Set2
        )

    # Style the chart background and fonts
    fig.update_layout(
        plot_bgcolor="#1a1a2e",    # Dark background for chart area
        paper_bgcolor="#0f1117",   # Dark background for paper
        font_color="white",
        title_font_size=16,
        legend_title="Indicator",
        height=450,
        xaxis=dict(
            showgrid=True,
            gridcolor="#1E3A5F",
            tickangle=-45
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#1E3A5F"
        )
    )

    # Display the chart in Streamlit
    # use_container_width=True makes chart fill the full width
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ Please select at least one indicator from the sidebar.")

# ── SECTION: GDP GROWTH INTERACTIVE CHART ─────────────────────
st.markdown('<div class="section-header">📈 GDP Growth Rate Analysis</div>',
            unsafe_allow_html=True)

col_left, col_right = st.columns([3, 2])  # 3:2 ratio — left is wider

with col_left:
    # Interactive GDP line chart with Plotly
    fig_gdp = go.Figure()

    # Add line trace
    fig_gdp.add_trace(go.Scatter(
        x=filtered_df["Year"],
        y=filtered_df["GDP_Growth_Rate"],
        mode="lines+markers+text",  # Line + dots + text labels
        name="GDP Growth Rate",
        line=dict(color="#42A5F5", width=3),
        marker=dict(size=10, color="#1565C0"),
        text=[f"{v:.1f}%" for v in filtered_df["GDP_Growth_Rate"]],
        textposition="top center",
        textfont=dict(size=10, color="#90CAF9"),
        fill="tozeroy",             # Fill area from line to x-axis
        fillcolor="rgba(66, 165, 245, 0.15)"  # Light blue transparent fill
    ))

    fig_gdp.update_layout(
        title="GDP Growth Rate Trend",
        plot_bgcolor="#1a1a2e",
        paper_bgcolor="#0f1117",
        font_color="white",
        height=380,
        xaxis=dict(showgrid=True, gridcolor="#1E3A5F", tickangle=-45),
        yaxis=dict(showgrid=True, gridcolor="#1E3A5F",
                   title="Growth Rate (%)"),
    )

    st.plotly_chart(fig_gdp, use_container_width=True)

with col_right:
    # Summary statistics for GDP in selected period
    st.markdown("### 📊 GDP Statistics")
    st.markdown("<br>", unsafe_allow_html=True)

    gdp_stats = filtered_df["GDP_Growth_Rate"]

    # Display each statistic nicely
    stats_data = {
        "📈 Highest Growth": f"{gdp_stats.max():.2f}% ({int(filtered_df.loc[gdp_stats.idxmax(), 'Year'])})",
        "📉 Lowest Growth": f"{gdp_stats.min():.2f}% ({int(filtered_df.loc[gdp_stats.idxmin(), 'Year'])})",
        "📊 Average Growth": f"{gdp_stats.mean():.2f}%",
        "📏 Std Deviation": f"{gdp_stats.std():.2f}%",
        "📋 Total Years": f"{len(filtered_df)} years"
    }

    for label, value in stats_data.items():
        st.markdown(f"""
            <div style="background:#1E2B3C; border-left:4px solid #42A5F5;
                        padding:12px 15px; margin:8px 0; border-radius:6px;">
                <span style="color:#90CAF9; font-size:13px;">{label}</span><br>
                <span style="color:white; font-size:16px; font-weight:bold;">{value}</span>
            </div>
        """, unsafe_allow_html=True)

# ── SECTION: TRADE ANALYSIS ────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">🚢 Trade Analysis — Exports vs Imports</div>',
            unsafe_allow_html=True)

col_trade1, col_trade2 = st.columns(2)

with col_trade1:
    # Grouped bar chart for Exports vs Imports
    fig_trade = go.Figure()

    fig_trade.add_trace(go.Bar(
        x=filtered_df["Year"],
        y=filtered_df["Exports_Billion_USD"],
        name="Exports",
        marker_color="#66BB6A",   # Green
        text=filtered_df["Exports_Billion_USD"].round(0),
        textposition="outside"
    ))

    fig_trade.add_trace(go.Bar(
        x=filtered_df["Year"],
        y=filtered_df["Imports_Billion_USD"],
        name="Imports",
        marker_color="#EF5350",   # Red
        text=filtered_df["Imports_Billion_USD"].round(0),
        textposition="outside"
    ))

    fig_trade.update_layout(
        title="Exports vs Imports (Billion USD)",
        barmode="group",
        plot_bgcolor="#1a1a2e",
        paper_bgcolor="#0f1117",
        font_color="white",
        height=380,
        xaxis=dict(showgrid=False, tickangle=-45),
        yaxis=dict(showgrid=True, gridcolor="#1E3A5F", title="Billion USD"),
    )

    st.plotly_chart(fig_trade, use_container_width=True)

with col_trade2:
    # Trade Balance (Exports - Imports)
    filtered_df_copy = filtered_df.copy()
    filtered_df_copy["Trade_Balance"] = (
        filtered_df_copy["Exports_Billion_USD"] - filtered_df_copy["Imports_Billion_USD"]
    )

    # Color: Green if positive (surplus), Red if negative (deficit)
    colors = ["#66BB6A" if v >= 0 else "#EF5350"
              for v in filtered_df_copy["Trade_Balance"]]

    fig_balance = go.Figure()
    fig_balance.add_trace(go.Bar(
        x=filtered_df_copy["Year"],
        y=filtered_df_copy["Trade_Balance"],
        name="Trade Balance",
        marker_color=colors,
        text=filtered_df_copy["Trade_Balance"].round(1),
        textposition="outside"
    ))

    # Add horizontal line at y=0
    fig_balance.add_hline(y=0, line_dash="dash", line_color="white", opacity=0.5)

    fig_balance.update_layout(
        title="Trade Balance (Exports − Imports)",
        plot_bgcolor="#1a1a2e",
        paper_bgcolor="#0f1117",
        font_color="white",
        height=380,
        xaxis=dict(showgrid=False, tickangle=-45),
        yaxis=dict(showgrid=True, gridcolor="#1E3A5F", title="Billion USD")
    )

    st.plotly_chart(fig_balance, use_container_width=True)

# ── SECTION: INFLATION & UNEMPLOYMENT ─────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">📉 Inflation & Unemployment Trends</div>',
            unsafe_allow_html=True)

fig_inf = go.Figure()

fig_inf.add_trace(go.Scatter(
    x=filtered_df["Year"],
    y=filtered_df["Inflation_Rate"],
    name="Inflation Rate (%)",
    mode="lines+markers",
    line=dict(color="#FF5252", width=3),
    marker=dict(size=9)
))

fig_inf.add_trace(go.Scatter(
    x=filtered_df["Year"],
    y=filtered_df["Unemployment_Rate"],
    name="Unemployment Rate (%)",
    mode="lines+markers",
    line=dict(color="#FFD740", width=3),
    marker=dict(size=9)
))

fig_inf.update_layout(
    title="Inflation Rate vs Unemployment Rate",
    plot_bgcolor="#1a1a2e",
    paper_bgcolor="#0f1117",
    font_color="white",
    height=400,
    xaxis=dict(showgrid=True, gridcolor="#1E3A5F", tickangle=-45),
    yaxis=dict(showgrid=True, gridcolor="#1E3A5F", title="Rate (%)"),
    hovermode="x unified"   # Shows all values at same X when hovering
)

st.plotly_chart(fig_inf, use_container_width=True)

# ── SECTION: SECTOR PIE CHART ──────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">🏭 Economic Sector Contribution</div>',
            unsafe_allow_html=True)

col_pie1, col_pie2 = st.columns([1, 1])

with col_pie1:
    # Year selector for pie chart
    selected_year_pie = st.selectbox(
        "Select Year for Sector Analysis:",
        options=sorted(filtered_df["Year"].tolist()),
        index=len(filtered_df) - 1  # Default to last year
    )

    # Get data for selected year
    year_data = filtered_df[filtered_df["Year"] == selected_year_pie].iloc[0]
    services_pct = 100 - year_data["Agriculture_Contribution"] - year_data["Industry_Contribution"]

    fig_pie = px.pie(
        values=[
            year_data["Agriculture_Contribution"],
            year_data["Industry_Contribution"],
            services_pct
        ],
        names=["Agriculture", "Industry", "Services"],
        title=f"Sector Contribution — {int(selected_year_pie)}",
        color_discrete_sequence=["#66BB6A", "#42A5F5", "#FFA726"],
        hole=0.35  # Donut style (hole in center)
    )

    fig_pie.update_layout(
        paper_bgcolor="#0f1117",
        font_color="white",
        title_font_size=15,
        height=400
    )

    fig_pie.update_traces(
        textposition="inside",
        textinfo="percent+label",
        textfont_size=13
    )

    st.plotly_chart(fig_pie, use_container_width=True)

with col_pie2:
    # Line chart showing how sectors changed over time
    fig_sector = px.line(
        filtered_df,
        x="Year",
        y=["Agriculture_Contribution", "Industry_Contribution"],
        title="Sector Contribution Trend Over Years",
        markers=True,
        color_discrete_map={
            "Agriculture_Contribution": "#66BB6A",
            "Industry_Contribution": "#42A5F5"
        }
    )

    fig_sector.update_layout(
        plot_bgcolor="#1a1a2e",
        paper_bgcolor="#0f1117",
        font_color="white",
        height=400,
        xaxis=dict(showgrid=True, gridcolor="#1E3A5F", tickangle=-45),
        yaxis=dict(showgrid=True, gridcolor="#1E3A5F", title="Contribution (%)"),
        legend_title="Sector"
    )

    st.plotly_chart(fig_sector, use_container_width=True)

# ── SECTION: POPULATION CHART ──────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">👥 Population Growth</div>',
            unsafe_allow_html=True)

fig_pop = px.area(
    filtered_df,
    x="Year",
    y="Population_Millions",
    title="India Population Growth (Millions)",
    color_discrete_sequence=["#26C6DA"]
)

fig_pop.update_traces(
    fill="tozeroy",
    fillcolor="rgba(38, 198, 218, 0.2)",
    line=dict(color="#00ACC1", width=3)
)

fig_pop.update_layout(
    plot_bgcolor="#1a1a2e",
    paper_bgcolor="#0f1117",
    font_color="white",
    height=380,
    xaxis=dict(showgrid=True, gridcolor="#1E3A5F", tickangle=-45),
    yaxis=dict(showgrid=True, gridcolor="#1E3A5F", title="Population (Millions)")
)

# Add text annotations for first and last year
if not filtered_df.empty:
    first = filtered_df.iloc[0]
    last = filtered_df.iloc[-1]
    for row in [first, last]:
        fig_pop.add_annotation(
            x=row["Year"],
            y=row["Population_Millions"],
            text=f"{row['Population_Millions']:.0f}M",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#00ACC1",
            font=dict(color="white", size=12),
            bgcolor="#0D47A1",
            bordercolor="#42A5F5",
            borderwidth=1
        )

st.plotly_chart(fig_pop, use_container_width=True)

# ── SECTION: SAVED CHART IMAGES ────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">🖼️ Static Analysis Charts (from visualization.py)</div>',
            unsafe_allow_html=True)

st.info("💡 These charts are generated by running: **python visualization.py**")

# List of all saved images
image_files = [
    ("images/chart1_gdp_growth.png", "Chart 1: GDP Growth Rate"),
    ("images/chart2_inflation_unemployment.png", "Chart 2: Inflation vs Unemployment"),
    ("images/chart3_exports_imports.png", "Chart 3: Exports vs Imports"),
    ("images/chart4_sector_pie.png", "Chart 4: Sector Contribution"),
    ("images/chart5_population.png", "Chart 5: Population Growth"),
    ("images/chart6_heatmap.png", "Chart 6: Correlation Heatmap"),
]

# Display images in pairs (2 per row)
for i in range(0, len(image_files), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(image_files):
            img_path, img_title = image_files[i + j]
            with cols[j]:
                if os.path.exists(img_path):  # Check if file exists
                    img = Image.open(img_path)
                    st.image(img, caption=img_title, use_column_width=True)
                else:
                    st.warning(f"⚠️ '{img_path}' not found.\n\n"
                               f"Run: **python visualization.py** first")

# ── SECTION: DATA TABLE ────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">📋 Raw Data Table</div>',
            unsafe_allow_html=True)

# Checkbox — show table only if user wants it
show_table = st.checkbox("📊 Show Full Data Table", value=True)

if show_table:
    st.markdown(f"**Showing {len(filtered_df)} records** for years "
                f"**{year_range[0]} to {year_range[1]}**")

    # Style the dataframe
    # highlight_max highlights the largest value in each column (green)
    # highlight_min highlights the smallest value (red)
    styled_df = filtered_df.style \
        .highlight_max(subset=["GDP_Growth_Rate", "Exports_Billion_USD"],
                       color="#1B5E20") \
        .highlight_min(subset=["GDP_Growth_Rate", "Inflation_Rate"],
                       color="#B71C1C") \
        .format({
            "GDP_Growth_Rate": "{:.2f}%",
            "Inflation_Rate": "{:.2f}%",
            "Unemployment_Rate": "{:.2f}%",
            "Exports_Billion_USD": "${:.1f}B",
            "Imports_Billion_USD": "${:.1f}B",
            "Agriculture_Contribution": "{:.2f}%",
            "Industry_Contribution": "{:.2f}%",
            "Population_Millions": "{:.1f}M"
        })

    st.dataframe(styled_df, use_container_width=True, height=400)

    # Download button — lets user download filtered data as CSV
    csv_download = filtered_df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv_download,
        file_name=f"india_data_{year_range[0]}_{year_range[1]}.csv",
        mime="text/csv"
    )

# ── FOOTER ────────────────────────────────────────────────────
st.markdown("""
    <div class="footer">
        India Economic Dashboard &nbsp;|&nbsp;
        Built with Python, Streamlit & Plotly &nbsp;|&nbsp;
        Data: india_economic_data.csv
    </div>
""", unsafe_allow_html=True)

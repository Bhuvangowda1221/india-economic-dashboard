# ============================================================
# visualization.py
# India Economic Data - Analysis and Chart Generation
# This file reads data and creates charts saved as images
# ============================================================

# ── STEP 1: Import Libraries ─────────────────────────────────
# Think of imports like opening your toolbox before starting work

import pandas as pd           # For reading and handling CSV data
import matplotlib.pyplot as plt  # For drawing charts
import matplotlib.patches as mpatches  # For custom legend items
import seaborn as sns         # For beautiful chart styling
import os                     # For creating folders automatically
import warnings               # To ignore unimportant warnings

# Ignore warning messages that are not important
warnings.filterwarnings("ignore")

# ── STEP 2: Settings ─────────────────────────────────────────
# Set the overall style for all charts
sns.set_theme(style="darkgrid")  # Dark grid background looks professional

# Set default figure size for all charts
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["font.size"] = 12

# ── STEP 3: Create Images Folder ─────────────────────────────
# If "images" folder doesn't exist, create it automatically
# os.makedirs creates the folder; exist_ok=True means no error if it already exists
os.makedirs("images", exist_ok=True)
print("✅ Images folder is ready.")

# ── STEP 4: Load the Dataset ─────────────────────────────────
# pd.read_csv reads your CSV file and stores it as a "DataFrame"
# A DataFrame is like an Excel table in Python

print("\n📂 Loading dataset...")
df = pd.read_csv("india_economic_data.csv")

# Clean column names
df.columns = df.columns.str.strip()

# 🔥 FIX MISSING VALUES (UPDATED)
df = df.ffill()

# Remove any remaining issues
df = df.dropna()

for col in df.columns:
    if col != "Year":
        df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.fillna(0)

# ── STEP 5: Explore the Data ─────────────────────────────────
print("\n" + "="*60)
print("📊 FIRST 5 ROWS OF DATA (df.head())")
print("="*60)
print(df.head())  # Shows first 5 rows — like peeking at the data

print("\n" + "="*60)
print("📐 DATASET SHAPE (rows, columns)")
print("="*60)
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n" + "="*60)
print("📈 STATISTICAL SUMMARY (df.describe())")
print("="*60)
print(df.describe())  # Shows min, max, average, etc. for all columns

print("\n" + "="*60)
print("🔍 MISSING VALUES CHECK")
print("="*60)
print(df.isnull().sum())  # Shows how many empty cells in each column

# ── CHART 1: GDP Growth Rate Over Years ──────────────────────
# WHY THIS CHART: Understand how India's economy grew year by year
# LINE CHART is best for showing trends over time

print("\n📊 Creating Chart 1: GDP Growth Rate...")

fig, ax = plt.subplots(figsize=(12, 6))
# Plot a line with dots at each data point
ax.plot(
    df["Year"],           # X-axis: Years
    df["GDP_Growth_Rate"], # Y-axis: GDP Growth Rate values
    color="#2196F3",       # Blue color
    linewidth=2.5,         # Thickness of line
    marker="o",            # Circle dot at each year
    markersize=8,          # Size of circle
    label="GDP Growth Rate"
)

# Add value labels on each point so reader can see exact numbers
for x, y in zip(df["Year"], df["GDP_Growth_Rate"]):
    ax.annotate(
        f"{y:.1f}%",              # Format: e.g., "7.2%"
        (x, y),                   # Position: at the data point
        textcoords="offset points", # Offset from the point
        xytext=(0, 12),           # 12 pixels above the point
        ha="center",              # Center-aligned text
        fontsize=9,
        color="#0D47A1"           # Dark blue color
    )

# Titles and labels
ax.set_title("India GDP Growth Rate Over Years", fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Year", fontsize=13)
ax.set_ylabel("GDP Growth Rate (%)", fontsize=13)
ax.legend(fontsize=11)
ax.set_xticks(df["Year"])          # Show every year on X-axis
ax.tick_params(axis="x", rotation=45)  # Rotate year labels to avoid overlap

plt.tight_layout()  # Automatically adjust spacing so nothing is cut off
plt.savefig("images/chart1_gdp_growth.png", dpi=150, bbox_inches="tight")
plt.close()  # Close chart to free memory
print("✅ Chart 1 saved: images/chart1_gdp_growth.png")

# ── CHART 2: Inflation vs Unemployment ───────────────────────
# WHY THIS CHART: Compare two economic problems side by side
# DUAL-LINE CHART shows both trends on the same graph

print("\n📊 Creating Chart 2: Inflation vs Unemployment...")

fig, ax = plt.subplots(figsize=(12, 6))

# Line 1 — Inflation Rate
ax.plot(
    df["Year"],
    df["Inflation_Rate"],
    color="#F44336",   # Red color
    linewidth=2.5,
    marker="s",        # Square marker
    markersize=8,
    label="Inflation Rate (%)"
)

# Line 2 — Unemployment Rate
ax.plot(
    df["Year"],
    df["Unemployment_Rate"],
    color="#FF9800",   # Orange color
    linewidth=2.5,
    marker="^",        # Triangle marker
    markersize=8,
    label="Unemployment Rate (%)"
)

ax.set_title("Inflation Rate vs Unemployment Rate Over Years",
             fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Year", fontsize=13)
ax.set_ylabel("Rate (%)", fontsize=13)
ax.legend(fontsize=11)
ax.set_xticks(df["Year"])
ax.tick_params(axis="x", rotation=45)

plt.tight_layout()
plt.savefig("images/chart2_inflation_unemployment.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 2 saved: images/chart2_inflation_unemployment.png")

# ── CHART 3: Exports vs Imports ───────────────────────────────
# WHY THIS CHART: See India's trade balance — did we export more or import more?
# BAR CHART is best for comparing two values side by side for each year

print("\n📊 Creating Chart 3: Exports vs Imports...")

# Width of each bar
bar_width = 0.35

# X positions for each year
x = range(len(df["Year"]))

fig, ax = plt.subplots(figsize=(14, 6))

# Bars for Exports — shifted left
bars1 = ax.bar(
    [i - bar_width/2 for i in x],  # Position slightly left
    df["Exports_Billion_USD"],
    width=bar_width,
    label="Exports (Billion USD)",
    color="#4CAF50",    # Green
    edgecolor="white"
)

# Bars for Imports — shifted right
bars2 = ax.bar(
    [i + bar_width/2 for i in x],  # Position slightly right
    df["Imports_Billion_USD"],
    width=bar_width,
    label="Imports (Billion USD)",
    color="#9C27B0",    # Purple
    edgecolor="white"
)

ax.set_title("India Exports vs Imports (Billion USD)", fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Year", fontsize=13)
ax.set_ylabel("Value (Billion USD)", fontsize=13)
ax.set_xticks(list(x))
ax.set_xticklabels(df["Year"], rotation=45)
ax.legend(fontsize=11)

plt.tight_layout()
plt.savefig("images/chart3_exports_imports.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 3 saved: images/chart3_exports_imports.png")

# ── CHART 4: Sector Contribution Pie Chart ───────────────────
# WHY THIS CHART: Show how Agriculture vs Industry contribute to economy
# PIE CHART is best for showing "parts of a whole"
# We use the LATEST YEAR's data for this

print("\n📊 Creating Chart 4: Sector Contribution Pie Chart...")

# Get the last row of data (most recent year)
latest = df.iloc[-1]  # iloc[-1] means "last row"

# Data for pie chart
sectors = ["Agriculture", "Industry", "Services (Remaining)"]

# Services = 100% - Agriculture% - Industry%
services = 100 - latest["Agriculture_Contribution"] - latest["Industry_Contribution"]
values = [
    latest["Agriculture_Contribution"],
    latest["Industry_Contribution"],
    services
]

colors = ["#66BB6A", "#42A5F5", "#FFA726"]   # Green, Blue, Orange
explode = (0.05, 0.05, 0.05)  # Slightly separate each slice

fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    values,
    labels=sectors,
    autopct="%1.1f%%",   # Show percentage on each slice
    colors=colors,
    explode=explode,
    startangle=140,
    textprops={"fontsize": 13}
)

ax.set_title(
    f"India Economic Sector Contribution ({int(latest['Year'])})",
    fontsize=16, fontweight="bold", pad=20
)

plt.tight_layout()
plt.savefig("images/chart4_sector_pie.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 4 saved: images/chart4_sector_pie.png")

# ── CHART 5: Population Growth ────────────────────────────────
# WHY THIS CHART: Show how India's population grew over years
# AREA CHART fills the area under the line — shows growth clearly

print("\n📊 Creating Chart 5: Population Growth...")

fig, ax = plt.subplots(figsize=(12, 6))

# fill_between fills color between the line and x-axis
ax.fill_between(
    df["Year"],
    df["Population_Millions"],
    alpha=0.4,          # 40% transparent fill
    color="#26C6DA",    # Cyan color
    label="Population (Millions)"
)

# Draw the line on top of the fill
ax.plot(
    df["Year"],
    df["Population_Millions"],
    color="#00838F",    # Darker cyan for the line
    linewidth=2.5,
    marker="o",
    markersize=7
)

ax.set_title("India Population Growth Over Years (Millions)",
             fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Year", fontsize=13)
ax.set_ylabel("Population (Millions)", fontsize=13)
ax.legend(fontsize=11)
ax.set_xticks(df["Year"])
ax.tick_params(axis="x", rotation=45)

plt.tight_layout()
plt.savefig("images/chart5_population.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 5 saved: images/chart5_population.png")

# ── CHART 6: Correlation Heatmap ─────────────────────────────
# WHY THIS CHART: See which economic factors are related to each other
# HEATMAP uses colors — dark red = strong positive relation, dark blue = negative

print("\n📊 Creating Chart 6: Correlation Heatmap...")

# Select only numeric columns for correlation
numeric_cols = [
    "GDP_Growth_Rate", "Inflation_Rate", "Unemployment_Rate",
    "Exports_Billion_USD", "Imports_Billion_USD",
    "Agriculture_Contribution", "Industry_Contribution", "Population_Millions"
]

# corr() calculates correlation between every pair of columns
# Result is a matrix (table) of correlation values from -1 to +1
correlation_matrix = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(12, 9))

# annot=True shows the number in each cell
# fmt=".2f" formats number to 2 decimal places
# cmap="RdYlBu" uses Red-Yellow-Blue color scheme
sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="RdYlBu",
    center=0,            # 0 = white/neutral color
    linewidths=0.5,
    linecolor="white",
    ax=ax,
    cbar_kws={"shrink": 0.8}
)

ax.set_title("Correlation Heatmap of India Economic Indicators",
             fontsize=16, fontweight="bold", pad=15)
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.yticks(fontsize=10)

plt.tight_layout()
plt.savefig("images/chart6_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 6 saved: images/chart6_heatmap.png")

# ── FINAL SUMMARY ─────────────────────────────────────────────
print("\n" + "="*60)
print("🎉 ALL CHARTS CREATED SUCCESSFULLY!")
print("="*60)
print("📁 Find your charts in the 'images' folder:")
print("   • chart1_gdp_growth.png")
print("   • chart2_inflation_unemployment.png")
print("   • chart3_exports_imports.png")
print("   • chart4_sector_pie.png")
print("   • chart5_population.png")
print("   • chart6_heatmap.png")
print("\n✅ Now run: streamlit run app.py")
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import os

sns.set_theme(style="whitegrid", palette="muted")
os.makedirs("output/charts", exist_ok=True)

def generate_charts(df: pd.DataFrame, city: str) -> list:
    """Generate all charts and return list of file paths."""
    chart_paths = []
    df = df.sort_values("date")

    # ── Chart 1: Temperature range over time ──
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.fill_between(df["date"], df["temp_min"], df["temp_max"],
                    alpha=0.3, color="tomato", label="Temp range")
    ax.plot(df["date"], df["temp_avg"], color="tomato",
            linewidth=2, label="Avg temp")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator())
    plt.xticks(rotation=45)
    ax.set_title(f"Temperature Overview — {city} (Last 30 Days)",
                 fontsize=14, fontweight="bold")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    plt.tight_layout()
    path1 = "output/charts/temperature.png"
    plt.savefig(path1, dpi=150)
    plt.close()
    chart_paths.append(path1)
    print("✅ Chart 1: Temperature saved")

    # ── Chart 2: Daily precipitation bar chart ──
    fig, ax = plt.subplots(figsize=(12, 4))
    colors = ["steelblue" if x > 0 else "lightgray"
              for x in df["precipitation"]]
    ax.bar(df["date"], df["precipitation"], color=colors, width=0.8)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator())
    plt.xticks(rotation=45)
    ax.set_title(f"Daily Precipitation — {city}",
                 fontsize=14, fontweight="bold")
    ax.set_ylabel("Precipitation (mm)")
    plt.tight_layout()
    path2 = "output/charts/precipitation.png"
    plt.savefig(path2, dpi=150)
    plt.close()
    chart_paths.append(path2)
    print("✅ Chart 2: Precipitation saved")

    # ── Chart 3: Wind speed trend ──
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(df["date"], df["wind_speed"], color="slateblue",
            linewidth=1.5, marker="o", markersize=3)
    ax.fill_between(df["date"], df["wind_speed"],
                    alpha=0.2, color="slateblue")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator())
    plt.xticks(rotation=45)
    ax.set_title(f"Wind Speed — {city}",
                 fontsize=14, fontweight="bold")
    ax.set_ylabel("Wind Speed (km/h)")
    plt.tight_layout()
    path3 = "output/charts/wind_speed.png"
    plt.savefig(path3, dpi=150)
    plt.close()
    chart_paths.append(path3)
    print("✅ Chart 3: Wind speed saved")

    # ── Chart 4: Temperature distribution ──
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["temp_avg"], bins=15, kde=True,
                 color="tomato", ax=ax)
    ax.set_title(f"Temperature Distribution — {city}",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Average Temperature (°C)")
    plt.tight_layout()
    path4 = "output/charts/temp_distribution.png"
    plt.savefig(path4, dpi=150)
    plt.close()
    chart_paths.append(path4)
    print("✅ Chart 4: Distribution saved")

    return chart_paths
import os
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def analyze_data(df: pd.DataFrame, city: str) -> dict:
    """Run statistical analysis + AI insight generation."""
    
    # ── Statistical analysis ──
    stats = {
        "avg_temp": round(df["temp_avg"].mean(), 1),
        "max_temp": round(df["temp_max"].max(), 1),
        "min_temp": round(df["temp_min"].min(), 1),
        "total_rain": round(df["precipitation"].sum(), 1),
        "avg_wind": round(df["wind_speed"].mean(), 1),
        "rainy_days": int((df["precipitation"] > 1).sum()),
        "hottest_day": df.loc[df["temp_max"].idxmax(), "date"].strftime("%B %d"),
        "coldest_day": df.loc[df["temp_min"].idxmin(), "date"].strftime("%B %d"),
    }
    
    # ── Anomaly detection ──
    temp_std = df["temp_avg"].std()
    temp_mean = df["temp_avg"].mean()
    anomalies = df[abs(df["temp_avg"] - temp_mean) > 1.5 * temp_std]
    anomaly_dates = anomalies["date"].dt.strftime("%b %d").tolist()
    
    # ── Trend detection ──
    df_sorted = df.sort_values("date")
    first_half = df_sorted.head(len(df_sorted)//2)["temp_avg"].mean()
    second_half = df_sorted.tail(len(df_sorted)//2)["temp_avg"].mean()
    trend = "warming" if second_half > first_half else "cooling"
    trend_delta = round(abs(second_half - first_half), 1)
    
    # ── AI-generated executive summary ──
    prompt = f"""You are a professional business intelligence analyst writing 
an executive summary for a weather report.

City: {city}
Period: Last 30 days
Key Statistics:
- Average temperature: {stats['avg_temp']}°C
- Highest temperature: {stats['max_temp']}°C on {stats['hottest_day']}
- Lowest temperature: {stats['min_temp']}°C on {stats['coldest_day']}
- Total rainfall: {stats['total_rain']}mm
- Rainy days: {stats['rainy_days']} out of 30
- Average wind speed: {stats['avg_wind']} km/h
- Temperature trend: {trend} by {trend_delta}°C over the period
- Temperature anomalies detected on: {', '.join(anomaly_dates) if anomaly_dates else 'None'}

Write a concise 3-paragraph executive summary:
1. Overall conditions overview
2. Notable events and anomalies
3. Business implications (impact on energy consumption, 
   agriculture, tourism, or logistics)

Be professional, specific, and data-driven. No bullet points."""

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
        max_tokens=500,
        temperature=0.3
    )
    
    ai_summary = response.choices[0].message.content
    
    return {
        "stats": stats,
        "anomalies": anomaly_dates,
        "trend": trend,
        "trend_delta": trend_delta,
        "ai_summary": ai_summary
    }

if __name__ == "__main__":
    df = pd.read_csv("data/raw_data.csv", parse_dates=["date"])
    results = analyze_data(df, "Algiers")
    print("\n── AI Executive Summary ──")
    print(results["ai_summary"])
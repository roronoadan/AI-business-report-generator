import streamlit as st
import pandas as pd
import os
from datetime import datetime
from data_collector import fetch_weather_data
from ai_analyzer import analyze_data
from chart_generator import generate_charts
from report_generator import generate_pdf
from dotenv import load_dotenv

load_dotenv()

# ── Page config ──
st.set_page_config(
    page_title="AI Business Report Generator",
    page_icon="🤖",
    layout="wide"
)

# ── Header ──
st.title("🤖 AI Business Report Generator")
st.markdown(
    "Automated pipeline · Real data → AI Analysis → "
    "Charts → PDF Report"
)
st.divider()

# ── Sidebar ──
with st.sidebar:
    st.header("⚙️ Configuration")

    city = st.text_input(
        "City",
        value="Algiers",
        placeholder="e.g. Montreal, Dubai, Paris..."
    )

    days = st.slider(
        "Analysis period (days)",
        min_value=7,
        max_value=90,
        value=30,
        step=7
    )

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get your free key at console.groq.com"
    )

    run_btn = st.button(
        "🚀 Generate Report",
        use_container_width=True,
        type="primary"
    )

    st.divider()
    st.caption("Built by Abderrahmane Hadj Hamdi")
    st.caption("github.com/roronoadan")

# ── Main area ──
if not run_btn:
    # Landing state
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Step 1**\nCollects real weather data from Open-Meteo API — no key needed")
    with col2:
        st.info("**Step 2**\nAI generates executive summary using Groq LLaMA 3.1")
    with col3:
        st.info("**Step 3**\nOutputs a professional PDF report with 4 charts")

    st.markdown("### Enter a city and click Generate Report to start")

else:
    # ── Validation ──
    if not city.strip():
        st.error("Please enter a city name")
        st.stop()

    if not api_key.strip():
        st.error("Please enter your Groq API key")
        st.stop()

    # Set API key for this session
    os.environ["GROQ_API_KEY"] = api_key.strip()

    # ── Pipeline ──
    os.makedirs("data", exist_ok=True)
    os.makedirs("output/charts", exist_ok=True)
    os.makedirs("output/reports", exist_ok=True)

    # Progress bar
    progress = st.progress(0, text="Starting pipeline...")

    try:
        # Step 1 — Collect data
        progress.progress(10, text=f" Fetching {days} days of data for {city}...")
        df = fetch_weather_data(city, days)
        df.to_csv("data/raw_data.csv", index=False)
        progress.progress(30, text="✅ Data collected")

        # Step 2 — AI analysis
        progress.progress(40, text=" Running AI analysis...")
        analysis = analyze_data(df, city)
        progress.progress(60, text="✅ AI analysis complete")

        # Step 3 — Charts
        progress.progress(65, text="Generating charts...")
        chart_paths = generate_charts(df, city)
        progress.progress(80, text="✅ Charts ready")

        # Step 4 — PDF
        progress.progress(85, text="Building PDF report...")
        report_path = generate_pdf(city, analysis, chart_paths)
        progress.progress(100, text="✅ Report complete!")

        st.success(f"✅ Report generated for **{city}**!")
        st.divider()

        # ── Results layout ──
        col_left, col_right = st.columns([1, 1])

        with col_left:
            # Key metrics
            st.subheader(" Key Metrics")
            stats = analysis["stats"]

            m1, m2, m3 = st.columns(3)
            m1.metric("Avg Temp", f"{stats['avg_temp']}°C")
            m2.metric("Max Temp", f"{stats['max_temp']}°C")
            m3.metric("Min Temp", f"{stats['min_temp']}°C")

            m4, m5, m6 = st.columns(3)
            m4.metric("Total Rain", f"{stats['total_rain']}mm")
            m5.metric("Rainy Days", f"{stats['rainy_days']}/30")
            m6.metric("Avg Wind", f"{stats['avg_wind']}km/h")

            st.divider()

            # Trend
            trend_emoji = "📈" if analysis["trend"] == "warming" else "📉"
            st.metric(
                f"{trend_emoji} Temperature Trend",
                f"{analysis['trend'].capitalize()}",
                delta=f"+{analysis['trend_delta']}°C over period"
            )

            # Anomalies
            if analysis["anomalies"]:
                st.warning(
                    f"⚠️ Temperature anomalies detected on: "
                    f"{', '.join(analysis['anomalies'])}"
                )
            else:
                st.success("✅ No temperature anomalies detected")

        with col_right:
            # AI summary
            st.subheader("AI Executive Summary")
            st.markdown(
                f"""<div style='background:#f8f9fa;padding:16px;
                border-radius:8px;border-left:4px solid #4a4a6a;
                font-size:14px;line-height:1.7;color:#2d2d2d'>
                {analysis['ai_summary'].replace(chr(10), '<br/>')}
                </div>""",
                unsafe_allow_html=True
            )

        st.divider()

        # ── Charts ──
        st.subheader(" Visual Analysis")

        chart_titles = [
            "Temperature Range",
            "Precipitation",
            "Wind Speed",
            "Temperature Distribution"
        ]

        # Row 1
        c1, c2 = st.columns(2)
        for i, (col, path, title) in enumerate(
            zip([c1, c2], chart_paths[:2], chart_titles[:2])
        ):
            with col:
                if os.path.exists(path):
                    st.caption(title)
                    st.image(path, use_container_width=True)

        # Row 2
        c3, c4 = st.columns(2)
        for i, (col, path, title) in enumerate(
            zip([c3, c4], chart_paths[2:], chart_titles[2:])
        ):
            with col:
                if os.path.exists(path):
                    st.caption(title)
                    st.image(path, use_container_width=True)

        st.divider()

        # ── Raw data table ──
        with st.expander(" View Raw Data"):
            st.dataframe(
                df.style.format({
                    "temp_max": "{:.1f}°C",
                    "temp_min": "{:.1f}°C",
                    "temp_avg": "{:.1f}°C",
                    "precipitation": "{:.1f}mm",
                    "wind_speed": "{:.1f}km/h"
                }),
                use_container_width=True
            )

        # ── Download PDF ──
        st.subheader(" Download Report")
        with open(report_path, "rb") as f:
            st.download_button(
                label=" Download PDF Report",
                data=f,
                file_name=os.path.basename(report_path),
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )

    except ValueError as e:
        progress.empty()
        st.error(f" City not found: {e}. Try a different city name.")
    except Exception as e:
        progress.empty()
        st.error(f" Pipeline error: {e}")
        st.caption("Check your API key and internet connection")
import os
import sys
from data_collector import fetch_weather_data
from ai_analyzer import analyze_data
from chart_generator import generate_charts
from report_generator import generate_pdf

os.makedirs("data", exist_ok=True)
os.makedirs("output/charts", exist_ok=True)
os.makedirs("output/reports", exist_ok=True)

def run_pipeline(city: str = "Algiers"):
    print(f"\n🚀 Starting BI Report Pipeline for: {city}")
    print("=" * 50)
    
    print("\n📡 Step 1: Collecting data...")
    df = fetch_weather_data(city, days=30)
    df.to_csv("data/raw_data.csv", index=False)
    
    print("\n🤖 Step 2: Running AI analysis...")
    analysis = analyze_data(df, city)
    
    print("\n📊 Step 3: Generating charts...")
    chart_paths = generate_charts(df, city)
    
    print("\n📄 Step 4: Building PDF report...")
    report_path = generate_pdf(city, analysis, chart_paths)
    
    print("\n" + "=" * 50)
    print(f"✅ Pipeline complete!")
    print(f"📄 Report: {report_path}")
    print(f"📊 Charts: output/charts/")
    return report_path

if __name__ == "__main__":
    city = sys.argv[1] if len(sys.argv) > 1 else "Algiers"
    run_pipeline(city)
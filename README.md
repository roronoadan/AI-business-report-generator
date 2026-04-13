# AI Business Intelligence Report Generator

Automated pipeline that collects real data, runs AI analysis, 
and generates professional PDF business reports — zero manual work.

## What It Does

```
Real Data → AI Analysis → Charts → PDF Report
    ↓              ↓           ↓          ↓
Open-Meteo    Groq LLaMA3  Matplotlib  ReportLab
```

## Sample Output

The pipeline generates a complete PDF containing:
- Executive summary written by AI (LLaMA 3)
- Key metrics table
- Temperature trend analysis
- Precipitation analysis  
- Anomaly detection
- 4 professional visualizations

## Quick Start

```bash
git clone https://github.com/roronoadan/ai-business-report-generator
cd ai-business-report-generator
pip install -r requirements.txt

# Add your free Groq API key (console.groq.com)
echo "GROQ_API_KEY=your_key_here" > .env

# Run for any city
python main.py "Montreal"
python main.py "Blida"
python main.py "Algiers"
```

## Tech Stack

| Layer | Tool |
|---|---|
| Data Collection | Open-Meteo API (free) |
| Data Processing | Python · Pandas |
| AI Insights | Groq API · LLaMA 3 (free) |
| Visualization | Matplotlib · Seaborn |
| Report Generation | ReportLab |

## Business Value

This pipeline automates what a business analyst does manually 
in 3+ hours. Use cases:
- Climate risk reporting for logistics companies
- Weather impact analysis for agriculture businesses  
- Monthly environmental reports for municipalities
- Any domain with time-series data

## Extend It

The pipeline is modular — swap the data source to:
- Financial data (Yahoo Finance API)
- Sales data (CSV input)
- IoT sensor data
- Social media metrics

Built by Abderrahmane Hadj Hamdi · 

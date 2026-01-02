# Quick Start Guide

## Setup (5 minutes)

1. **Install Python 3.11**
   - Download from python.org
   - Check: `python --version`

2. **Clone/Download project**
```bash
   cd edtech-portfolio
```

3. **Create virtual environment**
```bash
   python -m venv venv
   venv\Scripts\activate    # Windows
```

4. **Install packages**
```bash
   pip install -r requirements.txt
```

## Run Project (5 minutes)
```bash
# Run everything
python project-1-mapping/data_collector.py
python project-1-mapping/data_analysis.py
python project-1-mapping/visualizations.py
```

## View Results

Open in browser:
- `outputs/dashboard.html` - Main dashboard
- `outputs/map_visualization.html` - Interactive map

## Troubleshooting

**"Module not found"**
→ Activate venv: `venv\Scripts\activate`

**"File not found"**
→ Make sure you're in project root directory

**"No data to display"**
→ Run data_collector.py first

## Need Help?

Check the main README.md for detailed documentation.
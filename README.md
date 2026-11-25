# 🌍 Earthquake Risk Classification for Afghanistan
 
A machine learning project that analyzes 34 years of seismic data from Afghanistan and the surrounding region, and classifies the risk level of an earthquake scenario as **LOW**, **MEDIUM**, or **HIGH** through an interactive web dashboard.
 
**Status:** v1.0, complete. Built with Python, scikit-learn, and Streamlit.
 
![Dashboard screenshot](docs/dashboard_screenshot.png)
 
---
 
## Why I Built This
 
I grew up in Afghanistan and lived through several earthquakes with no warning system and no accessible risk information. Years later, in the United States, I received an alert on my phone before I felt a small, distant earthquake, and it changed how safe I felt. This project is my attempt to explore what data and machine learning can do for a region with very little ground-based monitoring infrastructure.
 
---
 
## What It Does
 
1. **Collects** 8,250 real earthquakes (magnitude 4.0+, 1990–2024) from the USGS catalog for a bounding box covering Afghanistan and its neighbors (29°N–39°N, 60°E–75°E)
2. **Explores** the data: magnitude distribution, activity over time, depth zones, and spatial clustering
3. **Engineers features**, including seismic energy, depth risk, and distance to Kabul
4. **Trains** a Random Forest classifier to assign a risk level to an earthquake
5. **Serves** the model in a Streamlit dashboard with a live risk assessment and a historical map
```
USGS catalog ──► Cleaning & EDA ──► Feature engineering ──► Random Forest ──► Streamlit dashboard
 (8,250 events)   (notebooks 01-02)    (notebook 03)         (notebook 04)       (dashboard/app.py)
```
 
---
 
## Key Findings
 
- **The Gutenberg-Richter law shows up in the data.** Light earthquakes (M4.0–4.9) make up the majority of events, and larger ones are exponentially rarer.
- **The region averages about 236 magnitude 4.0+ events per year**, roughly one every 1.5 days.
- **2005 was the most active year**, driven by the October 2005 Kashmir earthquake (M7.6) and its aftershocks.
- **The risk score singled out the right event.** The 2005 Kashmir earthquake (M7.6, depth 26 km) received the maximum score of 1.0 from the engineered risk formula.
- **Depth changes risk a lot.** The 2015 Hindu Kush earthquake (M7.5, but 231 km deep) scored 0.76, well below the shallow Kashmir event, which matches the seismology: deep earthquakes lose energy before reaching the surface.
### Model Results
 
| Metric | Value |
|---|---|
| Training set | 6,600 events (80%) |
| Test set | 1,650 events (20%, stratified) |
| Overall accuracy | **XX.X%** |
| HIGH-risk recall | **XX.X%** |
| HIGH-risk precision | **XX.X%** |
 
*Full classification report and confusion matrix are in `notebooks/04_ml_model.ipynb`.*
 
---
 
## Engineered Features
 
| Feature | What it captures |
|---|---|
| `depth_risk_score` | Shallow (0–70 km) = 3, intermediate (70–300 km) = 2, deep = 1 |
| `energy_proxy` | `10^(1.5 × magnitude)`. Each +1 magnitude releases about 32× more energy |
| `dist_to_kabul` | Haversine distance to Kabul, as a rough proxy for population exposure |
| `lat_grid`, `lon_grid` | Coordinates rounded to about 11 km grid cells |
| `combined_risk_score` | Weighted blend of normalized magnitude (0.40), energy (0.35), and depth risk (0.25), used to create the LOW / MEDIUM / HIGH labels |
 
**Risk labels:** LOW below 0.15, MEDIUM from 0.15 to 0.35, HIGH at 0.35 and above.
 
**On data leakage:** the labels come from `combined_risk_score`, so that column (and the redundant `mag_risk_score`) is deliberately **excluded** from the model's inputs. The classifier trains on seven features: `mag`, `depth`, `depth_risk_score`, `energy_proxy`, `dist_to_kabul`, `lat_grid`, `lon_grid`.
 
---
 
## Project Structure
 
```
earthquake-risk-afghanistan/
├── notebooks/
│   ├── 01_data_collection.ipynb      # USGS API → raw CSV
│   ├── 02_exploratory_analysis.ipynb # charts, trends, maps
│   ├── 03_feature_engineering.ipynb  # features + combined risk score
│   └── 04_ml_model.ipynb             # train, evaluate, save model
├── dashboard/
│   └── app.py                        # Streamlit app
├── models/
│   ├── random_forest_risk_classifier.pkl
│   └── feature_columns.json
├── docs/                             # screenshots
├── data/                             # not tracked by git (see below)
├── requirements.txt
└── README.md
```
 
---
 
## How to Run It
 
```bash
# 1. Clone and set up
git clone https://github.com/tahmina-07/earthquake-risk-afghanistan.git
cd earthquake-risk-afghanistan
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install streamlit-folium
 
# 2. Rebuild the data (the data/ folder is git-ignored)
#    Run notebooks 01 and 03 in order. They download the USGS data
#    and create data/usgs_afghanistan_features.csv
 
# 3. Launch the dashboard
streamlit run dashboard/app.py
```
 
The trained model is included in `models/`, so you only need to rebuild the data to see the dashboard's historical map. Open `notebooks/04_ml_model.ipynb` if you want to retrain.
 
**Dashboard usage:** set a magnitude, depth, and location in the sidebar. The app shows the predicted risk level, the model's confidence, the distance to Kabul, and how the 100 trees voted. The second tab maps every historical earthquake of magnitude 5+ with your scenario pinned on top.
 
---
 
## Limitations
 
I'd rather be upfront about what this project is and isn't.
 
- **The labels are heuristic.** Risk classes are derived from a scoring formula I designed, not from real impact data such as casualties or damage. The model learns to approximate that formula, so it shows the pipeline works, not that it predicts real-world harm.
- **It is not a true early warning system.** Early warning systems detect the first seismic waves in real time and alert people before strong shaking arrives. This tool classifies the risk of an earthquake from its parameters, which are only known once an event has happened. It is a risk assessment prototype and should not be used for real emergency decisions.
- **USGS catalog only.** Planned satellite inputs (SRTM elevation, Sentinel-1 surface deformation) were not included in this version.
- **Kabul is the only exposure point.** Population risk is approximated by distance to one city, not by real population or building-vulnerability data.
- **The region box includes neighboring countries.** Some events come from Pakistan and Tajikistan.
- **Catalog completeness varies over time.** Magnitude 4.0 events from the 1990s are likely under-recorded compared with recent years.
---
 
## Future Work
 
- Add SRTM terrain features and test whether they improve the model
- Validate against independent impact data (USGS PAGER alerts, casualty records)
- Add more population centers and population-density data
- Explore a real-time sensing component (e.g., a low-cost accelerometer node)
---
 
## Skills Demonstrated
 
API data collection · exploratory data analysis · geospatial analysis (Haversine, grid zoning, Folium) · feature engineering · supervised classification (Random Forest) · model evaluation (precision, recall, F1, confusion matrix) · avoiding data leakage · model persistence (joblib) · web app deployment (Streamlit) · Git/GitHub workflow
 
---
 
## Tech Stack
 
`Python 3.13` `pandas` `NumPy` `scikit-learn` `Matplotlib` `Seaborn` `Folium` `Streamlit` `joblib`
 
## Data Source
 
[USGS Earthquake Catalog](https://earthquake.usgs.gov/fdsnws/event/1/) (public domain)
 
---
 
**Author:** Tahmina Sahar, Computer Science student at University of the People
 

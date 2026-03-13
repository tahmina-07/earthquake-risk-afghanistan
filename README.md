# 🌍 Earthquake Risk Assessment for Afghanistan

> Using historical seismic data, satellite imagery, and machine learning to identify earthquake risk patterns and support early warning systems for vulnerable communities.

## Motivation

While living in Afghanistan, I experienced several earthquakes that had a strong physical and psychological impact. There were no effective early warning systems or accessible risk information available. After coming to the United States, I received an early warning notification before even feeling a small earthquake — which significantly reduced anxiety and felt much safer. This contrast motivated me to explore how satellite data and machine learning could support earthquake risk assessment and early warning efforts in regions with limited ground-based infrastructure.

---

## System Architecture

![System Architecture]([docs/architecture.svg](https://github.com/tahmina-07/earthquake-risk-afghanistan/blob/main/architecture.svg))

---

## Data Sources

| Source | Data | Use |
|--------|------|-----|
| [USGS Earthquake Catalog](https://earthquake.usgs.gov/fdsnws/event/1/) | Location, magnitude, depth, time | Ground truth seismic data |
| [NASA SRTM](https://www2.jpl.nasa.gov/srtm/) | Digital Elevation Model | Terrain & fault proximity features |
| [Sentinel-1 InSAR](https://sentinel.esa.int/web/sentinel/missions/sentinel-1) | Land surface deformation | Crustal stress indicators |
| Raspberry Pi / ROS2 | Real-time accelerometer readings | Ground sensor prototype |

---

## Project Structure

```
earthquake-risk-afghanistan/
├── data/             ← raw & processed datasets (not tracked by git)
├── notebooks/        ← Jupyter analysis notebooks
│   ├── 01_data_collection.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   ├── 03_feature_engineering.ipynb
│   └── 04_ml_modeling.ipynb
├── models/           ← saved trained ML models
├── dashboard/        ← Streamlit interactive risk map
├── src/              ← reusable Python modules
├── docs/             ← diagrams and paper assets
├── requirements.txt
└── README.md
```

---

## Roadmap

- [x] Week 1 — Project setup & USGS data collection
- [ ] Week 2 — Exploratory analysis & earthquake mapping
- [ ] Week 3 — NASA & Sentinel-1 satellite data integration
- [ ] Week 4 — Feature engineering & ML risk model
- [ ] Week 5 — Anomaly detection & early warning logic
- [ ] Week 6 — ROS2 sensor simulation / Raspberry Pi node
- [ ] Week 7 — Streamlit dashboard deployment
- [ ] Week 8 — Research paper write-up

---

## Tech Stack

`Python` `Pandas` `GeoPandas` `Scikit-learn` `XGBoost` `Folium` `Streamlit` `ROS2` `Raspberry Pi` `USGS API` `NASA SRTM` `Sentinel-1`

---

## Research Paper

This project accompanies a research paper exploring the question:

*"Can historical and satellite-based earthquake data be used with artificial intelligence to identify earthquake risk patterns and support early warning tools for vulnerable communities in Afghanistan?"*

---

*Built as a portfolio project by Tahmina Sahar — CS student passionate about using technology for humanitarian impact.*

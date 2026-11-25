from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

# ---------- Setup ----------
BASE = Path(__file__).resolve().parent.parent
KABUL_LAT, KABUL_LON = 34.5553, 69.2075

st.set_page_config(page_title="Afghanistan Earthquake Risk",
                   page_icon="🌍", layout="wide")

# ---------- Loaders (cached) ----------
@st.cache_resource
def load_model():
    model = joblib.load(BASE / "models" / "random_forest_risk_classifier.pkl")
    with open(BASE / "models" / "feature_columns.json") as f:
        cols = json.load(f)
    return model, cols

@st.cache_data
def load_history():
    return pd.read_csv(BASE / "data" / "usgs_afghanistan_features.csv")

# ---------- Helpers ----------
def haversine_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    a = (np.sin((lat2 - lat1) / 2) ** 2
         + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2)
    return 2 * np.arcsin(np.sqrt(a)) * 6371

def build_features(mag, depth, lat, lon):
    depth_score = 3 if depth < 70 else (2 if depth < 300 else 1)
    return pd.DataFrame({
        "mag": [mag],
        "depth": [depth],
        "depth_risk_score": [depth_score],
        "energy_proxy": [10 ** (1.5 * mag)],
        "dist_to_kabul": [haversine_km(lat, lon, KABUL_LAT, KABUL_LON)],
        "lat_grid": [round(lat, 1)],
        "lon_grid": [round(lon, 1)],
    })

# ---------- Page ----------
model, feature_columns = load_model()

st.title("🌍 Afghanistan Earthquake Risk Assessment")
st.caption("Research prototype. Not an official warning system.")

st.sidebar.header("Earthquake parameters")
mag = st.sidebar.slider("Magnitude", 4.0, 8.5, 6.0, 0.1)
depth = st.sidebar.slider("Depth (km)", 0, 300, 15)
lat = st.sidebar.number_input("Latitude", 29.0, 39.0, 34.5, 0.1)
lon = st.sidebar.number_input("Longitude", 60.0, 75.0, 69.2, 0.1)

X_new = build_features(mag, depth, lat, lon)[feature_columns]
prediction = model.predict(X_new)[0]
proba = model.predict_proba(X_new)[0]
dist = X_new["dist_to_kabul"].iloc[0]

tab1, tab2 = st.tabs(["Risk assessment", "Historical map"])

with tab1:
    if prediction == "HIGH":
        st.error(f"🔴 HIGH RISK: magnitude {mag}, depth {depth} km")
    elif prediction == "MEDIUM":
        st.warning(f"🟡 MEDIUM RISK: magnitude {mag}, depth {depth} km")
    else:
        st.success(f"🟢 LOW RISK: magnitude {mag}, depth {depth} km")

    c1, c2, c3 = st.columns(3)
    c1.metric("Predicted risk", prediction)
    c2.metric("Model confidence", f"{proba.max():.0%}")
    c3.metric("Distance to Kabul", f"{dist:.0f} km")

    st.subheader("How the 100 trees voted")
    st.bar_chart(pd.DataFrame({"probability": proba}, index=model.classes_))

with tab2:
    history = load_history()
    big = history[history["mag"] >= 5.0]

    m = folium.Map(location=[34.0, 67.7], zoom_start=6,
                   tiles="CartoDB dark_matter")
    for _, row in big.iterrows():
        color = "red" if row["mag"] >= 7 else "orange" if row["mag"] >= 6 else "yellow"
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=row["mag"] * 1.2, color=color,
            fill=True, fill_opacity=0.5,
            popup=f"M{row['mag']} | {row['depth']} km",
        ).add_to(m)

    folium.Marker([lat, lon], tooltip="Your scenario",
                  icon=folium.Icon(color="blue")).add_to(m)
    st_folium(m, width=1000, height=550)

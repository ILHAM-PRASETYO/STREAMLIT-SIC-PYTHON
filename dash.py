import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import random
from datetime import datetime
import time

# ------------------------
# PAGE CONFIG
# ------------------------
st.set_page_config(page_title="IoT Realtime Chart", layout="wide")

st.title("IoT – Realtime Sensor Dashboard (Demo)")

# ------------------------
# SESSION STATE (INIT)
# ------------------------
if "data" not in st.session_state:
    st.session_state.data = []

# ------------------------
# SIMULASI DATA (ganti dengan MQTT nanti)
# ------------------------
def generate_fake_data():
    return {
        "ts": datetime.now(),
        "temp": random.uniform(27, 35),
        "hum": random.uniform(60, 80),
        "pred": random.choice(["Dingin", "Normal", "Panas"])
    }

# ------------------------
# LOOP DISPLAY REALTIME
# ------------------------
placeholder = st.empty()

for _ in range(50):   # 50 update (demo)
    # Append data (in future → replace with MQTT incoming data)
    row = generate_fake_data()
    st.session_state.data.append(row)

    df = pd.DataFrame(st.session_state.data)

    with placeholder.container():
        st.subheader("Realtime Sensor Visualization")

        # 🎨 Warna untuk kondisi
        colors = df["pred"].map({
            "Panas": "red",
            "Normal": "green",
            "Dingin": "blue"
        })

        # Plot
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df["ts"], y=df["temp"],
                mode="lines+markers",
                name="Temp (°C)",
                marker=dict(color=colors)
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df["ts"], y=df["hum"],
                mode="lines+markers",
                name="Humidity (%)"
            )
        )

        fig.update_layout(height=450, xaxis_title="Timestamp")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Last Data")
        st.write(df.tail(1))

    time.sleep(1)  # update real-time


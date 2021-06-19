"""
Implements streamlit dashboard for PULSE data
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import os


class PULSEApp:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    @staticmethod
    def setup():
        st.title('PULSE')
        return None

    def test_plot(self):
        fig = px.histogram(self.data, x='REGION')
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    DATA_DIR = r'../data/raw'
    file_name = [file for file in os.listdir(DATA_DIR) if file.endswith(r'.csv')][0]
    df = pd.read_csv(os.path.join(DATA_DIR, file_name))
    pulse_app = PULSEApp(data=df)
    pulse_app.setup()
    pulse_app.test_plot()

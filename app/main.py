import streamlit as st
import pandas as pd
from transformers import pipeline

st.title("Kundenfeedback-Analyse")

# Lade Modell nur einmal
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

model = load_model()

# CSV-Upload
uploaded_file = st.file_uploader("CSV-Datei hochladen", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    if "text" not in df.columns:
        st.error("Die CSV-Datei muss eine Spalte namens 'text' enthalten.")
    else:
        st.write("Vorschau der Daten:")
        st.dataframe(df.head())

        if st.button("Analysieren"):
            results = model(df["text"].tolist())
            df["stimmung"] = [r["label"] for r in results]
            st.success("Analyse abgeschlossen!")
            st.dataframe(df)

# Alternativ: Manuelle Texteingabe
st.subheader("Oder manuelle Eingabe")
text = st.text_area("Gib dein Feedback ein:")

if text:
    result = model(text)
    st.write("Einzelergebnis:", result[0]['label'])

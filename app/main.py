import streamlit as st
import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ———————————————————————————————————————————
# Page-Config: Wide Layout
# ———————————————————————————————————————————
st.set_page_config(
    page_title="Kundenfeedback-Analyse für KMU",
    layout="wide"
)
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
st.image("static/logo.png", width=400)


# ———————————————————————————————————————————
# CSS: Nur die Textspalte umbrechen, alle anderen Spalten normal
# ———————————————————————————————————————————
st.markdown("""
<style>
  /* Text-Spalte (1. Spalte) darf umbrechen */
  .dataframe td:nth-child(1),
  .dataframe th:nth-child(1) {
    white-space: normal !important;
    word-wrap: break-word !important;
  }
  /* Alle anderen Spalten (rating, stimmung, score) nicht umbrechen */
  .dataframe td:nth-child(n+2),
  .dataframe th:nth-child(n+2) {
    white-space: nowrap !important;
  }
</style>
""", unsafe_allow_html=True)

# ———————————————————————————————————————————
# 1. Modell- und Topic-Loader
# ———————————————————————————————————————————
@st.cache_resource
def load_models():
    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
    tokenizer  = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    model      = AutoModelForSequenceClassification.from_pretrained(model_name)
    sentiment_pipe = pipeline(
        "sentiment-analysis",
        model=model,
        tokenizer=tokenizer,
        device=-1
    )
    def topic_loader(n_topics):
        vec = CountVectorizer(max_df=0.95, min_df=2, stop_words="english")
        lda = LatentDirichletAllocation(n_components=n_topics, random_state=0)
        return vec, lda

    return sentiment_pipe, tokenizer, topic_loader

sentiment_pipe, tokenizer, load_topic_components = load_models()

# ———————————————————————————————————————————
# Helper: Chunking für lange Texte
# ———————————————————————————————————————————
def sentiment_chunked(text: str):
    enc = tokenizer(text, return_tensors="pt", truncation=False)
    ids = enc["input_ids"][0]
    chunks = [ids[i : i + 512] for i in range(0, len(ids), 512)]
    results = []
    for c in chunks:
        txt = tokenizer.decode(c, skip_special_tokens=True)
        r = sentiment_pipe(txt, truncation=True, max_length=512, padding=True)[0]
        results.append(r)
    labels = [r["label"] for r in results]
    maj    = max(set(labels), key=labels.count)
    avg    = sum(r["score"] for r in results) / len(results)
    return {"label": maj, "score": avg}

# ———————————————————————————————————————————
# 2. Header
# ———————————————————————————————————————————
st.title("Kundenfeedback-Analyse für KMU")

# ———————————————————————————————————————————
# 3. CSV-Upload & Batch-Analyse
# ———————————————————————————————————————————
uploaded = st.file_uploader("CSV-Datei hochladen (Spalte 'text')", type="csv")
if uploaded:
    # Encoding-Handling
    try:
        df = pd.read_csv(uploaded, sep=None, engine="python", encoding="utf-8")
    except UnicodeDecodeError:
        uploaded.seek(0)
        df = pd.read_csv(uploaded, sep=None, engine="python", encoding="latin-1")

    if "text" not in df.columns:
        st.error("Die CSV-Datei muss eine Spalte namens 'text' enthalten.")
    else:
        st.subheader("Vorschau")
        preview = df.head(5)
        st.dataframe(preview, height=5*35 + 50, use_container_width=True)

        # Speichere den Upload im Session State
        st.session_state["batch_input_df"] = df.copy()

# Nur anzeigen, wenn ein Upload im State liegt
if "batch_input_df" in st.session_state:
    # Button für Analyse
    if st.button("Batch-Sentiment analysieren"):
        with st.spinner("Analysiere Batch…"):
            labs, scs = [], []
            for txt in st.session_state["batch_input_df"]["text"].astype(str):
                out = sentiment_chunked(txt)
                labs.append(out["label"])
                scs.append(out["score"])
        df = st.session_state["batch_input_df"].copy()
        df["stimmung"] = labs
        df["score"] = scs
        # Speichere Ergebnisse im State
        st.session_state["batch_result_df"] = df.copy()
        st.success("Batch-Analyse abgeschlossen!")

    # Ergebnisse zeigen, wenn vorhanden
    if "batch_result_df" in st.session_state:
        df = st.session_state["batch_result_df"]
        st.subheader("Ergebnisse")
        rows = df.shape[0]
        height = min(800, rows*35 + 50)
        st.dataframe(df, height=height, use_container_width=True)

        st.download_button(
            "Ergebnisse als CSV herunterladen",
            data=df.to_csv(index=False),
            file_name="sentiment_results.csv",
            mime="text/csv"
        )

        if st.checkbox("Themen extrahieren"):
            n = st.slider("Anzahl Themen", 2, 10, 5, key="topics_slider")
            vec, lda = load_topic_components(n)
            X = vec.fit_transform(df["text"].astype(str))
            lda.fit(X)
            st.write("**Top-Wörter pro Thema**")
            terms = vec.get_feature_names_out()
            for i, comp in enumerate(lda.components_):
                top10 = [terms[j] for j in comp.argsort()[-10:]]
                st.write(f"Topic {i+1}: {', '.join(top10)}")

# ———————————————————————————————————————————
# 4. Manuelle Einzel-Analyse
# ———————————————————————————————————————————
st.markdown("---")
st.subheader("Manuelle Einzel-Analyse")

text_input = st.text_area("Gib dein Feedback ein:")
if st.button("Einzel-Sentiment analysieren"):
    if text_input.strip():
        with st.spinner("Analysiere Text…"):
            out = sentiment_chunked(text_input)
        st.write(f"**Stimmung:** {out['label']}  &nbsp;&nbsp; **Score:** {out['score']:.2f}")
    else:
        st.warning("Bitte erst Text eingeben.")
# ———————————————————————————————————————————
# 5. Optional: Keyword-Analyse
# ———————————————————————————————————————————
st.markdown("---")
st.subheader("Zusätzliche Keyword-Analyse")

from model.keywords import extract_top_keywords

keyword_input = st.text_area("Texteingabe für Keyword-Analyse (mehrere Sätze möglich):", key="keywords_input")

if st.button("Top-Keywords anzeigen"):
    if keyword_input.strip():
        keywords = extract_top_keywords([keyword_input])
        st.write("**Häufigste Wörter:**")
        st.markdown(", ".join(keywords))
    else:
        st.warning("Bitte gib einen Text ein.")

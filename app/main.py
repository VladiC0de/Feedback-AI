import streamlit as st
import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# ———————————————————————————————————————————
# 1. Modell- und Topic‐Loader
# ———————————————————————————————————————————
@st.cache_resource
def load_models():
    # Sentiment-Pipeline auf BERT-Basis
    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    sentiment_pipe = pipeline(
        "sentiment-analysis",
        model=model,
        tokenizer=tokenizer,
        device=-1  # CPU; für GPU `device=0`
    )
    # LDA-Topic-Komponenten
    def topic_loader(n_topics):
        vec = CountVectorizer(max_df=0.95, min_df=2, stop_words="english")
        lda = LatentDirichletAllocation(n_components=n_topics, random_state=0)
        return vec, lda

    return sentiment_pipe, tokenizer, topic_loader

sentiment_pipe, tokenizer, load_topic_components = load_models()

def sentiment_chunked(text: str):
    """
    Zerlege einen beliebig langen Text in 512-Token-Chunks,
    führe Sentiment-Analyse auf jedem Chunk durch und
    aggregiere das Gesamtergebnis.
    """
    # Tokenize ohne Truncation, um komplette Länge zu sehen
    encoding = tokenizer(text, return_tensors="pt", truncation=False)
    ids = encoding["input_ids"][0]
    # Aufsplitten in aufeinanderfolgende 512-Token-Stücke
    chunks = [ids[i : i + 512] for i in range(0, len(ids), 512)]
    results = []
    for chunk in chunks:
        chunk_text = tokenizer.decode(chunk, skip_special_tokens=True)
        res = sentiment_pipe(
            chunk_text,
            truncation=True,
            max_length=512,
            padding=True
        )[0]
        results.append(res)
    # Aggregation: Mehrheitslabel + durchschnittlicher Score
    labels = [r["label"] for r in results]
    maj_label = max(set(labels), key=labels.count)
    avg_score = sum(r["score"] for r in results) / len(results)
    return {"label": maj_label, "score": avg_score}


# ———————————————————————————————————————————
# 2. App‐Header
# ———————————————————————————————————————————
st.title("Kundenfeedback-Analyse für KMU")

# ———————————————————————————————————————————
# 3. CSV-Batch-Analyse mit Chunking
# ———————————————————————————————————————————
uploaded_file = st.file_uploader("CSV-Datei hochladen (Spalte 'text')", type=["csv"])
if uploaded_file:
    # Encoding + Auto-Delimiter mit Python-Engine
    try:
        df = pd.read_csv(uploaded_file, sep=None, engine="python", encoding="utf-8")
    except UnicodeDecodeError:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, sep=None, engine="python", encoding="latin-1")

    if "text" not in df.columns:
        st.error("Die CSV-Datei muss eine Spalte namens 'text' enthalten.")
    else:
        st.write("**Vorschau der Daten**")
        st.dataframe(df.head())

        if st.button("Batch-Sentiment analysieren"):
            with st.spinner("Analysiere Batch (Chunking)..."):
                # Chunked Sentiment für jede Zeile
                out_labels = []
                out_scores = []
                for txt in df["text"].astype(str):
                    res = sentiment_chunked(txt)
                    out_labels.append(res["label"])
                    out_scores.append(res["score"])
            df["stimmung"] = out_labels
            df["score"]    = out_scores

            st.success("Batch-Analyse abgeschlossen!")
            st.dataframe(df)

            # Download-Button
            csv_data = df.to_csv(index=False)
            st.download_button(
                "Ergebnisse herunterladen",
                data=csv_data,
                file_name="sentiment_results.csv",
                mime="text/csv"
            )

            # Themen-Extraktion (optional)
            if st.checkbox("Themen extrahieren"):
                n_topics = st.slider("Anzahl Themen", min_value=2, max_value=10, value=5)
                vectorizer, lda = load_topic_components(n_topics)
                X = vectorizer.fit_transform(df["text"].astype(str))
                lda.fit(X)

                st.write("**Top-Wörter pro Thema**")
                terms = vectorizer.get_feature_names_out()
                for idx, comp in enumerate(lda.components_):
                    top = [terms[i] for i in comp.argsort()[-10:]]
                    st.write(f"Topic {idx+1}: {', '.join(top)}")

# ———————————————————————————————————————————
# 4. Manuelle Einzel-Analyse mit Chunking
# ———————————————————————————————————————————
st.markdown("---")
st.subheader("Manuelle Einzel-Analyse")

text_input = st.text_area("Gib dein Feedback ein:")
if st.button("Einzel-Sentiment analysieren"):
    if text_input.strip():
        with st.spinner("Analysiere Text (Chunking)..."):
            res = sentiment_chunked(text_input)
        st.write(f"**Stimmung:** {res['label']}")
        st.write(f"**Score:** {res['score']:.2f}")
    else:
        st.warning("Bitte erst Text eingeben.")

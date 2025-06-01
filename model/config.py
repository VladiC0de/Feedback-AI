# model/config.py

# Modellkonfiguration für Sentiment-Analyse
SENTIMENT_MODEL = {
    "name": "nlptown/bert-base-multilingual-uncased-sentiment",
    "type": "BERT",
    "language": "multilingual",
    "output": "1-5 stars sentiment score"
}

# Konfiguration für Topic-Modellierung
TOPIC_MODEL = {
    "vectorizer": "CountVectorizer",
    "model": "LatentDirichletAllocation",
    "params": {
        "max_df": 0.95,
        "min_df": 2,
        "stop_words": "english",
        "n_components_default": 5
    }
}

# Logging-Konfiguration
LOGGING = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "feedback_analysis.log"
}

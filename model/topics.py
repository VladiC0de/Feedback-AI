# model/topics.py
import logging
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from .config import TOPIC_MODEL, LOGGING

# Logging einrichten
logging.basicConfig(
    level=getattr(logging, LOGGING["level"]),
    format=LOGGING["format"]
)
logger = logging.getLogger("topic_model")

class TopicExtractor:
    """Klasse zur Extraktion von Themen mit LDA"""
    
    def __init__(self, n_topics=None):
        """Initialisiert das Topic-Modell"""
        self.params = TOPIC_MODEL["params"]
        self.n_topics = n_topics or self.params["n_components_default"]
        logger.info(f"Initialisiere Topic-Modell mit {self.n_topics} Themen")
        
        try:
            self.vectorizer = CountVectorizer(
                max_df=self.params["max_df"],
                min_df=self.params["min_df"],
                stop_words=self.params["stop_words"]
            )
            
            self.lda = LatentDirichletAllocation(
                n_components=self.n_topics,
                random_state=0
            )
            logger.info("Topic-Modell erfolgreich initialisiert")
        except Exception as e:
            logger.error(f"Fehler bei der Initialisierung des Topic-Modells: {e}")
            raise
    
    def extract_topics(self, texts):
        """Extrahiert Themen aus einer Liste von Texten"""
        if not texts or len(texts) < 2:
            logger.warning("Zu wenige Texte für Topic-Extraktion")
            return [], []
        
        try:
            X = self.vectorizer.fit_transform(texts)
            self.lda.fit(X)
            
            # Top-Wörter pro Thema extrahieren
            terms = self.vectorizer.get_feature_names_out()
            topics = []
            
            for i, comp in enumerate(self.lda.components_):
                top_terms_idx = comp.argsort()[:-11:-1]
                top_terms = [terms[idx] for idx in top_terms_idx]
                topics.append(top_terms)
            
            logger.info(f"{self.n_topics} Themen erfolgreich extrahiert")
            
            # Themen-Zuordnung für jeden Text
            doc_topics = self.lda.transform(X)
            
            return topics, doc_topics
        
        except Exception as e:
            logger.error(f"Fehler bei der Topic-Extraktion: {e}")
            return [], []
    
    def get_top_topics_for_document(self, doc_idx, doc_topics, n=2):
        """Gibt die Top-N Themen für ein Dokument zurück"""
        if doc_idx >= len(doc_topics):
            return []
        
        # Indizes der Top-N Themen für das Dokument
        top_topics_idx = doc_topics[doc_idx].argsort()[:-n-1:-1]
        return [(idx, doc_topics[doc_idx][idx]) for idx in top_topics_idx]
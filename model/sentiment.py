# model/sentiment.py
import logging
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from .config import SENTIMENT_MODEL, LOGGING

# Logging einrichten
logging.basicConfig(
    level=getattr(logging, LOGGING["level"]),
    format=LOGGING["format"]
)
logger = logging.getLogger("sentiment_model")

class SentimentAnalyzer:
    """Klasse zur Sentiment-Analyse mit BERT-Modell"""
    
    def __init__(self):
        """Initialisiert das Sentiment-Analyse-Modell"""
        self.model_name = SENTIMENT_MODEL["name"]
        logger.info(f"Initialisiere Sentiment-Modell: {self.model_name}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_fast=True)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.sentiment_pipe = pipeline(
                "sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer,
                device=-1  # CPU verwenden
            )
            logger.info("Sentiment-Modell erfolgreich geladen")
        except Exception as e:
            logger.error(f"Fehler beim Laden des Sentiment-Modells: {e}")
            raise
    
    def analyze(self, text):
        """Führt Sentiment-Analyse für einen Text durch"""
        if not text or not text.strip():
            logger.warning("Leerer Text für Sentiment-Analyse übergeben")
            return {"label": "neutral", "score": 0.5}
        
        try:
            # Chunking für lange Texte
            enc = self.tokenizer(text, return_tensors="pt", truncation=False)
            ids = enc["input_ids"][0]
            chunks = [ids[i : i + 512] for i in range(0, len(ids), 512)]
            
            if not chunks:
                logger.warning("Keine Chunks für Analyse gefunden")
                return {"label": "neutral", "score": 0.5}
            
            results = []
            for c in chunks:
                txt = self.tokenizer.decode(c, skip_special_tokens=True)
                r = self.sentiment_pipe(txt, truncation=True, max_length=512, padding=True)[0]
                results.append(r)
            
            labels = [r["label"] for r in results]
            maj = max(set(labels), key=labels.count)
            avg = sum(r["score"] for r in results) / len(results)
            
            logger.info(f"Sentiment-Analyse abgeschlossen: {maj} ({avg:.2f})")
            return {"label": maj, "score": avg}
        
        except Exception as e:
            logger.error(f"Fehler bei der Sentiment-Analyse: {e}")
            return {"label": "error", "score": 0.0}
# Feedback-AI: KI-basierte Kundenfeedback-Analyse für KMU

## Projektübersicht

Feedback-AI ist eine benutzerfreundliche Webanwendung, die kleinen und mittleren Unternehmen (KMU) ermöglicht, Kundenfeedback automatisch zu analysieren und zu visualisieren. Die Anwendung nutzt moderne KI-Technologien, um Stimmungen (Sentiment) in Texten zu erkennen und häufige Themen zu identifizieren, ohne dass eigene Data-Science-Ressourcen benötigt werden.

## Funktionen

- **Sentiment-Analyse**: Automatische Erkennung der Stimmung in Kundenfeedback (1-5 Sterne)
- **Themenmodellierung**: Identifikation häufiger Themen in Kundenfeedback
- **Batch-Verarbeitung**: Analyse großer Mengen von Feedback-Daten über CSV-Upload
- **Einzelanalyse**: Direkte Eingabe und Analyse einzelner Feedback-Texte
- **Datenvisualisierung**: Übersichtliche Darstellung der Analyseergebnisse
- **Export-Funktion**: Speichern der Ergebnisse als CSV-Datei

## Technologie-Stack

- **Programmiersprache**: Python 3.11
- **Frameworks**: 
  - Hugging Face Transformers (BERT-Modell für Sentiment-Analyse)
  - scikit-learn (für Themenmodellierung mit LDA)
- **Frontend**: Streamlit
- **Datenvisualisierung**: seaborn, plotly
- **Datenquellen**: Google Reviews API, CSV-Dateien, Umfragen

## Projektstruktur

```
feedback-ai/
├── data/                  → Beispieldaten
│   ├── google_reviews.csv → Google Reviews Beispieldaten
│   └── customer_reviews.csv → Synthetische Kundenfeedback-Daten
├── notebooks/             → Jupyter Notebooks für Exploration & Modelltraining
│   ├── data_inventory.xlsx → Übersicht aller Datenquellen
│   ├── sentiment_analysis_exploration.ipynb → Exploration der Sentiment-Analyse
│   └── topic_modeling_exploration.ipynb → Exploration der Themenmodellierung
├── model/                 → Trainierte Modelle und Konfiguration
│   ├── __init__.py
│   ├── config.py          → Modellkonfigurationen
│   ├── sentiment.py       → Sentiment-Analyse-Implementierung
│   └── topics.py          → Themenmodellierungs-Implementierung
├── app/                   → Streamlit Web-App
│   └── main.py            → Hauptanwendung
├── static/                → Bilder, Style-Guidelines
│   ├── logo.png           → Anwendungslogo
│   ├── style.css          → CSS-Stile für die Anwendung
│   └── style_guidelines.md → Design-Richtlinien
└── requirements.txt       → Abhängigkeiten
```

## Modellarchitektur und Datenfluss

Unten sehen Sie die grafische Übersicht über die Hauptkomponenten und den Datenfluss unserer KI-Anwendung.  
Das Responsive Design (Desktop & Mobile) beeinflusst dabei ausschließlich die Darstellung des letzten Blocks (Visualisierung & Export).

**Frontend / Responsive Design (Desktop & Mobile)**  
Dieser Block steht oberhalb der Pipeline und zeigt, dass sich die Darstellung der Analyseergebnisse je nach Endgerät unterscheidet. Der Pfeil führt direkt zum letzten Block.

**Daten-Eingabe**  
CSV-Upload oder Google Reviews API – das Feedback gelangt von hier in den Verarbeitungspfad.

**Text-Vorverarbeitung (Tokenisierung, Chunking)**  
Texte werden in Tokens zerlegt. Bei langen Texten erfolgt Chunking, um die 512-Token-Grenze des Modells einzuhalten.

**Sentiment-Modul (BERT: nlptown/bert-base-multilingual-uncased-sentiment)**  
Das Modell gibt eine Sternebewertung (1–5) zurück. Die Bewertung wird in Labels (positiv, neutral, negativ) überführt.

**Themenmodell (LDA: CountVectorizer → LDA)**  
Mittels CountVectorizer wird eine Dokument-Term-Matrix erstellt. LDA extrahiert auf dieser Basis Themen mit den häufigsten Schlüsselbegriffen.

**Visualisierung & Export (Streamlit: DataFrame, Charts, Download-Buttons)**  
Die Ergebnisse werden in einer interaktiven Oberfläche dargestellt. Export als CSV ist jederzeit möglich.

![Modellarchitektur](docs/model_architecture.png)


## Installation

1. Klonen Sie das Repository:
```bash
git clone https://github.com/username/feedback-ai.git
cd feedback-ai
```

2. Erstellen Sie eine virtuelle Umgebung und installieren Sie die Abhängigkeiten:
```bash
python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Starten Sie die Anwendung:
```bash
cd app
streamlit run main.py
```

## Nutzung

Die Anwendung bietet zwei Hauptfunktionen:

### 1. Batch-Analyse von CSV-Dateien

- Laden Sie eine CSV-Datei mit einer `text`-Spalte hoch
- Klicken Sie auf "Batch-Sentiment analysieren"
- Die Ergebnisse werden in einer Tabelle angezeigt
- Optional können Sie Themen extrahieren lassen
- Exportieren Sie die Ergebnisse als CSV-Datei

### 2. Manuelle Einzel-Analyse

- Geben Sie einen Text in das Textfeld ein
- Klicken Sie auf "Einzel-Sentiment analysieren"
- Das Ergebnis wird sofort angezeigt

Eine detaillierte Bedienungsanleitung finden Sie in der [Dokumentation](app_user_guide.md).

## Modelle

### Sentiment-Analyse

Für die Sentiment-Analyse wird das vortrainierte BERT-Modell `nlptown/bert-base-multilingual-uncased-sentiment` verwendet, das Texte auf einer Skala von 1-5 Sternen bewertet. Für lange Texte wird eine Chunking-Strategie implementiert.

### Themenmodellierung

Die Themenmodellierung verwendet Latent Dirichlet Allocation (LDA) aus scikit-learn, um häufige Themen in den Texten zu identifizieren. Die optimale Anzahl von Themen kann vom Benutzer festgelegt werden.

## Datenquellen

Die Anwendung kann Kundenfeedback aus verschiedenen Quellen verarbeiten:
- Google Reviews API
- CSV-Dateien mit Kundenbewertungen
- Umfrageergebnisse

Eine detaillierte Übersicht der Datenquellen finden Sie in der [Dateninventar-Tabelle](notebooks/data_inventory.xlsx).
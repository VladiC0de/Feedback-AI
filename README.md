Kundenfeedback-Analyse für KMU
1. Einleitung
Diese Anwendung ermöglicht kleinen und mittleren Unternehmen (KMU), Kundenfeedback automatisiert auszuwerten. Sie führt sowohl eine Sentiment-Analyse als auch eine Themen-/Keyword-Extraktion durch und visualisiert die Ergebnisse interaktiv in einer Web-App.

2. Zielsetzung
Zielgruppe: KMU ohne eigene Data-Science-Ressourcen
Funktionen:

Sentiment-Analyse (positiv, neutral, negativ)

Themen-/Schlagwort-Erkennung via LDA

Batch-Verarbeitung per CSV-Upload

Manuelle Einzel-Analyse

Download der Ergebnisse

3. Technologie-Stack
Programmiersprache: Python 3.11+

KI-Framework: Hugging Face Transformers

Themen-Modell: scikit-learn (CountVectorizer + LDA)

Web-Frontend: Streamlit

Datenvisualisierung: Plotly, seaborn (optional)

Datenhandling: pandas

4. Projektstruktur
feedback-ai/
├── app/ # Streamlit-App
│ └── main.py # Hauptskript
├── data/ # Beispieldaten & CSVs
├── model/ # (optional) persistierte Modelle
├── notebooks/ # Explorations-Notebooks
├── static/ # Style-Guidelines, Bilder
├── requirements.txt # Python-Abhängigkeiten
└── README.md # Diese Dokumentation

5. Installation
Repository klonen & Ordner wechseln
git clone <dein-repo-url>
cd feedback-ai

Virtuelle Umgebung anlegen & aktivieren
python3.11 -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\Activate.ps1 # Windows PowerShell

Abhängigkeiten installieren
pip install --upgrade pip
pip install -r requirements.txt

6. Nutzung
6.1 Start der App
streamlit run app/main.py
Öffne im Browser die angezeigte Adresse (meist http://localhost:8501).

6.2 CSV-Batch-Analyse
Unter „CSV-Datei hochladen“ eine .csv mit Spalte text auswählen.

Vorschau ansehen.

Auf „Batch-Sentiment analysieren“ klicken.

Nach kurzer Analyse:

Tabelle mit Spalten text, stimmung, score anzeigen

Download-Button für sentiment_results.csv

Optional: Checkbox „Themen extrahieren“ aktiviert LDA-Topics

6.3 Manuelle Einzel-Analyse
Unter „Manuelle Einzel-Analyse“ freien Text eingeben.

Auf „Einzel-Sentiment analysieren“ klicken.

Ergebnis (Label + Score) erscheint direkt darunter.

7. Dateninventar
Alle verwendeten Datensätze sind in notebooks/data_inventory.xlsx dokumentiert:
Name | Format | Datenmenge | Qualität
customer_reviews.csv | CSV | ca. 120 Zeilen | synthetisch / Demo-Daten
Google Reviews API | JSON | dynamisch | Original-Daten, teils umgangssprachlich
Umfrage-Export | CSV | variabel | manuell validiert

8. Bewertungskriterien (Modul 245)
Dateninventar (Name, Format, Menge, Qualität)

Modellarchitektur (Sentiment + LDA-Topic)

Interaktive Features (CSV-Upload, Spinner, Download)

Codequalität (Logging, Fehlerbehandlung, Caching)

Evaluierung (Accuracy/Metriken in Notebooks)

Style-Guidelines (UI-Farben, Layout, Responsivität)

Rechtliches (Datenlizenz, Modellquelle)

9. Lizenz & Rechtliches
Daten: öffentlich zugänglich oder synthetisch generiert
Modell: nlptown/bert-base-multilingual-uncased-sentiment (Hugging Face)
Lizenz: MIT (oder anpassen)

© 2025 Vladyslav Astashyn, Tim Wolf – Feedback-AI für KMU
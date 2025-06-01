# Bedienungsanleitung: Feedback-AI

## Einführung

Feedback-AI ist eine benutzerfreundliche Anwendung zur Analyse von Kundenfeedback für kleine und mittlere Unternehmen (KMU). Die App ermöglicht es Ihnen, Kundenfeedback automatisch auf Stimmung (Sentiment) zu analysieren und häufige Themen zu identifizieren, ohne dass Sie eigene Data-Science-Ressourcen benötigen.

## Funktionen im Überblick

1. **Batch-Analyse von CSV-Dateien**: Laden Sie CSV-Dateien mit Kundenfeedback hoch und analysieren Sie alle Einträge auf einmal.
2. **Manuelle Einzel-Analyse**: Geben Sie einzelne Texte ein, um deren Stimmung sofort zu analysieren.
3. **Themenextraktion**: Identifizieren Sie die häufigsten Themen in Ihrem Kundenfeedback.
4. **Ergebnisexport**: Speichern Sie Ihre Analyseergebnisse als CSV-Datei.

## Schritt-für-Schritt Anleitung

### 1. Batch-Analyse von CSV-Dateien

1. **CSV-Datei vorbereiten**:
   - Stellen Sie sicher, dass Ihre CSV-Datei eine Spalte mit dem Namen `text` enthält.
   - Diese Spalte sollte das zu analysierende Kundenfeedback enthalten.
   - Weitere Spalten (z.B. `rating`, `date`, `source`) sind optional.

2. **Datei hochladen**:
   - Klicken Sie auf "Browse files" im Bereich "CSV-Datei hochladen".
   - Wählen Sie Ihre vorbereitete CSV-Datei aus.
   - Die App zeigt eine Vorschau der ersten 5 Einträge an.

3. **Analyse starten**:
   - Klicken Sie auf den Button "Batch-Sentiment analysieren".
   - Warten Sie, bis die Analyse abgeschlossen ist (dies kann je nach Datenmenge einige Zeit dauern).
   - Die Ergebnisse werden in einer Tabelle angezeigt, mit zwei neuen Spalten:
     - `stimmung`: Die erkannte Stimmung (1-5 stars)
     - `score`: Der Konfidenzwert der Analyse

4. **Ergebnisse exportieren**:
   - Klicken Sie auf "Ergebnisse als CSV herunterladen", um die Analyseergebnisse zu speichern.

5. **Themen extrahieren** (optional):
   - Aktivieren Sie das Kontrollkästchen "Themen extrahieren".
   - Wählen Sie mit dem Schieberegler die gewünschte Anzahl an Themen (2-10).
   - Die App zeigt die Top-10 Wörter für jedes identifizierte Thema an.

### 2. Manuelle Einzel-Analyse

1. **Text eingeben**:
   - Scrollen Sie zum Abschnitt "Manuelle Einzel-Analyse".
   - Geben Sie den zu analysierenden Text in das Textfeld ein.

2. **Analyse starten**:
   - Klicken Sie auf "Einzel-Sentiment analysieren".
   - Das Ergebnis wird sofort unter dem Button angezeigt:
     - `Stimmung`: Die erkannte Stimmung (1-5 stars)
     - `Score`: Der Konfidenzwert der Analyse

## Tipps zur Verwendung

- **Optimale Textlänge**: Das System kann Texte jeder Länge verarbeiten, aber für die besten Ergebnisse sollten die Texte mindestens einen vollständigen Satz enthalten.
- **Mehrsprachigkeit**: Die Anwendung unterstützt mehrere Sprachen, einschließlich Deutsch und Englisch.
- **Große Dateien**: Bei sehr großen CSV-Dateien (>1000 Einträge) kann die Analyse mehrere Minuten dauern.
- **Themenanzahl**: Experimentieren Sie mit verschiedenen Themenanzahlen, um die optimale Granularität für Ihre Daten zu finden.

## Fehlerbehebung

- **Encoding-Probleme**: Wenn Ihre CSV-Datei Sonderzeichen enthält, die nicht korrekt angezeigt werden, versuchen Sie, die Datei mit UTF-8-Encoding zu speichern.
- **Fehlende 'text'-Spalte**: Stellen Sie sicher, dass Ihre CSV-Datei eine Spalte mit genau dem Namen `text` enthält.
- **Lange Ladezeiten**: Bei großen Dateien oder komplexen Texten kann die Analyse länger dauern. Bitte haben Sie Geduld.

## Technischer Support

Bei Fragen oder Problemen mit der Anwendung wenden Sie sich bitte an den Support unter support@feedback-ai.example.com.

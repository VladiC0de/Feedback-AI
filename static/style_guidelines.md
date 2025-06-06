# Style-Guidelines für Feedback-AI

## Farbpalette

- **Primärfarbe**: #2c3e50 (Dunkelblau)
- **Sekundärfarbe**: #3498db (Hellblau)
- **Akzentfarbe**: #e74c3c (Rot)
- **Hintergrundfarbe**: #f8f9fa (Hellgrau)
- **Textfarbe**: #333333 (Dunkelgrau)

## Typografie

- **Überschriften**: Roboto, sans-serif
- **Fließtext**: Open Sans, sans-serif
- **Monospace**: Consolas, monospace

## Layout

- **Containerbreite**: Responsive, max. 1200px
- **Abstand**: 16px Grundeinheit
- **Rundungen**: 4px für Buttons und Karten

## Komponenten

### Buttons

- **Primär**: Sekundärfarbe mit weißem Text
- **Sekundär**: Transparent mit Sekundärfarbe als Rahmen und Text
- **Hover-Effekt**: Leichte Verdunkelung und Schatten

### Karten

- **Hintergrund**: Weiß
- **Rahmen**: 1px solid #ecf0f1
- **Schatten**: 0 2px 4px rgba(0, 0, 0, 0.1)

### Tabellen

- **Header**: Primärfarbe mit weißem Text
- **Zeilen**: Abwechselnd weiß und #ecf0f1
- **Hover-Effekt**: Leichte Blaufärbung

## Responsive Design

- **Breakpoints**:
  - Mobile: < 576px
  - Tablet: 576px - 992px
  - Desktop: > 992px

- **Mobile Anpassungen**:
  - Stapel-Layout statt Spalten
  - Größere Touch-Targets (min. 44px)
  - Reduzierte Abstände

  ### Hinweis zu Limitationen im CSS-Styling

Die visuelle Anpassung der Anwendung erfolgte über eine eigene Datei `static/style.css`, in der Farben, Layout und Komponentendesign definiert wurden. 

Dabei wurde bewusst auf eine konsistente Farbgebung mit den zentralen Farben der Anwendung (#3498db und #2c3e50) geachtet.

Bei einzelnen dynamisch generierten Komponenten – insbesondere dem Slider (BaseWeb-Komponente von Streamlit) – ließ sich die Farbe des aktiven Balkens trotz gezielter Selektoren nicht vollständig überschreiben. Die Ursache liegt in der Kombination aus dynamischen Klassennamen und Inline-Styles, die nicht zuverlässig per CSS übersteuerbar sind.

**Fazit:** Die Funktionalität und das visuelle Gesamtkonzept sind nicht beeinträchtigt. Die Entscheidung, diesen Punkt nicht weiter zu forcieren, basiert auf einem bewussten Abwägen zwischen Aufwand und Nutzen.

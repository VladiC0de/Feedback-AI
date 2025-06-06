from collections import Counter
import re

def extract_top_keywords(texts, top_n=10):
    all_text = " ".join(texts).lower()
    words = re.findall(r'\b\w{4,}\b', all_text)  # nur Wörter mit ≥4 Buchstaben
    stopwords = {
        "aber", "nicht", "mehr", "oder", "dass", "doch", "schon", "ganz",
        "auch", "wenn", "noch", "dann", "vom", "immer", "sich", "eher",
        "kann", "sehr", "sind", "für", "mit", "und", "der", "die", "das", "den", "dem", "ein", "eine", "einen", "auf"
    }
    filtered = [word for word in words if word not in stopwords]
    freq = Counter(filtered)
    return [word for word, _ in freq.most_common(top_n)]

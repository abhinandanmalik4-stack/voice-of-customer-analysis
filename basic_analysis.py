"""Beginner feedback analysis: explicit keyword rules, no API calls."""
import re
import pandas as pd

THEMES = {
    "Setup": ["setup", "onboarding", "installation", "configure"],
    "Pricing": ["price", "pricing", "expensive", "cost", "billing"],
    "Bugs": ["bug", "crash", "crashes", "broken", "error", "slow"],
    "Feature requests": ["wish", "feature", "missing", "integration", "export"],
}
POSITIVE = ["easy", "helpful", "excellent", "smooth", "great", "affordable", "reliable"]
NEGATIVE = ["difficult", "confusing", "expensive", "broken", "error", "slow", "poor", "crash", "crashes"]
SAMPLE_REVIEWS = [
    "The setup is easy and the guide is helpful.",
    "The pricing is expensive.",
    "The app crashes when I open a report.",
    "I wish there was a calendar integration.",
    "The onboarding process is confusing.",
    "Support is helpful but the app is slow.",
    "The product is reliable.",
    "The setup is not easy.",
    "I use this product every week.",
    "The export feature is great.",
]

def contains(text, word):
    """Word boundaries prevent 'cost' from matching an unrelated longer word."""
    return bool(re.search(r"\b" + re.escape(word) + r"\b", text))

def analyze_reviews(raw_text):
    """One line is one review; skip blanks and normalized duplicate reviews."""
    records = []
    seen = set()
    for line in raw_text.splitlines():
        review = " ".join(line.split())
        normalized = review.casefold()
        if not review or normalized in seen:
            continue
        seen.add(normalized)
        themes = [theme for theme, words in THEMES.items()
                  if any(contains(normalized, word) for word in words)]
        positive = [word for word in POSITIVE if contains(normalized, word)]
        negative = [word for word in NEGATIVE if contains(normalized, word)]
        for word in list(positive):
            if re.search(r"\b(?:not|never)\s+(?:very\s+)?" + re.escape(word) + r"\b", normalized):
                positive.remove(word)
                negative.append("not/never " + word)
        if positive and negative:
            sentiment = "Mixed"
        elif negative:
            sentiment = "Negative"
        elif positive:
            sentiment = "Positive"
        else:
            sentiment = "Neutral"
        records.append({
            "Review": review,
            "Themes": "; ".join(themes or ["Other"]),
            "Sentiment": sentiment,
            "Matched clues": ", ".join(positive + negative) or "No sentiment keywords",
        })
    if not records:
        raise ValueError("Enter at least one review.")
    return pd.DataFrame(records)

def count_themes(results):
    """A review can mention several themes, so counts can exceed review count."""
    return results["Themes"].str.split("; ").explode().value_counts().rename("Reviews")

import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest
from basic_analysis import analyze_reviews, count_themes

class BasicAnalysisTests(unittest.TestCase):
    def test_blank_rejected(self):
        with self.assertRaises(ValueError):
            analyze_reviews(" \n ")
    def test_duplicates(self):
        self.assertEqual(len(analyze_reviews("Great setup\n great   SETUP \n")), 1)
    def test_multiple_themes(self):
        result = analyze_reviews("Setup confusing and pricing expensive")
        self.assertEqual(result.iloc[0]["Themes"], "Setup; Pricing")
        self.assertEqual(count_themes(result).sum(), 2)
    def test_mixed_and_negated(self):
        result = analyze_reviews("Support helpful but app slow\nSetup is not easy")
        self.assertEqual(result["Sentiment"].tolist(), ["Mixed", "Negative"])
    def test_unknown_neutral(self):
        self.assertEqual(analyze_reviews("Used every week").iloc[0]["Sentiment"], "Neutral")
    def test_interface(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1]/"basic_app.py")).run(timeout=30)
        self.assertFalse(app.exception)
        next(b for b in app.button if b.label=="Analyze reviews").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, "10")
        app.text_area(key="review_text").set_value(" \n ")
        next(b for b in app.button if b.label=="Analyze reviews").click().run()
        self.assertFalse(app.exception)
        self.assertTrue(app.error)
        self.assertEqual(len(app.metric), 0)

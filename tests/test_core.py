import unittest
from unittest.mock import patch
import pandas as pd
from core import *

def row(id,text="Setup confusing",synthetic="true"):
    return {"review_id":id,"text":text,"source":"demo","source_url":"","is_synthetic":synthetic}
class CoreTests(unittest.TestCase):
    def test_negation(self):
        self.assertEqual(classify("The setup is not easy.")["sentiment"],"negative")
        self.assertEqual(classify("Setup is not easy but support is helpful.")["sentiment"],"mixed")
    def test_multilabel(self):
        self.assertEqual(set(classify("Setup confusing and pricing expensive")["themes"]),{"setup","pricing"})
    def test_deduplication(self):
        self.assertEqual(len(prepare_reviews(pd.DataFrame([row("1"),row("2","  setup confusing  ")]))),1)
    def test_provenance(self):
        with self.assertRaises(ValueError): prepare_reviews(pd.DataFrame([row("1",synthetic="false")]))
    def test_empty_and_duplicate_ids(self):
        with self.assertRaises(ValueError): prepare_reviews(pd.DataFrame([row("1","")]))
        with self.assertRaises(ValueError): prepare_reviews(pd.DataFrame([row("1"),row("1","Other")]))
    def test_summary(self):
        result=analyze(pd.DataFrame([row("1","Setup confusing and price expensive")]))
        stats=summary(result)
        self.assertEqual(stats.mentions.sum(),2)
        self.assertEqual(stats.negative_mentions.sum(),2)
    def test_invalid_ai_result(self):
        with patch("core.claude_json",return_value={"themes":["invalid"],"sentiment":"negative","reason":"x"}):
            with self.assertRaises(ValueError): analyze(pd.DataFrame([row("1")]),True)

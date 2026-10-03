import tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
import integrations
class UITests(unittest.TestCase):
    def test_analyze_and_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/"data").mkdir()
            (root/"data"/"sample_reviews.csv").write_bytes((integrations.ROOT/"data"/"sample_reviews.csv").read_bytes())
            with patch.object(integrations,"ROOT",root):
                app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/"app.py")).run(timeout=30)
                self.assertFalse(app.exception)
                app.button(key="analyze").click().run(timeout=30)
                self.assertFalse(app.exception)
                self.assertEqual(app.metric[0].value,"150")
                app.multiselect(key="sentiments").set_value(["negative"]).run()
                self.assertFalse(app.exception)
                self.assertGreater(int(app.metric[0].value),0)
                app.multiselect(key="themes").set_value([]).run()
                self.assertFalse(app.exception)
                self.assertEqual(app.metric[0].value,"0")

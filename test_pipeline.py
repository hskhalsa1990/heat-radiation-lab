import io, json, threading, time, unittest, urllib.request, urllib.error
from http.server import ThreadingHTTPServer
import numpy as np, pandas as pd
import data_clean, thermal, report

def sample():
    return pd.DataFrame({"material": ["brick ", "Brick", "Glass", "Glass", "Glass"], "temp_K": [500, 500, -999, 600, 700],
                         "emissivity": [.9, .9, .9, np.nan, 9.9], "area_m2": [1] * 5, "surr_K": [300] * 5})

class Cleaning(unittest.TestCase):
    def test_clean_removes_bad(self):
        d = data_clean.clean(sample())
        self.assertFalse(d[["temp_K", "emissivity"]].isna().any().any())
        self.assertTrue(d.emissivity.between(0, 1).all()); self.assertTrue((d.temp_K > 0).all())
    def test_dedupe_and_names(self):
        d = data_clean.clean(sample()); self.assertIn("Brick", set(d.material)); self.assertEqual((d.material == "Brick").sum(), 1)
    def test_missing_columns(self):
        with self.assertRaises(ValueError): data_clean.clean(pd.DataFrame({"a": [1]}))
    def test_flux_positive_when_hotter(self): self.assertTrue((data_clean.clean(sample()).flux_Wm2 > 0).all())

class Thermal(unittest.TestCase):
    def grid(self):
        y, x = np.mgrid[0:100, 0:100]; g = 300 + np.zeros((100, 100))
        for cx, cy in [(25, 25), (70, 60)]: g += 150 * np.exp(-((x - cx)**2 + (y - cy)**2) / 30)
        return g
    def test_two_spots(self): self.assertEqual(len(thermal.detect_hotspots(self.grid())[2]), 2)
    def test_uniform_no_spots(self): self.assertEqual(len(thermal.detect_hotspots(np.full((50, 50), 300.0))[2]), 0)
    def test_mapping_range(self):
        T = thermal.to_temperature(np.random.rand(10, 10), 290, 420); self.assertAlmostEqual(T.min(), 290); self.assertAlmostEqual(T.max(), 420)

class Report(unittest.TestCase):
    def test_pdf_bytes(self):
        d = data_clean.clean(pd.read_csv("emissivity_raw.csv")); buf = io.BytesIO()
        g = TestThermalGrid.grid(); report.build_report(d, buf, g, thermal.detect_hotspots(g)[2])
        self.assertTrue(buf.getvalue().startswith(b"%PDF")); self.assertGreater(len(buf.getvalue()), 10000)

class TestThermalGrid(Thermal):
    pass
TestThermalGrid = Thermal()

class Api(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from server import Handler
        cls.srv = ThreadingHTTPServer(("127.0.0.1", 8766), Handler); threading.Thread(target=cls.srv.serve_forever, daemon=True).start(); time.sleep(.3)
    @classmethod
    def tearDownClass(cls): cls.srv.shutdown()
    def get(self, p): return json.load(urllib.request.urlopen("http://127.0.0.1:8766" + p))
    def test_flux(self): self.assertAlmostEqual(self.get("/api/flux?e=0.8&T=800&Ts=300")["flux_Wm2"], 18213.24, places=1)
    def test_bad_input(self):
        with self.assertRaises(urllib.error.HTTPError) as c: self.get("/api/flux?e=5&T=800")
        self.assertEqual(c.exception.code, 400)

if __name__ == "__main__": unittest.main()

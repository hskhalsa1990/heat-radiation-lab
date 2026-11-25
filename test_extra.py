import unittest, numpy as np
import radiation_extra as x

class T(unittest.TestCase):
    def test_parallel_square(self): self.assertAlmostEqual(float(x.view_factor_parallel_rects(1, 1, 1)), 0.1998, places=3)
    def test_perp_square(self): self.assertAlmostEqual(float(x.view_factor_perp_rects(1, 1, 1)), 0.2000, places=3)
    def test_emissivity_range(self): self.assertTrue(0 < x.total_emissivity(3000) < 1)
    def test_emissivity_rises_with_T(self): self.assertGreater(x.total_emissivity(3000), x.total_emissivity(1000) * 0.5)
    def test_selective_beats_black(self):
        self.assertGreater(x.solar_collector_efficiency(600, .95, .1, 1000, 10), x.solar_collector_efficiency(600, .95, .95, 1000, 10))
    def test_stagnation_ordering(self): self.assertGreater(x.stagnation_temperature(.95, .1), x.stagnation_temperature(.95, .9))
    def test_satellite_range(self): self.assertTrue(200 < x.satellite_temperature(.3, .8, 1, 4) < 400)
    def test_gas(self): self.assertAlmostEqual(float(x.gas_emissivity(0, 1, 1)), 0)

if __name__ == "__main__": unittest.main()

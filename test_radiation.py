import unittest, numpy as np
import radiation as r

class T(unittest.TestCase):
    def test_flux_zero_at_equilibrium(self): self.assertAlmostEqual(float(r.net_flux(.8, 300, 300)), 0)
    def test_flux_value(self): self.assertAlmostEqual(float(r.net_flux(1, 100, 0)), 5.670374419, places=6)
    def test_wien_sun(self): self.assertAlmostEqual(float(r.wien_peak(5778)) * 1e9, 501.5, delta=.5)
    def test_view_factor_range(self): self.assertTrue(0 < r.view_factor_parallel_discs(1, 1, 1) < 1)
    def test_shields_reduce_flux(self):
        self.assertLess(r.shield_flux(.8, .8, .1, 600, 300, 2), r.shield_flux(.8, .8, .1, 600, 300, 0))
    def test_cooling_monotonic(self):
        t, T = r.cooling_curve(1000, 300, .9, 1, 10, 500, 500, 5); self.assertTrue(np.all(np.diff(T) <= 0))
    def test_exchange_sign(self): self.assertGreater(r.exchange_two_surfaces(.8, .8, 1, 1, 500, 300), 0)

if __name__ == "__main__": unittest.main()

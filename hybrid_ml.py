"""Hybrid physics+ML with uncertainty (runs without torch).
Baseline = physics using the MATERIAL-MEAN emissivity; GradientBoosting learns the residual.
Uncertainty: RandomForest tree spread + split-conformal 90% intervals."""
import numpy as np, pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from radiation import net_flux

d = pd.read_csv("emissivity_clean.csv")
d["e_mat"] = d.groupby("material").emissivity.transform("mean")
d["base"] = net_flux(d.e_mat, d.temp_K, d.surr_K)
F = ["temp_K", "e_mat", "surr_K", "base"]
tr, te = train_test_split(d, test_size=.3, random_state=0)
tr, cal = train_test_split(tr, test_size=.3, random_state=0)

gb = GradientBoostingRegressor(random_state=0).fit(tr[F], tr.flux_Wm2 - tr.base)
pred = lambda x: x.base + gb.predict(x[F])
print("R2 physics baseline : %.4f" % r2_score(te.flux_Wm2, te.base))
print("R2 hybrid (phys+ML) : %.4f" % r2_score(te.flux_Wm2, pred(te)))

q = np.quantile(np.abs(cal.flux_Wm2 - pred(cal)), 0.9)
cover = np.mean(np.abs(te.flux_Wm2 - pred(te)) <= q)
print("Conformal 90%% interval: +/- %.0f W/m2, empirical coverage %.1f%%" % (q, 100 * cover))

rf = RandomForestRegressor(200, random_state=0).fit(tr[F[:3]], tr.flux_Wm2)
spread = np.std([t.predict(te[F[:3]].values) for t in rf.estimators_], axis=0)
print("RF ensemble spread: mean %.0f W/m2 (higher = less certain)" % spread.mean())

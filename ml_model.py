"""Machine learning: predict flux from features (scikit-learn)."""
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

d = pd.read_csv("emissivity_clean.csv")
X, y = d[["temp_K", "emissivity", "surr_K"]], d["flux_Wm2"]
Xt, Xv, yt, yv = train_test_split(X, y, test_size=.25, random_state=0)
m = RandomForestRegressor(200, random_state=0).fit(Xt, yt)
p = m.predict(Xv)
print("RandomForest R2=%.4f MAE=%.1f W/m2" % (r2_score(yv, p), mean_absolute_error(yv, p)))
print(dict(zip(X.columns, m.feature_importances_.round(3))))

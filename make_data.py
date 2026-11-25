"""Generate a deliberately dirty emissivity dataset."""
import numpy as np, pandas as pd
rng = np.random.default_rng(42)
mats = {"Polished aluminium":0.05,"Oxidised steel":0.79,"Black paint":0.96,"Concrete":0.92,
        "Copper polished":0.03,"Brick":0.93,"Glass":0.90,"Human skin":0.98,"Water":0.96,"Asphalt":0.93}
rows = []
for i in range(300):
    m = rng.choice(list(mats))
    e = mats[m] + rng.normal(0, 0.02)
    T = rng.uniform(300, 1200)
    rows.append({"material": m, "temp_K": round(T, 1), "emissivity": round(e, 3),
                 "area_m2": round(rng.uniform(0.1, 5), 2), "surr_K": 300})
df = pd.DataFrame(rows)
df.loc[rng.choice(300, 12), "emissivity"] = np.nan
df.loc[rng.choice(300, 6), "temp_K"] = -999
df.loc[rng.choice(300, 5), "emissivity"] = 9.9
df["material"] = df["material"].str.upper().where(rng.random(300) < .2, df["material"])
df = pd.concat([df, df.iloc[:8]])
df.to_csv("emissivity_raw.csv", index=False)
print("raw rows:", len(df))

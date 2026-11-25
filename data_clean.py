"""Data cleaning with pandas."""
import numpy as np, pandas as pd
from radiation import net_flux

REQUIRED = ["material", "temp_K", "emissivity", "area_m2", "surr_K"]

def clean(src="emissivity_raw.csv"):
    """src: CSV path or DataFrame with the REQUIRED columns."""
    df = (pd.read_csv(src) if isinstance(src, str) else src.copy())
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing: raise ValueError(f"missing columns: {missing}")
    df["material"] = df["material"].astype(str).str.strip().str.capitalize()
    df = df.drop_duplicates()
    df.loc[df["temp_K"] <= 0, "temp_K"] = np.nan
    df.loc[~df["emissivity"].between(0, 1), "emissivity"] = np.nan
    df["emissivity"] = df.groupby("material")["emissivity"].transform(lambda s: s.fillna(s.median()))
    df = df.dropna(subset=["temp_K", "emissivity"])
    df["flux_Wm2"] = net_flux(df["emissivity"], df["temp_K"], df["surr_K"])
    df["power_W"] = df["flux_Wm2"] * df["area_m2"]
    return df.reset_index(drop=True)

if __name__ == "__main__":
    d = clean(); d.to_csv("emissivity_clean.csv", index=False)
    print("clean rows:", len(d))

"""Data analyst report: summaries and comparison tables."""
import pandas as pd

def comparison(df):
    t = df.groupby("material").agg(n=("power_W", "size"), emissivity=("emissivity", "mean"),
        mean_flux=("flux_Wm2", "mean"), mean_power=("power_W", "mean"),
        max_power=("power_W", "max")).round(2).sort_values("mean_flux", ascending=False)
    return t

if __name__ == "__main__":
    df = pd.read_csv("emissivity_clean.csv")
    t = comparison(df)
    t.to_csv("comparison_table.csv")
    with open("comparison_table.md", "w") as f:
        f.write(t.reset_index().to_markdown(index=False) if hasattr(t, "to_markdown") else t.to_string())
    print(t)

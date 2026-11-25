"""PDF report (matplotlib only). CLI: python3 report.py [out.pdf]"""
import sys, io
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from radiation import net_flux, planck, wien_peak

def build_report(df, out, thermal_T=None, spots=None, title="Heat Radiation Report"):
    """df: cleaned dataframe (needs flux_Wm2, power_W). out: path or file-like. thermal_T: optional temperature grid."""
    with PdfPages(out) as pdf:
        fig = plt.figure(figsize=(8.27, 11.69)); fig.text(.5, .92, title, ha="center", fontsize=20, weight="bold")
        fig.text(.5, .88, "Author: Harpreet Singh | synthetic/user data - idealised grey-body physics", ha="center", fontsize=9)
        lines = [f"Rows analysed: {len(df)}", f"Materials: {df.material.nunique()}",
                 f"Temperature range: {df.temp_K.min():.0f}-{df.temp_K.max():.0f} K",
                 f"Mean net flux: {df.flux_Wm2.mean():,.0f} W/m2", f"Max net power: {df.power_W.max():,.0f} W",
                 "", "Notes: not for safety-critical design; verify emissivities against measured sources."]
        fig.text(.1, .8, "\n".join(lines), va="top", fontsize=11); pdf.savefig(fig); plt.close(fig)

        t = df.groupby("material").agg(n=("power_W", "size"), emissivity=("emissivity", "mean"),
            mean_flux=("flux_Wm2", "mean"), mean_power=("power_W", "mean")).round(2).sort_values("mean_flux", ascending=False)
        fig, ax = plt.subplots(figsize=(8.27, 11.69)); ax.axis("off"); ax.set_title("Material comparison", fontsize=14)
        tb = ax.table(cellText=t.reset_index().values, colLabels=["material", *t.columns], loc="upper center", cellLoc="center")
        tb.auto_set_font_size(False); tb.set_fontsize(8); tb.scale(1, 1.5); pdf.savefig(fig); plt.close(fig)

        fig, ax = plt.subplots(2, 2, figsize=(8.27, 11.69))
        t.mean_flux.sort_values().plot.barh(ax=ax[0, 0], color="darkorange", title="Mean flux (W/m2)")
        sc = ax[0, 1].scatter(df.temp_K, df.flux_Wm2 / 1e3, c=df.emissivity, s=8, cmap="viridis"); ax[0, 1].set_title("Flux vs T (kW/m2)")
        fig.colorbar(sc, ax=ax[0, 1]); wl = np.linspace(.1e-6, 20e-6, 400)
        for T in (500, 1000, 3000, 5778): ax[1, 0].plot(wl * 1e6, planck(wl, T), label=f"{T} K")
        ax[1, 0].set_yscale("log"); ax[1, 0].set_ylim(1e6, None); ax[1, 0].legend(fontsize=7); ax[1, 0].set_title("Planck curves")
        ax[1, 1].hist(df.emissivity, bins=20, color="teal"); ax[1, 1].set_title("Emissivity distribution")
        fig.tight_layout(); pdf.savefig(fig); plt.close(fig)

        if thermal_T is not None:
            fig, ax = plt.subplots(1, 2, figsize=(11.69, 5.5)); im = ax[0].imshow(thermal_T, cmap="inferno"); fig.colorbar(im, ax=ax[0], label="K")
            ax[0].set_title("Thermal image"); ax[0].axis("off")
            im2 = ax[1].imshow(net_flux(.9, thermal_T, 300) / 1e3, cmap="magma"); fig.colorbar(im2, ax=ax[1], label="kW/m2")
            ax[1].set_title("Radiated flux (e=0.9, surroundings 300 K)"); ax[1].axis("off")
            for i, s in enumerate(spots or [], 1): ax[0].annotate(str(i), (s["x"], s["y"]), color="cyan", fontsize=9)
            txt = "\n".join(f"{i}. ({s['x']},{s['y']}) peak {s['peak_K']} K, area {s['area_px']} px" for i, s in enumerate(spots or [], 1)) or "No hot spots"
            fig.text(.05, .02, "Hot spots:\n" + txt, fontsize=8, va="bottom"); pdf.savefig(fig); plt.close(fig)

def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "heat_radiation_report.pdf"
    df = pd.read_csv("emissivity_clean.csv"); build_report(df, out); print("saved", out)

if __name__ == "__main__": main()

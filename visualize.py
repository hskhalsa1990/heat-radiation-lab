"""3D diagrams, graphs, charts."""
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from radiation import net_flux, planck, wien_peak

def surface_3d():
    T = np.linspace(300, 1500, 60); E = np.linspace(0.05, 1, 60)
    TT, EE = np.meshgrid(T, E)
    fig = plt.figure(figsize=(8, 6)); ax = fig.add_subplot(111, projection="3d")
    s = ax.plot_surface(TT, EE, net_flux(EE, TT, 300) / 1e3, cmap="inferno")
    ax.set_xlabel("T (K)"); ax.set_ylabel("Emissivity"); ax.set_zlabel("Flux (kW/m2)")
    ax.set_title("3D: net radiative flux"); fig.colorbar(s, shrink=.6)
    fig.savefig("fig_3d_flux_surface.png", dpi=130); plt.close(fig)

def planck_curves():
    wl = np.linspace(0.1e-6, 20e-6, 600)
    fig, ax = plt.subplots(figsize=(8, 5))
    for T in (500, 1000, 2000, 3000, 5778):
        ax.plot(wl * 1e6, planck(wl, T), label=f"{T} K")
        ax.scatter(wien_peak(T) * 1e6, planck(wien_peak(T), T), s=15, c="k")
    ax.set_yscale("log"); ax.set_ylim(1e6, None); ax.set_xlabel("Wavelength (um)")
    ax.set_ylabel("Spectral radiance"); ax.set_title("Planck curves + Wien peaks"); ax.legend()
    fig.savefig("fig_planck_curves.png", dpi=130); plt.close(fig)

def material_charts(df):
    g = df.groupby("material")["flux_Wm2"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(8, 5)); g.plot.barh(ax=ax, color="darkorange")
    ax.set_xlabel("Mean flux (W/m2)"); ax.set_title("Material comparison")
    fig.tight_layout(); fig.savefig("fig_material_bar.png", dpi=130); plt.close(fig)
    fig, ax = plt.subplots(figsize=(6, 6))
    p = df.groupby("material")["power_W"].sum()
    ax.pie(p, labels=p.index, autopct="%1.0f%%", textprops={"fontsize": 7})
    ax.set_title("Share of total radiated power")
    fig.savefig("fig_power_pie.png", dpi=130); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 5))
    sc = ax.scatter(df.temp_K, df.flux_Wm2 / 1e3, c=df.emissivity, cmap="viridis", s=14)
    fig.colorbar(sc, label="Emissivity"); ax.set_xlabel("T (K)"); ax.set_ylabel("Flux (kW/m2)")
    ax.set_title("Flux vs temperature")
    fig.savefig("fig_scatter.png", dpi=130); plt.close(fig)

if __name__ == "__main__":
    d = pd.read_csv("emissivity_clean.csv")
    surface_3d(); planck_curves(); material_charts(d); print("figures saved")

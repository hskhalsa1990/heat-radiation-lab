"""Generate all diagrams (flat PNG files). Run: python3 diagrams.py"""
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import radiation as r

def box(ax, x, y, w, h, text, c="#ffd9a0"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02", fc=c, ec="k"))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=8)

def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=12, color="k"))

def architecture():
    fig, ax = plt.subplots(figsize=(11, 6)); ax.set_xlim(0, 11); ax.set_ylim(0, 6); ax.axis("off")
    box(ax, .2, 2.5, 1.8, 1, "make_data.py\nraw CSV", "#f4c2c2")
    box(ax, 2.5, 2.5, 1.8, 1, "data_clean.py\npandas", "#ffe5a0")
    box(ax, 4.8, 2.5, 1.8, 1, "analyst.py\ncomparison table", "#c8e6c9")
    for i, (t, c) in enumerate([("visualize.py\n3D + charts", "#bbdefb"), ("ml_model.py\nRandom Forest", "#d1c4e9"),
                                ("dl_model.py\nMLP", "#d1c4e9"), ("cv_thermal.py\nhot spots", "#b2dfdb")]):
        box(ax, 7.3, 4.6 - i*1.35, 1.9, .9, t, c); arrow(ax, 6.6, 3, 7.3, 5.05 - i*1.35)
    box(ax, 9.5, 2.5, 1.4, 1, "server.py\nJSON API", "#ffccbc"); arrow(ax, 6.6, 2.6, 9.5, 2.8)
    box(ax, 9.5, 0.6, 1.4, 1, "index.html\nnotebook", "#f0f4c3"); arrow(ax, 10.2, 2.5, 10.2, 1.6)
    arrow(ax, 2.0, 3, 2.5, 3); arrow(ax, 4.3, 3, 4.8, 3)
    box(ax, 2.5, 0.4, 4.1, .9, "radiation.py core physics (Stefan-Boltzmann, Planck, Wien, shields)", "#e1bee7")
    ax.set_title("Heat Radiation Lab - architecture"); fig.savefig("diagram_architecture.png", dpi=130, bbox_inches="tight"); plt.close(fig)

def cleaning_flow():
    steps = ["Load raw CSV", "Drop duplicates", "Fix material names", "Invalid T / emissivity -> NaN",
             "Median impute per material", "Drop remaining NaN", "Compute flux + power"]
    fig, ax = plt.subplots(figsize=(5, 9)); ax.set_xlim(0, 5); ax.set_ylim(0, len(steps) * 1.3); ax.axis("off")
    for i, s in enumerate(steps):
        y = (len(steps) - 1 - i) * 1.3; box(ax, .5, y, 4, .8, s, plt.cm.YlOrRd(.15 + .1 * i))
        if i: arrow(ax, 2.5, y + 1.3, 2.5, y + .8)
    ax.set_title("Data cleaning flow"); fig.savefig("diagram_cleaning_flow.png", dpi=130, bbox_inches="tight"); plt.close(fig)

def sphere_3d():
    u, v = np.mgrid[0:2*np.pi:60j, 0:np.pi:30j]
    X, Y, Z = np.cos(u)*np.sin(v), np.sin(u)*np.sin(v), np.cos(v)
    fig = plt.figure(figsize=(7, 7)); ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, facecolors=plt.cm.inferno(.5 + .5*Z), alpha=.9, linewidth=0)
    th, ph = np.meshgrid(np.linspace(0, np.pi, 9), np.linspace(0, 2*np.pi, 12))
    ax.quiver(1.0*np.sin(th)*np.cos(ph), 1.0*np.sin(th)*np.sin(ph), 1.0*np.cos(th),
              np.sin(th)*np.cos(ph), np.sin(th)*np.sin(ph), np.cos(th), length=.6, color="orange", linewidth=.6)
    ax.set_title("3D: sphere radiating (arrows = radiative flux)"); ax.set_axis_off()
    fig.savefig("diagram_3d_sphere.png", dpi=130); plt.close(fig)

def cooling_3d():
    fig = plt.figure(figsize=(8, 6)); ax = fig.add_subplot(111, projection="3d")
    for e in np.linspace(.1, 1, 10):
        t, T = r.cooling_curve(1000, 300, e, 1, 10, 500, 3000, 20)
        ax.plot(t / 60, np.full_like(t, e), T, color=plt.cm.plasma(e))
    ax.set_xlabel("Time (min)"); ax.set_ylabel("Emissivity"); ax.set_zlabel("T (K)")
    ax.set_title("3D: radiative cooling vs emissivity"); fig.savefig("diagram_3d_cooling.png", dpi=130); plt.close(fig)

def exchange_3d():
    E1, E2 = np.meshgrid(np.linspace(.05, 1, 50), np.linspace(.05, 1, 50))
    Q = r.exchange_two_surfaces(E1, E2, 1, 1, 600, 300)
    fig = plt.figure(figsize=(8, 6)); ax = fig.add_subplot(111, projection="3d")
    s = ax.plot_surface(E1, E2, Q, cmap="coolwarm"); fig.colorbar(s, shrink=.6)
    ax.set_xlabel("e1"); ax.set_ylabel("e2"); ax.set_zlabel("Q (W)"); ax.set_title("3D: exchange between two surfaces")
    fig.savefig("diagram_3d_exchange.png", dpi=130); plt.close(fig)

def em_spectrum():
    fig, ax = plt.subplots(figsize=(11, 4)); bands = [("Gamma", -13, -11), ("X-ray", -11, -8), ("UV", -8, -7), ("Visible", -7, -6.3),
        ("Infrared", -6.3, -3), ("Microwave", -3, -1), ("Radio", -1, 3)]
    cols = ["#9575cd", "#7986cb", "#64b5f6", "#81c784", "#e57373", "#ffb74d", "#a1887f"]
    for (n, a, b), c in zip(bands, cols):
        ax.add_patch(Rectangle((a, 0), b - a, 1, fc=c, ec="k")); ax.text((a + b) / 2, .5, n, ha="center", fontsize=8, rotation=90 if b - a < 1 else 0)
    for name, T in [("Skin 310K", 310), ("Heater 1000K", 1000), ("Lamp 3000K", 3000), ("Sun 5778K", 5778)]:
        x = np.log10(r.wien_peak(T)); ax.annotate(name, (x, 1), (x, 1.5), ha="center", arrowprops=dict(arrowstyle="->"), fontsize=8)
    ax.set_xlim(-13, 3); ax.set_ylim(0, 2); ax.set_yticks([]); ax.set_xlabel("log10 wavelength (m)")
    ax.set_title("EM spectrum with Wien peaks"); fig.savefig("diagram_em_spectrum.png", dpi=130, bbox_inches="tight"); plt.close(fig)

def shield_network():
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
    a = ax[0]; a.set_xlim(0, 10); a.set_ylim(0, 6); a.axis("off")
    for x, lab, c in [(1, "Hot plate\nT1", "#e53935"), (4, "Shield 1", "#90a4ae"), (6, "Shield 2", "#90a4ae"), (9, "Cold plate\nT2", "#1e88e5")]:
        a.add_patch(Rectangle((x - .15, .5), .3, 5, fc=c, ec="k")); a.text(x, .1, lab, ha="center", fontsize=8)
    for x1, x2 in [(1.2, 3.85), (4.2, 5.8), (6.2, 8.85)]:
        for y in (2, 3, 4): arrow(a, x1, y, x2, y)
    a.set_title("Parallel plates with 2 radiation shields")
    b = ax[1]; n = np.arange(0, 11)
    for es in (.05, .1, .3, .8): b.plot(n, r.shield_flux(.8, .8, es, 600, 300, n), marker="o", label=f"shield e={es}")
    b.set_yscale("log"); b.set_xlabel("Number of shields"); b.set_ylabel("Flux (W/m2)"); b.legend(); b.set_title("Shield effectiveness")
    fig.savefig("diagram_shield_network.png", dpi=130, bbox_inches="tight"); plt.close(fig)

def view_factor_map():
    R1, D = np.meshgrid(np.linspace(.2, 3, 60), np.linspace(.2, 3, 60))
    F = r.view_factor_parallel_discs(R1, R1, D)
    fig, ax = plt.subplots(figsize=(6.5, 5)); im = ax.pcolormesh(R1, D, F, cmap="viridis", shading="auto")
    fig.colorbar(im, label="F12"); ax.set_xlabel("Disc radius"); ax.set_ylabel("Separation d")
    ax.set_title("View factor, equal coaxial discs"); fig.savefig("diagram_view_factor.png", dpi=130); plt.close(fig)

def corr_heatmap(df):
    c = df[["temp_K", "emissivity", "area_m2", "flux_Wm2", "power_W"]].corr()
    fig, ax = plt.subplots(figsize=(6, 5)); im = ax.imshow(c, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(c))); ax.set_xticklabels(c.columns, rotation=45); ax.set_yticks(range(len(c))); ax.set_yticklabels(c.columns)
    for i in range(len(c)):
        for j in range(len(c)): ax.text(j, i, f"{c.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
    fig.colorbar(im); ax.set_title("Correlation heatmap"); fig.tight_layout(); fig.savefig("diagram_correlation.png", dpi=130); plt.close(fig)

def radar(df):
    g = df.groupby("material").agg(e=("emissivity", "mean"), f=("flux_Wm2", "mean"), p=("power_W", "mean"), n=("power_W", "size"))
    g = (g - g.min()) / (g.max() - g.min()); labs = list(g.columns); ang = np.linspace(0, 2*np.pi, len(labs), endpoint=False).tolist(); ang += ang[:1]
    fig = plt.figure(figsize=(7, 7)); ax = fig.add_subplot(111, polar=True)
    for m in g.index[:5]:
        v = g.loc[m].tolist() + [g.loc[m].iloc[0]]; ax.plot(ang, v, label=m); ax.fill(ang, v, alpha=.1)
    ax.set_xticks(ang[:-1]); ax.set_xticklabels(["emissivity", "flux", "power", "samples"]); ax.legend(fontsize=7, loc="upper right", bbox_to_anchor=(1.3, 1.1))
    ax.set_title("Radar comparison (5 materials)"); fig.savefig("diagram_radar.png", dpi=130, bbox_inches="tight"); plt.close(fig)

if __name__ == "__main__":
    d = pd.read_csv("emissivity_clean.csv")
    for f in (architecture, cleaning_flow, sphere_3d, cooling_3d, exchange_3d, em_spectrum, shield_network, view_factor_map): f()
    corr_heatmap(d); radar(d); print("diagrams saved")

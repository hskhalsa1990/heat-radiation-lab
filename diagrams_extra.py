"""Diagrams for the extra physics. Run: python3 diagrams_extra.py"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import radiation_extra as x

def emissivity():
    wl = np.linspace(.3e-6, 20e-6, 400); fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for T in (500, 1000, 2000, 3000): ax[0].plot(wl*1e6, x.spectral_emissivity_metal(wl, T), label=f"{T} K")
    ax[0].set_xlabel("Wavelength (um)"); ax[0].set_ylabel("Spectral emissivity"); ax[0].legend(); ax[0].set_title("Hagen-Rubens metal")
    Ts = np.linspace(400, 3500, 40); ax[1].plot(Ts, [x.total_emissivity(t) for t in Ts], "r")
    ax[1].set_xlabel("T (K)"); ax[1].set_ylabel("Total emissivity"); ax[1].set_title("Emissivity rises with temperature")
    fig.tight_layout(); fig.savefig("diagram_emissivity_spectral.png", dpi=130); plt.close(fig)

def collector():
    Tc = np.linspace(300, 1500, 100); fig, ax = plt.subplots(figsize=(7, 5))
    for lab, eps, C in [("Black, C=1", .95, 1), ("Selective, C=1", .1, 1), ("Black, C=50", .95, 50), ("Selective, C=50", .1, 50)]:
        ax.plot(Tc, np.clip(x.solar_collector_efficiency(Tc, .95, eps, 1000, C), 0, 1), label=lab)
    ax.set_xlabel("Absorber T (K)"); ax.set_ylabel("Efficiency"); ax.legend(); ax.set_title("Solar collector efficiency")
    fig.savefig("diagram_solar_collector.png", dpi=130); plt.close(fig)

def satellite_3d():
    A, E = np.meshgrid(np.linspace(.1, 1, 40), np.linspace(.1, 1, 40))
    T = x.satellite_temperature(A, E, 1, 4)
    fig = plt.figure(figsize=(7, 5.5)); ax = fig.add_subplot(111, projection="3d")
    s = ax.plot_surface(A, E, T, cmap="turbo"); fig.colorbar(s, shrink=.6)
    ax.set_xlabel("Absorptivity"); ax.set_ylabel("Emissivity"); ax.set_zlabel("T (K)"); ax.set_title("3D: satellite equilibrium temperature")
    fig.savefig("diagram_3d_satellite.png", dpi=130); plt.close(fig)

def rect_view_factors():
    r = np.linspace(.2, 4, 60); R1, R2 = np.meshgrid(r, r); fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
    for a, F, t in [(ax[0], x.view_factor_parallel_rects(R1, R2, 1), "Parallel rectangles a/c, b/c"),
                    (ax[1], x.view_factor_perp_rects(R1, R2, 1), "Perpendicular rectangles w/l, h/l")]:
        im = a.pcolormesh(R1, R2, F, cmap="viridis", shading="auto"); fig.colorbar(im, ax=a); a.set_title(t)
    fig.tight_layout(); fig.savefig("diagram_view_factor_rects.png", dpi=130); plt.close(fig)

if __name__ == "__main__": emissivity(); collector(); satellite_3d(); rect_view_factors(); print("extra diagrams saved")

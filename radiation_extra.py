"""Extra physics: spectral/temperature-dependent emissivity, gas radiation, solar collector,
satellite balance, view factors for rectangles."""
import numpy as np
from radiation import SIGMA, planck

def spectral_emissivity_metal(wavelength_m, T, rho0=5.6e-8, alpha=4.5e-3):
    """Hagen-Rubens emissivity of a metal; resistivity grows with T (default ~tungsten)."""
    rho = rho0 * (1 + alpha * (np.asarray(T, float) - 293.0))
    x = rho / np.asarray(wavelength_m, float)
    return np.clip(0.365 * np.sqrt(x) - 0.0667 * x + 0.006 * x**1.5, 0, 1)

def total_emissivity(T, rho0=5.6e-8, alpha=4.5e-3):
    """Planck-weighted total emissivity of the metal model at temperature T."""
    wl = np.linspace(0.2e-6, 60e-6, 4000); B = planck(wl, T)
    return float(np.trapezoid(spectral_emissivity_metal(wl, T, rho0, alpha) * B, wl) / np.trapezoid(B, wl))

def gas_emissivity(k_per_atm_m, p_atm, L_m):
    """Grey-gas emissivity 1-exp(-kpL) (Beer-Lambert)."""
    return 1 - np.exp(-k_per_atm_m * p_atm * L_m)

def solar_collector_efficiency(Tc, alpha, eps, G=1000.0, C=1.0, Ta=300.0, U=3.0):
    """Efficiency = absorbed - radiative loss - convective loss, per concentrated flux C*G."""
    Tc = np.asarray(Tc, float)
    return alpha - (eps * SIGMA * (Tc**4 - Ta**4) + U * (Tc - Ta)) / (C * G)

def stagnation_temperature(alpha, eps, G=1000.0, C=1.0, Ta=300.0, U=3.0):
    lo, hi = Ta, 4000.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if solar_collector_efficiency(mid, alpha, eps, G, C, Ta, U) > 0: lo = mid
        else: hi = mid
    return (lo + hi) / 2

def satellite_temperature(alpha, eps, A_sun, A_rad, Q_int=0.0, S=1361.0, earth_ir=237.0, A_earth=0.0):
    """Equilibrium temperature (K) of an isothermal satellite."""
    q_in = alpha * S * A_sun + eps * earth_ir * A_earth + Q_int
    return (q_in / (eps * SIGMA * A_rad)) ** 0.25

def view_factor_parallel_rects(a, b, c):
    """F12 for identical, aligned parallel rectangles a x b separated by c."""
    X, Y = a / c, b / c; sx, sy = np.sqrt(1 + X**2), np.sqrt(1 + Y**2)
    t = np.log(np.sqrt((1 + X**2) * (1 + Y**2) / (1 + X**2 + Y**2)))
    return 2 / (np.pi * X * Y) * (t + X * sy * np.arctan(X / sy) + Y * sx * np.arctan(Y / sx)
                                  - X * np.arctan(X) - Y * np.arctan(Y))

def view_factor_perp_rects(w, h, l):
    """F12 for perpendicular rectangles sharing an edge of length l (w, h are the other sides)."""
    W, H = w / l, h / l; s = np.sqrt(H**2 + W**2)
    a = ((1 + W**2) * (1 + H**2)) / (1 + W**2 + H**2)
    b = (W**2 * (1 + W**2 + H**2) / ((1 + W**2) * (W**2 + H**2))) ** (W**2)
    c = (H**2 * (1 + H**2 + W**2) / ((1 + H**2) * (H**2 + W**2))) ** (H**2)
    return (W * np.arctan(1 / W) + H * np.arctan(1 / H) - s * np.arctan(1 / s)
            + 0.25 * np.log(a * b * c)) / (np.pi * W)

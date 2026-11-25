"""Core heat radiation physics (numpy only)."""
import numpy as np

SIGMA = 5.670374419e-8   # W/m^2K^4
H = 6.62607015e-34
C = 2.99792458e8
KB = 1.380649e-23
WIEN_B = 2.897771955e-3

def net_flux(emissivity, T, T_surr):
    """Net radiative flux (W/m^2) = e*sigma*(T^4 - Ts^4)."""
    return emissivity * SIGMA * (np.asarray(T, float) ** 4 - np.asarray(T_surr, float) ** 4)

def net_power(emissivity, area, T, T_surr):
    return net_flux(emissivity, T, T_surr) * area

def planck(wavelength_m, T):
    """Spectral radiance B(lambda,T) in W/(sr m^3)."""
    wl = np.asarray(wavelength_m, float)
    return (2 * H * C**2 / wl**5) / np.expm1(H * C / (wl * KB * T))

def wien_peak(T):
    """Peak wavelength in metres."""
    return WIEN_B / np.asarray(T, float)

def view_factor_parallel_discs(r1, r2, d):
    """View factor F12 for coaxial parallel discs."""
    R1, R2 = r1 / d, r2 / d
    S = 1 + (1 + R2**2) / R1**2
    return 0.5 * (S - np.sqrt(S**2 - 4 * (R2 / R1) ** 2))

if __name__ == "__main__":
    print("Flux 800K, e=0.8, surr 300K: %.1f W/m2" % net_flux(0.8, 800, 300))
    print("Wien peak at 5778K: %.0f nm" % (wien_peak(5778) * 1e9))
    print("F12 discs r=1,1,d=1: %.4f" % view_factor_parallel_discs(1, 1, 1))

def exchange_two_surfaces(e1, e2, A1, A2, T1, T2, F12=1.0):
    """Net radiative power (W) between two grey surfaces (resistance network)."""
    R = (1 - e1) / (e1 * A1) + 1 / (A1 * F12) + (1 - e2) / (e2 * A2)
    return SIGMA * (np.asarray(T1, float) ** 4 - np.asarray(T2, float) ** 4) / R

def shield_flux(e1, e2, es, T1, T2, n=0):
    """Flux (W/m^2) between parallel plates with n identical radiation shields."""
    return SIGMA * (T1**4 - T2**4) / ((1 / e1 + 1 / e2 - 1) + n * (2 / es - 1))

def cooling_curve(T0, T_surr, e, A, m, cp, t_end, dt=1.0):
    """Radiation-only cooling of a lumped body. Returns (t, T)."""
    t = np.arange(0, t_end + dt, dt); T = np.empty_like(t); T[0] = T0
    for i in range(1, len(t)):
        T[i] = T[i-1] - dt * e * SIGMA * A * (T[i-1]**4 - T_surr**4) / (m * cp)
    return t, T

def main():
    """Console entry point (pip install -e . -> `heat-radiation`)."""
    print("Flux 800K, e=0.8, surr 300K: %.1f W/m2" % net_flux(0.8, 800, 300))
    print("Wien peak at 5778K: %.0f nm" % (wien_peak(5778) * 1e9))

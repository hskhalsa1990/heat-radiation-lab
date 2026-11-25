"""Streamlit dashboard. Run: streamlit run streamlit_app.py"""
import os
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st
import radiation as r

st.set_page_config(page_title="Heat Radiation Lab", page_icon="🔥", layout="wide")
st.title("🔥 Heat Radiation Lab")
st.caption("Author: Harpreet Singh · synthetic data, idealised grey-body physics, not for safety-critical design")

@st.cache_data
def load():
    if not os.path.exists("emissivity_clean.csv"):
        import make_data, data_clean
        data_clean.clean().to_csv("emissivity_clean.csv", index=False)
    return pd.read_csv("emissivity_clean.csv")

df = load()
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Calculator", "Planck / Wien", "Materials", "Shields & cooling", "3D", "Upload & report"])

with tab1:
    c = st.columns(3)
    e = c[0].slider("Emissivity", 0.01, 1.0, 0.8, 0.01)
    T = c[1].slider("Surface T (K)", 250, 2000, 800)
    Ts = c[2].slider("Surroundings T (K)", 200, 1000, 300)
    A = st.number_input("Area (m²)", 0.01, 100.0, 1.0)
    f = float(r.net_flux(e, T, Ts))
    m = st.columns(3)
    m[0].metric("Net flux (W/m²)", f"{f:,.1f}"); m[1].metric("Net power (W)", f"{f*A:,.1f}")
    m[2].metric("Wien peak (nm)", f"{float(r.wien_peak(T))*1e9:,.0f}")
    if not (df.temp_K.min() <= T <= df.temp_K.max()):
        st.warning("Outside the dataset range used for ML/DL models; the physics formula still applies.")

with tab2:
    temps = st.multiselect("Temperatures (K)", [300, 500, 1000, 2000, 3000, 5778], [500, 1000, 3000, 5778])
    wl = np.linspace(.1e-6, 20e-6, 600); fig, ax = plt.subplots(figsize=(8, 4))
    for t in temps:
        ax.plot(wl*1e6, r.planck(wl, t), label=f"{t} K"); ax.scatter(r.wien_peak(t)*1e6, r.planck(r.wien_peak(t), t), c="k", s=12)
    ax.set_yscale("log"); ax.set_ylim(1e6, None); ax.set_xlabel("Wavelength (µm)"); ax.legend(); st.pyplot(fig)

with tab3:
    mats = st.multiselect("Materials", sorted(df.material.unique()), sorted(df.material.unique()))
    d = df[df.material.isin(mats)]
    t = d.groupby("material").agg(n=("power_W", "size"), emissivity=("emissivity", "mean"),
        mean_flux=("flux_Wm2", "mean"), mean_power=("power_W", "mean")).round(2).sort_values("mean_flux", ascending=False)
    st.dataframe(t, use_container_width=True); st.bar_chart(t["mean_flux"])
    st.scatter_chart(d, x="temp_K", y="flux_Wm2", color="emissivity")
    st.download_button("Download cleaned data (CSV)", d.to_csv(index=False), "emissivity_clean.csv")

with tab4:
    c = st.columns(2)
    with c[0]:
        es = st.slider("Shield emissivity", .02, .9, .1); n = np.arange(0, 11)
        fig, ax = plt.subplots(); ax.plot(n, r.shield_flux(.8, .8, es, 600, 300, n), "o-"); ax.set_yscale("log")
        ax.set_xlabel("Shields"); ax.set_ylabel("Flux (W/m²)"); st.pyplot(fig)
    with c[1]:
        ec = st.slider("Body emissivity", .05, 1.0, .9); T0 = st.slider("Initial T (K)", 400, 1500, 1000)
        tt, TT = r.cooling_curve(T0, 300, ec, 1, 10, 500, 3000, 10)
        fig, ax = plt.subplots(); ax.plot(tt/60, TT); ax.set_xlabel("min"); ax.set_ylabel("K"); st.pyplot(fig)

with tab5:
    Tg = np.linspace(300, 1500, 50); Eg = np.linspace(.05, 1, 50); TT, EE = np.meshgrid(Tg, Eg)
    fig = plt.figure(figsize=(7, 5)); ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(TT, EE, r.net_flux(EE, TT, 300)/1e3, cmap="inferno"); ax.set_xlabel("T (K)"); ax.set_ylabel("e"); ax.set_zlabel("kW/m²")
    st.pyplot(fig)
    if os.path.exists("diagram_architecture.png"): st.image("diagram_architecture.png", caption="Architecture")

with tab6:
    import io, data_clean, thermal, report
    st.subheader("1. Your data (CSV)")
    st.caption("Columns required: " + ", ".join(data_clean.REQUIRED))
    up = st.file_uploader("Upload CSV", type=["csv"], key="csv")
    work = df
    if up is not None:
        try:
            work = data_clean.clean(pd.read_csv(up)); st.success(f"Cleaned {len(work)} rows from your file.")
            st.dataframe(work.head(20), use_container_width=True)
        except Exception as ex:
            st.error(f"Could not use this file: {ex}")
    st.subheader("2. Thermal image (optional)")
    img_file = st.file_uploader("Upload thermal image (PNG/JPG greyscale/colour) or .csv temperature grid", type=["png", "jpg", "jpeg", "csv"], key="img")
    tmin, tmax = st.columns(2); t_min = tmin.number_input("Darkest pixel = (K)", 200.0, 1500.0, 290.0); t_max = tmax.number_input("Brightest pixel = (K)", 200.0, 3000.0, 420.0)
    ksig = st.slider("Hot-spot threshold (std above mean)", 1.0, 6.0, 3.0, 0.5)
    G, spots = None, None
    if img_file is not None:
        try:
            if img_file.name.lower().endswith(".csv"): G = np.loadtxt(img_file, delimiter=",")
            else: G = thermal.to_temperature(plt.imread(io.BytesIO(img_file.read())), t_min, t_max)
            mask, lab, spots = thermal.detect_hotspots(G, ksig)
            c = st.columns(2); fig, a = plt.subplots(); im = a.imshow(G, cmap="inferno"); fig.colorbar(im); a.set_title("Temperature (K)"); c[0].pyplot(fig)
            fig, a = plt.subplots(); a.imshow(mask, cmap="gray"); a.set_title(f"{len(spots)} hot spot(s)"); c[1].pyplot(fig)
            st.dataframe(pd.DataFrame(spots), use_container_width=True)
            st.caption("Greyscale-to-temperature mapping is linear and only as accurate as the range you enter. Thermal images of people raise privacy concerns: use with consent.")
        except Exception as ex:
            st.error(f"Could not read this image: {ex}")
    st.subheader("3. PDF report")
    buf = io.BytesIO(); report.build_report(work, buf, G, spots); st.download_button("Download PDF report", buf.getvalue(), "heat_radiation_report.pdf", "application/pdf")

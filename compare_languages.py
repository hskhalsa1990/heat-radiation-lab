"""Cross-language check + benchmark. Builds each available toolchain into a temp dir (no files left in the repo).
Run: python3 compare_languages.py [N]    (default N = 5,000,000)"""
import os, shutil, subprocess, sys, tempfile, time
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from radiation import net_flux

N = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000
tmp = tempfile.mkdtemp()
TS = np.arange(400, 1201, 200)
REF = [f"{t},{float(net_flux(.8, t, 300)):.3f}" for t in TS]
BENCH_REF = sum(float(net_flux(.8, 300.0 + (i % 900), 300.0)) for i in range(0, 900)) * (N // 900) \
    + sum(float(net_flux(.8, 300.0 + (i % 900), 300.0)) for i in range(N % 900))

def sh(cmd, **k): return subprocess.run(cmd, capture_output=True, text=True, timeout=600, **k)

def toolchains():
    """name -> (needed tools, build cmd or None, run cmd list)"""
    return {
        "C": (["gcc"], ["gcc", "-O2", "radiation.c", "-o", f"{tmp}/rc", "-lm"], [f"{tmp}/rc"]),
        "C++": (["g++"], ["g++", "-O2", "radiation.cpp", "-o", f"{tmp}/rcpp"], [f"{tmp}/rcpp"]),
        "Go": (["go"], ["go", "build", "-o", f"{tmp}/rgo", "radiation.go"], [f"{tmp}/rgo"]),
        "Rust": (["rustc"], ["rustc", "-O", "radiation.rs", "-o", f"{tmp}/rrs"], [f"{tmp}/rrs"]),
        "Java": (["javac", "java"], ["javac", "-d", tmp, "Radiation.java"], ["java", "-cp", tmp, "Radiation"]),
        "JavaScript": (["node"], None, ["node", "radiation.js"]),
        "TypeScript": (["tsc", "node"], ["tsc", "radiation.ts", "--outDir", f"{tmp}/ts"], ["node", f"{tmp}/ts/radiation.js"]),
        "R": (["Rscript"], None, ["Rscript", "radiation.R"]),
        "Bash/awk": (["awk"], None, ["bash", "radiation.sh"]),
    }

rows = []
for name, (tools, build, run) in toolchains().items():
    if not all(shutil.which(t) for t in tools):
        rows.append(dict(language=name, status="skipped (toolchain not installed)")); continue
    if build and sh(build).returncode != 0:
        rows.append(dict(language=name, status="build failed")); continue
    out = sh(run).stdout.split()
    ok = len(out) == len(REF) and all(abs(float(a.split(",")[1]) - float(b.split(",")[1])) < 0.01 for a, b in zip(out, REF))
    n = N // 10 if name in ("R", "Bash/awk") else N          # slow interpreters get a smaller N
    t0 = time.perf_counter(); res = sh(run + ["bench", str(n)]); dt = time.perf_counter() - t0
    try: chk = float(res.stdout.strip().split(",")[1])
    except Exception: chk = float("nan")
    ref = BENCH_REF if n == N else sum(float(net_flux(.8, 300.0 + (i % 900), 300.0)) for i in range(n))
    rows.append(dict(language=name, status="ok" if ok and abs(chk - ref) / ref < 1e-6 else "MISMATCH",
                     n_evals=n, seconds=round(dt, 3), evals_per_s=round(n / dt)))

# Python references (pure loop + numpy vectorised)
n_py = N // 10
t0 = time.perf_counter(); s = 0.0
for i in range(n_py): t = 300.0 + (i % 900); s += .8 * 5.670374419e-8 * ((t*t)**2 - (300.0*300.0)**2)
dt = time.perf_counter() - t0; rows.append(dict(language="Python (loop)", status="ok", n_evals=n_py, seconds=round(dt, 3), evals_per_s=round(n_py/dt)))
t0 = time.perf_counter(); T = 300.0 + (np.arange(N) % 900); s = float(net_flux(.8, T, 300.0).sum()); dt = time.perf_counter() - t0
rows.append(dict(language="Python (numpy)", status="ok" if abs(s - BENCH_REF) / BENCH_REF < 1e-9 else "MISMATCH", n_evals=N, seconds=round(dt, 3), evals_per_s=round(N/dt)))

df = pd.DataFrame(rows); df.to_csv("benchmark_results.csv", index=False)
open("benchmark_results.md", "w").write(df.to_markdown(index=False) + "\n\nSame arithmetic in every language; interpreters R, awk and pure-Python use N/10. Timings are machine-dependent.\n")
print(df.to_string(index=False))
d = df.dropna(subset=["evals_per_s"]).sort_values("evals_per_s")
if len(d):
    fig, ax = plt.subplots(figsize=(8, 5)); ax.barh(d.language, d.evals_per_s, color="darkorange"); ax.set_xscale("log")
    ax.set_xlabel("Evaluations per second (log)"); ax.set_title("Language benchmark: Stefan-Boltzmann flux")
    fig.tight_layout(); fig.savefig("diagram_benchmark.png", dpi=130)
shutil.rmtree(tmp, ignore_errors=True)

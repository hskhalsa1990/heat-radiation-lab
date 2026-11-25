# Heat Radiation Lab

Flat (no subfolders) thermal radiation project: Stefan-Boltzmann, Planck, Wien, view factors, spectral emissivity, solar collectors, satellites. Data cleaning, ML/DL/CV, 3D diagrams, Jupyter notebook, Streamlit dashboard, JSON API, PDF reports, and the same physics in 10 languages.

**Author:** Harpreet Singh | **License:** MIT

## Quick start
```bash
pip install -r requirements.txt
./radiation.sh all                  # full pipeline: data, charts, diagrams, tests, report, benchmark
streamlit run streamlit_app.py      # dashboard (upload CSV / thermal image, download PDF report)
jupyter notebook heat_radiation.ipynb
python3 server.py                   # JSON API + index.html on http://localhost:8000
```
Or `make help`, or Docker: `docker build -t heat-radiation . && docker run -p 8501:8501 heat-radiation`.
Install as a package: `pip install -e .` gives `heat-radiation` and `heat-radiation-report` commands (`pip install -e .[dashboard]` adds Streamlit).

## Files
| File | Purpose |
|---|---|
| radiation.py, radiation_extra.py | Core physics; spectral emissivity, gas radiation, solar collector, satellite, rectangle view factors |
| make_data.py, data_clean.py, analyst.py | Synthetic dirty data, pandas cleaning (accepts CSV or DataFrame), comparison tables |
| visualize.py, diagrams.py, diagrams_extra.py | Charts, 3D plots, architecture/flow/physics diagrams |
| ml_model.py, hybrid_ml.py, dl_model.py, torch_models.py | Random Forest; physics+ML hybrid with conformal intervals; numpy MLP; PyTorch PINN + CNN |
| cv_thermal.py, thermal.py | Hot-spot detection (demo, real image, shared helpers) |
| report.py | PDF report (matplotlib only) |
| streamlit_app.py, server.py, index.html | Dashboard, API, web page |
| heat_radiation.ipynb | Notebook: cleaning, AI ethics, ML/DL/CV, diagrams, full-stack, report, benchmark |
| compare_languages.py, benchmark_results.md/.csv | Cross-language correctness check + speed benchmark |
| radiation.c / .cpp / .go / .rs / Radiation.java / radiation.js / radiation.ts / radiation.R / radiation.sh | Same flux table and benchmark in each language |
| analysis.R | R analysis and boxplot |
| test_*.py | 25 unit tests: `python3 -m unittest discover -s . -p "test_*.py"` |
| pyproject.toml, Makefile, Dockerfile, requirements.txt | Packaging and tooling (no GitHub Actions) |
| AI_ETHICS.md, reference_emissivity.csv | Ethics notes; approximate handbook emissivities (NOT measurements) |

## Languages
All implementations print `T,flux` CSV by default and take `bench N` to print a checksum:
```bash
gcc -O2 radiation.c -o rc -lm && ./rc bench 5000000
g++ -O2 radiation.cpp -o rcpp && ./rcpp
go run radiation.go bench 5000000
rustc -O radiation.rs && ./radiation
javac Radiation.java && java Radiation
node radiation.js
npx tsc radiation.ts --outDir /tmp/ts && node /tmp/ts/radiation.js
Rscript radiation.R
./radiation.sh bench 1000000
python3 compare_languages.py        # builds in a temp dir, checks all against Python, writes benchmark files
```
Missing toolchains are skipped and reported.

## Real data and thermal images
- Data: any CSV with columns `material,temp_K,emissivity,area_m2,surr_K` (upload in the dashboard, or `data_clean.clean("file.csv")`).
- Thermal image: `python3 cv_thermal.py image.png 290 420` (greyscale mapped linearly to 290-420 K), or a .csv/.npy temperature grid. Thermal images of people raise privacy issues; see AI_ETHICS.md.

## Notes
Idealised grey-body physics; not for safety-critical design. Models are trained on synthetic data. Credits: Copyright (c) 2026 Harpreet Singh.

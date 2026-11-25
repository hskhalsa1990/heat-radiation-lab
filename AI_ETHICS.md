# AI Ethics Notes

- **Data provenance:** the dataset is synthetic (`make_data.py`), not measured. Never present results as real measurements.
- **Coverage bias:** only 10 materials, 300-1200 K. Models extrapolate poorly outside this range.
- **Transparency:** physics formula (Stefan-Boltzmann) is the ground truth; ML/DL models are approximations, shown with R2/MAE.
- **Safety:** do not use predictions for furnace, fire-safety or medical design without validated physics and expert review.
- **Privacy:** thermal imaging of people can identify or surveil; this project uses synthetic images only.
- **Cleaning honesty:** imputation (median per material) and removals are logged in the notebook.
- **Reproducibility:** fixed random seeds; all steps scripted.

Author: Harpreet Singh

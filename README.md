# TW Air Quality Mini

A focused data analysis project for exploring and cleaning air quality data.
Raw CSV files are kept in `data/raw/` (read-only originals), cleaned outputs go to
`data/processed/`, exploratory notebooks live in `notebooks/`, and generated
reports (HTML/PDF) are written to `reports/`. Source helpers in `src/` provide
reusable `load_csv` and `clean` functions used across notebooks and scripts.

## How to run

```bash
# 1. Create and activate the virtual environment
python -m venv .venv
source .venv/Scripts/activate   # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch JupyterLab
jupyter lab

# 4. Open notebooks/01_explore.ipynb and run all cells
```

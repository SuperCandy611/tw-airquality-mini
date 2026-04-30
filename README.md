# TW Air Quality Mini

Exploratory analysis of Taiwan EPA air quality monitoring station data (2025).

## Quick start

```bash
git clone https://github.com/SuperCandy611/tw-airquality-mini.git
cd tw-airquality-mini
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook notebooks/01_explore.ipynb
```

## Project structure

```
data/raw/       原始 CSV（不入 git）
notebooks/      探索性分析
src/            共用函數
reports/        產生的圖表與 HTML
```

## Notes

Raw CSVs in `data/raw/` are excluded from version control (`.gitignore`).
Download station CSV files from the [Taiwan EPA AQI open data portal](https://data.epa.gov.tw/en/dataset/aqx_p_02) and place them there before running the notebooks.

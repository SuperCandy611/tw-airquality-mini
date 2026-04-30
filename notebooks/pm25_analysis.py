import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

np.random.seed(42)

plt.rcParams["font.family"] = "Microsoft JhengHei"
plt.rcParams["axes.unicode_minus"] = False

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "raw"
REPORTS_DIR = ROOT / "reports"
HOUR_COLS = [f"{h:02d}" for h in range(24)]
STATIONS = ["中山", "古亭", "新店", "板橋"]
THRESHOLD = 35  # µg/m³ Taiwan daily standard

# ── Step 1: load & filter ─────────────────────────────────────────────────────
frames = []
for s in STATIONS:
    df = pd.read_csv(
        DATA_DIR / f"{s}_2025.csv",
        encoding="utf-8-sig",   # strip BOM
        usecols=["測站", "日期", "測項"] + HOUR_COLS,
    )
    frames.append(df[df["測項"] == "PM2.5"])

raw = pd.concat(frames, ignore_index=True)

# ── Step 2: melt → long, daily mean ──────────────────────────────────────────
long = raw.melt(
    id_vars=["測站", "日期"],
    value_vars=HOUR_COLS,
    var_name="hour",
    value_name="pm25",
)
long["pm25"] = pd.to_numeric(long["pm25"], errors="coerce")   # '#' → NaN
long["日期"] = pd.to_datetime(long["日期"])

daily = (
    long.groupby(["測站", "日期"])["pm25"]
    .mean()
    .reset_index(name="pm25_mean")
)

# ── Step 3: summary stats ─────────────────────────────────────────────────────
print(f"{'站點':<6} {'mean':>8} {'p95':>8} {'days>35':>10}")
print("-" * 38)
for s in STATIONS:
    vals = daily.loc[daily["測站"] == s, "pm25_mean"].dropna()
    print(
        f"{s:<6} "
        f"{vals.mean():>7.2f}  "
        f"{vals.quantile(0.95):>7.2f}  "
        f"{int((vals > THRESHOLD).sum()):>7d}"
    )

# ── Step 4: plot ──────────────────────────────────────────────────────────────
COLORS = ["#e07b39", "#4c8fbd", "#5aab61", "#9b6bbf"]

fig, ax = plt.subplots(figsize=(13, 5))

for s, color in zip(STATIONS, COLORS):
    subset = daily[daily["測站"] == s].sort_values("日期")
    ax.plot(subset["日期"], subset["pm25_mean"], linewidth=1.2,
            color=color, label=s, alpha=0.85)

ax.axhline(THRESHOLD, color="crimson", linewidth=1.2,
           linestyle="--", label=f"{THRESHOLD} µg/m³ 標準值")

ax.set_title("四站 PM2.5 日均值趨勢 (2025)", fontsize=14, pad=12)
ax.set_xlabel("日期", fontsize=11)
ax.set_ylabel("PM2.5 日均值 (µg/m³)", fontsize=11)
ax.legend(loc="upper right", fontsize=10, framealpha=0.85)
ax.set_xlim(daily["日期"].min(), daily["日期"].max())
ax.set_ylim(bottom=0)
ax.grid(axis="y", linestyle=":", linewidth=0.6, alpha=0.7)
fig.autofmt_xdate()
fig.tight_layout()

out = REPORTS_DIR / "pm25_compare.png"
fig.savefig(out, dpi=150)
print(f"\n圖檔已儲存：{out}")

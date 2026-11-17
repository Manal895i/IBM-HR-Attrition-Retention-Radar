# Retention Radar: IBM HR Attrition Analytics

An interactive dashboard and Power BI project that shows **who leaves, when, and why**, built on the IBM HR Analytics Employee Attrition dataset (1,470 employees, 35 fields).

**Live demo:** `https://<your-username>.github.io/IBM-HR-Attrition-Retention-Radar/` (enable GitHub Pages, see below)

![Dashboard overview](docs/images/overview.png)

## Features

- **Workforce dot-matrix.** All 1,470 employees drawn as dots. Leavers are highlighted, and filters dim everyone else.
- **Cross-filtering.** Click a department, job role, or chip and every chart updates with animated transitions.
- **Hot spots.** Automatically ranks the groups (30+ people) that leave most above the company average.
- **Drivers page.** Attrition by overtime, age, income, travel, marital status, satisfaction, plus a department x tenure heatmap.
- **Cost of attrition.** Adjustable replacement-cost slider turns leavers into an estimated dollar figure.
- **Risk simulator.** Describe an employee and get an estimated attrition risk, the factors driving it, and the effect of retention levers (stop overtime, raise pay, and so on).
- Dark mode, CSV export of the filtered view, keyboard-accessible, respects reduced-motion settings, responsive.
- **Power BI version** with ready-to-paste DAX in [`powerbi/DAX_Measures.dax`](powerbi/DAX_Measures.dax) and a [step-by-step build guide](powerbi/Power_BI_Build_Guide.md).

## Key findings (from this dataset)

| Finding | Number |
|---|---|
| Overall attrition | 16.1% (237 of 1,470) |
| Overtime vs no overtime | 30.5% vs 10.4% (about 2.9x) |
| Sales Representatives | 39.8% attrition, the highest role |
| Single vs divorced employees | 25.5% vs 10.1% |
| Frequent travellers vs non-travellers | 24.9% vs 8.0% |
| First 2 years at the company | 29.8% attrition |
| Monthly income under 3K | 28.6% attrition |

The simulator model (logistic regression, 80/20 hold-out) reaches **AUC 0.848**. It reports associations in a fictional dataset and must not be used for real employment decisions.

## Repository structure

```
.
├── README.md
├── LICENSE
├── requirements.txt
├── data/                 # original IBM CSVs + DATA_DICTIONARY.md
├── src/
│   ├── build_dashboard.py       # trains the model, generates docs/index.html
│   └── dashboard_template.html  # dashboard source (HTML, CSS, JS)
├── docs/
│   ├── index.html        # generated, self-contained dashboard (GitHub Pages)
│   └── images/           # put screenshots here
└── powerbi/
    ├── DAX_Measures.dax
    └── Power_BI_Build_Guide.md
```

## Quick start

```bash
pip install -r requirements.txt
python src/build_dashboard.py     # regenerates docs/index.html
```

Then open `docs/index.html` in a browser. No server needed.

## Publish on GitHub

```bash
git init
git add .
git commit -m "Add Retention Radar dashboard and Power BI project"
git branch -M main
git remote add origin https://github.com/<your-username>/IBM-HR-Attrition-Retention-Radar.git
git push -u origin main
```

Then go to **Settings → Pages**, choose **Deploy from a branch**, branch `main`, folder `/docs`. Your demo link appears after a minute.

## Power BI

1. Open Power BI Desktop and load `data/IBM-HR-Analytics-Employee-Attrition-and-Performance.csv`.
2. Follow [`powerbi/Power_BI_Build_Guide.md`](powerbi/Power_BI_Build_Guide.md).
3. Save as `powerbi/HR-Attrition-Dashboard.pbix` and add page screenshots to `docs/images/`.

## Tech

Python (pandas, numpy) for data prep and the model. Plain HTML, CSS and JavaScript for the dashboard, with no chart libraries. DAX for Power BI.

## License

MIT, see [LICENSE](LICENSE). The dataset is a hypothetical dataset created by IBM data scientists.

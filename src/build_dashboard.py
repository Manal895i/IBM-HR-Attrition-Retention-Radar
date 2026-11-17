"""Builds docs/index.html (self-contained dashboard) from the IBM HR CSV.
Also trains a small logistic-regression model (numpy only) for the risk simulator."""
import json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT/"data"/"IBM-HR-Analytics-Employee-Attrition-and-Performance.csv", encoding="utf-8-sig")
y = (df.Attrition == "Yes").astype(int).values

# ---------- model ----------
NAMES = ["Age","MonthlyIncome","YearsAtCompany","DistanceFromHome","NumCompaniesWorked","JobSatisfaction",
         "WorkLifeBalance","EnvironmentSatisfaction","StockOptionLevel","YearsSinceLastPromotion",
         "OverTime","FrequentTravel","Single"]
X = pd.DataFrame({n: df[n] for n in NAMES[:10]})
X["MonthlyIncome"] = np.log(df.MonthlyIncome)
X["OverTime"] = (df.OverTime == "Yes").astype(int)
X["FrequentTravel"] = (df.BusinessTravel == "Travel_Frequently").astype(int)
X["Single"] = (df.MaritalStatus == "Single").astype(int)
X = X[NAMES].values.astype(float)
mu, sd = X.mean(0), X.std(0); Z = (X-mu)/sd

def fit(idx, iters=4000, lr=0.3, l2=0.01):
    w, b = np.zeros(Z.shape[1]), 0.0
    for _ in range(iters):
        p = 1/(1+np.exp(-(Z[idx]@w+b))); e = p-y[idx]
        w -= lr*(Z[idx].T@e/len(idx)+l2*w); b -= lr*e.mean()
    return w, b

perm = np.random.default_rng(42).permutation(len(df)); te, tr = perm[:len(df)//5], perm[len(df)//5:]
w, b = fit(tr); s = pd.Series(Z[te]@w+b).rank()
yt = y[te]; npos, nneg = yt.sum(), (1-yt).sum()
auc = float((s[yt == 1].sum()-npos*(npos+1)/2)/(npos*nneg))
w, b = fit(np.arange(len(df)))
model = dict(names=NAMES, mean=mu.tolist(), std=sd.tolist(), w=w.tolist(), b=float(b), auc=round(auc, 3), base=float(y.mean()))

# ---------- dashboard rows ----------
sat = {1:"1 Low", 2:"2 Medium", 3:"3 High", 4:"4 Very High"}
d = pd.DataFrame({
 "Att": y, "Department": df.Department, "JobRole": df.JobRole, "OverTime": df.OverTime, "Gender": df.Gender,
 "AgeGroup": pd.cut(df.Age, [0,25,35,45,55,100], right=False, labels=["18-24","25-34","35-44","45-54","55+"]).astype(str),
 "IncomeBand": pd.cut(df.MonthlyIncome, [0,3000,6000,10000,1e9], right=False, labels=["1 Low (<3K)","2 Medium (3-6K)","3 High (6-10K)","4 Very High (10K+)"]).astype(str),
 "TenureBand": pd.cut(df.YearsAtCompany, [-1,2,5,10,100], labels=["1: 0-2 yrs","2: 3-5 yrs","3: 6-10 yrs","4: 11+ yrs"]).astype(str),
 "BusinessTravel": df.BusinessTravel.map({"Non-Travel":"Non-Travel","Travel_Rarely":"Travels rarely","Travel_Frequently":"Travels frequently"}),
 "MaritalStatus": df.MaritalStatus,
 "JobSatisfaction": df.JobSatisfaction.map(sat), "WorkLifeBalance": df.WorkLifeBalance.map(sat),
 "EnvironmentSatisfaction": df.EnvironmentSatisfaction.map(sat),
 "MonthlyIncome": df.MonthlyIncome, "YearsAtCompany": df.YearsAtCompany,
}).sort_values(["Department","Att"]).reset_index(drop=True)
payload = {"K": list(d.columns), "R": d.values.tolist(), "M": model}

tpl = (ROOT/"src"/"dashboard_template.html").read_text(encoding="utf-8")
(ROOT/"docs"/"index.html").write_text(tpl.replace("/*__DATA__*/null", json.dumps(payload, separators=(",", ":"))), encoding="utf-8")

print(f"rows={len(df)} left={y.sum()} rate={y.mean():.3f} AUC={auc:.3f}")
for k in ["OverTime","Department","JobRole","MaritalStatus","BusinessTravel","TenureBand","IncomeBand"]:
    print(k, d.groupby(k).Att.mean().round(3).sort_values(ascending=False).head(3).to_dict())
print(dict(zip(NAMES, np.round(w, 2))))

# Online Retail Analytics Platform

Platformë analitike për të dhëna të shitjeve retail — bazuar në datasetin
[Online Retail II (UCI)](https://archive.ics.uci.edu/dataset/502/online+retail+ii).

Për planin e plotë të projektit dhe ndarjen e punës, shih dokumentet në `docs/`.

## Struktura e projektit

```
online-retail-analytics/
├── data/
│   ├── raw/            # CSV/Excel origjinale, të pangarkuara në git (shih .gitignore)
│   └── processed/      # Dataset i pastruar (output i clean_data())
├── notebooks/
│   └── 01_data_exploration.ipynb   # Eksplorimi fillestar (Hapi 1.1)
├── src/
│   ├── data_cleaning.py            # clean_data(df) -> df_clean  (Hapi 1.2)
│   ├── analysis.py                 # Funksionet e EDA-s (Hapi 2.1)
│   ├── recommendation_engine.py    # generate_recommendations(df) (Hapi 2.2)
│   └── db_connector.py             # Lidhja me MongoDB (Hapi 4.1)
├── app/
│   └── app.py                      # Aplikacioni Streamlit (Faza 3)
├── docs/                           # Planet e projektit
├── tests/                          # Testet
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Përdorimi

**Notebook fillestar:**
```bash
jupyter notebook notebooks/01_data_exploration.ipynb
```

**Aplikacioni Streamlit** (kur të jetë ndërtuar, Faza 3):
```bash
streamlit run app/app.py
```

## Dataset

Dataseti "Online Retail II" nga UCI ngarkohet automatikisht online gjatë ekzekutimit të skripteve dhe notebooks, duke mos pasur nevojë të shkarkohet manualisht në dosjen `data/raw/`.
Burimi: https://archive.ics.uci.edu/dataset/502/online+retail+ii

## Statusi aktual

- [x] Struktura bazë e repos
- [ ] Hapi 1.1 — Eksplorimi fillestar i datasetit (Dev A)
- [ ] Hapi 1.2 — `clean_data()` (Dev A)
- [ ] Hapi 2.1 — EDA (Dev B)
- [ ] Hapi 2.2 — RFM + Motori i Rekomandimeve (Dev B)
- [ ] Faza 3 — Aplikacioni Streamlit (Dev C)
- [ ] Faza 4 — MongoDB (Dev D)

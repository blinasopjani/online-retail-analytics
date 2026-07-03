# Plani Hap-pas-Hapi i Ekzekutimit — Ndarja e Punës për 4 Zhvillues

**Projekti:** Online Retail Analytics Platform
**Ekipi:** 4 zhvillues (Dev A, Dev B, Dev C, Dev D)
**Qëllimi i këtij dokumenti:** Të tregojë me radhë **çfarë bëhet, kush e bën, dhe si lidhet me hapin pasardhës**, që projekti të ecë si zinxhir pa u bllokuar askush.

---

## 0. Ndarja e Roleve (fikse gjatë gjithë projektit)

| Rol | Përgjegjësia kryesore |
|-----|------------------------|
| **Dev A — Data Engineer** | Pastrimi i të dhënave, pipeline i përpunimit (pandas/numpy), funksionet e analizës bazë |
| **Dev B — Data Analyst / BI** | EDA e thelluar, RFM, KPI, motori i rekomandimeve, logjika e "what-if" |
| **Dev C — Frontend/Streamlit Developer** | Ndërtimi i aplikacionit Streamlit, dashboard, UI, integrimi i grafikëve |
| **Dev D — Backend/Database Engineer** | MongoDB (skema, lidhja, ruajtja e historikut), deployment, dokumentacioni teknik |

> Këto role nuk janë të izoluara — çdo person varet nga output-i i personit para vetes. Prandaj radhitja e hapave më poshtë është **kritike**.

---

## FAZA 1 — Themeli i të Dhënave (bazë për gjithçka tjetër)

### Hapi 1.1 — Marrja dhe eksplorimi fillestar i datasetit
**Kush:** Dev A
**Çfarë bën:**
- Shkarkon "Online Retail II" nga UCI.
- E hap me pandas, shikon strukturën, tipet e kolonave, vlerat mungesë, duplicates.
- Dokumenton problemet e gjetura (p.sh. `CustomerID` bosh, `Quantity` negative, `InvoiceNo` me "C").

**Output:** Një notebook `01_data_exploration.ipynb` + një listë me problemet e identifikuara.
**Lidhet me hapin tjetër:** Kjo listë problemesh është input direkt për 1.2 — pa e ditur çfarë është "e ndotur", nuk mund të pastrohet.

---

### Hapi 1.2 — Pastrimi dhe standardizimi i të dhënave
**Kush:** Dev A
**Çfarë bën:**
- Trajton `CustomerID` mungesë (i shënon si "Guest" ose i izolon në grup të veçantë).
- Vendos rregull për `Quantity` negative → i klasifikon si kthime/refunds, jo i fshin verbërisht.
- Filtron/analizon `UnitPrice <= 0`.
- Konverton `InvoiceDate` në format datetime.
- Krijon kolonën `Revenue = Quantity * UnitPrice`.
- E kthen gjithë procesin në **një funksion/script të ripërdorshëm**: `clean_data(df) -> df_clean`.

**Output:** `data_cleaning.py` (funksion i gatshëm) + dataset i pastruar (`.parquet` ose `.csv`).
**Lidhet me hapin tjetër:** Ky funksion `clean_data()` do të përdoret **dy herë**: një herë tani nga Dev B për EDA, dhe më vonë nga Dev C brenda Streamlit-it për çdo CSV të ri që klienti ngarkon. Prandaj duhet shkruar që në fillim si funksion i pastër, jo si kod i shpërndarë nëpër notebook.

> ⚠️ Pika kritike e ekipit: Dev A duhet ta japë `data_cleaning.py` te Dev B **dhe** Dev C njëkohësisht, sepse që të dy varen prej tij paralelisht që tani e tutje.

---

## FAZA 2 — Analiza (varet nga Faza 1)

### Hapi 2.1 — EDA e thelluar
**Kush:** Dev B (përdor `clean_data()` nga Dev A)
**Çfarë bën:**
- Analiza e shitjeve sipas kohës (mujore/javore/orare).
- Top produkte sipas sasisë dhe të ardhurave; produkte me shitje të ulëta.
- Analiza e fitimit/humbjes: të ardhura totale, humbje nga kthimet.
- Analiza gjeografike sipas `Country`.

**Output:** `02_eda_analysis.ipynb` me funksione të veçuara për çdo analizë (jo vetëm kod "inline"), p.sh. `get_monthly_revenue(df)`, `get_top_products(df)`.
**Lidhet me hapin tjetër:** Këto funksione do të thirren nga Dev C brenda Streamlit-it për t'i shfaqur si grafikë. Prandaj Dev B duhet t'i shkruajë si funksione që kthejnë DataFrame/dict, **jo** vetëm `print()` apo grafik i printuar direkt në notebook.

---

### Hapi 2.2 — Segmentimi RFM dhe motori i rekomandimeve
**Kush:** Dev B
**Çfarë bën:**
- Llogarit Recency, Frequency, Monetary për çdo klient.
- Ndan klientët në segmente (VIP, në rrezik, të rinj, etj.).
- Shkruan rregullat e rekomandimeve (rule-based): p.sh. nëse marzhi i produktit X është i ulët por volumi i lartë → sugjero rishikim çmimi.
- Për çdo rekomandim, llogarit një **vlerësim numerik të mundshëm të ndikimit në fitim** (formulë e thjeshtë bazuar në historikun e të dhënave).

**Output:** `recommendation_engine.py` me funksionin kryesor `generate_recommendations(df) -> list[dict]`.
**Lidhet me hapin tjetër:** Ky funksion është "truri" i seksionit të rekomandimeve dhe modulit "what-if" në Streamlit (Faza 3) dhe do të thirret drejtpërdrejt nga Dev C. Gjithashtu, rezultatet e tij do të ruhen nga Dev D në koleksionin `recommendations_log` (Faza 4).

---

### Hapi 2.3 — Vizualizimet dhe raporti fillestar
**Kush:** Dev B (me ndihmën e Dev A për të dhëna shtesë nëse duhen)
**Çfarë bën:**
- Krijon grafikët kryesorë me matplotlib/seaborn/plotly (trend mujor, top produkte, heatmap, RFM scatter).
- Përgatit një raport (PDF/Word) me gjetjet kryesore për klientin.

**Output:** Set grafikësh + raport `raporti_analizes.pdf`.
**Lidhet me hapin tjetër:** Vizualizimet plotly (jo matplotlib statike) do të riparaqiten drejtpërdrejt në Streamlit nga Dev C — prandaj preferohet plotly që nga fillimi për të shmangur rishkrimin.

---

## FAZA 3 — Aplikacioni Streamlit (varet nga Faza 1 + Faza 2)

### Hapi 3.1 — Skeleti i aplikacionit dhe upload CSV
**Kush:** Dev C
**Çfarë bën:**
- Krijon strukturën bazë të Streamlit-it (`app.py`, faqe/sections).
- Ndërton komponentin e upload-it të CSV.
- Thërret `clean_data()` (nga Dev A) automatikisht pas upload-it.
- Validim: krahason kolonat e CSV-së së re me formatin origjinal; shfaq mesazh gabimi nëse nuk përputhet.

**Output:** `app.py` funksional që pranon CSV dhe e pastron.
**Lidhet me hapin tjetër:** Pa këtë hap, asnjë analizë/grafik s'ka nga vjen — është "porta hyrëse" për gjithçka që vjen pas.

---

### Hapi 3.2 — Dashboard dhe integrimi i analizave
**Kush:** Dev C (përdor funksionet e Dev B nga Hapi 2.1)
**Çfarë bën:**
- Shfaq KPI kryesore (të ardhura totale, porosi, klientë aktivë, marzh).
- Integron grafikët plotly të krijuar nga Dev B.
- Ndërton seksionin e rekomandimeve duke thirrur `generate_recommendations()` (nga Dev B, Hapi 2.2).

**Output:** Dashboard interaktiv i plotë brenda `app.py`.
**Lidhet me hapin tjetër:** Ky dashboard tani është gati për t'u "ushqyer" me të dhëna historike nga MongoDB (Faza 4), dhe për të pritur modulin what-if (Faza 5).

---

## FAZA 4 — MongoDB (mund të fillojë paralelisht me Fazën 3, por lidhet në fund)

### Hapi 4.1 — Skema dhe lidhja fillestare
**Kush:** Dev D
**Çfarë bën:**
- Krijon databazën dhe 4 koleksionet: `raw_uploads`, `monthly_analytics`, `recommendations_log`, `kpi_history`.
- Shkruan funksionet e lidhjes (`db_connector.py`) me pymongo.

**Output:** `db_connector.py` + databaza gati (lokale ose Atlas).
**Shënim paralelizmi:** Dev D mund ta bëjë këtë **njëkohësisht** me Fazën 3, sepse nuk varet nga Streamlit-i — varet vetëm nga struktura e të dhënave që del nga Faza 1 dhe 2 (çfarë fushash do ruhen).

---

### Hapi 4.2 — Lidhja e MongoDB me Streamlit-in
**Kush:** Dev D + Dev C (së bashku)
**Çfarë bën:**
- Çdo herë që klienti bën upload CSV (Hapi 3.1), të dhënat e papërpunuara ruhen te `raw_uploads`.
- Rezultatet e analizës (KPI, agregime nga Hapi 2.1) ruhen te `monthly_analytics` dhe `kpi_history`.
- Rekomandimet e gjeneruara (Hapi 2.2) ruhen te `recommendations_log`.
- Shtohet seksioni "Krahasimi Historik" në dashboard, që lexon nga `kpi_history` dhe krahason muajin aktual me të mëparshmit.

**Output:** Streamlit + MongoDB plotësisht të lidhur; grafik krahasues muaj-me-muaj funksional.
**Lidhet me hapin tjetër:** Tani ekziston historik i vërtetë — pikë kritike që modulit what-if (Faza 5) t'i jepen të dhëna reale krahasimi, jo vetëm muaji aktual i izoluar.

---

## FAZA 5 — Moduli "What-if" (varet nga Faza 2.2 + Faza 4.2)

### Hapi 5.1 — Ndërtimi i simulimit të projeksionit të fitimit
**Kush:** Dev B (logjika) + Dev C (UI)
**Çfarë bën:**
- Dev B shkruan funksionin që merr një supozim (p.sh. "+10% retention klientë VIP") dhe kthen një projeksion fitimi bazuar në formulat/rregullat e Hapit 2.2 dhe historikun nga `kpi_history`.
- Dev C ndërton input-et në Streamlit (slider/input fusha) dhe shfaq rezultatin e projeksionit si grafik/numër.

**Output:** Seksion "What-if" funksional brenda dashboard-it.
**Lidhet me hapin tjetër:** Ky është hapi i fundit funksional — mbetet vetëm eksportimi dhe testimi.

---

### Hapi 5.2 — Eksportimi i raportit
**Kush:** Dev C (me template raporti nga Dev B, Hapi 2.3)
**Çfarë bën:**
- Buton në Streamlit që gjeneron PDF/Excel me KPI-të, grafikët kryesorë dhe rekomandimet e muajit aktual.

**Output:** Funksioni "Shkarko Raportin" në aplikacion.

---

## FAZA 6 — Testim, Integrim Final, Dorëzim

### Hapi 6.1 — Testim i integruar (të gjithë së bashku)
**Kush:** Dev A, B, C, D (secili teston pjesën e vet + testim i kryqëzuar)
**Çfarë bëhet:**
- Dev A teston pastrimin me 2-3 CSV muaj-provë me probleme të ndryshme (formate të gabuara, kolona mungesë).
- Dev B verifikon saktësinë e rekomandimeve dhe projeksioneve.
- Dev C teston rrjedhën e plotë të përdoruesit (upload → dashboard → rekomandime → what-if → export).
- Dev D verifikon që çdo upload/analizë ruhet saktë në MongoDB dhe se krahasimet historike janë korrekte.

**Output:** Listë gabimesh (bug list) dhe korrigjime.

---

### Hapi 6.2 — Dokumentimi dhe trajnimi i klientit
**Kush:** Dev D (koordinon), me kontribut nga të gjithë
**Çfarë bëhet:**
- Shkruhet udhëzuesi i përdorimit (si bëhet upload, si lexohen rekomandimet, si përdoret what-if).
- Përgatitet dokumentacioni teknik (arkitektura, skema MongoDB, si të mirëmbahet/zgjerohet aplikacioni).
- Sesion demonstrimi/trajnimi me klientin.

**Output:** Dokumentacion final + dorëzimi i projektit.

---

## Tabela Përmbledhëse e Varësive (Dependency Map)

| Hapi | Varet nga | Kush pret këtë output |
|------|-----------|--------------------------|
| 1.1 Eksplorim | — | 1.2 |
| 1.2 Pastrim (`clean_data()`) | 1.1 | 2.1, 3.1 |
| 2.1 EDA (funksione analize) | 1.2 | 3.2 |
| 2.2 RFM + Rekomandime | 1.2, 2.1 | 3.2, 4.2, 5.1 |
| 2.3 Vizualizime/Raport | 2.1 | 3.2, 5.2 |
| 3.1 Upload CSV (Streamlit) | 1.2 | 3.2, 4.2 |
| 3.2 Dashboard | 2.1, 2.2, 2.3, 3.1 | 4.2, 5.1 |
| 4.1 Skema MongoDB | (paralel, s'pret asgjë) | 4.2 |
| 4.2 Lidhja Streamlit–MongoDB | 3.1, 3.2, 4.1 | 5.1, 6.1 |
| 5.1 What-if | 2.2, 4.2 | 5.2, 6.1 |
| 5.2 Eksportim | 2.3, 5.1 | 6.1 |
| 6.1 Testim | Të gjitha më lart | 6.2 |
| 6.2 Dokumentim/Dorëzim | 6.1 | — |

---

## Rregulli i Artë i Koordinimit

1. **Dev A punon i pari** dhe jep `clean_data()` sa më shpejt — çdo vonesë këtu vonon të gjithë ekipin.
2. **Dev D mund të fillojë paralelisht** me skemën e MongoDB që në ditën e parë (nuk pret askënd), por lidhja reale (Hapi 4.2) pret Streamlit-in.
3. **Dev B dhe Dev C punojnë në "handoff" të vazhdueshëm**: çdo funksion analize që shkruan Dev B duhet menjëherë t'i kalohet Dev C si funksion i thirrshëm (jo si notebook i veçantë), përndryshe Dev C mbetet i bllokuar.
4. **Stand-up i shkurtër çdo ditë** (10-15 min) mes 4 zhvilluesve për të thënë: "çfarë përfundova, çfarë po pres nga dikush tjetër, a jam i bllokuar".

---

*Ky plan mund të përshtatet nëse ekipi vendos të punojë me sprint-e (p.sh. Scrum 1-javor) — struktura e varësive mbetet e njëjtë, ndryshon vetëm ritmi i dorëzimit.*

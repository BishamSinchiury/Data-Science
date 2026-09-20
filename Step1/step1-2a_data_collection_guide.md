# [Video](https://youtu.be/wybGoLqI2oU)
# [Video2](https://youtu.be/9uNOeFR6wnU)

# Data Science Project Guide: Data Collection & Wrangling

This is our running walkthrough of the project so far: gathering all four datasets (house prices, broadband speed, crime, and air quality), then loading, inspecting, and filtering them down to our 20 selected towns. Every step below says what we're doing and why we're doing it that way, so this doubles as a record we can lean on when writing up the report's methodology.

---

## Step 2: Data Collection

### Step 2.0 — Create the Assignment Report

**What:** Set up the report document (`assignment_report.docx`) before touching any data.

**Why:** We'll keep coming back to this file and building on it after every step, so we always have a finished, submittable document rather than scattered notes we'd have to assemble at the end under time pressure.

---

### Step 2.1 — Create a Kaggle Account

**What:** Sign up for a free [Kaggle](https://www.kaggle.com) account.

**Why:** Two of our four datasets are hosted on Kaggle (house prices, originally, and crime), so an account is needed before downloading either.

---

### Step 2.2 — House Price Data (HM Land Registry)

**What:** Originally downloaded from [UK Housing Prices Paid — HM Land Registry](https://www.kaggle.com/datasets/hm-land-registry/uk-housing-prices-paid) on Kaggle: one 770MB file, `price_paid_records.csv`, covering every property transaction in England and Wales since 1995, with columns including `Transaction unique identifier`, `Price`, `Date of Transfer`, `Property Type`, `Town/City`, `District`, `County`, and `PPD Category Type`.

**Why we changed this:** in practice, the single 770MB file caused file-access (`PermissionError`) issues when read directly from disk, and loading a file covering 1995–2024 was unnecessary anyway, since our other three datasets only cover 2021 onward. We switched to HM Land Registry's own **yearly** Price Paid Data files, published directly at [gov.uk/government/statistical-data-sets/price-paid-data-yearly-file](https://www.gov.uk/government/statistical-data-sets/price-paid-data-yearly-file). We downloaded four files — `pp-2021.csv`, `pp-2022.csv`, `pp-2023.csv`, `pp-2024.csv` — each 70–230MB, matching the date range of our other datasets. This is also a primary source rather than a Kaggle mirror, which strengthens our data provenance. The column schema and licence (Open Government Licence v3.0) are unchanged; these yearly files, like the original, have **no header row**.

```
Data/raw/
  pp-2021.csv
  pp-2022.csv
  pp-2023.csv
  pp-2024.csv
```

---

### Step 2.3 — Broadband Speed Data (Ofcom)

**What:** [Fixed performance local and unitary authority data (ZIP, 25.2 KB)](https://www.ofcom.org.uk/siteassets/resources/documents/research-and-data/multi-sector/infrastructure-research/connected-nations-2022/data-downloads/202205_fixed_laua_performance_r02.zip?v=194127), plus its [column reference PDF](https://www.ofcom.org.uk/siteassets/resources/documents/research-and-data/multi-sector/infrastructure-research/connected-nations-2022/data-downloads/about-this-data-fixed-performance-local-and-unitary-authority?v=328974).

**Why this file specifically:** it gives average broadband speeds **per local authority** — Kent's districts (Maidstone, Ashford, and so on) plus Monmouthshire — which lines up much better with our town-level analysis than raw postcode-level data would (that version runs to millions of messy rows). It's also small (25.2 KB), public, and needs no login.

**Limitation to carry into the report:** this data is a snapshot from May 2022 (the *Connected Nations 2022* report), not current broadband speeds.

```
Data/raw/
  202205_fixed_laua_performance_r02.csv
  about-this-data-broadband.pdf
```

---

### Step 2.4 — Crime Data (police.uk, via Kaggle)

**What:** [UK Police Data (Kaggle mirror of data.police.uk)](https://www.kaggle.com/datasets/mexwell/uk-police-data) — street-level crime records with columns `Crime ID`, `Month`, `Reported by`, `Falls within`, `Longitude`, `Latitude`, `Location`, `LSOA code`, `LSOA name`, `Crime type`, `Last outcome category`.

**Why a Kaggle mirror here (unlike house prices):** the official portal (data.police.uk) requires manually drawing a map area and downloading per force, which doesn't scale well to needing two forces across 36 months. The Kaggle mirror bundles the same underlying data into one download. We cite both the original data.police.uk source and the Kaggle access point in the report, for full provenance.

**Which police force each county needs:**

| County | Police force |
|---|---|
| Kent | Kent Police |
| Monmouthshire | Gwent Police (there's no separate "Monmouthshire Police") |

```
Data/raw/
  2021-06/
    2021-06-kent-street.csv
    2021-06-gwent-street.csv
    ... (plus outcomes / stop-and-search files we don't need)
  2021-07/
  ...
  2024-05/
```

**Why we don't filter this yet:** like the house price data, this covers far more of the country than we need (36 months × ~44 police forces × 3 file types). We filter it properly in Stage 2b below, once our Town/District reference mapping exists to filter against.

---

### Step 2.5 — Update the Report's Data Sources Section

**What:** Pause and write up each dataset's origin, licence, and known limitations in the report.

**Why now rather than at the end:** doing this while each dataset is fresh means we capture details (exact URLs, quirks noticed while downloading) accurately, rather than trying to reconstruct them later from memory.

---

### Step 2.6 — Air Quality Data (Defra) — Our Fourth Factor

**What:** [PM2.5 by Local Authority 2023 (CSV)](https://uk-air.defra.gov.uk/datastore/pcm/popwmpm252023byUKlocalauthority.csv), background reading at [Modelled background pollution data — DEFRA UK Air](https://uk-air.defra.gov.uk/data/pcm-data). Columns: `LA code`, `PM2.5 2023 (total)`, `PM2.5 2023 (non-anthropogenic)`, `PM2.5 2023 (anthropogenic)`, `Local Authority`. Note the file has **2 metadata rows above the real header row**.

**Why PM2.5 as our chosen fourth factor:** it's the pollutant most consistently linked to respiratory and cardiovascular harm, it's the same metric Defra itself uses for official mortality-burden estimates, and reliable, pre-aggregated, government-published data exists for every UK local authority — making it a defensible, policy-relevant choice rather than an arbitrary one.

**Limitation to carry into the report:** same granularity issue as broadband — local-authority-level, not individual-town level. This becomes an important, recurring thread once we build the Town → District mapping in Stage 2 (see below): several of our towns turn out to share a district, so this limitation affects more towns than it first appears to.

```
Data/raw/
  popwmpm252023byUKlocalauthority.csv
```

---

## Step 3: Data Wrangling — Stage 1: Load & Inspect

**What:** Before cleaning or filtering anything, we wrote `stage1_load_inspect.py` to load each of the four raw datasets and print out real column names, sample rows, and basic counts.

**Why this step exists on its own:** loading raw government/Kaggle data almost always surfaces small surprises — a missing header row, an unexpected delimiter, metadata rows before the real header, a column name that doesn't quite match documentation. Catching these in an inspection-only script, before writing any real filtering or cleaning logic, means we fix them once instead of debugging them halfway through a bigger script.

**What we found and fixed along the way:**
- House price yearly files have **no header row** — we name all 15 columns ourselves, matching HM Land Registry's official schema (including `PAON`, `SAON`, `Street`, `Locality`, which the single Kaggle file's truncated address format didn't include).
- The script's `Data/raw` path had to be built relative to the script's own file location (`Path(__file__).resolve().parent.parent`), since the script lives in `Step1/` but the data lives in a sibling `Data/` folder — a relative path only works if you always run the script from the same folder, which isn't reliable.
- The air quality file needed `skiprows=2` to skip its two metadata rows before the real header.
- The crime data's real outcome column is called `Last outcome category`, not `Outcome type` as first assumed — confirmed once we could see actual sample rows.

**Result:** confirmed 4,150,644 house price rows across 2021–2024 (119,432 in Kent, 6,945 in Monmouthshire), 374 local authorities in the broadband data, 361 in the air quality data, and all 36 monthly crime folders present with 14 distinct crime types.

---

## Step 3: Data Wrangling — Stage 2: Reference Data & Filtering

### Stage 2, Part 1 — Building the Town → District reference (`reference_towns.py`)

**What:** A single Python dictionary mapping each of our 20 selected towns to its real local authority District (or unitary authority) name, built from actual UK local government structure rather than guessed from town names.

**Why this had to be its own step, done carefully:** District names don't always match town names in an obvious way (Folkestone's district is "Folkestone and Hythe"; Tunbridge Wells' town name is "Royal Tunbridge Wells" but its district is "Tunbridge Wells"). More importantly, **several of our towns share the same District**:

| District | Towns in it |
|---|---|
| Medway | Chatham, Rochester, Gillingham |
| Thanet | Margate, Ramsgate |

This means our 20 towns actually correspond to only **13 unique districts**. Since broadband and air quality data is only available at District level, **Chatham, Rochester, and Gillingham will have identical broadband and air quality figures** — and the same is true for Margate and Ramsgate. This isn't a mistake in our data; it's a genuine structural fact about how these datasets are published, and it's worth stating explicitly in the report's limitations section rather than only in the code comments.

House prices and crime data don't have this problem, since they carry town-level or LSOA-level detail even within a shared District.

**Why we built this as a shared reference file rather than repeating the mapping in each filtering script:** if we ever need to correct a town-to-district mapping (for example, if Ofcom's data spells a district differently than we expect), we only need to fix it in one place, and every downstream script picks up the correction automatically.

### Stage 2, Part 2 — Grouping crime types (`reference_crime_groups.py`)

**What:** A mapping from the 14 raw `Crime type` values found in Stage 1 into three broader categories: **Violent**, **Property**, and **Other**.

**Why we grouped now rather than later:** 14 categories is too granular for a scoring system that needs one clean "crime" score per town. Grouping follows the same broad approach used in official UK crime statistics, so it's a defensible, recognisable grouping rather than an arbitrary one we invented. Doing this in Stage 2, alongside the town/district reference, means both pieces of "shared logic" live together before we write any actual filtering code that depends on them.

### Stage 2, Part 3 — Filtering house prices, broadband, and air quality (`stage2a_filter_prices_broadband_air.py`)

**What:** Filters all three District-matched datasets down to just our 13 selected districts, using the reference mapping above.

**Why house prices are read in chunks:** even filtered to four years instead of the full 1995–2024 range, each yearly file still has 800,000–1,300,000 rows. Reading the whole file into memory before filtering risks the same kind of resource problems we hit with the original single 770MB file. Reading in chunks of 200,000 rows, filtering each chunk, and only keeping the matching rows keeps memory use low throughout.

**Why the script prints WARNING lines for missing districts:** if a district name in our reference mapping doesn't exactly match the spelling used in the real Ofcom or Defra data (for example, an "&" instead of "and"), a silent filter would just quietly drop that entire town's data with no visible sign anything went wrong. Printing an explicit warning means a mismatch gets caught and fixed immediately, rather than surfacing much later as an unexplained gap in the exploratory analysis.

---

## Where We Should Be Now

- ✅ `assignment_report.docx` covers county/town selection, data sources (including the house-price source switch), and our fourth factor
- ✅ All four raw datasets sit in `Data/raw/`
- ✅ `stage1_load_inspect.py` runs cleanly, confirming real structure for all four datasets
- ✅ `reference_towns.py` and `reference_crime_groups.py` define the shared logic every later step depends on
- ✅ `stage2a_filter_prices_broadband_air.py` filters house prices, broadband, and air quality down to our 13 districts

**Next: Stage 2b — filtering crime.** We'll filter the 36 monthly folders down to just Kent Police and Gwent Police street-level files, apply the Violent / Property / Other grouping, and normalise crime counts per head of population so they're comparable between Kent's larger towns and Monmouthshire's smaller ones.

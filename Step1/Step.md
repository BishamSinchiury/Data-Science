# [Video](https://youtu.be/wybGoLqI2oU)
# [Video2](https://youtu.be/9uNOeFR6wnU)
# Step 2: Data Collection Guide

This is our walkthrough for gathering all four datasets needed for the housing recommendation project: house prices, broadband speed, crime, and air quality (our chosen fourth factor). We'll also set up the report document that ties everything together.

---

## Step 2.0 — Create the Assignment Report

Before we touch any data, we'll set up the report document (`assignment_report.docx`). This is the file we'll keep coming back to and building on after every step, so we always have a finished, submittable document rather than scattered notes.

---

## Step 2.1 — Create a Kaggle Account

We'll need a free [Kaggle](https://www.kaggle.com) account to download two of our four datasets. If you don't already have one, head over and sign up — it only takes a minute.

---

## Step 2.2 — House Price Data (HM Land Registry)

**Dataset:** [UK Housing Prices Paid — HM Land Registry](https://www.kaggle.com/datasets/hm-land-registry/uk-housing-prices-paid)

Here's what we'll do:

1. Open the link above and log in with the Kaggle account.
2. Click the **Download** button (top right). This pulls a `.zip` file (~770 MB), so we'll give it a minute or two to finish.
3. Inside, we'll find one file: `price_paid_records.csv`, with columns including:
   - `Transaction unique identifier`
   - `Price`
   - `Date of Transfer`
   - `Postcode`
   - `Property Type`
   - `Old/New`
   - `Duration`
   - `Town/City`
   - `District`
   - `County`
   - `PPD Category Type`
4. Once it's downloaded, we'll unzip it and move `price_paid_records.csv` into our data folder:

```
data-science-project/
  data/
    raw/
      price_paid_records.csv
```

**A note on this file:** it's huge, covering the whole of England and Wales since 1995 — millions of rows. We won't try to filter it manually in Excel; that would crash most spreadsheet software. Instead, we'll filter it down to just our Kent and Monmouthshire towns (and a sensible recent date range, e.g. the last 3–5 years) together in **Step 3: Data Wrangling**, using pandas.

---

## Step 2.3 — Broadband Speed Data (Ofcom)

**Dataset:** [Fixed performance local and unitary authority data (ZIP, 25.2 KB)](https://www.ofcom.org.uk/siteassets/resources/documents/research-and-data/multi-sector/infrastructure-research/connected-nations-2022/data-downloads/202205_fixed_laua_performance_r02.zip?v=194127)
**Column reference:** [About this data: Fixed performance local and unitary authority (PDF)](https://www.ofcom.org.uk/siteassets/resources/documents/research-and-data/multi-sector/infrastructure-research/connected-nations-2022/data-downloads/about-this-data-fixed-performance-local-and-unitary-authority?v=328974)

This file gives us average broadband speeds **per local authority** — Kent's districts (Maidstone, Ashford, and so on) plus Monmouthshire — which lines up much better with our town-level analysis than raw postcode-level data would (that version runs to millions of messy rows).

Here's what we'll do:

1. Click the first link above. It downloads a small `.zip` file (25.2 KB) instantly — no login required, since this is public open data.
2. We'll unzip it to get a CSV named something like `202205_fixed_laua_performance_r02.csv`.
3. Let's open it briefly and check it contains rows for local authorities like Maidstone, Ashford, Tunbridge Wells, and Monmouthshire (as a single unitary authority).
4. We'll also grab the second link — a short PDF explaining each column (download speed, upload speed, % superfast coverage, etc.). Worth skimming now, since we'll want it later for our report's data dictionary.
5. Both files go into our data folder:

```
data-science-project/
  data/
    raw/
      price_paid_records.csv
      202205_fixed_laua_performance_r02.csv
      about-this-data-broadband.pdf
```

**A note on this data:** it comes from the *Connected Nations 2022* report, so it reflects a snapshot from May 2022, not current broadband speeds. That's completely normal for coursework, but we'll flag it as a limitation/caveat in our report.

---

## Step 2.4 — Crime Data (police.uk, via Kaggle)

**Dataset:** [UK Police Data (Kaggle mirror of data.police.uk)](https://www.kaggle.com/datasets/mexwell/uk-police-data)

Here's what we'll do:

1. Open the link above and click **Download**. Since this covers the whole country, the file can run to several GB — that's expected, so we'll just let it finish.
2. We'll unzip it and look for the **street-level crime CSV(s)**. Typical columns include:
   - `Crime ID`
   - `Month`
   - `Reported by`
   - `Falls within`
   - `Longitude`
   - `Latitude`
   - `Location`
   - `LSOA code`
   - `LSOA name`
   - `Crime type`
   - `Last outcome category`

**Important — which police force we need:**

| County | Police force |
|---|---|
| Kent | Kent Police |
| Monmouthshire | Gwent Police (there's no separate "Monmouthshire Police") |

3. We'll move the file into our data folder:

```
data-science-project/
  data/
    raw/
      price_paid_records.csv
      202205_fixed_laua_performance_r02.csv
      about-this-data-broadband.pdf
      uk_police_crime_data.csv
```

**A note on citation:** since this is a Kaggle *mirror* of the original data.police.uk source, we'll cite both in our report — [data.police.uk](https://data.police.uk) as the authoritative origin (licensed under OGL v3.0), and the Kaggle page as the specific access point we used. This shows good understanding of data provenance, which examiners like to see.

**A note on filtering:** just like the house price data, this file covers far more of the country than we need. We won't filter it yet — we'll do that together in **Step 3: Data Wrangling**, filtering by `LSOA name` or `Falls within` (force name) using pandas. It's a simple operation once we get there.

---

## Step 2.5 — Update the Report's Data Sources Section

Once the first three datasets are downloaded, we'll pause and update our report's Data Sources section, documenting each dataset's origin, licence, and any limitations while it's fresh.

---

## Step 2.6 — Air Quality Data (Defra) — Our Fourth Factor

**Dataset:** [PM2.5 by Local Authority 2023 (CSV)](https://uk-air.defra.gov.uk/datastore/pcm/popwmpm252023byUKlocalauthority.csv)
**Background reading:** [Modelled background pollution data — DEFRA UK Air](https://uk-air.defra.gov.uk/data/pcm-data)

Here's what we'll do:

1. Click the first link above — it downloads directly as a CSV, no login needed, since this is public Defra open data.
2. Let's open it and check the columns. We should see roughly:
   - `Code` (local authority code)
   - `PM2.5 2023 (total)`
   - `PM2.5 2023 (non-anthropogenic)`
   - `PM2.5 2023 (anthropogenic)`
   - `Name` (local authority name)
3. We'll confirm it has rows for Kent's districts and for Monmouthshire.
4. Into the data folder it goes:

```
data-science-project/
  data/
    raw/
      price_paid_records.csv
      202205_fixed_laua_performance_r02.csv
      about-this-data-broadband.pdf
      uk_police_crime_data.csv
      popwmpm252023byUKlocalauthority.csv
```

**A note on limitations:** this shares the same granularity issue as our broadband data — it's local-authority-level, so Kent's districts map fairly well to individual towns, but Monmouthshire is just one row for the whole county. Worth stating explicitly in our report. It's actually a nice analytical thread to pull through the discussion section: two of our four factors (broadband and air quality) share this granularity limitation, while house prices and crime can be pinned down more precisely at town level.

---

## Where We Should Be Now

By the end of this step, we should have:

- ✅ `assignment_report.docx` started, with sections on county/town selection, data sources, and our fourth factor
- ✅ All four raw datasets sitting in `data/raw/`
- ✅ A Kaggle account set up
- ✅ A clear note of each dataset's licence, date, and known limitations, ready to carry into the report

Next, we'll move into **Step 3: Data Wrangling** — this is where we open up Python and pandas, load all four files, filter them down to our 20 towns, clean them up, and start building the relational data model the assignment requires.

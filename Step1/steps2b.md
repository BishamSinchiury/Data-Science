# Project Steps Log

A running record of what we do from here on, in order. Each entry has what we did, why, and what it produced. Earlier steps (county/town selection, data collection, Stage 1 load/inspect, Stage 2a filtering) are documented in `step2_data_collection_guide.md` — this file picks up from Stage 2b onward.

---

## Stage 2b — Filter & Aggregate Crime Data

**Scripts:** `reference_towns.py` (updated), `stage2b_filter_crime.py`

**What we did:** Filtered the 36 monthly crime folders down to just Kent Police and Gwent Police street-level files, matched each record to one of our 20 towns using LSOA name prefixes, grouped the 14 raw crime types into Violent / Property / Other, and aggregated into one row per town with a total count and a crimes-per-1,000-residents figure.

**Why:** Crime data has no District column like broadband/air quality/house prices do, so town-matching had to use LSOA names instead. LSOA names in Kent and Monmouthshire generally follow the local authority district name, which meant handling multi-word prefixes correctly (e.g. "Tunbridge Wells 003A") and explicitly deciding what to do about Medway (Chatham/Rochester/Gillingham) and Thanet (Margate/Ramsgate) — towns that share a district and therefore share identical LSOA-derived crime figures, same as they already share broadband and air quality figures.

**Why normalise per 1,000 residents:** a raw crime count is only meaningful relative to population — Maidstone (pop. 113,137) will naturally have more crimes than Usk (pop. 3,000) even if Usk is less safe per resident. Normalising makes the recommendation system's later crime score fair across very different town sizes.

**Output:** `Data/processed/crime_by_town.csv` — one row per town with `TotalCrimes_36Months`, `Violent`, `Property`, `Other`, and `CrimesPer1000Residents_36Months`.

---

## Stage 3 — Combine Into One Dataset / Build the Relational Data Model

*(Not started yet — planned next)*

**What we'll do:** Bring the four processed files (`house_prices_filtered.csv`, `broadband_filtered.csv`, `air_quality_filtered.csv`, `crime_by_town.csv`) together into either one combined per-town table for analysis, or a proper relational database normalized to at least 3NF, as the assignment brief requires (separate tables for Towns, HousePrices, Broadband, Crime, AirQuality, linked by a town/district ID).

**Why this needs care:** house prices and crime are still at individual-transaction/individual-crime level at this point (many rows per town), while broadband and air quality are one row per district. Combining them means deciding on the right level of aggregation — e.g. average/median house price per town — before joining, and being explicit in the report about which of our 13 districts represent more than one of our 20 towns (Medway, Thanet, Monmouthshire covers all 5 of its towns as one row).

---

## Stage 4 — Exploratory Data Analysis (EDA)

*(Not started yet)*

**What we'll do:** Use pandas, matplotlib, and seaborn to explore distributions, spot outliers, and compare towns and counties across all four factors.

**Why:** Required by the assignment brief, and it's also where we'll properly document the Medway/Thanet/Monmouthshire granularity limitation with real numbers and charts, not just as a caveat in prose.

---

## Stage 5 — Statistical Analysis

*(Not started yet)*

**What we'll do:** Look for correlations between our four factors (e.g. does higher broadband speed correlate with higher house prices?).

---

## Stage 6 — Recommendation System

*(Not started yet)*

**What we'll do:** Normalise each of the four factors onto a 0–10 scale per town, combine them into one score, and rank the towns to produce a top-3 recommendation.

---

## Stage 7 — Report Write-Up

*(Ongoing throughout — not a separate final stage)*

Each stage above gets written into `assignment_report.docx` as we complete it, rather than left until the end.

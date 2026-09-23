# Step 1 & 2: Data Collection and Wrangling

## Problem Statement
For our analysis and recommendation system, we needed to gather four distinct real-world datasets—House Prices, Broadband Speeds, Air Quality, and Crime Rates—for 20 selected towns across Kent and Monmouthshire. 

However, raw government data is messy and cannot be analyzed directly out of the box because:
1. **Size and Scope:** The raw HM Land Registry house price file covers every UK transaction since 1995 and is 770MB+, which causes memory and permission errors when loaded all at once.
2. **Inconsistent Granularity:** Some datasets (like broadband and air quality) are only published at the **Local Authority/District** level, while others (like house prices and crime) contain granular street, town, or LSOA (Lower Layer Super Output Area) level data.
3. **Format Quirks:** Files often have missing header rows, hidden metadata rows, or inconsistent naming conventions (e.g., "Tunbridge Wells" vs. "Royal Tunbridge Wells").

## Solution Implemented (What & How)

### 1. Data Collection & Sourcing
We sourced our datasets from authoritative government and public data portals to ensure provenance:
- **House Prices:** Downloaded yearly chunks (2021-2024) directly from HM Land Registry to avoid loading the massive 1995-2024 master file.
- **Broadband Speeds:** Sourced from Ofcom's *Connected Nations* report.
- **Air Quality:** Sourced PM2.5 levels from Defra (Department for Environment, Food & Rural Affairs), as it is the most reliable metric for health impact.
- **Crime Data:** Sourced 36 months of street-level data for Kent Police and Gwent Police (since Monmouthshire falls under Gwent) via a Kaggle mirror of police.uk data.

### 2. Stage 1: Load & Inspect (`stage1_load_inspect.py`)
Before building complex filtering logic, we wrote a script just to load and print samples of the data. 
- *Why:* This allowed us to catch format surprises early. For example, we discovered the house price files had no header row (so we had to manually apply the schema), and the Defra air quality file had two hidden metadata rows that needed to be skipped (`skiprows=2`).

### 3. Stage 2a: Reference Mapping & Filtering (`stage2a_filter_prices_broadband_air.py`)
To merge these distinct datasets later, we needed a unified standard. We built a master mapping file (`reference_towns.py`) linking our 20 towns to their 13 overarching Local Authority Districts.
- *How:* We read the massive house price files in **chunks** of 200,000 rows to prevent RAM exhaustion. We filtered the broadband, air quality, and house prices down to only keep records matching our 13 districts.

### 4. Stage 2b: Crime Grouping & Normalization (`stage2b_filter_crime.py`)
Crime data required a unique approach because it doesn't contain a "District" column—only LSOA (neighborhood) names.
- *How:* We mapped LSOA prefixes (e.g., "Tunbridge Wells 003A") to our towns. 
- *Why:* The raw data had 14 different crime categories, which is too noisy for a recommendation engine. We mapped these into three distinct, standard buckets: **Violent**, **Property**, and **Other** (`reference_crime_groups.py`).
- *Normalization:* We divided the total crimes by the town's population to calculate **"crimes per 1,000 residents"**. *Why:* Comparing raw crime totals between Maidstone (pop. 113k) and Usk (pop. 3k) is unfair. Normalizing per capita ensures an apples-to-apples safety comparison.

## How is Our Data Structured?
At the end of Step 1 & 2, our data is structured as follows:

1. **Town-Level Data (Granular):**
   - **House Prices:** Filtered down to our towns, keeping individual transaction prices, dates, and property types.
   - **Crime Rates:** Aggregated to one row per town, containing total crimes, our 3 grouped categories, and the normalized per-1,000-residents metric.
2. **District-Level Data (Broad):**
   - **Broadband & Air Quality:** One row per District.
   - *Important Limitation:* Because multiple towns share a district (e.g., Chatham, Rochester, and Gillingham all sit in Medway), they inherently **share the exact same broadband speed and air quality score**. This is a structural fact of how the UK publishes this data, which we explicitly model in our Stage 3 database schema.

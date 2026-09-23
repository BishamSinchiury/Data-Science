"""
Stage 2a: Filter House Prices, Broadband, Air Quality
-------------------------------------------------------
Filters the three District-level/Town-level datasets down to our 20
selected towns, using the Town -> District mapping in reference_towns.py.
Crime is handled separately (stage2b) since it filters by police force
and LSOA name rather than District.

Run from: D:\\Data Science\\Assignment\\Step1>
    python stage2a_filter_prices_broadband_air.py

Output: three filtered CSVs written to Data/processed/
"""

import pandas as pd
from pathlib import Path
from reference_towns import TOWN_TO_DISTRICT, SELECTED_DISTRICTS

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW = PROJECT_ROOT / "Data" / "raw"
PROCESSED = PROJECT_ROOT / "Data" / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)

HOUSE_PRICE_YEAR_FILES = [
    RAW / "pp-2021.csv",
    RAW / "pp-2022.csv",
    RAW / "pp-2023.csv",
    RAW / "pp-2024.csv",
]
BROADBAND_FILE = RAW / "202205_fixed_laua_performance_r02.csv"
AIR_QUALITY_FILE = RAW / "popwmpm252023byUKlocalauthority.csv"

house_price_columns = [
    "TransactionID", "Price", "DateOfTransfer", "Postcode", "PropertyType",
    "OldNew", "Duration", "PAON", "SAON", "Street", "Locality",
    "Town", "District", "County", "PPDCategoryType", "RecordStatus"
]


def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# --------------------------------------------------------------------
# 1. House prices — filter by District, in chunks (file is too big to
#    load in full without risking the same memory/permission issues
#    we saw with the original single file).
# --------------------------------------------------------------------

section("1. HOUSE PRICES — filtering by District")

price_frames = []

for year_file in HOUSE_PRICE_YEAR_FILES:
    if not year_file.exists():
        print(f"MISSING: {year_file.name}")
        continue

    kept_rows = 0
    total_rows = 0

    # Reading in chunks keeps memory use low even on a 1M+ row file.
    for chunk in pd.read_csv(
        year_file,
        header=None,
        names=house_price_columns,
        chunksize=200_000,
    ):
        total_rows += len(chunk)
        filtered = chunk[chunk["District"].str.upper().isin(SELECTED_DISTRICTS)]
        kept_rows += len(filtered)
        if len(filtered) > 0:
            price_frames.append(filtered)

    print(f"{year_file.name}: kept {kept_rows:,} of {total_rows:,} rows")

df_prices_filtered = pd.concat(price_frames, ignore_index=True)

# Add our own Town label back on, using the District -> list-of-towns
# reverse of TOWN_TO_DISTRICT, since District alone doesn't tell us
# which specific town within Medway/Thanet a row belongs to. For rows
# in a District that maps to only one of our towns, this is exact; for
# Medway/Thanet, the actual town field from the data itself is used
# instead, since we still have that.
df_prices_filtered["District"] = df_prices_filtered["District"].str.upper()

print(f"\nTotal house price rows kept: {len(df_prices_filtered):,}")
print(df_prices_filtered["District"].value_counts())

output_path = PROCESSED / "house_prices_filtered.csv"
df_prices_filtered.to_csv(output_path, index=False)
print(f"\nSaved: {output_path}")


# --------------------------------------------------------------------
# 2. Broadband — filter by laua_name
# --------------------------------------------------------------------

section("2. BROADBAND — filtering by local authority")

df_broadband = pd.read_csv(BROADBAND_FILE)
df_broadband["laua_name"] = df_broadband["laua_name"].str.upper()

df_broadband_filtered = df_broadband[
    df_broadband["laua_name"].isin(SELECTED_DISTRICTS)
].copy()

print(f"Kept {len(df_broadband_filtered)} of {len(SELECTED_DISTRICTS)} expected districts")
missing = set(SELECTED_DISTRICTS) - set(df_broadband_filtered["laua_name"])
if missing:
    print(f"WARNING — districts not found in broadband data: {missing}")

print(df_broadband_filtered[["laua", "laua_name"]])

output_path = PROCESSED / "broadband_filtered.csv"
df_broadband_filtered.to_csv(output_path, index=False)
print(f"\nSaved: {output_path}")


# --------------------------------------------------------------------
# 3. Air quality — filter by Local Authority
# --------------------------------------------------------------------

section("3. AIR QUALITY — filtering by local authority")

df_air = pd.read_csv(AIR_QUALITY_FILE, skiprows=2)
df_air["Local Authority"] = df_air["Local Authority"].str.upper()

df_air_filtered = df_air[
    df_air["Local Authority"].isin(SELECTED_DISTRICTS)
].copy()

print(f"Kept {len(df_air_filtered)} of {len(SELECTED_DISTRICTS)} expected districts")
missing = set(SELECTED_DISTRICTS) - set(df_air_filtered["Local Authority"])
if missing:
    print(f"WARNING — districts not found in air quality data: {missing}")

print(df_air_filtered[["LA code", "Local Authority", "PM2.5 2023 (total)"]])

output_path = PROCESSED / "air_quality_filtered.csv"
df_air_filtered.to_csv(output_path, index=False)
print(f"\nSaved: {output_path}")


section("STAGE 2a COMPLETE")
print("""
Three filtered files are now in Data/processed/:
  - house_prices_filtered.csv
  - broadband_filtered.csv
  - air_quality_filtered.csv

Check the WARNING lines above (if any) — a missing district usually
means a small spelling difference between our reference_towns.py
mapping and the exact name used in that dataset. Fix the mapping,
not the data, if that happens.

Next: stage2b_filter_crime.py, which filters the 36 monthly crime
folders down to Kent Police + Gwent Police street-level files only.
""")

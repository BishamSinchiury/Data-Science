"""
Stage 1: Load & Inspect
------------------------
We load each of the four raw datasets and confirm they contain what we
expect before doing any real cleaning. Run this first, read the printed
output, and only move on to stage 2 once everything here looks right.

Run from: D:\\Data Science\\Assignment>
    python stage1_load_inspect.py
"""

import pandas as pd
from pathlib import Path

# --------------------------------------------------------------------
# Paths — adjust here if your folder names ever change
# --------------------------------------------------------------------
# This script lives in Assignment/Step1/, but the data lives in
# Assignment/Data/raw/ — one level up, then into Data/raw. Building the
# path from this file's own location means it works no matter which
# folder you run the script from.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW = PROJECT_ROOT / "Data" / "raw"

# We switched from the single 770MB Kaggle mirror to HM Land Registry's
# own yearly files, downloaded directly from gov.uk. These are smaller,
# split by year, and are the primary source rather than a third-party
# mirror. We only need the years matching our crime/broadband/air
# quality data (2021 through 2024).
HOUSE_PRICE_YEAR_FILES = [
    RAW / "pp-2021.csv",
    RAW / "pp-2022.csv",
    RAW / "pp-2023.csv",
    RAW / "pp-2024.csv",
]
BROADBAND_FILE = RAW / "202205_fixed_laua_performance_r02.csv"
AIR_QUALITY_FILE = RAW / "popwmpm252023byUKlocalauthority.csv"
CRIME_ROOT = RAW  # monthly folders (2021-06, 2021-07, ...) live directly here

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 160)


def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)



# --------------------------------------------------------------------
# 1. House prices
# --------------------------------------------------------------------

section("1. HOUSE PRICES — HM Land Registry yearly files (2021-2024)")

# Unlike the Kaggle mirror, HM Land Registry's yearly files have NO
# header row, so we name the columns ourselves, matching the official
# schema documented on gov.uk.
house_price_columns = [
    "TransactionID", "Price", "DateOfTransfer", "PropertyType",
    "OldNew", "Duration", "PAON", "SAON", "Street", "Locality",
    "Town", "District", "County", "PPDCategoryType", "RecordStatus"
]

# We load each year file separately and check it before combining,
# so a problem in one year's file is easy to spot.
year_frames = {}
for year_file in HOUSE_PRICE_YEAR_FILES:
    if not year_file.exists():
        print(f"MISSING: {year_file.name} — check it's in Data/raw/")
        continue

    df_year = pd.read_csv(
        year_file,
        header=None,
        names=house_price_columns,
    )
    year_frames[year_file.stem] = df_year
    print(f"{year_file.name}: {len(df_year):,} rows loaded")


if year_frames:
    # Combine all loaded years into one DataFrame for inspection.
    df_prices = pd.concat(year_frames.values(), ignore_index=True)

    print("\nCombined rows across all years:", f"{len(df_prices):,}")
    print(df_prices.head(3))
    print("\nColumns:", list(df_prices.columns))
    print("Sample of County values:", df_prices["County"].unique()[:10])
    print("Sample of Town values:", df_prices["Town"].unique()[:10])

    print(
        "\nKENT rows across 2021-2024:",
        f"{(df_prices['County'] == 'KENT').sum():,}"
    )
    print(
        "MONMOUTHSHIRE rows across 2021-2024:",
        f"{(df_prices['County'] == 'MONMOUTHSHIRE').sum():,}"
    )
else:
    print("\nNo year files found — check Data/raw/ contains pp-2021.csv etc.")

# --------------------------------------------------------------------
# 2. Broadband
# --------------------------------------------------------------------

section("2. BROADBAND — 202205_fixed_laua_performance_r02.csv")

df_broadband = pd.read_csv(BROADBAND_FILE)

print(df_broadband.head(3))
print("\nColumns:", list(df_broadband.columns))
print("Number of local authorities:", len(df_broadband))

# Check Kent districts and Monmouthshire are present
kent_check = df_broadband[
    df_broadband["laua_name"].str.contains(
        "MAIDSTONE|ASHFORD|CANTERBURY|MONMOUTHSHIRE",
        case=False, na=False
    )
]
print("\nMatching rows (Kent districts / Monmouthshire):")
print(kent_check[["laua", "laua_name"]])


# # --------------------------------------------------------------------
# # 3. Air quality (PM2.5)
# # --------------------------------------------------------------------

section("3. AIR QUALITY — popwmpm252023byUKlocalauthority.csv")

# This file has 2 metadata rows above the real header, so we skip them.
df_air = pd.read_csv(AIR_QUALITY_FILE, skiprows=2)

print(df_air.head(3))
print("\nColumns:", list(df_air.columns))
print("Number of local authorities:", len(df_air))

air_check = df_air[
    df_air["Local Authority"].str.contains(
        "Maidstone|Ashford|Canterbury|Monmouthshire",
        case=False, na=False
    )
]
print("\nMatching rows (Kent districts / Monmouthshire):")
print(air_check[["LA code", "Local Authority", "PM2.5 2023 (total)"]])


# --------------------------------------------------------------------
# 4. Crime — just check ONE month/force file first
# --------------------------------------------------------------------

section("4. CRIME — sample file check (2021-06 Kent street data)")

sample_crime_file = CRIME_ROOT / "2021-06" / "2021-06-kent-street.csv"

if sample_crime_file.exists():
    df_crime_sample = pd.read_csv(sample_crime_file)
    print(df_crime_sample.head(3))
    print("\nColumns:", list(df_crime_sample.columns))
    print("Rows in this one file:", len(df_crime_sample))
    print("Unique crime types:", df_crime_sample["Crime type"].unique())
else:
    print(f"File not found at expected path: {sample_crime_file}")
    print("Check your folder structure matches Data/raw/2021-06/...")

# Count how many monthly folders we actually have
month_folders = sorted(
    [p for p in CRIME_ROOT.iterdir() if p.is_dir() and p.name[:4].isdigit()]
)
print(f"\nFound {len(month_folders)} monthly folders:")
print([p.name for p in month_folders[:3]], "...", [p.name for p in month_folders[-3:]])
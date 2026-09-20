"""
Stage 2b: Filter & Aggregate Crime Data
------------------------------------------
Filters the 36 monthly crime folders down to just Kent Police and
Gwent Police street-level files, matches records to our towns using
LSOA name prefixes, groups the 14 raw crime types into Violent /
Property / Other, and produces one row per town with total and
per-category crime counts.

Population figures are needed to normalise crime counts (a raw count
is meaningless without knowing the town's size), so this script also
carries the population figures from Section 1 of the report.

Run from: D:\\Data Science\\Assignment\\Step1>
    python stage2b_filter_crime.py

Output: Data/processed/crime_by_town.csv
"""

import pandas as pd
from pathlib import Path
from reference_towns import TOWN_TO_LSOA_PREFIX, KENT_POLICE_FORCE, GWENT_POLICE_FORCE
from reference_crime_groups import group_crime_type

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW = PROJECT_ROOT / "Data" / "raw"
PROCESSED = PROJECT_ROOT / "Data" / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)

# Population figures from Section 1 of the report. Used to normalise
# crime counts per 1,000 residents, so a large town and a small town
# can be compared fairly. Where several towns share a district (Medway,
# Thanet, Monmouthshire), the crime data itself is shared too (see
# reference_towns.py), but we still keep each town's own population
# for the per-1,000 calculation.
TOWN_POPULATION = {
    "MAIDSTONE": 113137, "GILLINGHAM": 104157, "DARTFORD": 87415,
    "CHATHAM": 76792, "ASHFORD": 74204, "ROCHESTER": 62982,
    "MARGATE": 61223, "ROYAL TUNBRIDGE WELLS": 57772, "GRAVESEND": 55467,
    "CANTERBURY": 50402, "FOLKESTONE": 51337, "SITTINGBOURNE": 48948,
    "DOVER": 43070, "RAMSGATE": 40515, "TONBRIDGE": 38657,
    "ABERGAVENNY": 13691, "CHEPSTOW": 11934, "CALDICOT": 9813,
    "MONMOUTH": 10500, "USK": 3000,
}


def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# --------------------------------------------------------------------
# 1. Find all Kent/Gwent street-level files across all 36 months
# --------------------------------------------------------------------

section("1. FINDING RELEVANT CRIME FILES")

month_folders = sorted(
    [p for p in RAW.iterdir() if p.is_dir() and p.name[:4].isdigit()]
)
print(f"Found {len(month_folders)} monthly folders")

crime_files = []
for month_folder in month_folders:
    for force_slug in ["kent", "gwent"]:
        candidate = month_folder / f"{month_folder.name}-{force_slug}-street.csv"
        if candidate.exists():
            crime_files.append(candidate)
        else:
            print(f"  Missing expected file: {candidate.name}")

print(f"\nFound {len(crime_files)} Kent/Gwent street files "
      f"(expected up to {len(month_folders) * 2})")


# --------------------------------------------------------------------
# 2. Load, filter, and match every file to a town
# --------------------------------------------------------------------

section("2. LOADING, FILTERING & MATCHING TO TOWNS")

all_records = []

for f in crime_files:
    df = pd.read_csv(f, usecols=["Falls within", "LSOA name", "Crime type"])

    # Sanity check: only keep rows genuinely from Kent Police or Gwent
    # Police, in case a file ever contains rows attributed elsewhere.
    df = df[df["Falls within"].isin([KENT_POLICE_FORCE, GWENT_POLICE_FORCE])]

    # Drop rows with no LSOA name at all (e.g. "No Location" crimes,
    # which can't be attributed to any town).
    df = df.dropna(subset=["LSOA name"])

    df["LSOA_prefix"] = df["LSOA name"].str.upper().str.rsplit(" ", n=1).str[0]

    all_records.append(df)

df_crime = pd.concat(all_records, ignore_index=True)
print(f"Total Kent/Gwent street-level records loaded: {len(df_crime):,}")

# Build a reverse lookup: LSOA prefix -> list of towns that share it
prefix_to_towns = {}
for town, prefix in TOWN_TO_LSOA_PREFIX.items():
    prefix_to_towns.setdefault(prefix, []).append(town)

# Match each crime record's LSOA prefix to the district-level prefix
# used in our mapping (e.g. "MAIDSTONE 001A" -> prefix "MAIDSTONE").
# Some LSOA names have more than one word before the code (e.g.
# "Tunbridge Wells 001A"), so we match against the known set of
# prefixes directly rather than assuming a single-word prefix.
known_prefixes = sorted(set(TOWN_TO_LSOA_PREFIX.values()), key=len, reverse=True)


def find_matching_prefix(lsoa_name_upper: str) -> str | None:
    for prefix in known_prefixes:
        if lsoa_name_upper.startswith(prefix):
            return prefix
    return None


df_crime["MatchedPrefix"] = df_crime["LSOA name"].str.upper().apply(find_matching_prefix)

matched = df_crime[df_crime["MatchedPrefix"].notna()]
print(f"Records matching one of our districts: {len(matched):,} of {len(df_crime):,}")


# --------------------------------------------------------------------
# 3. Group crime types, then aggregate per town
# --------------------------------------------------------------------

section("3. GROUPING CRIME TYPES & AGGREGATING PER TOWN")

matched = matched.copy()
matched["CrimeGroup"] = matched["Crime type"].apply(group_crime_type)

town_rows = []

for town, prefix in TOWN_TO_LSOA_PREFIX.items():
    town_records = matched[matched["MatchedPrefix"] == prefix]

    total = len(town_records)
    violent = (town_records["CrimeGroup"] == "Violent").sum()
    property_ = (town_records["CrimeGroup"] == "Property").sum()
    other = (town_records["CrimeGroup"] == "Other").sum()

    population = TOWN_POPULATION.get(town)
    per_1000 = round((total / population) * 1000, 2) if population else None

    town_rows.append({
        "Town": town,
        "District_LSOA_Prefix": prefix,
        "Population": population,
        "TotalCrimes_36Months": total,
        "Violent": violent,
        "Property": property_,
        "Other": other,
        "CrimesPer1000Residents_36Months": per_1000,
    })

df_town_crime = pd.DataFrame(town_rows)
print(df_town_crime.to_string(index=False))

output_path = PROCESSED / "crime_by_town.csv"
df_town_crime.to_csv(output_path, index=False)
print(f"\nSaved: {output_path}")


section("STAGE 2b COMPLETE")
print("""
Data/processed/crime_by_town.csv now has one row per town, with total
crime count, a Violent/Property/Other breakdown, and a crimes-per-1000-
residents figure covering the full 36-month period (2021-06 to
2024-05).

Reminder for the report: Chatham, Rochester and Gillingham share
identical crime figures (all matched to the Medway LSOA prefix), and
Margate/Ramsgate share identical figures too (Thanet). This is the
same structural limitation already noted for broadband and air
quality, not a bug in this script.

Next: Stage 3 will bring all four processed files together into one
combined table (or a proper 3NF relational database), ready for
exploratory data analysis.
""")

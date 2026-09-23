"""
Stage 3: Build the Relational Database (3NF)
------------------------------------------------
Creates a SQLite database with a schema normalized to 3NF, then loads
our four processed datasets (house prices, broadband, air quality,
crime) into it. This turns the flat CSVs from Stage 2 into a proper
relational structure, as the project brief requires.

Schema summary (see schema_design_notes.txt for the full reasoning):
    counties      (1 row per county)
    districts     (1 row per district, FK -> counties)
    towns         (1 row per town, FK -> districts)
    broadband     (1 row per DISTRICT, FK -> districts)
    air_quality   (1 row per DISTRICT, FK -> districts)
    house_prices  (1 row per TOWN, FK -> towns)
    crime         (1 row per TOWN, FK -> towns)

Broadband and air_quality key on district_id (not town_id) because
that is genuinely the level those datasets are published at -- see
Section 4.2 of the report. Keying them on town_id instead would mean
storing the same value multiple times (once for Chatham, once for
Rochester, once for Gillingham), which is exactly the kind of
redundancy 3NF is designed to remove.

Run from: D:\\Data Science\\Assignment\\Step1>
    python stage3_build_database.py

Output: Data/processed/project.db
"""

import sqlite3
import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from Step1.reference_towns import TOWN_TO_DISTRICT
PROCESSED = PROJECT_ROOT / "Data" / "processed"
DB_PATH = PROCESSED / "project.db"

# Population figures (same source as Section 1 / Stage 2b)
TOWN_POPULATION = {
    "MAIDSTONE": 113137, "GILLINGHAM": 104157, "DARTFORD": 87415,
    "CHATHAM": 76792, "ASHFORD": 74204, "ROCHESTER": 62982,
    "MARGATE": 61223, "ROYAL TUNBRIDGE WELLS": 57772, "GRAVESEND": 55467,
    "CANTERBURY": 50402, "FOLKESTONE": 51337, "SITTINGBOURNE": 48948,
    "DOVER": 43070, "RAMSGATE": 40515, "TONBRIDGE": 38657,
    "ABERGAVENNY": 13691, "CHEPSTOW": 11934, "CALDICOT": 9813,
    "MONMOUTH": 10500, "USK": 3000,
}

TOWN_TO_COUNTY = {
    town: ("KENT" if district != "MONMOUTHSHIRE" else "MONMOUTHSHIRE")
    for town, district in TOWN_TO_DISTRICT.items()
}


def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# --------------------------------------------------------------------
# 1. Create schema
# --------------------------------------------------------------------

section("1. CREATING SCHEMA")

if DB_PATH.exists():
    DB_PATH.unlink()
    print("Removed existing database to rebuild from scratch.")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE counties (
    county_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    county_name TEXT NOT NULL UNIQUE
);

CREATE TABLE districts (
    district_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    district_name TEXT NOT NULL UNIQUE,
    county_id     INTEGER NOT NULL,
    FOREIGN KEY (county_id) REFERENCES counties(county_id)
);

CREATE TABLE towns (
    town_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    town_name   TEXT NOT NULL UNIQUE,
    district_id INTEGER NOT NULL,
    population  INTEGER,
    FOREIGN KEY (district_id) REFERENCES districts(district_id)
);

CREATE TABLE broadband (
    district_id            INTEGER PRIMARY KEY,
    median_download_mbps   REAL,
    average_download_mbps  REAL,
    average_upload_mbps    REAL,
    FOREIGN KEY (district_id) REFERENCES districts(district_id)
);

CREATE TABLE air_quality (
    district_id             INTEGER PRIMARY KEY,
    pm25_total              REAL,
    pm25_anthropogenic      REAL,
    pm25_non_anthropogenic  REAL,
    FOREIGN KEY (district_id) REFERENCES districts(district_id)
);

CREATE TABLE house_prices (
    town_id           INTEGER PRIMARY KEY,
    median_price      REAL,
    transaction_count INTEGER,
    min_price         REAL,
    max_price         REAL,
    FOREIGN KEY (town_id) REFERENCES towns(town_id)
);

CREATE TABLE crime (
    town_id              INTEGER PRIMARY KEY,
    total_crimes         INTEGER,
    violent_crimes       INTEGER,
    property_crimes      INTEGER,
    other_crimes         INTEGER,
    crimes_per_1000      REAL,
    FOREIGN KEY (town_id) REFERENCES towns(town_id)
);
""")
conn.commit()
print("Created 7 tables: counties, districts, towns, broadband, air_quality, house_prices, crime")


# --------------------------------------------------------------------
# 2. Populate counties, districts, towns
# --------------------------------------------------------------------

section("2. POPULATING COUNTIES, DISTRICTS, TOWNS")

counties = sorted(set(TOWN_TO_COUNTY.values()))
county_ids = {}
for county_name in counties:
    cur.execute("INSERT INTO counties (county_name) VALUES (?)", (county_name,))
    county_ids[county_name] = cur.lastrowid
print(f"Inserted {len(counties)} counties: {counties}")

districts = sorted(set(TOWN_TO_DISTRICT.values()))
district_ids = {}
for district_name in districts:
    # A district's county is whichever county its towns belong to
    towns_here = [t for t, d in TOWN_TO_DISTRICT.items() if d == district_name]
    county_name = TOWN_TO_COUNTY[towns_here[0]]
    cur.execute(
        "INSERT INTO districts (district_name, county_id) VALUES (?, ?)",
        (district_name, county_ids[county_name])
    )
    district_ids[district_name] = cur.lastrowid
print(f"Inserted {len(districts)} districts")

town_ids = {}
for town_name, district_name in TOWN_TO_DISTRICT.items():
    population = TOWN_POPULATION.get(town_name)
    cur.execute(
        "INSERT INTO towns (town_name, district_id, population) VALUES (?, ?, ?)",
        (town_name, district_ids[district_name], population)
    )
    town_ids[town_name] = cur.lastrowid
print(f"Inserted {len(town_ids)} towns")

conn.commit()


# --------------------------------------------------------------------
# 3. Load broadband (per district)
# --------------------------------------------------------------------

section("3. LOADING BROADBAND (per district)")

broadband_file = PROCESSED / "broadband_filtered.csv"
if broadband_file.exists():
    df_bb = pd.read_csv(broadband_file)
    df_bb["laua_name"] = df_bb["laua_name"].str.upper()

    inserted = 0
    for _, row in df_bb.iterrows():
        district_name = row["laua_name"]
        if district_name not in district_ids:
            continue
        cur.execute(
            """INSERT INTO broadband
               (district_id, median_download_mbps, average_download_mbps, average_upload_mbps)
               VALUES (?, ?, ?, ?)""",
            (
                district_ids[district_name],
                row.get("Median download speed (Mbit/s)"),
                row.get("Average download speed (Mbit/s)"),
                row.get("Average upload speed (Mbit/s)"),
            )
        )
        inserted += 1
    conn.commit()
    print(f"Inserted broadband rows for {inserted} districts")
else:
    print(f"MISSING: {broadband_file} — run stage2a first")


# --------------------------------------------------------------------
# 4. Load air quality (per district)
# --------------------------------------------------------------------

section("4. LOADING AIR QUALITY (per district)")

air_file = PROCESSED / "air_quality_filtered.csv"
if air_file.exists():
    df_air = pd.read_csv(air_file)
    df_air["Local Authority"] = df_air["Local Authority"].str.upper()

    inserted = 0
    for _, row in df_air.iterrows():
        district_name = row["Local Authority"]
        if district_name not in district_ids:
            continue
        cur.execute(
            """INSERT INTO air_quality
               (district_id, pm25_total, pm25_anthropogenic, pm25_non_anthropogenic)
               VALUES (?, ?, ?, ?)""",
            (
                district_ids[district_name],
                row.get("PM2.5 2023 (total)"),
                row.get("PM2.5 2023 (anthropogenic)"),
                row.get("PM2.5 2023 (non-anthropogenic)"),
            )
        )
        inserted += 1
    conn.commit()
    print(f"Inserted air quality rows for {inserted} districts")
else:
    print(f"MISSING: {air_file} — run stage2a first")


# --------------------------------------------------------------------
# 5. Load & aggregate house prices (per town, median)
# --------------------------------------------------------------------

section("5. AGGREGATING & LOADING HOUSE PRICES (median per town)")

prices_file = PROCESSED / "house_prices_filtered.csv"
if prices_file.exists():
    df_prices = pd.read_csv(prices_file)
    df_prices["District"] = df_prices["District"].str.upper()

    # We aggregate by TOWN, not District, using the Town column already
    # present in the house price data itself (not our District mapping),
    # since house prices retain individual-town detail even within a
    # shared district like Medway.
    df_prices["Town"] = df_prices["Town"].str.upper()

    inserted = 0
    skipped = []
    for town_name in town_ids:
        town_records = df_prices[df_prices["Town"] == town_name]
        if len(town_records) == 0:
            skipped.append(town_name)
            continue
        cur.execute(
            """INSERT INTO house_prices
               (town_id, median_price, transaction_count, min_price, max_price)
               VALUES (?, ?, ?, ?, ?)""",
            (
                town_ids[town_name],
                float(town_records["Price"].median()),
                len(town_records),
                float(town_records["Price"].min()),
                float(town_records["Price"].max()),
            )
        )
        inserted += 1
    conn.commit()
    print(f"Inserted house price summaries for {inserted} towns")
    if skipped:
        print(f"No house price transactions found for: {skipped}")
        print("(Expected for very small towns like Usk — check the report's limitations section)")
else:
    print(f"MISSING: {prices_file} — run stage2a first")


# --------------------------------------------------------------------
# 6. Load crime (per town)
# --------------------------------------------------------------------

section("6. LOADING CRIME (per town)")

crime_file = PROCESSED / "crime_by_town.csv"
if crime_file.exists():
    df_crime = pd.read_csv(crime_file)
    df_crime["Town"] = df_crime["Town"].str.upper()

    inserted = 0
    for _, row in df_crime.iterrows():
        town_name = row["Town"]
        if town_name not in town_ids:
            continue
        cur.execute(
            """INSERT INTO crime
               (town_id, total_crimes, violent_crimes, property_crimes, other_crimes, crimes_per_1000)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                town_ids[town_name],
                int(row["TotalCrimes_36Months"]),
                int(row["Violent"]),
                int(row["Property"]),
                int(row["Other"]),
                row["CrimesPer1000Residents_36Months"],
            )
        )
        inserted += 1
    conn.commit()
    print(f"Inserted crime summaries for {inserted} towns")
else:
    print(f"MISSING: {crime_file} — run stage2b first")


# --------------------------------------------------------------------
# 7. Verify with a joined query
# --------------------------------------------------------------------

section("7. VERIFICATION — SAMPLE JOINED QUERY")

sample = pd.read_sql_query("""
    SELECT
        t.town_name,
        d.district_name,
        c.county_name,
        t.population,
        hp.median_price,
        b.average_download_mbps,
        aq.pm25_total,
        cr.crimes_per_1000
    FROM towns t
    JOIN districts d ON t.district_id = d.district_id
    JOIN counties c ON d.county_id = c.county_id
    LEFT JOIN house_prices hp ON t.town_id = hp.town_id
    LEFT JOIN broadband b ON d.district_id = b.district_id
    LEFT JOIN air_quality aq ON d.district_id = aq.district_id
    LEFT JOIN crime cr ON t.town_id = cr.town_id
    ORDER BY c.county_name, t.town_name
""", conn)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 160)
print(sample.to_string(index=False))

conn.close()

section("STAGE 3 COMPLETE")
print(f"""
Database created at: {DB_PATH}

The joined query above should show all 20 towns with their district,
county, population, and — where available — median house price,
broadband speed, air quality, and crime rate.

Check specifically:
  - Chatham, Rochester, Gillingham should show IDENTICAL broadband
    and air quality figures (same district), but DIFFERENT house
    price and crime figures (town-level detail preserved).
  - Any blank/NaN cells likely mean a town had zero matching
    transactions or crime records — note these in the report.

Next: Stage 4 — exploratory data analysis on this database.
""")

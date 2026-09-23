# Stage 3: Building the Relational Database (3NF)

## Problem Statement
In Stages 1 and 2, we successfully collected, cleaned, and filtered four distinct datasets:
1. **House Prices** (Transaction level, mapped to towns)
2. **Broadband Speeds** (Aggregated at the Local Authority/District level)
3. **Air Quality** (Aggregated at the Local Authority/District level)
4. **Crime Rates** (Street-level, aggregated to towns)

The outputs were a set of flat CSV files. However, the project brief requires us to combine these into a proper relational database normalized to the **Third Normal Form (3NF)**.

A naïve approach would be to combine all this data into a single, massive spreadsheet-like table where each row represents a town. This creates a significant problem: **Redundancy**. Because multiple towns can share the same district (e.g., Chatham, Rochester, and Gillingham all belong to the Medway district), assigning district-level data (broadband and air quality) directly to the town level would mean duplicating identical values across multiple rows. This is a textbook violation of 3NF, where non-key attributes must depend *only* on the primary key.

## Solution Implemented
To solve this, we designed a relational schema that explicitly models the hierarchy of the geography (County -> District -> Town) and attaches the data to the correct level of granularity. We implemented this using Python's `sqlite3` library to build a SQLite database (`project.db`).

### Schema Design & 3NF Justification
We created 7 distinct tables:

1. **`counties`**: `county_id` (PK), `county_name`
   - *Why:* Prevents repeating the county name on every single town or district row.
2. **`districts`**: `district_id` (PK), `district_name`, `county_id` (FK)
   - *Why:* Acts as the structural anchor for district-level data.
3. **`towns`**: `town_id` (PK), `town_name`, `district_id` (FK), `population`
4. **`broadband`**: `district_id` (PK, FK), `median_download_mbps`, etc.
   - *Why:* Keyed to the district, not the town. This ensures the data is stored exactly once per district, removing the redundancy that would occur if we put it on the `towns` table.
5. **`air_quality`**: `district_id` (PK, FK), `pm25_total`, etc.
   - *Why:* Same reasoning as broadband; the data is published at the district level.
6. **`house_prices`**: `town_id` (PK, FK), `median_price`, etc.
   - *Why:* Keyed to the town, as we have specific property transactions for each town.
7. **`crime`**: `town_id` (PK, FK), `total_crimes`, `crimes_per_1000`, etc.
   - *Why:* Keyed to the town, as we mapped street-level crime to specific town LSOAs.

**How this achieves 3NF:**
* **1NF:** Every column holds a single atomic value.
* **2NF:** Every non-key column depends on the whole primary key.
* **3NF:** No non-key column depends on another non-key column. For example, county name is only reachable via `county_id` -> `counties` table. Broadband metrics depend strictly on the `district_id` and are not duplicated across towns.

## How We Built It (`stage3_build_database.py`)
We automated the database construction with a Python script executing the following steps:

1. **Database Initialization:** The script clears any existing `project.db` and uses `sqlite3` to execute DDL statements that create the 7 tables with strict Primary Key (PK) and Foreign Key (FK) constraints.
2. **Populating the Hierarchy:** Using our `TOWN_TO_DISTRICT` reference dictionary from Stage 1, the script populates the `counties`, `districts`, and `towns` tables, generating unique IDs for each.
3. **Loading District-Level Data:** We use `pandas` to read the filtered `broadband` and `air_quality` CSVs. The script matches the district names to fetch the correct `district_id` and inserts the rows.
4. **Loading Town-Level Data:**
   - **House Prices:** The script reads the filtered house price CSV. Because the raw data is transactional (multiple rows per town), we use pandas to aggregate the transactions, calculating the **median price** and transaction count per town before inserting.
   - **Crime:** We read the crime CSV (which was already aggregated to the town level in Stage 2b) and insert the records using the `town_id`.
5. **Verification:** The script concludes by running a massive `JOIN` query across all 7 tables. This verifies that the relational links work properly, proving that a town like Rochester correctly inherits Medway's broadband speed while retaining its own distinct house price data.

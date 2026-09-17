# Steps to Complete the Assignment

## Step 1: Pick Counties & Towns

### Choose Counties and Towns

Choose two counties in England and Wales. Pick counties where you can realistically find housing, broadband, and crime data, e.g. Kent and Powys, or Surrey and Gwynedd.

Then shortlist approximately 8–15 main towns per county.

Justify your selection method, for example:

> Select towns with a population greater than 10,000.
---

## Step 2: Gather the Datasets

### Collect the Required Data

Source data from Kaggle (required) plus the ONS Open Geography Portal for postcode/district lookups.

You need:

- UK house prices — HM Land Registry data via Kaggle
- Broadband speed — Ofcom data
- Crime data — Police.uk or a suitable mirror
- One additional factor of your choice:
  - Schools
  - Green space
  - Transport
  - Healthcare
  - Employment
  - etc.

---

## Step 3: Clean & Build a Data Model

### Clean the Data and Design the Database

You need to:

- Standardize column names
- Handle missing values
- Fix incorrect data types
- Remove or investigate duplicates
- Handle inconsistent town/district names
- Design a relational database schema
- Normalize the database to at least **3NF**
- Link tables using appropriate town/district IDs

For example, you could have separate tables for:

- `Towns`
- `HousePrices`
- `Broadband`
- `Crime`
- `ExtraFactors`

All tables should be appropriately linked using a town/district ID.

Load the cleaned data into a relational database such as:

- SQLite
- PostgreSQL

---

## Step 4: Exploratory Data Analysis

### Explore the Data

Use Python libraries such as:

- `pandas`
- `matplotlib`
- `seaborn`

Explore the datasets to:

- Understand the distributions
- Identify missing values
- Spot outliers
- Compare towns
- Compare the two counties
- Identify important patterns
- Visualize trends

Create appropriate charts and explain what each visualization shows.

---

## Step 5: Look for Correlations Between Variables

### Statistical Relationships

Investigate relationships between the different variables.

For example:

> Does higher broadband speed correlate with higher house prices?

Other possible questions include:

- Does crime rate correlate with house prices?
- Does the additional factor correlate with house prices?
- Are there noticeable relationships between different factors?

Use appropriate statistical methods, such as correlation analysis, and explain the results.

---

## Step 6: Build the Recommendation System

### Score and Rank the Towns

For each town:

1. Take the four selected characteristics.
2. Normalize each characteristic to a **0–10 scale**.
3. Combine the four scores using a suitable method, such as a weighted average.
4. Calculate an overall score for each town.
5. Rank the towns based on the overall score.
6. Display the **Top 3 towns**.

For example:

```text
Town       Price   Broadband   Crime   Extra   Overall
-------------------------------------------------------
Town A       8        7          9       8       8.1
Town B       7        9          8       7       7.8
Town C       9        6          7       8       7.6
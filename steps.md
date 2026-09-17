# Steps to The Assignment Complition

## Step 1
### Pick Counties & towns
#### Choose two counties in England and Wales. Pick counties where you can realistically find housing, broadbadn and crime data, eg Ket and Powys, or Surrey and Gwynedd. Then shortlist ~8-15 main towns per county (justify your selection method. e.g. towns with population > 10,000).

## Step 2
### Gather the datasets
#### Source data from kaggel (required) plus ONS Open Geography Portal for postcode/district lookups. You need: UK house prices (HM Land Registry via kaggle), broadband speed(Ofcom data), crime data(police.uk or mirror), and one extra factor of your choice( schools, green space, transport etc.).

## Step 3
### Clean & build a data model
#### Standardize column names, handle missing values, fix data types, and design a relational schema normalized to at least 3NF (e.g. separate tables for Towns, Houseprices, Broadband, Crime, ExtraFactors all linked by a town/district ID). Load into SQLite or PstgresSQL.

## Step 4
### Exploratory Data Analysis
#### Use pandas/matplotlib/seaboarn to explore distributions, spot outliers, compare towns, and visualize trends across your two counties

## Step 5
### Look for correlations between variables(eg: does higher broadband speed correalte with higher house prices?)

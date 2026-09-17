# The Assignment, in Plain Terms
## Your relatives wants to buy a home in England and Wales. You need to build a python system that recommends the best towns based on:
* #### House Prices
* #### Broadband speed
* #### Crime rate
* #### + One more factor you Choose and justify

### You will clean the data, put into a proper realational database(normalized to 3NF), explore it statistically, and build a simple scoring system (0-10 per factor) that ranks towns and shows **top 3**.
### Marks breakdown (100):
## Marks Breakdown (100 Total)

| Criteria | Marks |
|---|---:|
| Data gathering & justification | 10 |
| Cleaning/preprocessing/data model | 15 |
| EDA | 15 |
| Statistical methods | 15 |
| Recommendation system | 10 |
| Code quality | 10 |
| Legal/ethical discussion | 5 |
| Conclusions/reflection | 10 |
| Report quality | 10 |
| **Total** | **100** |



## 1. Data Gathering & Justification — 10 Marks

### What this means

You need to find appropriate datasets for the four factors used in your recommendation system.

The required factors are:

- House prices
- Broadband speed
- Crime rate
- One additional factor of your choice

You must explain where the data came from and why each dataset is suitable.

### What you should include

For every dataset, explain:

- The name of the dataset
- The source
- What the dataset measures
- The geographical level of the data
- The time period covered
- Important columns/variables
- Why the data is relevant to buying a home
- Any limitations of the dataset

For example:

### House Prices

You might use an official house-price dataset containing:

- Town/location
- Average or median house price
- Date/year
- Property type

You should explain why house prices matter.

For example:

"House price is included because affordability is an important consideration when choosing a town to purchase a home."

### Broadband Speed

You could use broadband data containing:

- Location
- Average download speed
- Average upload speed
- Coverage percentage

Explain why broadband matters, particularly for people working or studying from home.

### Crime Rate

The crime dataset could contain:

- Town/location
- Number of crimes
- Population
- Crime rate

You should be careful to distinguish between the raw number of crimes and crime rate.

A large town may naturally have more reported crimes simply because it has more residents.

### Fourth Factor

You must choose one additional factor and justify it.

Possible factors include:

- Distance to schools
- Air quality
- Employment
- Green space
- Healthcare access
- Public transport
- Average income
- Population density

The important part is not simply choosing a factor. You need to explain why it is useful for deciding where to buy a home.

### What earns marks

A strong submission should:

- Use reliable sources
- Prefer official or reputable datasets
- Clearly document sources
- Explain why each dataset was selected
- Make sure the datasets can actually be connected by geographical location
- Discuss limitations

### Common mistake

Do not simply write:

"Data was downloaded from the internet."

You need to identify the actual source and explain why it is appropriate.

---

# 2. Cleaning / Preprocessing / Data Model — 15 Marks

This section is worth 15 marks, so it is one of the most important parts of the project.

It has two major components:

1. Cleaning and preprocessing the data
2. Designing a proper relational database

---

## 2.1 Data Cleaning

Real-world datasets are rarely ready to use immediately.

You should identify and deal with problems such as:

- Missing values
- Duplicate records
- Incorrect data types
- Inconsistent town names
- Different spellings
- Invalid values
- Incorrect units
- Outliers
- Different date formats

For example:

One dataset might contain:

"Cambridge"

while another contains:

"CAMBRIDGE"

and another contains:

"Cambridge Town"

These may need to be standardized before the datasets can be joined.

---

## 2.2 Missing Values

You should identify missing values and decide how to handle them.

Possible approaches include:

- Removing records
- Replacing values using a justified method
- Using median/mean values where appropriate
- Keeping missing values and explaining why

You should not automatically replace every missing value with zero.

For example, if broadband speed is missing, setting it to `0 Mbps` would incorrectly suggest that the town has no broadband.

---

## 2.3 Data Types

Make sure columns have appropriate data types.

For example:

```python
house_price = 250000
crime_rate = 45.6
broadband_speed = 72.5
town = "Cambridge"
"""
Crime type grouping
--------------------
The raw police.uk data has 14 distinct "Crime type" values (confirmed
in Stage 1's sample output). For scoring towns later, 14 categories is
too granular — we group them into 3 broader categories that are easy
to reason about and to weight in the recommendation system.

Grouping choices are deliberately simple and are explained in the
report: they follow the same broad approach used in official crime
statistics (violent crime / acquisitive & property crime / other).
"""

CRIME_TYPE_GROUPS = {
    # Violent / personal crime
    "Violence and sexual offences": "Violent",
    "Robbery": "Violent",
    "Possession of weapons": "Violent",

    # Property / acquisitive crime
    "Burglary": "Property",
    "Vehicle crime": "Property",
    "Other theft": "Property",
    "Theft from the person": "Property",
    "Bicycle theft": "Property",
    "Shoplifting": "Property",
    "Criminal damage and arson": "Property",

    # Everything else
    "Anti-social behaviour": "Other",
    "Public order": "Other",
    "Drugs": "Other",
    "Other crime": "Other",
}

def group_crime_type(raw_crime_type: str) -> str:
    """Map a raw 'Crime type' string to one of Violent / Property / Other.
    Anything not in the mapping (e.g. a new category police.uk adds
    later) falls back to 'Other' rather than crashing the pipeline,
    but this is printed as a warning so it doesn't go unnoticed.
    """
    if raw_crime_type in CRIME_TYPE_GROUPS:
        return CRIME_TYPE_GROUPS[raw_crime_type]
    print(f"WARNING: unrecognised crime type '{raw_crime_type}' -> grouped as 'Other'")
    return "Other"

if __name__ == "__main__":
    print("Crime type grouping:")
    for group in ["Violent", "Property", "Other"]:
        types_here = [t for t, g in CRIME_TYPE_GROUPS.items() if g == group]
        print(f"\n{group}:")
        for t in types_here:
            print(f"  - {t}")




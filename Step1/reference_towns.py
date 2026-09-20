"""
Stage 2 — Reference data: Town -> District mapping
-----------------------------------------------------
This is the single source of truth for which District each of our 20
towns belongs to. All four datasets get filtered using this mapping,
so we only have to get it right in one place.

Important: several Kent towns share the same District. For example,
Chatham, Rochester and Gillingham are all in the Medway district.
That means when we filter by District, we will sometimes pull in a
slightly wider area than the town itself — this is expected, and is
worth noting as a limitation in the report (see note at bottom).
"""

# Kent towns -> Kent District (or unitary authority) name, as used by
# ONS/Ofcom/Defra local authority data (laua_name / Local Authority).
KENT_TOWN_TO_DISTRICT = {
    "MAIDSTONE": "MAIDSTONE",
    "GILLINGHAM": "MEDWAY",
    "DARTFORD": "DARTFORD",
    "CHATHAM": "MEDWAY",
    "ASHFORD": "ASHFORD",
    "ROCHESTER": "MEDWAY",
    "MARGATE": "THANET",
    "ROYAL TUNBRIDGE WELLS": "TUNBRIDGE WELLS",
    "GRAVESEND": "GRAVESHAM",
    "CANTERBURY": "CANTERBURY",
    "FOLKESTONE": "FOLKESTONE AND HYTHE",
    "SITTINGBOURNE": "SWALE",
    "DOVER": "DOVER",
    "RAMSGATE": "THANET",
    "TONBRIDGE": "TONBRIDGE AND MALLING",
}

# Monmouthshire towns all share the same single unitary authority.
MONMOUTHSHIRE_TOWN_TO_DISTRICT = {
    "ABERGAVENNY": "MONMOUTHSHIRE",
    "CHEPSTOW": "MONMOUTHSHIRE",
    "CALDICOT": "MONMOUTHSHIRE",
    "MONMOUTH": "MONMOUTHSHIRE",
    "USK": "MONMOUTHSHIRE",
}

TOWN_TO_DISTRICT = {**KENT_TOWN_TO_DISTRICT, **MONMOUTHSHIRE_TOWN_TO_DISTRICT}

# The set of District names we filter broadband/air-quality/crime data
# to. Built automatically from the mapping above so it can't drift out
# of sync — Medway only appears once even though 3 towns map to it.
SELECTED_DISTRICTS = sorted(set(TOWN_TO_DISTRICT.values()))

# For house price filtering, we match on the "District" column of the
# HM Land Registry data using this same set of names.

# For crime filtering, we only need the two police forces, since crime
# data doesn't come with a District column — LSOA names contain the
# town name instead (see stage2_filter_crime.py).
KENT_POLICE_FORCE = "Kent Police"
GWENT_POLICE_FORCE = "Gwent Police"

# For matching crime records to specific towns, we use LSOA name
# prefixes (e.g. "Maidstone 001A" -> Maidstone). LSOA names generally
# follow the local authority District name, not the individual town
# name, EXCEPT where the town IS the district (e.g. "Maidstone 001A"
# works because Maidstone town and Maidstone district share a name).
#
# For Medway and Thanet, whose LSOAs are named after the district
# ("Medway 001A", "Thanet 001A") rather than the individual towns
# within them, we cannot separate Chatham from Rochester from
# Gillingham using LSOA name alone. This mirrors the same limitation
# already noted for broadband/air quality: those three towns share a
# single crime figure too, derived from all Medway LSOAs combined.
# The same applies to Margate and Ramsgate within Thanet.
TOWN_TO_LSOA_PREFIX = {
    "MAIDSTONE": "MAIDSTONE",
    "ASHFORD": "ASHFORD",
    "CANTERBURY": "CANTERBURY",
    "DARTFORD": "DARTFORD",
    "DOVER": "DOVER",
    "GRAVESEND": "GRAVESHAM",
    "SITTINGBOURNE": "SWALE",
    "FOLKESTONE": "FOLKESTONE AND HYTHE",
    "ROYAL TUNBRIDGE WELLS": "TUNBRIDGE WELLS",
    "TONBRIDGE": "TONBRIDGE AND MALLING",
    # Shared-district towns: LSOA prefix is the district name, so these
    # three all match the same LSOAs and will carry identical crime
    # figures, same as their broadband/air quality figures.
    "CHATHAM": "MEDWAY",
    "ROCHESTER": "MEDWAY",
    "GILLINGHAM": "MEDWAY",
    # Shared-district towns: Thanet
    "MARGATE": "THANET",
    "RAMSGATE": "THANET",
    # Monmouthshire towns: LSOA naming in Wales generally follows the
    # same district-name pattern.
    "ABERGAVENNY": "MONMOUTHSHIRE",
    "CHEPSTOW": "MONMOUTHSHIRE",
    "CALDICOT": "MONMOUTHSHIRE",
    "MONMOUTH": "MONMOUTHSHIRE",
    "USK": "MONMOUTHSHIRE",
}

if __name__ == "__main__":
    print("Town -> District mapping:")
    for town, district in TOWN_TO_DISTRICT.items():
        print(f"  {town:<25} -> {district}")

    print(f"\n{len(SELECTED_DISTRICTS)} unique Districts covering {len(TOWN_TO_DISTRICT)} towns:")
    for d in SELECTED_DISTRICTS:
        towns_here = [t for t, dist in TOWN_TO_DISTRICT.items() if dist == d]
        print(f"  {d:<25} <- {', '.join(towns_here)}")

    print("""
NOTE FOR THE REPORT:
Medway (Chatham, Rochester, Gillingham) and Thanet (Margate, Ramsgate)
each cover more than one of our selected towns. This means broadband
and air quality figures for these towns will be identical, since
those datasets are only available at District/unitary-authority level.
House prices and crime can still be told apart within a shared
district, since those datasets carry town-level or LSOA-level detail.
""")

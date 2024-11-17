import os
import glob
import pandas as pd
from rdflib import Graph, Namespace, Literal, RDF, URIRef
from rdflib.namespace import XSD, DCTERMS
import urllib.parse

# Define namespaces
EX = Namespace("https://sanctions.streamlit.app/ns#")
QB = Namespace("http://purl.org/linked-data/cube#")
WIKIDATA = Namespace("http://www.wikidata.org/entity/")
GR = Namespace("http://purl.org/goodrelations/v1#")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
PROV = Namespace("http://www.w3.org/ns/prov#")

# Initialize graph
g = Graph()
g.bind("ex", EX)
g.bind("qb", QB)
g.bind("dct", DCTERMS)
g.bind("wikidata", WIKIDATA)
g.bind("gr", GR)
g.bind("dcat", DCAT)
g.bind("prov", PROV)

# Define the folder path where the CSV files are stored
folder_path = 'data/armenia_export_eurostat'

# Create an empty DataFrame to store combined data
combined_df = pd.DataFrame()

# Loop through all CSV files in the folder and append them to the combined DataFrame
for file in glob.glob(os.path.join(folder_path, '*.csv')):
    df = pd.read_csv(file)
    combined_df = pd.concat([combined_df, df], ignore_index=True)

print(combined_df)

# Function to map country names to Wikidata URIs
def get_country_uri(country_name):
    country_map = {
        "Austria": WIKIDATA['Q40'],
        "Belgium (incl. Luxembourg 'LU' -> 1998)": WIKIDATA['Q31'],
        "Bulgaria": WIKIDATA['Q219'],
        "Croatia": WIKIDATA['Q224'],
        "Cyprus": WIKIDATA['Q229'],
        "Czechia": WIKIDATA['Q213'],
        "Denmark": WIKIDATA['Q35'],
        "Estonia": WIKIDATA['Q191'],
        "Finland": WIKIDATA['Q33'],
        "France (incl. Saint Barthélemy 'BL' -> 2012; incl. French Guiana 'GF', Guadeloupe 'GP', Martinique 'MQ', Réunion 'RE' from 1997; incl. Mayotte 'YT' from 2014)": WIKIDATA['Q142'],
        "Germany (incl. German Democratic Republic 'DD' from 1991)": WIKIDATA['Q183'],
        "Greece": WIKIDATA['Q41'],
        "Hungary": WIKIDATA['Q28'],
        "Ireland (Eire)": WIKIDATA['Q27'],
        "Italy (incl. San Marino 'SM' -> 1993)": WIKIDATA['Q38'],
        "Latvia": WIKIDATA['Q211'],
        "Lithuania": WIKIDATA['Q37'],
        "Luxembourg": WIKIDATA['Q32'],
        "Netherlands": WIKIDATA['Q55'],
        "Poland": WIKIDATA['Q36'],
        "Portugal": WIKIDATA['Q45'],
        "Romania": WIKIDATA['Q218'],
        "Slovakia": WIKIDATA['Q214'],
        "Slovenia": WIKIDATA['Q215'],
        "Spain (incl. Canary Islands 'XB' from 1997)": WIKIDATA['Q29'],
        "Sweden": WIKIDATA['Q34'],
        "Euro area (AT-01/1999, BE-01/1999, CY-01/2008, DE-01/1999, EE-01/2011, ES-01/1999, FI-01/1999, FR-01/1999, GR-01/2001, HR-01/2023, IE-01/1999, IT-01/1999, LT-01/2015, LU-01/1999, LV-01/2014, MT-01/2008, NL-01/1999, PT-01/1999, SI-01/2007, SK-01/2009)": WIKIDATA['Q25127'],
        "Euro area - 20 countries (AT, BE, CY, DE, EE, ES, FI, FR, GR, HR, IE, IT, LT, LU, LV, MT, NL, PT, SI, SK)": WIKIDATA['Q25127'],
        "European Union (AT-01/1995, BE-01/1958, BG-01/2007, CY-05/2004, CZ-05/2004, DE-01/1958, DK-01/1973, EE-05/2004, ES-01/1986, FI-01/1995, FR-01/1958, GB-01/1973->01/2020, GR-01/1981, HR-07/2013, HU-05/2004, IE-01/1973, IT-01/1958, LT-05/2004, LU-01/1958, LV-05/2004, MT-05/2004, NL-01/1958, PL-05/2004, PT-01/1986, RO-01/2007, SE-01/1995, SI-05/2004, SK-05/2004)": WIKIDATA['Q458'],
        "European Union - 27 countries (AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK)": WIKIDATA['Q458'],
        "Russia": WIKIDATA['Q159'],
        "Armenia": WIKIDATA['Q399'],
        "Kazakhstan": WIKIDATA['Q232'],
        "Kyrgyzstan": WIKIDATA['Q813'],
        "Georgia": WIKIDATA['Q230']
    }
    return country_map.get(country_name, URIRef(EX + "country/" + urllib.parse.quote(country_name.replace(' ', '_'))))

# Define catalog and dataset URIs
catalog_uri = EX["catalog"]
dataset_uri = EX["dataset/eurostat_exports"]

# Add catalog metadata
g.add((catalog_uri, RDF.type, DCAT.Catalog))
g.add((catalog_uri, DCTERMS.title, Literal("EU Export Dataset Catalog", datatype=XSD.string)))
g.add((catalog_uri, DCTERMS.description, Literal("A catalog of datasets representing EU export information.", datatype=XSD.string)))
g.add((catalog_uri, DCTERMS.publisher, WIKIDATA["Q458"]))  # Assuming EU as publisher
g.add((catalog_uri, DCAT.dataset, dataset_uri))

# Add dataset metadata
g.add((dataset_uri, RDF.type, DCAT.Dataset))
g.add((dataset_uri, DCTERMS.title, Literal("EU Export Data for Various Countries", datatype=XSD.string)))
g.add((dataset_uri, DCTERMS.description, Literal("This dataset contains export data from the European Union to multiple countries, covering 2022-2024.", datatype=XSD.string)))
g.add((dataset_uri, DCTERMS.creator, WIKIDATA["Q458"]))
g.add((dataset_uri, DCTERMS.issued, Literal("2024-11-17", datatype=XSD.date)))
g.add((dataset_uri, DCTERMS.temporal, Literal("2019-01 to 2024-12", datatype=XSD.string)))
g.add((dataset_uri, DCTERMS.spatial, WIKIDATA["Q458"]))  # Representing the EU
g.add((dataset_uri, DCAT.distribution, URIRef("https://sanctions.streamlit.app/data/ttl/eurostat_data.ttl")))
license_uri = URIRef("https://creativecommons.org/licenses/by/4.0/")
g.add((dataset_uri, DCTERMS.license, license_uri))

# Iterate over rows
for idx, row in combined_df.iterrows():
    print(row)
    obs_uri = EX[f'observation{idx+1}']
    g.add((obs_uri, RDF.type, QB.Observation))

    # Use standard URIs where possible
    reporter_uri = get_country_uri(row['REPORTER'])
    partner_uri = get_country_uri(row['PARTNER'])
    flow_uri = URIRef(GR['Sell']) if row['FLOW'] == 'EXPORT' else URIRef(GR['Buy'])  # Use GoodRelations to denote type of action

    # Add triples to the graph
    g.add((obs_uri, EX.reporter, reporter_uri))
    g.add((obs_uri, EX.partner, partner_uri))
    g.add((obs_uri, EX.flow, flow_uri))
    g.add((dataset_uri, DCAT.hasPart, obs_uri))  # Link dataset to observation

    # Convert period to xsd:gYearMonth format
    try:
        period = pd.to_datetime(row['PERIOD'], errors='coerce').strftime('%Y-%m')
        if pd.isna(period):
            raise ValueError(f"Invalid date format for PERIOD: {row['PERIOD']}")
        g.add((obs_uri, EX.period, Literal(period, datatype=XSD.gYearMonth)))
    except Exception as e:
        print(f"Error parsing date: {e}")

    # Add the value in EUR
    try:
        value = float(row['VALUE_IN_EUR'])
        g.add((obs_uri, EX.valueInEUR, Literal(value, datatype=XSD.decimal)))
    except ValueError:
        print(f"Invalid VALUE_IN_EUR: {row['VALUE_IN_EUR']}")

# Serialize the graph to Turtle format
print(g.serialize(format='turtle'))

# Save graph to file
g.serialize(destination='data/ttl/eurostat_data.ttl', format='turtle')

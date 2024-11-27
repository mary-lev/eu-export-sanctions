import streamlit as st
from rdflib import Graph

st.set_page_config(page_title="RDF Metadata and Validation", page_icon="🌍", layout="wide")

def load_rdf_metadata(file_path):
    g = Graph()
    g.parse(file_path, format='turtle')
    return g

with st.sidebar:
    st.markdown('''
    ### About
    This project hypothesizes 
    that Russia is circumventing EU sanctions 
    by increasing trade through intermediary countries 
    such as Kyrgyzstan and Armenia, 
    which is reflected in anomalous trade data patterns post-2022.
    ''')

st.title("RDF Assertion of the Metadata")

st.markdown("""
This page provides RDF metadata for the EU Export Insights project. You can view the metadata in Turtle format, download it, and explore how the project and datasets are described.
""")

tab1, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Dataset in Turtle",
    "Download Options",
    "Validation"
])

# ------------------- Overview Tab -------------------
with tab1:
    st.header("Overview")
    st.write("""
    The RDF metadata and combined dataset are structured to align with the DCAT-AP standard, providing semantic descriptions of the project and data. 
    The metadata can be downloaded in Turtle and JSON-LD formats for integration with other systems.
    """)

    st.header("RDF Metadata in Turtle Format")

    file_path = 'data/ttl/eurostat_metadata.ttl'
    metadata_graph = load_rdf_metadata(file_path)
    rdf_metadata_turtle = metadata_graph.serialize(format='turtle')

    st.text_area("Turtle Representation", rdf_metadata_turtle, height=500)

# ------------------- Dataset in Turtle Tab -------------------
with tab3:
    st.header("RDF Dataset in Turtle Format")

    file_path_dataset = 'data/ttl/eurostat_data.ttl'
    dataset_graph = load_rdf_metadata(file_path_dataset)

    rdf_dataset_turtle = dataset_graph.serialize(format='turtle')

    st.text_area("Turtle Representation of Dataset", rdf_dataset_turtle, height=500)

# ------------------- Download Options Tab -------------------
with tab4:
    st.header("Download Options")
    st.write("You can download the metadata and dataset in Turtle and JSON-LD formats below.")

    st.download_button(
        label="Download RDF Metadata (Turtle)",
        data=rdf_metadata_turtle,
        file_name='eurostat_metadata.ttl',
        mime='text/turtle'
    )

    rdf_metadata_jsonld = metadata_graph.serialize(format='json-ld')
    st.download_button(
        label="Download RDF Metadata (JSON-LD)",
        data=rdf_metadata_jsonld,
        file_name='eurostat_metadata.json',
        mime='application/ld+json'
    )

    st.download_button(
        label="Download RDF Dataset (Turtle)",
        data=rdf_dataset_turtle,
        file_name='eurostat_data.ttl',
        mime='text/turtle'
    )

    rdf_dataset_jsonld = dataset_graph.serialize(format='json-ld')
    st.download_button(
        label="Download RDF Dataset (JSON-LD)",
        data=rdf_dataset_jsonld,
        file_name='eurostat_data.json',
        mime='application/ld+json'
    )

# ------------------- Validation Tab -------------------
with tab5:
    st.header("Validation")
    st.write("The dataset and metadata were validated using the [DCAT-AP validator](https://www.itb.ec.europa.eu/shacl/dcat-ap/upload). Below are the validation results.")
    
    st.image("images/validation.png", caption="DCAT-AP Dataset Validation Results", width=600)
    st.image("images/metadata_validation.png", caption="DCAT-AP Metadata Validation Report", width=600)

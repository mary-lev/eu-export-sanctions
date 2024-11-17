import streamlit as st
from rdflib import Graph

st.set_page_config(page_title="RDF Assertion of the Metadata", page_icon="🌍", layout="wide")

# Load RDF metadata
def load_rdf_metadata(file_path):
    g = Graph()
    g.parse(file_path, format='turtle')
    return g

# Add sidebar
with st.sidebar:
    st.markdown('''
    ### About
    This project hypothesizes 
    that Russia is circumventing EU sanctions 
    by increasing trade through intermediary countries 
    such as Kyrgyzstan and Armenia, 
    which is reflected in anomalous trade data patterns post-2022.
    ''')
    

# Streamlit App for "RDF Assertion of the Metadata"
st.title("RDF Assertion of the Metadata")

st.markdown("""
This page provides RDF metadata for the EU Export Insights project. You can view the metadata in Turtle format, download it, and explore how the project and datasets are described.
""")

# Load the RDF graph
file_path = 'data/ttl/eurostat_metadata.ttl'  # Change the path to load only metadata
metadata_graph = load_rdf_metadata(file_path)

# Serialize the graph to Turtle format
rdf_metadata_turtle = metadata_graph.serialize(format='turtle')

# Display the RDF Metadata in the Streamlit App
st.subheader("RDF Metadata in Turtle Format")
st.text_area("Turtle Representation", rdf_metadata_turtle, height=500)

# Provide a download button for the RDF metadata
st.download_button(
    label="Download RDF Metadata",
    data=rdf_metadata_turtle,
    file_name='eurostat_metadata.ttl',
    mime='text/turtle'
)

# Load the entire RDF dataset graph for download
file_path_dataset = 'data/ttl/eurostat_data.ttl'
dataset_graph = load_rdf_metadata(file_path_dataset)

# Serialize the entire dataset to Turtle format
rdf_dataset_turtle = dataset_graph.serialize(format='turtle')

# Provide a download button for the entire RDF dataset
st.download_button(
    label="Download Complete Dataset in RDF (TTL)",
    data=rdf_dataset_turtle,
    file_name='eurostat_data.ttl',
    mime='text/turtle'
)

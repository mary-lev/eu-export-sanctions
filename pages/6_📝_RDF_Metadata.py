import streamlit as st
from rdflib import Graph

# Load RDF metadata
def load_rdf_metadata(file_path):
    g = Graph()
    g.parse(file_path, format='turtle')
    return g

# Streamlit App for "RDF Assertion of the Metadata"
st.title("RDF Assertion of the Metadata")

st.markdown("""
This page provides RDF metadata for the EU Export Insights project. You can view the metadata in Turtle format, download it, and explore how the project and datasets are described.
""")

# Load the RDF graph
file_path = 'data/ttl/eurostat_data.ttl'
g = load_rdf_metadata(file_path)

# Serialize the graph to Turtle format
rdf_turtle = g.serialize(format='turtle')

# Display the RDF in the Streamlit App
st.subheader("RDF Metadata in Turtle Format")
st.text_area("Turtle Representation", rdf_turtle, height=500)

# Provide a download button for the RDF metadata
st.download_button(
    label="Download RDF Metadata",
    data=rdf_turtle,
    file_name='eurostat_data_metadata.ttl',
    mime='text/turtle'
)

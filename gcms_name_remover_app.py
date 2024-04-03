import streamlit as st
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_trf")

PLACEHOLDER = "[NAME REMOVED]"

def remove_names(text):
    # Process the text through spaCy to find named entities
    doc = nlp(text)
    # Iterate over detected entities in reverse order to avoid indexing issues when replacing
    for ent in reversed(doc.ents):
        # Check if the entity is a person's name
        if ent.label_ == "PERSON":
            # Replace the entity with the placeholder
            text = text[:ent.start_char] + PLACEHOLDER + text[ent.end_char:]
    return text

# Streamlit app layout
st.title("Name Remover App")

# User input
user_input = st.text_area("Enter your text here:", height=150)
process_text = st.button("Remove Names")

if process_text:
    cleaned_text = remove_names(user_input)
    st.markdown("## Processed Text")
    st.write(cleaned_text)

import streamlit as st
import spacy
import re
import subprocess
import sys

# Hardcoded model name
MODEL_NAME = "en_core_web_trf"

# Attempt to load the spaCy model, download if not available
try:
    nlp = spacy.load(MODEL_NAME)
except OSError:
    print(f"{MODEL_NAME} not found, downloading...")
    # Download the spaCy model using subprocess
    subprocess.run([sys.executable, "-m", "spacy", "download", MODEL_NAME], check=True)
    nlp = spacy.load(MODEL_NAME)

PLACEHOLDER = "[NAME REMOVED]"

def clean_text(text):
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    text = re.sub(r'![.*?](.*?)', '', text)  # Corrected Markdown images pattern
    text = re.sub(r'<img.*?>', '', text)  # HTML <img> tags
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,}\b', '', text)
    return text

def remove_names(text):
    doc = nlp(text)
    for ent in reversed(doc.ents):
        if ent.label_ == "PERSON":
            text = text[:ent.start_char] + PLACEHOLDER + text[ent.end_char:]
    return text

def preprocess_and_remove_names(text):
    cleaned_text = clean_text(text)
    return remove_names(cleaned_text)

st.set_page_config(layout="wide")
st.title("Text Cleaner App")

st.sidebar.header("What does this app clean?")
st.sidebar.markdown("""
- **URLs**: Removes http and https links.
- **Email Addresses**: Removes email addresses.
- **Image Tags/References**: Removes HTML `<img>` tags and Markdown image references.
- **Names**: Replaces names with a placeholder.
  
**Example**:
- Input: `Dr. John Smith's email is john.smith@example.com. Check out https://example.com`
- Output: `[NAME REMOVED]'s email is . Check out `
""")

user_input = st.text_area("Enter your comment(s) here:", height=150)
clean_option = st.button("Clean Text")

if clean_option:
    cleaned_text = preprocess_and_remove_names(user_input)
    st.markdown("## Cleaned Text")
    st.write(cleaned_text)

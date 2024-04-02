import torch
import streamlit as st
import spacy
import re
import subprocess
import sys

# Set PyTorch to use CPU explicitly to avoid device mismatch errors
torch.set_default_tensor_type('torch.FloatTensor')

def download_spacy_model(model_name):
    try:
        subprocess.run([sys.executable, "-m", "spacy", "download", model_name], check=True)
    except subprocess.CalledProcessError as e:
        st.error(f"Failed to download {model_name}: {e}")

MODEL_NAME = "en_core_web_trf"
try:
    nlp = spacy.load(MODEL_NAME)
except OSError:
    st.info(f"{MODEL_NAME} not found, downloading...")
    download_spacy_model(MODEL_NAME)
    nlp = spacy.load(MODEL_NAME)

PLACEHOLDER = "[NAME REMOVED]"

def clean_text(text):
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    # Remove image tags or Markdown image references
    text = re.sub(r'![.*?](.*?)', '', text)  # Corrected Markdown images pattern
    text = re.sub(r'<img.*?>', '', text)  # HTML <img> tags
    # Remove emails
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
st.markdown("## *Text Cleaner App*")

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

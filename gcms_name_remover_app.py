import streamlit as st
import spacy
import re

# Load the spaCy model
nlp = spacy.load("en_core_web_lg")

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

def clean_text(text):
    """
    Cleans the text by removing URLs, hyperlinks, Markdown image references,
    HTML <img> tags, emails, mailto links, text within square brackets, dangling brackets,
    and any leftover angle brackets.
    """
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    text = re.sub(r'www\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'<img.*?>', '', text)
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
    # Remove "mailto:" links and any following email address.
    text = re.sub(r'mailto:[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', '', text)
    # Improved removal for mailto links without specifying the email directly after mailto:
    text = re.sub(r'mailto:[^\s>]*', '', text)  # Removes mailto: followed by any character that is not a space or '>'
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\[$', '', text)
    # Remove any leftover angle brackets
    text = re.sub(r'<[^>]*>', '', text)  # Removes content within angle brackets and the brackets themselves
    return text

def remove_names(text):
    """
    Removes names identified by the spaCy model from the text, replacing them with a placeholder.
    """
    doc = nlp(text)
    for ent in reversed(doc.ents):
        if ent.label_ == "PERSON":
            text = text[:ent.start_char] + PLACEHOLDER + text[ent.end_char:]
    return text

def preprocess_and_remove_names(text):
    """
    Preprocesses the text by cleaning it and removing names, also returns the original
    and cleaned text lengths and the percentage reduction.
    """
    original_len = len(text.split())
    cleaned_text = clean_text(text)
    cleaned_len = len(cleaned_text.split())
    percentage_reduction = 100 * (1 - (cleaned_len / original_len if original_len > 0 else 0))
    no_names_text = remove_names(cleaned_text)
    return no_names_text, original_len, cleaned_len, percentage_reduction

# Streamlit app setup and layout configuration.
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
    cleaned_text, original_len, cleaned_len, percentage_reduction = preprocess_and_remove_names(user_input)
    st.markdown("## Cleaned Text")
    st.write(cleaned_text)
    st.markdown(f"**Original Length:** {original_len} words")
    st.markdown(f"**Cleaned Length:** {cleaned_len} words")
    st.markdown(f"**Reduction:** {percentage_reduction:.2f}%")

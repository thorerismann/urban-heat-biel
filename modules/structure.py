import streamlit as st
from pathlib import Path

CONTENT_DIR = Path.cwd() / "content"

def main_display():
    st.title("Hot Biel Summer")

    # Language options with file mappings
    LANGUAGES = {
        "English": CONTENT_DIR / "welcome.md",
        "Français": CONTENT_DIR / "bienvenue.md",
        "Deutsch": CONTENT_DIR / "wilkomen.md",
    }
    st.text('This app visualizes the UHI data available for Biel/Bienne from the summer 2023 measurement campaign. Expand below for more information.')
    selected_language = st.selectbox(
        "Select Language / Choisissez la langue / Sprache wählen",
        options=['None'] + list(LANGUAGES.keys()),
        index=0,
        key='main_language'# Default to English
    )

    # Load and display the selected language's markdown content
    if selected_language == "None":
        return
    else:
        markdown_file = LANGUAGES[selected_language]
        markdown_content = load_markdown(markdown_file)
        st.markdown(markdown_content)

def load_markdown(file_path: Path) -> str:
    """
    Load the content of a markdown file.

    Parameters
    ----------
    file_path : Path
        Path to the markdown file.

    Returns
    -------
    str
        Content of the markdown file as a string.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: {file_path.name} not found."



def fitnah_explanation():
    LANGUAGES = {
        "English": CONTENT_DIR / "fitnah_english.md",
        "Français": CONTENT_DIR / "fitnah_french.md",
        "Deutsch": CONTENT_DIR / "fitnah_german.md",
    }
    selected_language = st.selectbox(
        "Select Language / Choisissez la langue / Sprache wählen",
        options=['None'] + list(LANGUAGES.keys()),
        index=0,
        key = 'fitnah_language'
    )
    if selected_language == "None":
        return
    else:
        markdown_file = LANGUAGES[selected_language]
        markdown_content = load_markdown(markdown_file)
        st.markdown(markdown_content)

def uhi_explanation():
    LANGUAGES = {
        "English": CONTENT_DIR / "uhi_english.md",
        "Français": CONTENT_DIR / "uhi_french.md",
        "Deutsch": CONTENT_DIR / "uhi_german.md",
    }
    selected_language = st.selectbox(
        "Select Language / Choisissez la langue / Sprache wählen",
        options=['None'] + list(LANGUAGES.keys()),
        index=0,
        key='uhi_language'
    )
    if selected_language == "None":
        return
    else:
        markdown_file = LANGUAGES[selected_language]
        markdown_content = load_markdown(markdown_file)
        st.markdown(markdown_content)

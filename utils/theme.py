# utils/theme.py

import streamlit as st

def apply_theme():
    dark_mode = st.session_state.get("dark_mode", False)
    if dark_mode:
        image_url = "https://lamanne-paris.fr/wp-content/uploads/2021/07/astuces-ruiner-2048x1234.jpeg"
        overlay_color = "rgba(0, 0, 0, 0.7)"
        text_color = "#ffffff"
        box_bg_color = "rgba(0, 0, 0, 0.6)"
        button_bg = "#222831"
        button_text = "#ffffff"
        button_hover_bg = "#e6b78e4c"
        button_hover_text = "#222"
    else:
        image_url = "https://lamanne-paris.fr/wp-content/uploads/2021/07/astuces-ruiner-2048x1234.jpeg"
        overlay_color = "rgba(255, 255, 255, 0.5)"
        text_color = "#000000"
        box_bg_color = "rgba(255, 255, 255, 0.85)"
        button_bg = "#ffffffff"
        button_text = "#222"
        button_hover_bg = "#e6b78e4c"
        button_hover_text = "#222"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient({overlay_color}, {overlay_color}),
                        url("{image_url}");
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-position: center;
        }}

        .stApp > div:first-child {{
            background-color: {box_bg_color};
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
        }}

        [data-testid="stMarkdownContainer"],
        [data-testid="stHeader"],
        [data-testid="stText"],
        [data-testid="stTitle"],
        [data-testid="stSubheader"],
        [data-testid="stCaption"],
        [data-testid="stExpander"],
        [data-testid="stForm"],
        .stMarkdown, .stText, .stTitle, .stSubheader {{
            color: {text_color} !important;
        }}

        div[data-testid="stAlert"] {{
            background-color: rgba(255, 0, 0, 0.2) !important;
            border-left: none !important;
            color: {text_color} !important;
        }}

        input, textarea, select {{
            color: {text_color} !important;
        }}

        .stDataFrame, .stTable {{
            color: {text_color} !important;
        }}

        /* BUTTONS */
        .stButton > button {{
            color: {button_text} !important;
            background-color: {button_bg} !important;
            border: 1.5px solid #ffb08533 !important;
            font-weight: 700 !important;
            transition: 0.2s;
        }}
        .stButton > button:hover {{
            background-color: {button_hover_bg} !important;
            color: {button_hover_text} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
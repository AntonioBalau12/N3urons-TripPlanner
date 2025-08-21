def get_styles(colors):
    """Returnează CSS-ul responsive + blobs animate pe fundal"""
    return f"""
    <style>
    :root {{
        --primary-color: {colors['primary']};
        --background-color: {colors['background']};
        --secondary-background-color: {colors['secondary']};
        --text-color: {colors['text']};
        --font: {colors['font']};
    }}

    .stApp {{
        background-color: var(--background-color);
        color: var(--text-color);
        font-family: var(--font);
        z-index: 0;
    }}

    .header-container {{
        display: flex;
        align-items: center;
        justify-content: start;
        background-color: {colors['primary']};
        padding: 10px 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        flex-wrap: wrap;
        z-index: auto;
    }}

    .header-container img {{
        width: 50px;
        height: auto;
        border-radius: 50%;
        margin-right: 20px;
    }}

    .header-container h1 {{
        color: white;
        margin: 0;
        font-size: 2rem;
    }}

    .stButton>button {{
        background-color: var(--primary-color);
        color: white;
        border-radius: 5px;
        border: none;
        transition: 0.3s;
        width: 100%;
    }}

    .stButton>button:hover {{
        background-color: {colors['accent']};
    }}

    .stTextInput>div>div>input, 
    .stTextArea>div>textarea {{
        background-color: {colors['secondary']};
        color: var(--text-color);
        border-radius: 5px;
        border: 1px solid {colors['primary']};
    }}

    .custom-dropdown {{
        position: relative;
        display: inline-block;
        width: 100%;
        margin-bottom: 15px;
    }}

    .custom-dropdown select {{
        background-color: {colors['secondary']};
        color: var(--text-color);
        padding: 10px 15px;
        border: 1px solid {colors['primary']};
        border-radius: 5px;
        width: 100%;
        font-size: 16px;
        appearance: none;
        -webkit-appearance: none;
        -moz-appearance: none;
        cursor: pointer;
    }}

    .custom-dropdown select:hover {{
        border-color: {colors['accent']};
    }}

    .rating-container {{
        background-color: {colors['secondary']};
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }}

    .rating-stars {{
        font-size: 24px;
        color: {colors['accent']};
        margin: 10px 0;
    }}

    .rating-stars .star {{
        cursor: pointer;
        transition: all 0.2s;
    }}

    .rating-stars .star:hover {{
        transform: scale(1.2);
    }}

    .rating-recommendation {{
        font-style: italic;
        color: {colors['text']};
    }}

    /* Responsive */
    @media (max-width: 768px) {{
        .rating-container {{
            padding: 10px;
        }}

        .rating-stars {{
            font-size: 20px;
        }}

        .custom-dropdown select {{
            padding: 8px 12px;
            font-size: 14px;
        }}

        .header-container {{
            justify-content: center;
            text-align: center;
            padding: 10px;
            z-index: auto;
        }}

        .header-container img {{
            margin-right: 0;
            margin-bottom: 10px;
        }}

        .header-container h1 {{
            font-size: 1.5rem;
            width: 100%;
        }}

        .stButton>button {{
            padding: 0.5rem;
        }}

        .stTextInput>div>div>input, 
        .stTextArea>div>textarea {{
            font-size: 14px;
        }}
    }}
    </style>

    """

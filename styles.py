import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styles."""
    st.markdown("""
        <style>
        .main {
            padding: 1rem;
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            background-color: #FF5733;
            color: white;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        .settings-btn {
            position: fixed;
            top: 1rem;
            right: 1rem;
        }
        .qr-container {
            display: flex;
            justify-content: center;
            margin: 2rem 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .stTextInput>div>div>input {
            border-radius: 5px;
        }
        .history-item {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            border-left: 5px solid #FF5733;
            transition: all 0.3s ease;
        }
        .history-item:hover {
            transform: translateX(5px);
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .history-amount {
            color: #FF5733;
            font-size: 1.2em;
            font-weight: bold;
        }
        .history-upi {
            color: #6c757d;
            font-size: 0.9em;
            text-align: right;
        }
        .history-datetime {
            color: #495057;
            font-size: 0.8em;
        }
        .app-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .app-subtitle {
            color: #6c757d;
            font-size: 1.1em;
            margin-bottom: 2rem;
            text-align: center;
        }
        .tooltip {
            position: relative;
            display: inline-block;
            cursor: help;
        }
        .tooltip:hover::after {
            content: attr(data-tooltip);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            padding: 5px 10px;
            background: #333;
            color: white;
            border-radius: 4px;
            font-size: 12px;
            white-space: nowrap;
            z-index: 1000;
        }
        @media (max-width: 768px) {
            .main {
                padding: 0.5rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)
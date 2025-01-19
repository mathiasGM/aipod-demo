import streamlit as st

def check_states(*keys) -> bool:
    """Check if all specified keys exist and are not None in session state"""
    return all(key in st.session_state and st.session_state[key] is not None for key in keys)
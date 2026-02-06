import streamlit as st

st.set_page_config(page_title="...", layout="wide")

# Centrar el contenido
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    st.markdown("""
    <style>
    .big-font {
        font-family: 'Courier New', Courier, monospace;
        font-size: 20px;
        white-space: pre;
        text-align: center;
        margin-top: 100px;
    }
    </style>
    <div class="big-font">
    ** ** ** ***** **
    *** ** **** ** ** ****
    ** ** ** ** ** ** ** ** **
    ** **** ****** ** ** ******
    ** *** ** ** ** ** ** **
    ** ** ** ** ***** ** **
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center; color: grey;'>PROYECTO DETENIDO</h3>", unsafe_allow_html=True)


import streamlit as st

# ----- BASIC CONFIGURATION -----

st.set_page_config(page_title="Streamlit App", page_icon=":bar_chart:", layout="wide")

# ----- LOAD ASSETS -----

# This section is meant to load animations, datasets, graphs, images, etc. that will be used in the app

# ----- HEADER SECTION -----

# A container allows us to organize the contents of the web app, but you don't necessarily need it
with st.container():
    st.title("Streamlit App Model")
    st.header("This is a header")
    st.subheader("This is a subheader")
    st.write("This is a text")
    st.write("[This is a link to Atenea](https://atenea.upc.edu/login/index.php)")
    st.markdown("This is a markdown, where you can write in markdown usual format")


# ----- PRACTICE DETAILS -----

with st.container():
    st.header("Practice details")
    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("Practice description")
        st.write("This is a description of the practice")

    with right_col:
        st.subheader("Practice objectives")
        st.write("""
                 This is a description of the practice objectives:
                 - Objective 1
                 - Objective 2
                 - Objective 3
                 """)
        

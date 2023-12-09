import streamlit as st


if __name__ == '__main__':
    st.title("Test")


    options = ['a', 'b', 'c']
    # multi select box
    multi = st.multiselect('Multiselect', options)

    if multi:
        st.write(multi)

    st.radio('Radio', options)

    reset = st.button('Reset')
    if reset:
        st.rerun()  # Rerun the app


    on = st.toggle('Activate feature')

    if on:
        st.write('Feature activated!')
import streamlit as st

# Define the layout of the app
def app():
    # [theme]
    # primaryColor="#F63366"
    # backgroundColor="#FFFFFF"
    # secondaryBackgroundColor="#F0F2F6"
    # textColor="#262730"


    st.set_page_config(layout="wide")

    st.title("My Streamlit App")
    
    # Add some interactive widgets
    name = st.text_input("Enter your name:")
    age = st.slider("Enter your age:", 0, 100)
    
    # Display the user's input
    st.write("Your name is:", name)
    st.write("Your age is:", age)

    # st.markdown("""
    #             <style>
    #             .reportview-container {
    #                 background: url("url_goes_here")
    #             }
    #         .sidebar .sidebar-content {
    #                 background: url("url_goes_here")
    #             }
    #             </style>
    #             """,
    #             unsafe_allow_html=True
    #             )

if __name__ == '__main__':
    app()

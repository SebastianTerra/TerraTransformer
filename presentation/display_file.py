import streamlit as st
import pandas as pd

def display_file(uploaded_file):
    st.write("Uploaded File:", uploaded_file.name)

    # Read the uploaded Excel file into a Pandas DataFrame
    try:
        df = pd.read_excel(uploaded_file)

        # Convert all columns to strings so Streamlit's Arrow backend doesn't
        # raise type conversion errors when displaying mixed types
        df = df.astype(str)

        # Display the head of the DataFrame
        st.write("Here is the preview of the file:")
        st.write(df)

    except Exception as e:
        df = None
        st.error(f"Error reading the Excel file: {e}")

    return df




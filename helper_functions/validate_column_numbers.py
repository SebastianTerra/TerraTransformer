import streamlit as st

def validate_column_number(column_to_extract, pd_file):
    column_indices = []
    if column_to_extract:
        try:
            # Split the input string by commas, strip whitespace, convert to integers
            column_indices = [int(x.strip()) for x in column_to_extract.split(',') if x.strip()]
            # Ensure indices are within the bounds
            max_index = len(pd_file.columns) - 1
            invalid_indices = [i + 1 for i in column_indices if i < 0 or i > max_index]
            column_indices = [i for i in column_indices if 0 <= i <= max_index]
            if invalid_indices:
                st.warning(f"Invalid column numbers ignored: {invalid_indices}")

        except ValueError:
            st.error("Invalid column numbers entered. Please enter integers separated by commas.")
    else:
        column_indices = []

    return column_indices
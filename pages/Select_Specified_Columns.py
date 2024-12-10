import streamlit as st

from helper_functions.get_selected_columns import get_index_selected_columns
from helper_functions.validate_column_numbers import validate_column_number
from presentation.display_file import display_file
import pandas as pd
from io import BytesIO

# Initialize state variables in session_state
if 'currentState' not in st.session_state:
    st.session_state.currentState = 0

if 'current_row' not in st.session_state:
    st.session_state.current_row = 0

st.title('Terralabor File Transformer')
file = st.file_uploader('Please Select the File To Transform', type=['xlsx', 'xls'])

pd_file = None
if file:
    pd_file = display_file(file)
    if st.session_state.currentState == 0:
        headers = pd_file.iloc[[st.session_state.current_row]]
        st.write("Is this the header row?")
        st.write(headers)
        # Provide "Yes" and "No" buttons with callbacks
        col1, col2 = st.columns(2)

        def yes_button_clicked():
            st.session_state.currentState = 1

        def no_button_clicked():
            st.session_state.current_row += 1

        with col1:
            st.button("Yes, this is the header", on_click=yes_button_clicked)
        with col2:
            st.button("No, this is not the header", on_click=no_button_clicked)


if st.session_state.currentState == 1:
    st.write("Select the headers to extract")

    # Ensure that the correct header row is being used
    header_row = st.session_state.current_row

    # Extract the header row, fill NaN with 'Unnamed', strip spaces
    header_series = pd_file.iloc[header_row].fillna('Unnamed').astype(str).str.strip()

    # Function to make column names unique
    def make_unique(seq):
        seen = {}
        result = []
        for item in seq:
            count = seen.get(item, 0)
            if count == 0:
                seen[item] = 1
                result.append(item)
            else:
                seen[item] += 1
                result.append(f"{item}_{seen[item]}")
        return result

    new_headers = make_unique(header_series)

    # Ensure the number of headers matches the number of columns
    if len(new_headers) != pd_file.shape[1]:
        st.error("The selected header row does not match the number of columns. Please check the data.")
    else:
        # Update column names and clean up the DataFrame
        pd_file.columns = new_headers
        pd_file = pd_file.drop(pd_file.index[0:header_row + 1]).reset_index(drop=True)

        # Use updated column names for selection
        list_headers = list(pd_file.columns)
        # remove any empty headers
        list_headers = [x for x in list_headers if "Unnamed" not in x ]
        st.write("Available headers:")
        st.write(list_headers)

        # Allow user to select headers
        selected_headers = st.multiselect("Select the headers to extract", list_headers)

        # input the column numbers you also want to extract
        column_to_extract = st.text_input("Enter the column numbers you also want to extract (IF Any) separated by commas")

        # Submit button to proceed
        if st.button("Submit"):
            column_to_indices = validate_column_number(column_to_extract, pd_file)
            dict_selected_columns  = get_index_selected_columns(selected_headers,pd_file)
            st.write("Selected headers:")
            st.write(dict_selected_columns)

            combine_indices = column_to_indices + list(dict_selected_columns.values())
            combine_indices = sorted(list(set(combine_indices)))

            st.write("Data preview:")
            # selected_columns =  pd_file[selected_headers]
            pd_remove_empty = pd_file.iloc[:, combine_indices].dropna(how='all').reset_index(drop=True)
            st.write(pd_remove_empty)
            st.session_state.currentState = 2
            # Store the transformed DataFrame in session_state for later use
            st.session_state.transformed_data = pd_remove_empty

if st.session_state.currentState == 2:
    # Display a button to download the transformed file
    st.write("Download the transformed file:")

    # Retrieve the transformed DataFrame from session_state
    transformed_data = st.session_state.get('transformed_data')

    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        processed_data = output.getvalue()
        return processed_data

    excel_data = to_excel(transformed_data)

    st.download_button(
        label="Download file to Excel",
        data=excel_data,
        file_name='transformed_file.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

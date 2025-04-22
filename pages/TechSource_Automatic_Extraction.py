import streamlit as st
import pandas as pd

from merge_sheets_services.convert_df import convert_df
from presentation.display_file import display_file
from io import BytesIO

st.title('Terralabor File Transformer')

file = st.file_uploader('Please Select the File To Transform', type=['xlsx', 'xls'])

if file:
    pd_file = display_file(file)

    column_to_extract = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

    # Extract the columns
    pd_file = pd_file.iloc[:, column_to_extract]

    # make the first row the header
    pd_file.columns = pd_file.iloc[0].astype(str).str.strip()
    pd_file = pd_file[1:]
    
    # Process person names to remove job titles after "-"
    # First, try to find the Employee Name column if it exists
    employee_name_col = None
    if 'Employee Name' in pd_file.columns:
        employee_name_col = 'Employee Name'
    # If not found by name, use the 4th column (index 3) as a fallback
    elif len(pd_file.columns) > 3:
        employee_name_col = pd_file.columns[3]
        
    if employee_name_col:
        # Remove everything after "-" in the employee name column (handling both with and without space)
        pd_file[employee_name_col] = pd_file[employee_name_col].astype(str).apply(
            lambda x: x.split(' -')[0] if ' -' in x else (x.split('-')[0] if '-' in x else x))

    file_extracted = convert_df(pd_file)
    st.download_button(
        key="download_sorted",
        label="Export To Excel",
        data=file_extracted,
        file_name=f"TechSource.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
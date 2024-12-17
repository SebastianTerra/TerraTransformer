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

    file_extracted = convert_df(pd_file)
    st.download_button(
        key="download_sorted",
        label="Export To Excel",
        data=file_extracted,
        file_name=f"TechSource.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
import streamlit as st
import pandas as pd

import io

@st.cache_data
def convert_df(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

        # Access the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        # Define a header format (black background, white text)
        header_format = workbook.add_format({
            'bold': True,
            'fg_color': 'black',
            'font_color': 'white'
        })

        # Apply the header format and set column widths
        for col_num, col_name in enumerate(df.columns):
            # Set the header format
            worksheet.write(0, col_num, col_name, header_format)

            # Calculate the max length for this column
            col_values = df[col_name].astype(str)
            max_len = max(
                [len(str(col_name))] +
                col_values.map(len).tolist()
            )
            # Add some buffer to the column width
            worksheet.set_column(col_num, col_num, max_len + 2)

    processed_data = output.getvalue()
    return processed_data
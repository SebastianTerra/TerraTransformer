# if uploaded_file is not None:
#     # Display file name
#
#     # Enter Headers to Extract
#     st.write("Enter the headers to extract:")
#     headers = st.text_input("Enter the headers separated by commas")
#
#     if headers:
#         headers = headers.split(",")
#         header_row = get_header_row(df, headers)
#         st.write("Extracted Header Row:", header_row)
#         columns_headers = df.iloc[header_row].values
#         st.write("Columns Headers:", columns_headers)
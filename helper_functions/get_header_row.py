def get_header_row(df, headers):
    # Convert headers to lowercase and remove spaces
    headers = set([str(x).lower().replace(" ", "") for x in headers])

    for index, row in df.iterrows():
        # Convert each row to a list of strings, lowercase, and remove spaces
        list_row = [str(x).lower().replace(" ", "") for x in row]
        set_row = set(list_row)

        # If any value in headers is found in the row
        if headers.intersection(set_row):
            return index




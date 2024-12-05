def get_index_selected_columns(selected_headers, pd_file):
    # Get the indices of the selected columns
    dict_selected_columns = {header: pd_file.columns.get_loc(header) for header in selected_headers}
    return dict_selected_columns

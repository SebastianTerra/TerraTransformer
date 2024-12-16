import streamlit as st
import pandas as pd

from merge_sheets_services.convert_df import convert_df

# Function to convert df to a downloadable Excel file


st.title("Multi-Step Excel Sheet Merger")

# Load the Excel file
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    # Check if we already have a dfs in session_state; if not, load it
    if "dfs" not in st.session_state:
        excel_data = pd.ExcelFile(uploaded_file)
        st.session_state.dfs = {sheet_name: excel_data.parse(sheet_name) for sheet_name in excel_data.sheet_names}
        st.session_state.last_merged_name = None
    # Initialize session_state if not present
    if "selected_sheets" not in st.session_state:
        st.session_state.selected_sheets = []

    sheet_names = list(st.session_state.dfs.keys())

    # If there's only one sheet left, just allow export
    if len(sheet_names) == 1:
        st.write("Only one sheet remains: ", sheet_names[0])
        final_df = st.session_state.dfs[sheet_names[0]]
        st.dataframe(final_df)

        merged_file = convert_df(final_df)
        st.download_button(
            label="Download Final Merged DataFrame",
            data=merged_file,
            file_name="merged_output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        # If we just merged, show the merged sheet and two buttons:
        # If we just merged, show the merged sheet and two buttons:
        if st.session_state.last_merged_name and st.session_state.last_merged_name in st.session_state.dfs:
            st.write("### Current Merged DataFrame")
            merged_df = st.session_state.dfs[st.session_state.last_merged_name]
            st.dataframe(merged_df)

            # Create three columns for buttons
            col3, col2, col1 = st.columns(3)

            with col3:
                if st.button("Sort by Column"):
                    st.session_state.sorting_mode = True  # Flag to show sorting options
                    st.rerun()

            with col2:
                if st.button("Merge Another Sheet"):
                    # Clear last_merged_name to show mapping UI again
                    st.session_state.last_merged_name = None
                    st.rerun()

            with col1:
                merged_file = convert_df(merged_df)
                st.download_button(
                    label="Download Current Merged",
                    data=merged_file,
                    file_name=f"{st.session_state.last_merged_name}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            # If the user clicked "Sort by Column"
            if "sorting_mode" in st.session_state and st.session_state.sorting_mode:
                st.write("### Sort Data by a Column")
                sort_col = st.selectbox("Select a column to sort by:", merged_df.columns)
                sort_order = st.radio("Sort order:", ("Ascending", "Descending"))

                if st.button("Apply Sorting"):
                    ascending = True if sort_order == "Ascending" else False
                    sorted_df = merged_df.sort_values(by=sort_col, ascending=ascending)

                    # Update session state with the sorted dataframe
                    st.session_state.dfs[st.session_state.last_merged_name] = sorted_df
                    st.write("### Sorted DataFrame")
                    st.dataframe(sorted_df)
                    st.session_state.sorting_mode = False

                    merged_file = convert_df(sorted_df)
                    st.download_button(
                        key="download_sorted",
                        label="Download Current Merged",
                        data=merged_file,
                        file_name=f"{st.session_state.last_merged_name}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )


        else:
            # Show UI to select and map sheets for merging
            st.sidebar.title("Sheets")
            # Determine if the widget should be disabled
            disabled = len(st.session_state.selected_sheets) == 2

            # Create the multiselect widget
            selected_sheets = st.sidebar.multiselect(
                "Select 2 Sheets for Merging",
                sheet_names,
                default=st.session_state.selected_sheets,
                disabled=disabled
            )

            # If user selection changed, update session_state and possibly rerun
            if selected_sheets != st.session_state.selected_sheets:
                st.session_state.selected_sheets = selected_sheets
                # If the user just reached 2 selections, rerun to disable the widget
                if len(selected_sheets) == 2:
                    st.rerun()

            if len(st.session_state.selected_sheets) > 1:
                # Initialize dataframes to merge
                df_a1 = st.session_state.dfs[st.session_state.selected_sheets[0]]
                df_a2 = st.session_state.dfs[st.session_state.selected_sheets[1]]

                # Ensure unique columns in df_a1 and df_a2 before proceeding
                df_a1 = df_a1.loc[:, ~df_a1.columns.duplicated()].copy()
                df_a2 = df_a2.loc[:, ~df_a2.columns.duplicated()].copy()

                # Map columns
                st.write("### Map Columns:")
                mappings = {}

                for col in df_a1.columns:
                    if col in df_a2.columns:
                        # Automatically map the column
                        mappings[col] = col
                        st.success(f"**`{col}`** automatically mapped to **`{col}`** from df_a2.")
                    else:
                        st.warning(f"**`{col}`** does not exist in df_a2. Please select a column to map.")
                        selected_column = st.selectbox(
                            f"Map `{col}` to a column in df_a2:",
                            [None] + list(df_a2.columns),
                            key=f"{col}_a2"
                        )
                        if selected_column:
                            mappings[col] = selected_column

                # Check if mapping leads to duplicates
                if len(set(mappings.values())) < len(mappings.values()):
                    st.error(
                        "Your mappings produce duplicate column names. Please ensure each df_a1 column maps to a unique df_a2 column.")
                    st.stop()

                if st.button("Append the second Sheets"):
                    # Perform the merge
                    merged_df = df_a1.copy()
                    df_a2_subset = df_a2[list(mappings.values())].copy()

                    # Rename columns
                    df_a2_subset.rename(columns={v: k for k, v in mappings.items()}, inplace=True)

                    # Check for duplicates again after renaming
                    if df_a2_subset.columns.duplicated().any():
                        st.error("Renaming resulted in duplicate columns. Please revise your mappings.")
                        st.stop()

                    # Concatenate
                    merged_df = pd.concat([merged_df, df_a2_subset], ignore_index=True)

                    # Remove the merged sheets from session_state and add the new merged sheet
                    del st.session_state.dfs[st.session_state.selected_sheets[0]]
                    del st.session_state.dfs[st.session_state.selected_sheets[1]]

                    # Generate a unique name for the merged sheet
                    merged_name = "merged"
                    count = 1
                    while merged_name in st.session_state.dfs:
                        merged_name = f"merged_{count}"
                        count += 1

                    st.session_state.dfs[merged_name] = merged_df
                    st.session_state.last_merged_name = merged_name
                    st.session_state.selected_sheets = [merged_name]

                    st.rerun()
            else:
                # If user does not pick at least 2 sheets
                st.warning("Please select at least 2 sheets to merge.")

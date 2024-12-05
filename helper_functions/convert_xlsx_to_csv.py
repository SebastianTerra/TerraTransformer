import pandas as pd
import tempfile
import os


def convert_xlsx_to_csv(uploaded_file):
    """
    Converts an uploaded Excel file to a CSV file.

    Args:
        uploaded_file: The uploaded Excel file from Streamlit.

    Returns:
        str: The file path of the converted CSV file.
    """
    try:
        # Read the Excel file into a Pandas DataFrame
        df = pd.read_excel(uploaded_file)

        # Create a temporary directory to save the CSV file
        temp_dir = tempfile.gettempdir()
        csv_file_path = os.path.join(temp_dir, f"{os.path.splitext(uploaded_file.name)[0]}.csv")

        # Save the DataFrame to a CSV file
        df.to_csv(csv_file_path, index=False)

        return csv_file_path
    except Exception as e:
        raise ValueError(f"Failed to convert file to CSV: {e}")
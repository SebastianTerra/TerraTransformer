import os
import tempfile


def write_temp_file(file_data, file_name):
    """
    Writes the uploaded file data to a temporary file and returns the file path.

    Args:
        file_data (BytesIO): The file content as bytes.
        file_name (str): The name of the file.

    Returns:
        str: The path to the temporary file.
    """
    # Create a temporary directory
    temp_dir = tempfile.gettempdir()

    # Create a temporary file path with the specified file name
    temp_file_path = os.path.join(temp_dir, file_name)

    # Write the file data to the temporary file
    with open(temp_file_path, 'wb') as temp_file:
        temp_file.write(file_data)

    return temp_file_path



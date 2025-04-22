# TerraLabor File Transformer

A Streamlit application for transforming and processing Excel files from TerraLabor. This tool helps you clean and transform data from specific Excel formats, including removing job titles from employee names.

## Online Access

You can access the application online without any installation at:
[TerraLabor File Transformer](https://your-streamlit-app-url.streamlit.app) *(Update this URL after deployment)*

## Features

- Automatic extraction of data from Excel files
- Removal of job titles from employee names
- Formatting of date fields
- Calculation of totals
- Easy export to cleaned Excel files

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/TerralaborFileTransformer.git
   cd TerralaborFileTransformer
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:
   ```
   streamlit run main.py
   ```

2. Open your browser and navigate to http://localhost:8501

3. Upload your Excel file using the file uploader

4. The application will automatically process the file and display the transformed data

5. Click "Download file to Excel" to save the processed data

## Data Processing Features

- **Employee Name Processing**: Removes job titles that appear after the dash in employee names
- **Work Day Formatting**: Converts date formats to a standardized YYYY-MM-DD format
- **Summary Calculation**: Calculates and adds summary row for totals
- **Column Formatting**: Automatically formats columns with appropriate types

## Dependencies

The application requires the following main packages:
- streamlit
- pandas
- openpyxl
- xlsxwriter

A complete list of dependencies is available in the requirements.txt file.

## License

[Include your license information here]

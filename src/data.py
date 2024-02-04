import base64
import calendar
from datetime import datetime
from typing import List, Optional

import pandas as pd
import streamlit as st

COLUMN_ORDER = [
    "Date",
    "Day of Week",
    "Month",
    "Year",
    "Description",
    "Transaction Amount",
    "Category"
]

SUPPORTED_FILE_TYPES = {
    "csv": "text/csv",
    "txt": "text/plain",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}

def df_to_csv(df: pd.DataFrame):
    """
    Converts a Pandas DataFrame to a UTF-8 encoded CSV file for download
    """
    return df.to_csv(index=False).encode('utf-8')

def uploaded_file_requirements():
    # Example dataframe
    df = pd.DataFrame({
        "Date": ["1/1/2024", "1/2/2024", "1/3/2024", "1/4/2024", "1/5/2024"],
        "Description": ["Starbucks","Trader Joe's","Venmo","Amazon", "ATM"],
        "Transaction Amount": [-4.65,-55.79,80.00,-25.83, -40.00]
    })
    
    # Convert dataframe to csv
    csv = df_to_csv(df=df)

    # Base64 encoded representation of the dataframe
    b64 = base64.b64encode(csv).decode()

    # File requirements
    message = f"""
        - File must contain columns titled **Date**, **Description**, and 
        **Transaction Amount** (see <a href="data:file/csv;base64,{b64}"
        download="example.csv">example</a>). 
        
        - Optionally, file may also include a column titled **Category** if 
        your transactions already have category labels.
    """

    # Write Caption
    return message

def upload_file():
    """
    Returns a container with a file uploader and additional information

    Returns:
        container (st.expander): the resulting container
    """
    container = st.expander(
        label="Upload Bank Transactions",
        expanded=True
    )
    file_requirements = container.caption(
        uploaded_file_requirements(),
        unsafe_allow_html=True
    )
    uploaded_file = container.file_uploader(
        label="Upload Bank Transactions",
        type=["csv", "xlsx", "txt"],
        key="uploaded_file",
        label_visibility="hidden"
    )

    return container

def read_uploaded_file(
    file,
    nrows: Optional[int] = None,
    parse_dates: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Reads an uploaded file into a Pandas DataFrame

    Arguments:
        file: CSV, XLSX, or TXT file
        nrows (int): Number of rows of file to read
        parse_dates (List[str]): list of datetime columns to parse

    Returns:
        df (pd.DataFrame): the resulting dataframe
    """  
    # Read file as a Pandas DataFrame
    if file.type == SUPPORTED_FILE_TYPES["csv"]:
        df = pd.read_csv(
            file,
            nrows=nrows,
            delimiter=",",
            parse_dates=parse_dates
        )
    elif file.type == SUPPORTED_FILE_TYPES["txt"]:
        df = pd.read_csv(
            file,
            nrows=nrows,
            delimiter="\t",
            parse_dates=parse_dates
        )
    elif file.type == SUPPORTED_FILE_TYPES["xlsx"]:
        df = pd.read_excel(
            file,
            nrows=nrows,
            parse_dates=parse_dates
        )

    # Return the raw dataframe
    return df

def validate_uploaded_file(file) -> bool:
    """
    Validates that an uploaded file is a supported file type and contains the 
    required columns. Returns a boolean to indicate whether validation passed.

    Arguments:
        file: CSV, XLSX, or TXT file

    Returns:
        (bool): indicates whether or not validation passed
    """
     # Validate that uploaded file is a supported file type
    if file.type not in SUPPORTED_FILE_TYPES.values():
        raise ValueError(
            "Unsupported file type. Supported types are CSV, TXT, and XLSX"
        )
    
    # Define required columns
    required_columns = ["Date", "Description", "Transaction Amount"]

    # Scan uploaded file for column names
    file_columns = read_uploaded_file(file=file, nrows=1).columns
    
    # Identify any missing columns
    missing_columns = [
        column for column in required_columns 
        if column not in file_columns
    ]

    # Validate that uploaded file contains all required columns
    if len(missing_columns) > 0:
        raise ValueError(
            f"File is missing required columns: {', '.join(missing_columns)}"
        )
    else:
        return True

@st.cache_data(show_spinner=True)
def categorize_df(
    df: pd.DataFrame,
    categories: Optional[List[str]] = None,
    num_categories: Optional[int] = None
) -> pd.DataFrame:
    """
    Categorizes the transactions in the dataframe

    Arguments:
        df (pd.DataFrame): the uncategorized transactions
        categories (List[str]): the list of categories to use for 
            categorization
        num_categories (int): the number of categories to generate

    Returns:
        df (pd.DataFrame): the categorized transactions
    """
    df["Category"] = pd.Series()
    return df

def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the dataframe of transactions

    Arguments:
        df (pd.DataFrame): the raw dataframe

    Returns:
        df (pd.DataFrame): the cleaned dataframe
    """
    # Parse date
    df["Day of Week"] = df["Date"].dt.strftime("%A")
    df["Month"] = df["Date"].dt.strftime('%B')
    df["Year"] = df["Date"].dt.year

    # Sort by date
    df = df.sort_values(by="Date", ascending=False)

    # Return cleaned dataframe
    return df

def column_configuration() -> dict:
    """
    Returns the configuration for the columns of the dataframe
    """
    configuration = {}
    
    configuration["Date"] = st.column_config.DateColumn(
        label="Date",
        help="The date of the transaction",
        disabled=True,
        required=True,
        default=datetime.now(),
        format="MM/DD/YYYY",
        step=1
    )

    configuration["Day of Week"] = st.column_config.TextColumn(
        label="Day of Week",
        help="The day of the week in which the transaction took place",
        disabled=True,
        required=True,
        default=datetime.now().strftime("%A"),
        validate=f"^({'|'.join(list(calendar.day_name))})$"
    )

    configuration["Month"] = st.column_config.TextColumn(
        label="Month",
        help="The month in which the transaction took place",
        disabled=True,
        required=True,
        default=datetime.now().strftime("%B"),
        validate=f"^({'|'.join(list(calendar.month_name))})$"
    )

    configuration["Year"] = st.column_config.NumberColumn(
        label="Year",
        help="The year in which the transaction took place",
        disabled=True,
        required=True,
        default=datetime.now().year,
        format="%i",
        step=1
    )

    configuration["Description"] = st.column_config.TextColumn(
        label="Description",
        help="The description of the transaction",
        disabled=True,
        required=True,
    )

    configuration["Transaction Amount"] = st.column_config.NumberColumn(
        label="Transaction Amount ($)",
        help="The dollar amount of the transaction",
        disabled=True,
        required=True,
        format="%.2f",
    )

    configuration["Category"] = st.column_config.TextColumn(
        label="Category",
        help="The category label given to the transaction",
    )

    return configuration

def display_dataframe(file):
    """
    Handles uploaded file

    Arguments:
        transactions: the uploaded file
    """
    # Initialize container
    container = st.container()

    # Validate data
    try:
        validation_passed = validate_uploaded_file(file=file)
        
    except ValueError as e:
        container.error(e, icon="🚨")
        validation_passed = False

    if validation_passed:
        # Reset the buffer
        file.seek(0)

        # Read data
        df = read_uploaded_file(file=file, parse_dates=["Date"])

        # Categorize transactions
        df = categorize_df(df=df)
        categorize_df.clear()

        # Clean dataframe
        df = clean_df(df=df)

        # Display labeled dataframe
        labeled_transactions = container.data_editor(
            data=df,
            column_order=COLUMN_ORDER,
            column_config=column_configuration(),
            use_container_width=True,
            hide_index=True,
            num_rows="fixed",
        )

        # Download dataframe
        container.download_button(
            label="Download labeled transactions",
            data=df_to_csv(df=labeled_transactions),
            file_name="labeled_transactions.csv",
            mime="text/csv"
        )
    
    return container
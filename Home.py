import streamlit as st

from src.data import display_dataframe, upload_file
from src.utils import page_configuration

def main():
    page_configuration('Spending Insights')

    st.write(
        """
        Hey there!👋 Spending Insights categorizes your bank transactions 
        and presents a visual overview of your spending patterns. Upload a 
        dataset of your bank transactions (don't worry, we don't collect or 
        store any of your data) and each transaction will automatically be 
        categorized. Feel free to edit the number of categories or customize 
        the categories themselves.
        """
    )

    transactions = upload_file()

    if st.session_state["uploaded_file"] is not None:
        dataframe = display_dataframe(file=st.session_state["uploaded_file"])

if __name__ == '__main__':
    main()
import streamlit as st

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


if __name__ == '__main__':
    main()
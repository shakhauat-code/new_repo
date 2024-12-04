import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# Define function for data cleaning
def clean_data(df):
    # Handle missing values
    df = df.fillna("Missing")

    # Drop duplicates
    df = df.drop_duplicates()

    # Convert columns to appropriate types if possible
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except ValueError:
            pass  # Keep as original type if conversion fails
    return df


# Define function for validation
def validate_data(df, required_columns):
    missing_columns = [col for col in required_columns if col not in df.columns]
    return missing_columns


# Streamlit UI
st.title("Self-Analytics Data App")
st.sidebar.title("Options")

uploaded_file = st.sidebar.file_uploader("Upload your dataset", type=["csv", "xlsx"])

if uploaded_file:
    # Read dataset
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.write("### Uploaded Data")
        st.dataframe(df)

        # Clean data
        cleaned_df = clean_data(df)

        st.write("### Cleaned Data")
        st.dataframe(cleaned_df)

        # Validate data
        required_columns = st.sidebar.multiselect("Required Columns", options=cleaned_df.columns)
        missing_columns = validate_data(cleaned_df, required_columns)

        if missing_columns:
            st.warning(f"Missing required columns: {', '.join(missing_columns)}")
        else:
            st.success("All required columns are present!")

        # Exploratory Data Analysis (EDA)
        st.write("### Exploratory Data Analysis")
        st.write("#### Summary Statistics")
        st.write(cleaned_df.describe())

        st.write("#### Data Visualization")
        col_x = st.selectbox("Select X-axis for visualization", cleaned_df.columns)
        col_y = st.selectbox("Select Y-axis for visualization", cleaned_df.columns)
        chart = px.scatter(cleaned_df, x=col_x, y=col_y, title="Scatter Plot")
        st.plotly_chart(chart)

        # Download cleaned data
        csv = cleaned_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Cleaned Data", csv, "cleaned_data.csv", "text/csv")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Please upload a dataset to proceed.")

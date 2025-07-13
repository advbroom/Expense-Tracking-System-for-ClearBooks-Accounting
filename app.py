import streamlit as st
import pandas as pd

# File names
RECORDS_FILE = 'Expense_Records_ClearBooks.csv'
SUMMARY_FILE = 'Expense_Summary_By_Category.csv'

# Load and clean data
@st.cache_data
def load_data():
    try:
        records = pd.read_csv(RECORDS_FILE)
        summary = pd.read_csv(SUMMARY_FILE)
    except FileNotFoundError:
        st.error("CSV files not found. Please upload the required files.")
        return None, None

    # Clean records
    records['Date'] = pd.to_datetime(records['Date'], errors='coerce')
    records = records.dropna(subset=['Date', 'AmountINR', 'Category'])
    records = records[records['AmountINR'] > 0]

    return records, summary

# Generate summary
def generate_summary(df):
    summary = df.groupby('Category')['AmountINR'].sum().reset_index()
    summary = summary.sort_values(by='AmountINR', ascending=False)
    summary['AmountINR'] = summary['AmountINR'].round(2)
    return summary

# Compare summaries
def compare_summaries(generated, provided):
    provided['AmountINR'] = provided['AmountINR'].round(2)
    comparison = pd.merge(
        generated, provided, on='Category', how='outer',
        suffixes=('_Generated', '_Provided')
    )
    comparison['Difference'] = comparison['AmountINR_Generated'].fillna(0) - comparison['AmountINR_Provided'].fillna(0)
    return comparison

# Main app layout
def main():
    st.title("💰 ClearBooks Expense Tracker")

    records_df, summary_df = load_data()
    if records_df is None:
        return

    st.sidebar.title("Navigation")
    option = st.sidebar.radio("Select a section", (
        "📋 View Expense Records",
        "📊 Summary by Category",
        "📈 Compare with Provided Summary",
        "📤 Export Cleaned Data"
    ))

    if option == "📋 View Expense Records":
        st.subheader("First 10 Expense Records")
        st.dataframe(records_df.head(10))

    elif option == "📊 Summary by Category":
        st.subheader("Generated Summary by Category")
        generated_summary = generate_summary(records_df)
        st.dataframe(generated_summary)

    elif option == "📈 Compare with Provided Summary":
        st.subheader("Comparison with Provided Summary")
        generated_summary = generate_summary(records_df)
        comparison_df = compare_summaries(generated_summary, summary_df)
        st.dataframe(comparison_df)

    elif option == "📤 Export Cleaned Data":
        generated_summary = generate_summary(records_df)
        records_df.to_csv('Cleaned_Expense_Records.csv', index=False)
        generated_summary.to_csv('Generated_Summary_By_Category.csv', index=False)
        st.success("Data exported successfully.")
        st.write("✅ `Cleaned_Expense_Records.csv` and `Generated_Summary_By_Category.csv` saved.")

if __name__ == "__main__":
    main()

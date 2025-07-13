# Expense-Tracking-System-for-ClearBooks-Accounting

AIM:-
To develop a Python-based application that enables ClearBooks Accounting and its clients to record, categorize, analyze, and export business expenses in an organized manner, ensuring better financial reporting and tax preparation.

Tools & Libraries Used:-
•	Python
•	Pandas
•	Streamlit
•	csv files

Step by Step Implementation:-
#Jupyter Notebook:
1.	Import Required Libraries and Load Datasets:
        
        import pandas as pd
        records_df = pd.read_csv('Expense_Records_ClearBooks.csv')
        summary_df = pd.read_csv('Expense_Summary_By_Category.csv')
        print(records_df.head())
        print(summary_df.head())




<img width="591" height="409" alt="Screenshot 2025-07-10 010017" src="https://github.com/user-attachments/assets/e5f0e2a6-9dac-4bc0-b3e5-cb23578da577" />





2.	Clean the Data:

# Convert 'Date' column to datetime format
    records_df['Date'] = pd.to_datetime(records_df['Date'], errors='coerce')

# Remove rows with missing/invalid entries
    records_df.dropna(subset=['Date', 'AmountINR', 'Category'], inplace=True)

# Keep only positive amounts
    records_df = records_df[records_df['AmountINR'] > 0]
    
    records_df.reset_index(drop=True, inplace=True)
    records_df.head()

3.	Generate Summary by Category:

        generated_summary = records_df.groupby('Category')['AmountINR'].sum().reset_index()
        generated_summary = generated_summary.sort_values(by='AmountINR', ascending=False)
        generated_summary['AmountINR'] = generated_summary['AmountINR'].round(2)
        generated_summary







<img width="415" height="234" alt="Screenshot 2025-07-10 010802" src="https://github.com/user-attachments/assets/61c15c53-31fd-430d-a8ec-1b6dc326f8a4" />









4.	Compare with Provided Summary:

# Round values for comparison
    generated_summary['AmountINR'] = generated_summary['AmountINR'].round(2)
    summary_df['AmountINR'] = summary_df['AmountINR'].round(2)

# Merge and compare
    comparison = pd.merge(generated_summary, summary_df, on='Category', how='outer', suffixes=('_Generated', '_Provided'))
    
    comparison['Difference'] = comparison['AmountINR_Generated'] - comparison['AmountINR_Provided']
    
    print(comparison)

<img width="734" height="233" alt="Screenshot 2025-07-10 010937" src="https://github.com/user-attachments/assets/02ff5047-739e-4416-a63b-afea3aa48e9b" />

5.	Export the Cleaned Data and Summary & Visualizations:

        def main_menu():
           while True:
            print("\n--- ClearBooks Expense Tracker ---")
            print("1. View All Records")
            print("2. View Summary by Category")
            print("3. Compare with Provided Summary")
            print("4. Export Cleaned Data")
            print("5. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            print("\n--- First 10 Expense Records ---")
            print(records_df.head(10).to_string(index=False))

        elif choice == '2':
            print("\n--- Summary by Category ---")
            print(generated_summary.to_string(index=False))

        elif choice == '3':
            print("\n--- Comparison with Provided Summary ---")
            print(comparison.to_string(index=False))

        elif choice == '4':
            records_df.to_csv('Cleaned_Expense_Records.csv', index=False)
            generated_summary.to_csv('Generated_Summary.csv', index=False)
            print("Files exported successfully.")

        elif choice == '5':
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

# Make sure this is at the bottom of your script
    if __name__ == '__main__':
    main_menu()

<img width="802" height="167" alt="Screenshot 2025-07-10 011401" src="https://github.com/user-attachments/assets/677c7e35-a4e8-4134-87af-541767d09797" />

# App.py : 

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

#Files inside Folder:-

#Run Streamlit App Command:-

    python -m streamlit run app.py

OUTPUT:

 
<img width="1920" height="1080" alt="Screenshot 2025-07-10 012420" src="https://github.com/user-attachments/assets/1874f00d-d129-4773-aae2-985ca6774727" />

 
 <img width="1920" height="1080" alt="Screenshot 2025-07-10 012429" src="https://github.com/user-attachments/assets/11462883-72e2-4ab8-8e35-161dbee26ca1" />


<img width="1920" height="1080" alt="Screenshot 2025-07-10 012437" src="https://github.com/user-attachments/assets/6619c0b2-896a-4b24-87bc-fd0c84f0b23e" />


<img width="1920" height="1080" alt="Screenshot 2025-07-10 012448" src="https://github.com/user-attachments/assets/183412db-870c-494b-809a-93ac946c0622" />





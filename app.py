import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

CSV_FILE = "expenses.csv"

# Initialize the CSV file if it doesn't exist
def init_file():
    try:
        pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Date", "Category", "Amount"])
        df.to_csv(CSV_FILE, index=False)

# Load expenses data from CSV
def load_data():
    return pd.read_csv(CSV_FILE)

# Add a new expense to the CSV
def add_expense(date, category, amount):
    df = load_data()
    new_entry = pd.DataFrame([[date, category, amount]], columns=df.columns)
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

# Show summary charts
def show_summary(df):
    df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")
    summary = df.groupby(["Month", "Category"])["Amount"].sum().unstack().fillna(0)

    st.subheader("📊 Monthly Expenses by Category")
    st.bar_chart(summary)

    st.subheader("🥧 Total Expenses by Category")
    total = df.groupby("Category")["Amount"].sum()
    fig, ax = plt.subplots()
    ax.pie(total, labels=total.index, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

# Main Streamlit app
def main():
    st.title("💸 Budget & Expense Tracker")

    init_file()
    df = load_data()

    with st.form("expense_form"):
        st.subheader("➕ Add New Expense")
        date = st.date_input("Date", datetime.today())
        category = st.selectbox("Category", ["Food", "Rent", "Utilities", "Transport", "Entertainment", "Other"])
        amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
        submitted = st.form_submit_button("Add Expense")

        if submitted:
            add_expense(date.isoformat(), category, amount)
            st.success("Expense added!")

    st.subheader("📋 Expense Table")
    st.dataframe(load_data())

    if not df.empty:
        show_summary(df)

if __name__ == "__main__":
    main()

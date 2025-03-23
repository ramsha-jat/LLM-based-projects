import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import google.generativeai as genai  # Google Gemini API

# Set up Gemini API with available model
genai.configure(api_key="your Open AI  key")  # Replace with your actual API key

st.set_page_config(page_title="Finance Story Teller", layout="wide")

# Sidebar for File Upload
st.sidebar.header("Upload Financial Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("File uploaded successfully!")

    # Convert date column to datetime if present
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Sort data by date for accurate trend visualization
    df = df.sort_values(by="date")

    # Display Data Preview
    st.subheader("📂 Financial Dataset Overview")
    st.dataframe(df.head())

    # Function to generate a structured financial report
    def generate_financial_report(df):
        return f"""
        Financial Performance Analysis

        Report Period: {df['date'].min().strftime('%Y-%m-%d')} - {df['date'].max().strftime('%Y-%m-%d')}

        Executive Summary:
        This report provides an in-depth analysis of the company's financial performance, highlighting key trends, risks, and opportunities. The dataset includes revenue, expenses, net income, and other critical financial indicators.

        1. Revenue and Profitability Performance:
        - Total Revenue: ${df['Total Revenue'].sum():,.2f}
        - Average Quarterly Revenue: ${df['Total Revenue'].mean():,.2f}
        - Gross Profit: ${df['Gross Profit'].sum():,.2f}
        - Average Gross Profit Margin: {df['Gross Profit'].mean() / df['Total Revenue'].mean() * 100:.2f}%

        2. Expense and Cost Analysis:
        - Cost of Revenue: ${df['Cost Of Revenue'].sum():,.2f}
        - Selling, General & Administrative Expenses: ${df['Selling General Administrative'].sum():,.2f}
        - Research & Development Expenses: ${df['Research Development'].sum():,.2f}

        3. Key Financial Metrics:
        - Operating Income: ${df['Operating Income'].sum():,.2f}
        - EBIT (Earnings Before Interest & Taxes): ${df['Ebit'].sum():,.2f}
        - Net Income: ${df['Net Income'].sum():,.2f}
        - Interest Expenses: ${df['Interest Expense'].sum():,.2f}

        4. Key Insights:
        - Revenue and gross profit show strong trends, but net income fluctuates, indicating potential inefficiencies.
        - High cost of revenue impacts profitability.
        - Research & Development spending may impact long-term financial sustainability.

        5. Recommendations:
        - Optimize cost structures to improve profitability.
        - Conduct detailed financial forecasting for better expense control.
        - Enhance revenue diversification to mitigate risks.

        Appendix:
        - Data Reference Period: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}
        """

    # Generate Story
    st.subheader("📖 Financial Report")
    report_text = generate_financial_report(df)
    st.text_area("Generated Report", value=report_text, height=500)

    # Function to plot individual financial metrics
    def plot_financial_metric(df, column_name, title):
        plt.figure(figsize=(5, 3))
        plt.plot(df["date"], df[column_name], marker="o", linestyle="-", label=column_name)
        plt.xlabel("Date")
        plt.ylabel("Amount ($)")
        plt.title(title)
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True)
        st.pyplot(plt)

    # Display individual financial metric graphs
    st.subheader("📉 Individual Financial Metrics")

    plot_financial_metric(df, "Total Revenue", "Total Revenue Trend")
    plot_financial_metric(df, "Gross Profit", "Gross Profit Trend")
    plot_financial_metric(df, "Net Income", "Net Income Trend")
    plot_financial_metric(df, "Operating Income", "Operating Income Trend")
    plot_financial_metric(df, "Cost Of Revenue", "Cost of Revenue Trend")
    plot_financial_metric(df, "Ebit", "EBIT Trend")
    plot_financial_metric(df, "Selling General Administrative", "SG&A Expenses Trend")
    plot_financial_metric(df, "Research Development", "Research & Development Expenses Trend")

    # AI-Powered Financial Storytelling with Gemini API
    use_ai = st.sidebar.checkbox("Enable AI-Powered Analysis")
    if use_ai:
        st.subheader("AI-Generated Financial Insights")

        # AI Prompt
        prompt = f"""
        Provide a professional financial analysis based on the following dataset:
        {report_text}

        Focus on:
        - Trends in revenue, profitability, and expenses.
        - Key financial risks and opportunities.
        - Strategic recommendations for improving financial performance.
        """

        try:
            # Use Gemini AI for Report
            model = genai.GenerativeModel("gemini-1.5-pro-latest")
            response = model.generate_content(prompt)
            ai_report = response.text if response.text else "AI response was empty."
            st.text_area("AI-Generated Financial Report", value=ai_report, height=500)
        except Exception as e:
            st.error(f"Error in AI generation: {e}")

    # Export Report
    if st.button("Download Report as Text File"):
        with open("financial_report.txt", "w") as file:
            file.write(report_text)
        st.success("Report saved as 'financial_report.txt'!")

else:
    st.sidebar.warning("Please upload a CSV file to generate insights.")
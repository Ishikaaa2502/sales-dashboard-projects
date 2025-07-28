import pandas as pd
import streamlit as st
import plotly.express as px

# Load CSV data
df = pd.read_csv("sales_dashboard_data.csv")

# Check column names
st.write("📋 Column Names:", df.columns.tolist())

# Convert 'Date' to datetime
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
regions = df['Region'].dropna().unique().tolist()
products = df['Product'].dropna().unique().tolist()

selected_regions = st.sidebar.multiselect("Select Region(s):", regions, default=regions)
selected_products = st.sidebar.multiselect("Select Product(s):", products, default=products)

# Filter data
filtered_df = df[(df['Region'].isin(selected_regions)) & (df['Product'].isin(selected_products))]

# Main title
st.title("📊 Interactive Sales Dashboard")

# KPIs
total_revenue = filtered_df['Total Sales'].sum()
total_quantity = filtered_df['Quantity'].sum()

col1, col2 = st.columns(2)
col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
col2.metric("📦 Total Quantity Sold", int(total_quantity))

# 📍 Revenue by Region
st.subheader("📍 Revenue by Region")
rev_by_region = filtered_df.groupby('Region')['Total Sales'].sum().reset_index()
fig_region = px.bar(rev_by_region, x='Region', y='Total Sales', color='Region', title="Revenue by Region")
st.plotly_chart(fig_region)

# 📦 Revenue by Product
st.subheader("📦 Revenue by Product")
rev_by_product = filtered_df.groupby('Product')['Total Sales'].sum().reset_index()
fig_product = px.bar(rev_by_product, x='Product', y='Total Sales', color='Product', title="Revenue by Product")
st.plotly_chart(fig_product)

# 📈 Monthly Revenue Trend
st.subheader("📈 Monthly Revenue Trend")
filtered_df['Month'] = filtered_df['Date'].dt.to_period('M').astype(str)
monthly_revenue = filtered_df.groupby('Month')['Total Sales'].sum().reset_index()
fig_trend = px.line(monthly_revenue, x='Month', y='Total Sales', markers=True, title="Monthly Revenue Trend")
st.plotly_chart(fig_trend)

# 📥 Download filtered data
st.subheader("📥 Download")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Filtered Data", data=csv, file_name='filtered_sales.csv', mime='text/csv')

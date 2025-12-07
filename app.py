import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Customer Analytics Dashboard")
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
df = pd.DataFrame()

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Dataset preview:")
    st.dataframe(df.head())
    

    df = pd.DataFrame({
    "customer_id": [1, 2, 3],
    "name": ["Sara", "Omar", "Lina"],
    "total_purchases": [5, 12, 1],
    "lifetime_value": [500, 1200, 100],
    "last_purchase_date": ["2024-10-01", "2024-09-20", "2024-01-11"]
})
    
#1-Customer Lookup-----> search for a specific customer and view key details
st.title("Customer Lookup")
customer_id = st.number_input("Enter Customer ID:", min_value=1)


if st.button("Search"):
    result = df[df["customer_id"] == customer_id]
    if not result.empty:
        st.write(result)

        
        days = (datetime.now() - pd.to_datetime(result["last_purchase_date"].iloc[0])).days
        score = 100 - days 
        st.metric("Behavior Score", max(score, 0))
    else:
        st.warning("Customer not found")
        
#2-segment explorer-----> explore customer segments using demographic and behavioral filters
st.header("Segment Explorer")
countries = st.multiselect("Country", df.get("country", []))
min_age, max_age = st.slider("Age Range", 18, 80, (20, 40))

if st.button("Apply Filters"):
    seg = df.copy()
    

    if countries:
        seg = seg[seg["country"].isin(countries)]
    #to filiter data

    if "age" in df.columns:
        seg = seg[df["age"].between(min_age, max_age)]
    
    st.dataframe(seg)


#conversions = audience * conversion_rate
#revenue = conversions * avg_order_value
#roi = (revenue - cost) / cost

#3-campingn simulator------> Test campaign scenarios and estimate ROI before launching
st.header("Campaign Simulator")

audience = st.number_input("Audience Size", min_value=1)
conversion_rate = st.slider("Conversion Rate (%)", 0.0, 50.0, 5.0)
avg_order = st.number_input("Avg Order Value", min_value=1.0)
cost = st.number_input("Campaign Cost", min_value=1.0)

if st.button("Simulate"):
    conv = audience * (conversion_rate / 100)
    revenue = conv * avg_order
    roi = (revenue - cost) / cost

    st.metric("Conversions", int(conv))   #conversions(no of customers will buy)
    st.metric("Revenue", f"${revenue:.2f}")
    st.metric("ROI", f"{roi*100:.1f}%")    #The benefit
    
#4-ltv(lifetime value) forecat-----> predict future customer lifetime value using historical behavior
st.header("LTV Forecast")

months = st.slider("Months", 1, 24, 12)

arpu = st.number_input("ARPU (Monthly)", min_value=1.0)#(Average Revenue Per User)

retention = st.slider("Retention Rate", 0.5, 0.99, 0.9)
#Customer retention rate per month

#A simple model for compiling monthly revenue
ltv = 0
r = 1
for i in range(months):
    ltv += arpu * r
    r *= retention

st.metric("Predicted LTV", f"${ltv:.2f}")

# preaper seg answer
seg = pd.DataFrame()

if not df.empty:
    seg = df.copy()

    
    if "country" in df.columns:
        countries = st.multiselect("Country", df["country"].unique())
        if countries:
            seg = seg[seg["country"].isin(countries)]

#5-download----> Download filtered customer lists for marketing use
st.download_button(
    "Download Segment",
    seg.to_csv(index=False),
    "segment.csv",
    "text/csv"
)
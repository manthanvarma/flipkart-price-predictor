import streamlit as st
import pandas as pd
import numpy as np
import joblib

model = joblib.load("model.pkl")

st.title("🛒 Flipkart Product Price Predictor")
st.markdown("Predict the price of a product based on its features like category, discount, rating, and more.")

st.sidebar.header("Product Details")

main_cat = st.sidebar.selectbox("Main Category", ["Electronics", "Home", "Fashion"])
sub_cat = st.sidebar.selectbox("Sub Category", ["Smartphones", "Laptops", "Smartwatches", "Decor", "Clothing"])
seller = st.sidebar.selectbox("Seller", ["Flipkart Retailer", "XYZ Store", "Other"])
return_policy = st.sidebar.selectbox("Return Policy", ["No Return", "7-Day Return", "30-Day Return"])

rating = st.sidebar.slider("Rating (★)", 0.0, 5.0, 4.0)
buyers = st.sidebar.number_input("Number of Buyers", 0, 100000, 1000)
sold = st.sidebar.number_input("Total Sold", 0, 100000, 1000)
stock = st.sidebar.number_input("Available Stock", 1, 100000, 100)  # No zero to avoid divide by zero
discount = st.sidebar.slider("Discount (%)", 0, 100, 20)

buyers_stock_ratio = buyers / stock
sold_stock_ratio = sold / stock
effective_price = 1000 * (1 - discount / 100)  # Dummy base price, will be predicted
is_returnable = 1 if "return" in return_policy.lower() else 0

input_df = pd.DataFrame({
    "Rating (★)": [rating],
    "Number of Buyers": [buyers],
    "Total Sold": [sold],
    "Available Stock": [stock],
    "Discount (%)": [discount],
    "Buyers-to-Stock Ratio": [buyers_stock_ratio],
    "Sold-to-Stock Ratio": [sold_stock_ratio],
    "Effective Price (₹)": [effective_price],
    "Is Returnable": [is_returnable],
    "Main Category": [main_cat],
    "Sub Category": [sub_cat],
    "Seller": [seller],
    "Return Policy": [return_policy]
})

if st.button("Predict Price"):
    prediction = model.predict(input_df)[0]
    st.success(f"💰 Predicted Price: ₹{prediction:,.2f}")

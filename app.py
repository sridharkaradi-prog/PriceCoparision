import streamlit as st
import pandas as pd
import random
import time

# --- MOCK SCRAPER FUNCTIONS ---
# Note: In a real scenario, you'd use Playwright or internal API URLs found via proxy sniffing.
# For this app, I'm simulating the data structure you'd receive.

def fetch_blinkit_price(product_name, pincode):
    # This would be your Playwright/API call
    time.sleep(1) # Simulating network delay
    base_price = random.randint(40, 60)
    return {"store": "Blinkit", "price": base_price, "delivery": 15, "delivery_time": "10 mins", "offer": "Flat ₹10 off"}

def fetch_zepto_price(product_name, pincode):
    time.sleep(1)
    base_price = random.randint(35, 55)
    return {"store": "Zepto", "price": base_price, "delivery": 0, "delivery_time": "8 mins", "offer": "Buy 1 Get 1"}

def fetch_swiggy_price(product_name, pincode):
    time.sleep(1)
    base_price = random.randint(45, 65)
    return {"store": "Instamart", "price": base_price, "delivery": 25, "delivery_time": "15 mins", "offer": "Extra 5% off"}

def fetch_bigbasket_price(product_name, pincode):
    time.sleep(1)
    base_price = random.randint(38, 58)
    return {"store": "Bigbasket", "price": base_price, "delivery": 30, "delivery_time": "30 mins", "offer": "No current offers"}

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Quick Commerce Compare", layout="wide")
st.title("🛒 Grocery Price Sniper")
st.write("Compare real-time prices across Blinkit, Zepto, Swiggy Instamart, and BigBasket.")

# --- SEARCH SIDEBAR ---
with st.sidebar:
    st.header("Search Parameters")
    product_query = st.text_input("Enter Product Name", placeholder="Amul Milk 500ml")
    pincode = st.text_input("Delivery Pincode", value="560001")
    search_button = st.button("Compare Prices")

# --- MAIN LOGIC ---
if search_button and product_query:
    with st.spinner(f"Searching for '{product_query}' in {pincode}..."):
        # Parallel Execution (simulated here)
        data = [
            fetch_blinkit_price(product_query, pincode),
            fetch_zepto_price(product_query, pincode),
            fetch_swiggy_price(product_query, pincode),
            fetch_bigbasket_price(product_query, pincode)
        ]

        df = pd.DataFrame(data)
        
        # Calculate Total Cost
        df['Total'] = df['price'] + df['delivery']
        df = df.sort_values(by='Total')

        # UI Results
        st.subheader(f"Best Price for: {product_query}")
        
        # Winner Highlight
        winner = df.iloc[0]
        st.success(f"🏆 **{winner['store']}** is the cheapest today! Total cost: **₹{winner['Total']}**")

        # Comparison Table
        cols = st.columns(len(df))
        for i, row in df.iterrows():
            with cols[i]:
                st.metric(label=row['store'], value=f"₹{row['Total']}", delta=f"{row['delivery_time']}")
                st.info(f"Item: ₹{row['price']}\n\nDel: ₹{row['delivery']}")
                st.caption(f"🎁 {row['offer']}")

        # Raw Data View
        with st.expander("Detailed Breakdown"):
            st.table(df)

else:
    st.info("👈 Enter a product name (e.g., 'Maggi', 'Eggs') in the sidebar to compare prices.")

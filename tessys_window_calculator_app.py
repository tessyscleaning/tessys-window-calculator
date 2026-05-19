
import streamlit as st
from datetime import date
from math import ceil

st.set_page_config(
    page_title="Tessy's Window Washing Calculator",
    page_icon="🪟",
    layout="centered"
)

st.markdown("""
# 🪟 Tessy's Window Washing Calculator
### Interior & Exterior Quote Estimator
**Tessy's Residential Cleaning Service**  
📞 925-349-5668  
🌐 tessysresidentialcleaning.com
""")

st.divider()

with st.expander("⚙️ Pricing Settings", expanded=False):
    interior_rate = st.number_input("Interior price per standard window", value=6.00, step=1.00)
    exterior_rate = st.number_input("Exterior price per standard window", value=6.00, step=1.00)
    screen_rate = st.number_input("Screen cleaning price each", value=3.00, step=1.00)
    track_rate = st.number_input("Track cleaning price each", value=4.00, step=1.00)
    french_pane_rate = st.number_input("French/small pane add-on each", value=5.00, step=1.00)
    sliding_door_rate = st.number_input("Sliding glass door price each", value=25.00, step=5.00)
    skylight_rate = st.number_input("Skylight price each", value=25.00, step=5.00)
    hard_water_rate = st.number_input("Hard water removal minimum add-on", value=100.00, step=10.00)
    second_story_fee = st.number_input("Second story / ladder access fee", value=75.00, step=10.00)
    minimum_job = st.number_input("Minimum job price", value=150.00, step=10.00)

st.divider()
st.subheader("Customer Information")

customer_name = st.text_input("Customer name")
phone = st.text_input("Phone number")
address = st.text_input("Service address")
quote_date = st.date_input("Quote date", value=date.today())

st.divider()
st.subheader("Window Details")

service_type = st.selectbox("Service type", ["Interior only", "Exterior only", "Interior + Exterior"])
standard_windows = st.number_input("Standard window openings", min_value=0, value=20, step=1)
large_windows = st.number_input("Large picture windows", min_value=0, value=0, step=1)
french_panes = st.number_input("French / small panes", min_value=0, value=0, step=1)
sliding_doors = st.number_input("Sliding glass doors", min_value=0, value=1, step=1)
screens = st.number_input("Screens to clean", min_value=0, value=0, step=1)
tracks = st.number_input("Tracks to clean", min_value=0, value=0, step=1)
skylights = st.number_input("Skylights", min_value=0, value=0, step=1)

st.divider()
st.subheader("Condition & Access")

home_level = st.selectbox("Home access / story level", ["Single story / easy access", "Two-story / ladder needed", "Difficult access / custom"])
condition = st.selectbox("Window condition", ["Light maintenance", "Average", "Heavy buildup"])
hard_water = st.radio("Hard water removal needed?", ["No", "Yes"], horizontal=True)
include_screens_tracks = st.checkbox("Include screens and tracks in quote", value=True)

adjusted_window_count = standard_windows + (large_windows * 2)

if service_type == "Interior only":
    base_price = adjusted_window_count * interior_rate
elif service_type == "Exterior only":
    base_price = adjusted_window_count * exterior_rate
else:
    base_price = adjusted_window_count * (interior_rate + exterior_rate)

addon_total = 0
addon_total += french_panes * french_pane_rate
addon_total += sliding_doors * sliding_door_rate
addon_total += skylights * skylight_rate

if include_screens_tracks:
    addon_total += screens * screen_rate
    addon_total += tracks * track_rate

if hard_water == "Yes":
    addon_total += hard_water_rate

if home_level == "Two-story / ladder needed":
    addon_total += second_story_fee
elif home_level == "Difficult access / custom":
    addon_total += second_story_fee * 2

condition_multiplier = {
    "Light maintenance": 1.00,
    "Average": 1.15,
    "Heavy buildup": 1.35
}[condition]

subtotal = (base_price + addon_total) * condition_multiplier
recommended_quote = max(subtotal, minimum_job)
recommended_quote = ceil(recommended_quote / 5) * 5

low_range = max(minimum_job, recommended_quote - 25)
high_range = recommended_quote + 75

st.divider()
st.subheader("Recommended Quote")

col1, col2, col3 = st.columns(3)
col1.metric("Base Price", f"${base_price:,.0f}")
col2.metric("Add-ons", f"${addon_total:,.0f}")
col3.metric("Recommended Quote", f"${recommended_quote:,.0f}")

st.success(f"Suggested client range: **${low_range:,.0f} – ${high_range:,.0f}**")

st.divider()
st.subheader("Ready-to-Send Quote Message")

quote_message = f"""Hi {customer_name or '[Name]'}, thank you for reaching out to Tessy's Residential Cleaning Service!

Based on the window details provided for {address or 'your home'}, the estimated price for {service_type.lower()} window washing is approximately ${low_range:,.0f}–${high_range:,.0f}, depending on final access, condition, screens/tracks, and any hard water buildup.

This estimate includes:
• Standard windows: {standard_windows}
• Large windows: {large_windows}
• Sliding doors: {sliding_doors}
• Screens: {screens}
• Tracks: {tracks}
• Skylights: {skylights}

We’d be happy to confirm the final price with a quick walkthrough or photos.

Tessy's Residential Cleaning Service
925-349-5668
tessysresidentialcleaning.com
"""

st.text_area("Copy this message:", quote_message, height=300)

st.download_button(
    label="Download Quote Message",
    data=quote_message,
    file_name=f"window_washing_quote_{customer_name or 'customer'}.txt",
    mime="text/plain"
)

st.caption("Pricing is an estimate only. Final pricing may vary depending on access, height, condition, hard water, window style, and customer expectations.")

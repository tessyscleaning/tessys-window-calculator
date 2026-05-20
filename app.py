import streamlit as st
from datetime import date
from math import ceil
from urllib.parse import quote

st.set_page_config(
    page_title="Tessy's Window Washing Calculator",
    page_icon="🪟",
    layout="centered"
)

st.markdown("""
# 🪟 Tessy's Window Washing Calculator
### Interior + Exterior Quote Estimator
**Tessy's Residential Cleaning Service**  
📞 925-349-5668  
🌐 tessysresidentialcleaning.com
""")

st.info("Built for fast iPhone/iPad walkthrough estimates. Pricing can be adjusted anytime in Pricing Settings.")

st.divider()

with st.expander("⚙️ Pricing Settings", expanded=False):
    st.write("These are updated professional window washing baseline prices. Adjust anytime.")
    interior_rate = st.number_input("Interior price per standard window opening", value=8.00, step=1.00)
    exterior_rate = st.number_input("Exterior price per standard window opening", value=10.00, step=1.00)
    both_sides_discount = st.number_input("Both sides package adjustment per standard window", value=-2.00, step=1.00)
    screen_rate = st.number_input("Screen cleaning price each", value=4.00, step=1.00)
    track_rate = st.number_input("Track cleaning price each", value=5.00, step=1.00)
    french_pane_rate = st.number_input("French/small pane add-on each", value=4.00, step=1.00)
    sliding_door_rate = st.number_input("Sliding glass door price each", value=35.00, step=5.00)
    skylight_rate = st.number_input("Skylight price each", value=35.00, step=5.00)
    hard_water_rate = st.number_input("Hard water removal minimum add-on", value=125.00, step=10.00)
    second_story_fee = st.number_input("Second story / ladder access fee", value=100.00, step=10.00)
    difficult_access_fee = st.number_input("Difficult access fee", value=175.00, step=10.00)
    minimum_job = st.number_input("Minimum job price", value=200.00, step=10.00)

st.divider()
st.subheader("Customer Information")

customer_name = st.text_input("Customer name")
customer_email = st.text_input("Customer email")
customer_phone = st.text_input("Phone number")
address = st.text_input("Service address")
quote_date = st.date_input("Quote date", value=date.today())

st.divider()
st.subheader("Window Washing Details")

service_type = st.selectbox("Service type", ["Interior + Exterior", "Interior only", "Exterior only"])

standard_windows = st.number_input("Standard window openings", min_value=0, value=20, step=1)
large_windows = st.number_input("Large picture windows", min_value=0, value=0, step=1)
french_panes = st.number_input("French / divided small panes", min_value=0, value=0, step=1)
sliding_doors = st.number_input("Sliding glass doors", min_value=0, value=1, step=1)
screens = st.number_input("Screens", min_value=0, value=0, step=1)
tracks = st.number_input("Tracks", min_value=0, value=0, step=1)
skylights = st.number_input("Skylights", min_value=0, value=0, step=1)

st.divider()
st.subheader("Condition & Access")

home_level = st.selectbox(
    "Access / story level",
    ["Single story / easy access", "Two-story / ladder needed", "Difficult access / custom"]
)

condition = st.selectbox(
    "Window condition",
    ["Light maintenance", "Average", "Heavy buildup"]
)

hard_water = st.radio("Hard water removal needed?", ["No", "Yes"], horizontal=True)
include_screens_tracks = st.checkbox("Include screens and tracks", value=True)

notes = st.text_area("Internal notes", placeholder="Example: pets, steep hill, locked gate, hard water, customer preferences...")

adjusted_window_count = standard_windows + (large_windows * 2)

if service_type == "Interior only":
    glass_total = adjusted_window_count * interior_rate
elif service_type == "Exterior only":
    glass_total = adjusted_window_count * exterior_rate
else:
    both_rate = interior_rate + exterior_rate + both_sides_discount
    glass_total = adjusted_window_count * both_rate

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
    addon_total += difficult_access_fee

condition_multiplier = {
    "Light maintenance": 1.00,
    "Average": 1.15,
    "Heavy buildup": 1.35
}[condition]

subtotal_before_condition = glass_total + addon_total
subtotal = subtotal_before_condition * condition_multiplier
recommended_quote = max(subtotal, minimum_job)
recommended_quote = ceil(recommended_quote / 10) * 10

low_range = max(minimum_job, recommended_quote - 30)
high_range = recommended_quote + 80

st.divider()
st.subheader("Recommended Quote")

col1, col2, col3 = st.columns(3)
col1.metric("Glass", f"${glass_total:,.0f}")
col2.metric("Add-ons", f"${addon_total:,.0f}")
col3.metric("Recommended", f"${recommended_quote:,.0f}")

st.success(f"Suggested client range: **${low_range:,.0f} – ${high_range:,.0f}**")

st.divider()
st.subheader("Ready-to-Send Quote")

quote_subject = "Window Washing Estimate from Tessy's Residential Cleaning Service"

quote_message = f"""Hi {customer_name or '[Name]'},

Thank you for reaching out to Tessy's Residential Cleaning Service!

Based on the window details provided for {address or 'your home'}, the estimated price for {service_type.lower()} window washing is approximately ${low_range:,.0f}–${high_range:,.0f}, depending on final access, condition, screens/tracks, and any hard water buildup.

Estimate summary:
• Service type: {service_type}
• Standard windows: {standard_windows}
• Large picture windows: {large_windows}
• French / divided panes: {french_panes}
• Sliding glass doors: {sliding_doors}
• Screens: {screens}
• Tracks: {tracks}
• Skylights: {skylights}
• Access level: {home_level}
• Condition: {condition}
• Hard water removal: {hard_water}

Recommended quote: ${recommended_quote:,.0f}

We’d be happy to confirm the final price with a quick walkthrough or photos.

Thank you,
Tessy's Residential Cleaning Service
925-349-5668
tessysresidentialcleaning.com

Pricing is an estimate only. Final pricing may vary depending on access, height, condition, hard water, window style, and customer expectations.
"""

st.text_area("Copy this quote message:", quote_message, height=420)

st.download_button(
    label="⬇️ Download Quote Message",
    data=quote_message,
    file_name=f"window_washing_quote_{customer_name or 'customer'}.txt",
    mime="text/plain"
)

mailto_to = customer_email if customer_email else ""
gmail_link = (
    "https://mail.google.com/mail/?view=cm&fs=1"
    f"&to={quote(mailto_to)}"
    f"&su={quote(quote_subject)}"
    f"&body={quote(quote_message)}"
)

mailto_link = (
    f"mailto:{quote(mailto_to)}"
    f"?subject={quote(quote_subject)}"
    f"&body={quote(quote_message)}"
)

st.markdown("### Send Options")
st.markdown(
    f"""
    <a href="{gmail_link}" target="_blank">
        <button style="background-color:#0f766e;color:white;padding:14px 20px;border:none;border-radius:10px;font-size:16px;cursor:pointer;margin-right:8px;">
            📧 Open in Gmail
        </button>
    </a>
    <a href="{mailto_link}" target="_blank">
        <button style="background-color:#1f4e78;color:white;padding:14px 20px;border:none;border-radius:10px;font-size:16px;cursor:pointer;">
            ✉️ Open Email App
        </button>
    </a>
    """,
    unsafe_allow_html=True
)

st.caption("If the email buttons do not open on iPhone/iPad, copy the quote message and paste it into Gmail, Mail, Messages, or Jobber.")

st.divider()
st.subheader("Pricing Notes")
st.markdown("""
- Standard window opening = one window unit/opening.
- Large picture windows are counted as 2 standard windows.
- French/divided panes add detail time.
- Screens, tracks, skylights, hard water, ladder work, and difficult access should increase price.
- Minimum job protects travel time, setup time, and admin time.
""")

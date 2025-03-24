import streamlit as st
from utils import validate_upi_id, validate_amount
from database import get_analytics_data, clear_history
import pandas as pd
from datetime import datetime, timedelta

def settings_modal():
    """Settings modal component."""
    with st.form("settings_form"):
        st.subheader("Settings")

        current_upi = st.session_state.get('upi_id', '')
        new_upi = st.text_input("UPI ID", 
                               value=current_upi,
                               placeholder="username@bank")

        merchant_name = st.text_input("Merchant Name (Optional)",
                                    value=st.session_state.get('merchant_name', ''),
                                    placeholder="Your Business Name")

        submitted = st.form_submit_button("Save Settings")

        if submitted:
            if validate_upi_id(new_upi):
                st.session_state['upi_id'] = new_upi
                st.session_state['merchant_name'] = merchant_name
                st.success("Settings saved successfully!")
                return True
            else:
                st.error("Invalid UPI ID format. Please check and try again.")
                return False
    return False

def payment_form():
    """Payment form component."""
    with st.form("payment_form"):
        amount = st.text_input("Amount (₹)", 
                             placeholder="Enter amount",
                             help="Enter amount between ₹1 and ₹1,00,000")

        generate_btn = st.form_submit_button("Generate QR Code")

        if generate_btn:
            if not st.session_state.get('upi_id'):
                st.error("Please configure UPI ID in settings first!")
                return None

            # Check for special code to clear history
            if amount == "ezhn9zwnax":
                clear_history()
                st.success("History cleared successfully!")
                return None

            if not validate_amount(amount):
                st.error("Please enter a valid amount between ₹1 and ₹1,00,000")
                return None

            return float(amount)
    return None

def analytics_dashboard():
    """Analytics dashboard component."""
    st.subheader("Analytics Dashboard")

    # Get analytics data
    data = get_analytics_data()

    # Display key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total QR Codes", f"{data['total_qr_codes']:,}")
    with col2:
        st.metric("Total Amount", f"₹{data['total_amount']:,.2f}")
    with col3:
        st.metric("Average Amount", f"₹{data['avg_amount']:,.2f}")

    # Daily Generation Trend
    st.subheader("Daily QR Code Generation")
    dates = list(data['daily_counts'].keys())
    counts = list(data['daily_counts'].values())

    trend_data = pd.DataFrame({
        'Date': dates,
        'QR Codes Generated': counts
    })
    st.line_chart(trend_data.set_index('Date'))
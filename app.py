import streamlit as st
import sqlite3
from components import settings_modal, payment_form, analytics_dashboard
from utils import generate_upi_qr, image_to_bytes, get_download_link, get_share_link
from styles import apply_custom_styles
from database import init_db, save_qr_generation, get_generation_history
from datetime import datetime

def main():
    # Initialize database
    init_db()

    # Page config
    st.set_page_config(
        page_title="UPI QR Generator",
        page_icon="💸",
        layout="centered"
    )

    # Apply custom styles
    apply_custom_styles()

    # Initialize session state
    if 'show_settings' not in st.session_state:
        st.session_state.show_settings = False
    if 'show_history' not in st.session_state:
        st.session_state.show_history = False
    if 'show_analytics' not in st.session_state:
        st.session_state.show_analytics = False

    # Main container
    with st.container():
        # Header with aligned buttons
        col1, col2, col3, col4 = st.columns([5, 1, 1, 1])
        with col1:
            st.title("UPI QR Generator")
            st.markdown('<p class="app-subtitle">Generate and track UPI payment QR codes effortlessly</p>', unsafe_allow_html=True)
        with col2:
            if st.button("📊 History", help="View your QR code generation history"):
                st.session_state.show_history = not st.session_state.show_history
                st.session_state.show_settings = False
                st.session_state.show_analytics = False
        with col3:
            if st.button("📈 Analytics", help="View analytics and trends"):
                st.session_state.show_analytics = not st.session_state.show_analytics
                st.session_state.show_history = False
                st.session_state.show_settings = False
        with col4:
            if st.button("⚙️ Settings", help="Configure your UPI ID and merchant details"):
                st.session_state.show_settings = not st.session_state.show_settings
                st.session_state.show_history = False
                st.session_state.show_analytics = False

        # Show settings modal
        if st.session_state.show_settings:
            if settings_modal():
                st.session_state.show_settings = False
                st.rerun()

        # Show analytics dashboard
        elif st.session_state.show_analytics:
            analytics_dashboard()
            if st.button("Close Analytics"):
                st.session_state.show_analytics = False
                st.rerun()

        # Show history
        elif st.session_state.show_history:
            st.subheader("Generation History")
            history = get_generation_history()
            for entry in history:
                # Parse datetime
                dt = datetime.strptime(entry['created_at'], '%Y-%m-%d %H:%M:%S')
                formatted_date = dt.strftime('%d %b %Y')
                formatted_time = dt.strftime('%I:%M %p')

                # Create styled history item
                st.markdown(f"""
                    <div class="history-item">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span class="history-amount">₹{entry['amount']:.2f}</span>
                            <span class="history-upi">{entry['upi_id']}</span>
                        </div>
                        <div class="history-datetime">
                            {formatted_date} at {formatted_time}
                        </div>
                        {f'<div class="history-merchant">{entry["merchant_name"]}</div>' if entry['merchant_name'] else ''}
                    </div>
                """, unsafe_allow_html=True)

            if st.button("Close History"):
                st.session_state.show_history = False
                st.rerun()

        # Main content
        else:
            # Show configured UPI ID
            if upi_id := st.session_state.get('upi_id'):
                st.caption(f"Configured UPI ID: {upi_id}")
            else:
                st.info("👆 Please configure your UPI ID in settings first!")

            # Payment form
            amount = payment_form()

            # Generate and display QR code
            if amount is not None:
                with st.spinner("Generating your QR code..."):
                    # Generate QR code
                    qr_image = generate_upi_qr(
                        st.session_state['upi_id'],
                        amount,
                        st.session_state.get('merchant_name', '')
                    )

                    # Save to history
                    save_qr_generation(
                        st.session_state['upi_id'],
                        amount,
                        st.session_state.get('merchant_name', '')
                    )

                    # Success message
                    st.success("QR code generated successfully!")

                    # Display QR code
                    st.markdown('<div class="qr-container">', unsafe_allow_html=True)
                    st.image(image_to_bytes(qr_image), 
                            caption=f"Payment QR Code for ₹{amount:,.2f}",
                            use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Download and Share buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="⬇️ Download QR",
                            data=image_to_bytes(qr_image),
                            file_name=f"upi_qr_{amount}.png",
                            mime="image/png",
                            help="Download QR code as PNG image"
                        )
                    with col2:
                        share_link = get_share_link(
                            st.session_state['upi_id'],
                            amount,
                            st.session_state.get('merchant_name', '')
                        )
                        st.markdown(f'<a href="{share_link}" target="_blank"><button style="width:100%;padding:10px;background-color:#FF5733;color:white;border:none;border-radius:5px;">🔗 Share Payment Link</button></a>', 
                                  unsafe_allow_html=True)

if __name__ == "__main__":
    main()
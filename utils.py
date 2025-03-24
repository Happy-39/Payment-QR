import re
import qrcode
import base64
from io import BytesIO
from PIL import Image
from datetime import datetime

def validate_upi_id(upi_id: str) -> bool:
    """Validate UPI ID format."""
    upi_pattern = r'^[\w\.\-]+@[\w\.\-]+$'
    return bool(re.match(upi_pattern, upi_id))

def validate_amount(amount: str) -> bool:
    """Validate payment amount."""
    try:
        amount = float(amount)
        return amount > 0 and amount <= 100000
    except ValueError:
        return False

def generate_upi_qr(upi_id: str, amount: float, name: str = "") -> Image.Image:
    """Generate UPI payment QR code."""
    # UPI URI format
    upi_uri = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_uri)
    qr.make(fit=True)

    # Create image
    qr_image = qr.make_image(fill_color="black", back_color="white")
    return qr_image

def image_to_bytes(image: Image.Image) -> bytes:
    """Convert PIL Image to bytes."""
    buf = BytesIO()
    image.save(buf, format='PNG')
    return buf.getvalue()

def get_download_link(image: Image.Image) -> str:
    """Generate a download link for the QR code image."""
    buf = BytesIO()
    image.save(buf, format='PNG')
    img_str = base64.b64encode(buf.getvalue()).decode()
    href = f'data:image/png;base64,{img_str}'
    return href

def get_share_link(upi_id: str, amount: float, name: str = "") -> str:
    """Generate a shareable UPI payment link."""
    return f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"
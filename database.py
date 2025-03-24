import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect('qr_history.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS qr_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            upi_id TEXT NOT NULL,
            amount REAL NOT NULL,
            merchant_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_qr_generation(upi_id: str, amount: float, merchant_name: str = ""):
    """Save QR code generation details to database."""
    conn = sqlite3.connect('qr_history.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO qr_history (upi_id, amount, merchant_name)
        VALUES (?, ?, ?)
    ''', (upi_id, amount, merchant_name))
    conn.commit()
    conn.close()

def clear_history():
    """Clear all QR generation history."""
    conn = sqlite3.connect('qr_history.db')
    c = conn.cursor()
    c.execute('DELETE FROM qr_history')
    conn.commit()
    conn.close()

def get_generation_history() -> List[Dict]:
    """Retrieve QR code generation history."""
    conn = sqlite3.connect('qr_history.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''
        SELECT * FROM qr_history 
        ORDER BY created_at DESC 
        LIMIT 10
    ''')
    history = [dict(row) for row in c.fetchall()]
    conn.close()
    return history

def get_analytics_data() -> Dict:
    """Get analytics data for dashboard."""
    conn = sqlite3.connect('qr_history.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Total QR codes generated
    c.execute('SELECT COUNT(*) as total FROM qr_history')
    total_qr_codes = c.fetchone()['total']

    # Total amount processed
    c.execute('SELECT SUM(amount) as total FROM qr_history')
    total_amount = c.fetchone()['total'] or 0

    # Average amount per QR
    c.execute('SELECT AVG(amount) as avg FROM qr_history')
    avg_amount = c.fetchone()['avg'] or 0

    # Daily generation counts (last 7 days)
    seven_days_ago = datetime.now() - timedelta(days=7)
    c.execute('''
        SELECT date(created_at) as date, COUNT(*) as count 
        FROM qr_history 
        WHERE created_at >= ?
        GROUP BY date(created_at)
        ORDER BY date
    ''', (seven_days_ago.strftime('%Y-%m-%d'),))
    daily_counts = dict(c.fetchall())

    conn.close()

    return {
        'total_qr_codes': total_qr_codes,
        'total_amount': total_amount,
        'avg_amount': avg_amount,
        'daily_counts': daily_counts
    }
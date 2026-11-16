
from database import get_db_connection
from config import SERVICE_TIME
from services.prediction_service import predict_waiting_time

# Recalculate waiting times using ML
def update_waiting_times():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM customers
        WHERE status = 'waiting'
        ORDER BY token_number
    """)

    customers = cursor.fetchall()

    total_waiting = len(customers)

    for index, customer in enumerate(customers):

        waiting_time = predict_waiting_time(
            customers_ahead=index,
            total_waiting=total_waiting,
            average_service_time=SERVICE_TIME
        )

        cursor.execute("""
            UPDATE customers
            SET waiting_time = ?
            WHERE id = ?
        """, (waiting_time, customer["id"]))

    conn.commit()
    conn.close()

# Add a new customer
def add_customer(name):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(token_number) FROM customers")
    result = cursor.fetchone()

    token_number = (result[0] or 0) + 1

    cursor.execute("""
        INSERT INTO customers (name, token_number, waiting_time)
        VALUES (?, ?, 0)
    """, (name, token_number))

    conn.commit()
    conn.close()

    update_waiting_times()

    # Get the new customer's predicted waiting time
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT waiting_time FROM customers
        WHERE token_number = ?
    """, (token_number,))

    result = cursor.fetchone()
    conn.close()

    return {
        "name": name,
        "token_number": token_number,
        "waiting_time": result["waiting_time"],
        "status": "waiting"
    }

# Get all waiting customers
def get_queue():

    update_waiting_times()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM customers
        WHERE status = 'waiting'
        ORDER BY token_number
    """)

    customers = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return customers

# Serve next customer
def serve_customer():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM customers
        WHERE status = 'waiting'
        ORDER BY token_number
        LIMIT 1
    """)

    customer = cursor.fetchone()

    if customer is None:
        conn.close()
        return None

    cursor.execute("""
        UPDATE customers
        SET status = 'served'
        WHERE id = ?
    """, (customer["id"],))

    conn.commit()
    conn.close()

    served_customer = dict(customer)
    served_customer["status"] = "served"

    update_waiting_times()

    return served_customer

# Cancel customer token
def cancel_customer(token_number):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE customers
        SET status = 'cancelled'
        WHERE token_number = ? AND status = 'waiting'
    """, (token_number,))

    updated = cursor.rowcount

    conn.commit()
    conn.close()

    if updated > 0:
        update_waiting_times()

    return updated > 0
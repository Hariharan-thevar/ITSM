import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# ---------------- Database ----------------
conn = sqlite3.connect("flight_booking.db", check_same_thread=False)
cursor = conn.cursor()

# Create Tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_no TEXT,
    source TEXT,
    destination TEXT,
    departure TEXT,
    seats INTEGER,
    price REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_id INTEGER,
    passenger_name TEXT,
    booking_date TEXT
)
""")

conn.commit()

st.set_page_config(page_title="Flight Booking System", layout="wide")
st.title("✈ Flight Booking Management System")

menu = st.sidebar.selectbox("Menu", 
                            ["Add Flight (Admin)", "Search & Book Flight", "View Bookings"])

# ---------------- Add Flight ----------------
if menu == "Add Flight (Admin)":
    st.subheader("➕ Add New Flight")

    flight_no = st.text_input("Flight Number")
    source = st.text_input("Source")
    destination = st.text_input("Destination")
    departure = st.text_input("Departure Time")
    seats = st.number_input("Total Seats", min_value=1)
    price = st.number_input("Ticket Price", min_value=0.0)

    if st.button("Add Flight"):
        cursor.execute("""
            INSERT INTO flights (flight_no, source, destination, departure, seats, price)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (flight_no, source, destination, departure, seats, price))
        conn.commit()
        st.success("Flight Added Successfully!")

# ---------------- Search & Book ----------------
elif menu == "Search & Book Flight":
    st.subheader("🔎 Search Flights")

    df = pd.read_sql_query("SELECT * FROM flights", conn)

    if not df.empty:
        st.dataframe(df)

        flight_ids = df["id"].tolist()
        selected_flight = st.selectbox("Select Flight ID", flight_ids)
        passenger_name = st.text_input("Passenger Name")

        if st.button("Book Ticket"):
            cursor.execute("SELECT seats FROM flights WHERE id=?", (selected_flight,))
            available_seats = cursor.fetchone()[0]

            if available_seats > 0:
                cursor.execute("""
                    INSERT INTO bookings (flight_id, passenger_name, booking_date)
                    VALUES (?, ?, ?)
                """, (selected_flight, passenger_name,
                      datetime.now().strftime("%Y-%m-%d %H:%M")))

                cursor.execute("""
                    UPDATE flights SET seats = seats - 1 WHERE id=?
                """, (selected_flight,))

                conn.commit()
                st.success("✅ Ticket Booked Successfully!")
            else:
                st.error("❌ No Seats Available")
    else:
        st.info("No flights available.")

# ---------------- View Bookings ----------------
elif menu == "View Bookings":
    st.subheader("📋 All Bookings")

    df_bookings = pd.read_sql_query("""
        SELECT bookings.id, flights.flight_no, passenger_name, booking_date
        FROM bookings
        JOIN flights ON bookings.flight_id = flights.id
    """, conn)

    if not df_bookings.empty:
        st.dataframe(df_bookings)
    else:
        st.info("No bookings available.")            
            conn.commit()
            st.success("Ticket Created Successfully ✅")
        else:
            st.warning("Please fill all fields")

# -----------------------
# View Tickets
# -----------------------
if menu == "View Tickets":
    st.subheader("All Tickets")
    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()

    if tickets:
        for t in tickets:
            st.write(f"**ID:** {t[0]}")
            st.write(f"Name: {t[1]}")
            st.write(f"Issue: {t[2]}")
            st.write(f"Status: {t[3]}")
            st.write("---")
    else:
        st.info("No tickets found")

conn.close()if __name__ == '__main__':
    app.run(debug=True)

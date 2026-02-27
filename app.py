import streamlit as st
import sqlite3

st.title("💼 ITSM Ticket Management System")

# Create Database
conn = sqlite3.connect("tickets.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    issue TEXT,
    status TEXT
)
""")
conn.commit()

menu = st.sidebar.selectbox("Menu", ["Create Ticket", "View Tickets"])

# Create Ticket
if menu == "Create Ticket":
    st.subheader("Create New Ticket")
    name = st.text_input("Enter Your Name")
    issue = st.text_area("Describe Your Issue")

    if st.button("Submit Ticket"):
        if name and issue:
            cursor.execute("INSERT INTO tickets (name, issue, status) VALUES (?, ?, ?)",
                           (name, issue, "Open"))
            conn.commit()
            st.success("Ticket Created Successfully ✅")
        else:
            st.warning("Please fill all fields")

# View Tickets
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
            if t[3] == "Open":
                if st.button(f"Close Ticket {t[0]}"):
                    cursor.execute("UPDATE tickets SET status='Closed' WHERE id=?", (t[0],))
                    conn.commit()
                    st.success(f"Ticket {t[0]} Closed")
            st.write("---")
    else:
        st.info("No tickets found")

conn.close()        return redirect('/tickets')
    return render_template('create_ticket.html')

@app.route('/tickets')
def view_tickets():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()
    conn.close()
    return render_template('view_tickets.html', tickets=tickets)

@app.route('/close/<int:id>')
def close_ticket(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE tickets SET status='Closed' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/tickets')

if __name__ == '__main__':
    app.run(debug=True)

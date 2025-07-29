import streamlit as st
import mysql.connector
from mysql.connector import Error

# MySQL Connection
def connect_db():
    return mysql.connector.connect(
        host="sql.freedb.tech",
        user="freedb_preeti_mishra",
        password="QUUFH#EGu2rb99#",
        database="freedb_user_db"
    )
# ✅ Function to create the table if it doesn't exist
def create_table():
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                age INT
            )
        """)
        db.commit()
        cursor.close()
        db.close()
    except Error as e:
        st.error(f"Error creating table: {e}")

# ✅ Function to insert data
def insert_data(name, age):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
        db.commit()
        cursor.close()
        db.close()
    except Error as e:
        st.error(f"Insert Error: {e}")

# ✅ Function to fetch data
def fetch_data():
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        cursor.close()
        db.close()
        return rows
    except Error as e:
        st.error(f"Fetch Error: {e}")
        return []

# ✅ Streamlit UI
st.title("MySQL + Streamlit App on Replit")

# Create table when app starts
create_table()

name = st.text_input("Enter Name")
age = st.number_input("Enter Age", 1, 100)

if st.button("Add to DB"):
    if name:
        insert_data(name, age)
        st.success("Data inserted!")
    else:
        st.warning("Please enter a name.")

if st.button("Show All Data"):
    data = fetch_data()
    if data:
        st.write("User Data:")
        for row in data:
            st.write(row)
    else:
        st.info("No data found.")


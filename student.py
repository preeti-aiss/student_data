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

# ✅ Create BMI table
def create_table():
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                weight FLOAT,
                height FLOAT,
                bmi FLOAT,
                category VARCHAR(50)
            )
        """)
        db.commit()
        cursor.close()
        db.close()
    except Error as e:
        st.error(f"Error creating table: {e}")

# ✅ Insert BMI data
def insert_data(name, weight, height, bmi, category):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO bmi_users (name, weight, height, bmi, category) VALUES (%s, %s, %s, %s, %s)",
            (name, weight, height, bmi, category)
        )
        db.commit()
        cursor.close()
        db.close()
    except Error as e:
        st.error(f"Insert Error: {e}")

# ✅ Fetch all BMI records
def fetch_data():
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM bmi_users")
        rows = cursor.fetchall()
        cursor.close()
        db.close()
        return rows
    except Error as e:
        st.error(f"Fetch Error: {e}")
        return []

# ✅ BMI Calculation
def calculate_bmi(weight, height):
    if height == 0:
        return 0, "Invalid height"
    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 2)
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obese"
    return bmi, category

# ✅ Streamlit UI
st.title("BMI Calculator with MySQL")

# Create table on start
create_table()

# Input Fields
name = st.text_input("Enter Name")
weight = st.number_input("Enter Weight (kg)", min_value=1.0, step=0.5)
height = st.number_input("Enter Height (cm)", min_value=1.0, step=0.5)

if st.button("Calculate & Save BMI"):
    if name:
        bmi, category = calculate_bmi(weight, height)
        insert_data(name, weight, height, bmi, category)
        st.success(f"{name}'s BMI is {bmi} ({category}) and saved to database.")
    else:
        st.warning("Please enter a name.")

if st.button("Show All Records"):
    records = fetch_data()
    if records:
        st.write("Stored BMI Records:")
        for rec in records:
            st.write(f"Name: {rec[1]}, Weight: {rec[2]} kg, Height: {rec[3]} cm, BMI: {rec[4]}, Category: {rec[5]}")
    else:
        st.info("No records found.")

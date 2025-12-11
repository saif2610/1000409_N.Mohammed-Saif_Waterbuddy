import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import json
import os
import matplotlib.pyplot as plt
import time

# ---------------------- File Paths ----------------------
USERS_FILE = "users.json"
LOGS_FILE = "water_logs.json"

# ---------------------- Helper Functions ----------------------
def load_data(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ---------------------- User Authentication ----------------------
def signup():
    st.title("Create Account")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=5, max_value=100)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        users = load_data(USERS_FILE)

        if email in users:
            st.error("Email already exists. Try logging in.")
            return

        users[email] = {
            "name": name,
            "age": age,
            "password": password
        }

        save_data(USERS_FILE, users)
        st.success("Account created successfully! Please log in.")

def login():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_data(USERS_FILE)

        if email in users and users[email]["password"] == password:
            st.session_state["email"] = email
            st.rerun()
        else:
            st.error("Invalid email or password.")

# ---------------------- Water Intake Tracking ----------------------
def add_water_intake(email):
    st.title("💧 Water Intake Tracker")

    logs = load_data(LOGS_FILE)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if email not in logs:
        logs[email] = {}

    if today not in logs[email]:
        logs[email][today] = 0

    st.subheader("Today's Intake")
    intake = st.number_input("Enter water intake (ml):", min_value=0)

    if st.button("Add Intake"):
        logs[email][today] += intake
        save_data(LOGS_FILE, logs)
        st.success(f"Added {intake} ml!")
        time.sleep(1)
        st.rerun()

    st.progress(min(logs[email][today] / 3000, 1.0))
    st.text(f"Total: {logs[email][today]} ml / 3000 ml")

    if st.button("Reset Today's Water Intake ❌"):
        logs[email][today] = 0
        save_data(LOGS_FILE, logs)
        st.success("Today's intake reset!")
        time.sleep(1)
        st.rerun()

    st.write("---")
    show_weekly_graph(email)

# ---------------------- Graph ----------------------
def show_weekly_graph(email):
    st.subheader("📊 Weekly Water Intake")

    logs = load_data(LOGS_FILE)
    today = datetime.now(timezone.utc).date()
    dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]

    intake_values = [logs.get(email, {}).get(day, 0) for day in dates]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, intake_values)
    plt.xticks(rotation=45)
    plt.ylabel("Intake (ml)")
    plt.xlabel("Date")
    plt.title("Past 7 Days Water Intake")

    st.pyplot(plt)

    # ---------------------------------------------------------------
    # ✅ NEW BUTTON ADDED BELOW GRAPH (you requested this)
    # ---------------------------------------------------------------
    st.markdown("### 🔁 Reset Today's Water Intake (Below Graph)")

    if st.button("Reset Today (Below Graph)"):
        logs = load_data(LOGS_FILE)
        today_key = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        if email in logs and today_key in logs[email]:
            logs[email][today_key] = 0
            save_data(LOGS_FILE, logs)
            st.success("Today's data has been reset!")
            time.sleep(1)
            st.rerun()
        else:
            st.info("No water intake logged for today.")
    # ---------------------------------------------------------------

# ---------------------- Main App ----------------------
def main():
    if "email" not in st.session_state:
        menu = st.sidebar.selectbox("Menu", ["Login", "Sign Up"])

        if menu == "Login":
            login()
        else:
            signup()
        return

    st.sidebar.write(f"Logged in as: {st.session_state['email']}")
    page = st.sidebar.selectbox("Navigate", ["Add Intake", "Logout"])

    if page == "Add Intake":
        add_water_intake(st.session_state["email"])
    else:
        del st.session_state["email"]
        st.rerun()

if __name__ == "__main__":
    main()

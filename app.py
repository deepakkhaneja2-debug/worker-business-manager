import os
from datetime import date
import streamlit as st

try:
    from supabase import create_client
except ImportError:
    create_client = None

st.set_page_config(page_title="Worker & Business Manager", page_icon="👷", layout="wide")

st.title("👷 Worker & Business Manager")
st.caption("Workers • Attendance • Dena/Lena • Shops/Godowns • Events")

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

def get_client():
    if not create_client:
        return None
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_client()

if not supabase:
    st.warning(
        "Cloud database is not connected yet. Add SUPABASE_URL and SUPABASE_KEY "
        "in Streamlit secrets/environment variables."
    )

tabs = st.tabs([
    "🏠 Dashboard", "👷 Workers", "📅 Attendance",
    "💰 Dena/Lena", "🏪 Locations", "🎪 Events"
])

with tabs[0]:
    st.subheader("Dashboard")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Workers", "—")
    c2.metric("Present Today", "—")
    c3.metric("Upcoming Events", "—")
    c4.metric("Pending Amount", "—")
    st.info("Next: connect Supabase and create the database tables from schema.sql.")

with tabs[1]:
    st.subheader("Worker Management")
    with st.form("worker_form"):
        name = st.text_input("Worker Name *")
        phone = st.text_input("Mobile")
        wage_type = st.selectbox("Wage Type", ["Daily", "Monthly"])
        wage = st.number_input("Wage / Salary", min_value=0.0, step=100.0)
        joining_date = st.date_input("Joining Date", value=date.today())
        submitted = st.form_submit_button("Add Worker")
        if submitted:
            if not supabase:
                st.error("Connect Supabase first.")
            elif not name.strip():
                st.error("Worker name is required.")
            else:
                row = {
                    "name": name.strip(),
                    "phone": phone.strip() or None,
                    "wage_type": wage_type.lower(),
                    "wage_amount": wage,
                    "joining_date": str(joining_date),
                    "active": True,
                }
                supabase.table("workers").insert(row).execute()
                st.success(f"{name} added.")

    if supabase:
        result = supabase.table("workers").select("*").eq("active", True).order("name").execute()
        st.dataframe(result.data, use_container_width=True)

with tabs[2]:
    st.subheader("Daily Attendance")
    st.info("Worker-wise Present / Absent / Half Day / Overtime entry will be enabled here after database setup.")

with tabs[3]:
    st.subheader("Dena / Lena")
    st.info("Payments, advances, recoveries and running worker balance will be enabled here.")

with tabs[4]:
    st.subheader("Shop / Godown")
    st.info("Locations, rent, security deposit, due date and rent payments will be enabled here.")

with tabs[5]:
    st.subheader("Events")
    st.info("Upcoming events, venue, client and assigned workers will be enabled here.")

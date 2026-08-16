import os
from datetime import date
import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Worker & Business Manager", page_icon="👷", layout="wide")

url = os.getenv("SUPABASE_URL", "")
key = os.getenv("SUPABASE_KEY", "")
if not url or not key:
    st.error("Supabase secrets are missing.")
    st.stop()

supabase = create_client(url, key)

st.title("👷 Worker & Business Manager")
st.caption("Workers • Attendance • Dena/Lena • Shops/Godowns • Events")

tabs = st.tabs(["🏠 Dashboard","👷 Workers","📅 Attendance","💰 Dena/Lena","🏪 Locations","🎪 Events"])

with tabs[0]:
    workers = supabase.table("workers").select("id", count="exact").eq("active", True).execute()
    events = supabase.table("events").select("id", count="exact").eq("status", "upcoming").execute()
    a,b,c = st.columns(3)
    a.metric("Active Workers", workers.count or 0)
    b.metric("Upcoming Events", events.count or 0)
    c.metric("Cloud", "Connected")
    st.success("☁️ Supabase connected.")

with tabs[1]:
    st.subheader("👷 Workers")
    with st.form("add_worker"):
        name = st.text_input("Worker Name *")
        phone = st.text_input("Mobile")
        wage_type = st.selectbox("Wage Type", ["Daily","Monthly"])
        wage = st.number_input("Wage / Salary", min_value=0.0, step=100.0)
        joining = st.date_input("Joining Date", value=date.today())
        if st.form_submit_button("Add Worker"):
            if not name.strip():
                st.error("Worker name is required.")
            else:
                supabase.table("workers").insert({
                    "name": name.strip(), "phone": phone.strip() or None,
                    "wage_type": wage_type.lower(), "wage_amount": wage,
                    "joining_date": str(joining), "active": True
                }).execute()
                st.success("Worker added.")
                st.rerun()

    result = supabase.table("workers").select("*").eq("active", True).order("name").execute()
    for w in result.data or []:
        a,b,c,d = st.columns([3,2,2,1])
        a.write(f"**{w['name']}**")
        b.write(w.get("phone") or "No mobile")
        c.write(f"{w['wage_type'].title()}: ₹{w['wage_amount']}")
        if d.button("Remove", key=f"remove_{w['id']}"):
            supabase.table("workers").update({"active": False}).eq("id", w["id"]).execute()
            st.rerun()

with tabs[2]:
    st.subheader("📅 Attendance")
    st.info("Attendance module next.")

with tabs[3]:
    st.subheader("💰 Dena / Lena")
    st.info("Worker ledger module next.")

with tabs[4]:
    st.subheader("🏪 Locations")
    st.info("Shop/Godown + rent module next.")

with tabs[5]:
    st.subheader("🎪 Events")
    with st.form("event_form"):
        name = st.text_input("Event Name *")
        client = st.text_input("Client")
        venue = st.text_input("Venue / Location")
        start = st.date_input("Start Date", value=date.today())
        end = st.date_input("End Date", value=date.today())
        show_location = st.toggle("📍 Show Location to Workers", False)
        show_items = st.toggle("📦 Show Samaan to Workers", True)
        if st.form_submit_button("Create Event"):
            if not name.strip():
                st.error("Event name is required.")
            else:
                supabase.table("events").insert({
                    "name": name.strip(), "client_name": client.strip() or None,
                    "venue": venue.strip() or None, "start_date": str(start),
                    "end_date": str(end), "status": "upcoming",
                    "show_location_to_workers": show_location,
                    "show_items_to_workers": show_items
                }).execute()
                st.success("Event created.")
                st.rerun()

    evs = supabase.table("events").select("*").order("start_date").execute()
    for ev in evs.data or []:
        with st.expander(f"🎪 {ev['name']} — {ev['start_date']}"):
            st.write(f"**Client:** {ev.get('client_name') or '-'}")
            st.write(f"**Location:** {ev.get('venue') or '-'}")
            st.write(f"📍 Location to workers: {'ON' if ev.get('show_location_to_workers') else 'OFF'}")
            st.write(f"📦 Samaan to workers: {'ON' if ev.get('show_items_to_workers') else 'OFF'}")

            active = supabase.table("workers").select("id,name").eq("active", True).order("name").execute()
            selected = st.multiselect("Assign Workers", active.data or [],
                                      format_func=lambda x: x["name"],
                                      key=f"workers_{ev['id']}")
            if st.button("Save Worker Assignment", key=f"assign_{ev['id']}"):
                supabase.table("event_workers").delete().eq("event_id", ev["id"]).execute()
                if selected:
                    supabase.table("event_workers").insert(
                        [{"event_id": ev["id"], "worker_id": x["id"]} for x in selected]
                    ).execute()
                st.success("Workers assigned.")

            st.markdown("#### 📦 Samaan Checklist")
            item = st.text_input("Samaan", key=f"item_{ev['id']}")
            qty = st.number_input("Quantity", min_value=1.0, value=1.0, step=1.0,
                                  key=f"qty_{ev['id']}")
            if st.button("Add Samaan", key=f"add_{ev['id']}"):
                if item.strip():
                    supabase.table("event_items").insert({
                        "event_id": ev["id"], "item_name": item.strip(),
                        "quantity": qty, "loaded": False
                    }).execute()
                    st.rerun()

            items = supabase.table("event_items").select("*").eq("event_id", ev["id"]).order("item_name").execute()
            for x in items.data or []:
                p,q,r = st.columns([4,1,4])
                p.write(f"{x['item_name']} × {x['quantity']}")
                loaded = q.checkbox("Loaded", value=x["loaded"], key=f"load_{x['id']}")
                note = r.text_input("Note", value=x.get("note") or "", key=f"note_{x['id']}")
                if loaded != x["loaded"] or note != (x.get("note") or ""):
                    supabase.table("event_items").update({
                        "loaded": loaded, "note": note
                    }).eq("id", x["id"]).execute()

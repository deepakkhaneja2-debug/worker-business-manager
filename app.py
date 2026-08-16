import os
from datetime import date

import streamlit as st
from supabase import create_client


# =========================================================
# APP CONFIG
# =========================================================

st.set_page_config(
    page_title="Worker & Business Manager",
    page_icon="👷",
    layout="wide",
)


# =========================================================
# SUPABASE
# =========================================================

def get_secret(name):
    try:
        return st.secrets[name]
    except Exception:
        return os.getenv(name, "")


SUPABASE_URL = get_secret("SUPABASE_URL")
SUPABASE_KEY = get_secret("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Supabase secrets are missing.")
    st.stop()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# =========================================================
# HEADER
# =========================================================

st.title("👷 Worker & Business Manager")
st.caption(
    "Workers • Attendance • Dena/Lena • Shops/Godowns • Events"
)


# =========================================================
# TABS
# =========================================================

(
    dashboard_tab,
    workers_tab,
    attendance_tab,
    money_tab,
    locations_tab,
    events_tab,
    master_tab,
) = st.tabs(
    [
        "🏠 Dashboard",
        "👷 Workers",
        "📅 Attendance",
        "💰 Dena/Lena",
        "🏪 Locations",
        "🎪 Events",
        "⚙️ Samaan Master",
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

with dashboard_tab:

    st.subheader("🏠 Dashboard")

    try:
        workers_result = (
            supabase
            .table("workers")
            .select("id", count="exact")
            .eq("active", True)
            .execute()
        )

        events_result = (
            supabase
            .table("events")
            .select("id", count="exact")
            .eq("status", "upcoming")
            .execute()
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Active Workers",
            workers_result.count or 0,
        )

        col2.metric(
            "Upcoming Events",
            events_result.count or 0,
        )

        col3.metric(
            "System",
            "Connected",
        )

        st.success("☁️ Supabase connected successfully.")

    except Exception as e:
        st.error(f"Dashboard error: {e}")


# =========================================================
# WORKERS
# =========================================================

with workers_tab:

    st.subheader("👷 Workers")

    with st.expander("➕ Add Worker", expanded=True):

        with st.form("add_worker_form"):

            worker_name = st.text_input(
                "Worker Name *"
            )

            worker_phone = st.text_input(
                "Mobile"
            )

            wage_type = st.selectbox(
                "Wage Type",
                ["Daily", "Monthly"],
            )

            wage_amount = st.number_input(
                "Wage / Salary",
                min_value=0.0,
                step=100.0,
            )

            joining_date = st.date_input(
                "Joining Date",
                value=date.today(),
            )

            submitted = st.form_submit_button(
                "Add Worker"
            )

            if submitted:

                if not worker_name.strip():

                    st.error(
                        "Worker name is required."
                    )

                else:

                    try:

                        supabase.table(
                            "workers"
                        ).insert(
                            {
                                "name": worker_name.strip(),
                                "phone": (
                                    worker_phone.strip()
                                    or None
                                ),
                                "wage_type": wage_type.lower(),
                                "wage_amount": wage_amount,
                                "joining_date": str(
                                    joining_date
                                ),
                                "active": True,
                            }
                        ).execute()

                        st.success(
                            "Worker added successfully."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Could not add worker: {e}"
                        )

    st.markdown("### Active Workers")

    try:

        workers = (
            supabase
            .table("workers")
            .select("*")
            .eq("active", True)
            .order("name")
            .execute()
        )

        if not workers.data:

            st.info(
                "No active workers found."
            )

        for worker in workers.data:

            col1, col2, col3, col4 = st.columns(
                [3, 2, 2, 1]
            )

            col1.write(
                f"**{worker['name']}**"
            )

            col2.write(
                worker.get("phone")
                or "No mobile"
            )

            col3.write(
                f"{worker['wage_type'].title()}: "
                f"₹{worker['wage_amount']}"
            )

            if col4.button(
                "Remove",
                key=f"remove_worker_{worker['id']}",
            ):

                supabase.table(
                    "workers"
                ).update(
                    {"active": False}
                ).eq(
                    "id",
                    worker["id"],
                ).execute()

                st.success(
                    "Worker removed."
                )

                st.rerun()

    except Exception as e:

        st.error(
            f"Workers error: {e}"
        )


# =========================================================
# ATTENDANCE
# =========================================================

with attendance_tab:

    st.subheader("📅 Attendance")

    st.info(
        "Attendance module will be connected next."
    )


# =========================================================
# MONEY
# =========================================================

with money_tab:

    st.subheader("💰 Dena / Lena")

    st.info(
        "Worker payment ledger will be connected next."
    )


# =========================================================
# LOCATIONS
# =========================================================

with locations_tab:

    st.subheader("🏪 Shops / Godowns")

    st.info(
        "Shop/Godown and rent management will be connected next."
    )


# =========================================================
# EVENTS
# =========================================================

with events_tab:

    st.subheader("🎪 Events")

    # -----------------------------------------------------
    # CREATE EVENT
    # -----------------------------------------------------

    with st.expander(
        "➕ Create New Event",
        expanded=True,
    ):

        with st.form("create_event_form"):

            event_name = st.text_input(
                "Event Name *"
            )

            client_name = st.text_input(
                "Client Name"
            )

            venue = st.text_input(
                "Event Location"
            )

            start_date = st.date_input(
                "Start Date",
                value=date.today(),
            )

            end_date = st.date_input(
                "End Date",
                value=date.today(),
            )

            show_location = st.toggle(
                "📍 Show Location to Workers",
                value=False,
            )

            show_items = st.toggle(
                "📦 Show Samaan to Workers",
                value=True,
            )

            create_event = st.form_submit_button(
                "Create Event"
            )

            if create_event:

                if not event_name.strip():

                    st.error(
                        "Event name is required."
                    )

                else:

                    try:

                        supabase.table(
                            "events"
                        ).insert(
                            {
                                "name": event_name.strip(),
                                "client_name": (
                                    client_name.strip()
                                    or None
                                ),
                                "venue": (
                                    venue.strip()
                                    or None
                                ),
                                "start_date": str(
                                    start_date
                                ),
                                "end_date": str(
                                    end_date
                                ),
                                "status": "upcoming",
                                "show_location_to_workers":
                                    show_location,
                                "show_items_to_workers":
                                    show_items,
                            }
                        ).execute()

                        st.success(
                            "Event created successfully."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Could not create event: {e}"
                        )

    # -----------------------------------------------------
    # EVENT LIST
    # -----------------------------------------------------

    try:

        events = (
            supabase
            .table("events")
            .select("*")
            .order("start_date")
            .execute()
        )

    except Exception as e:

        st.error(
            f"Could not load events: {e}"
        )

        events = None

    if events and events.data:

        for event in events.data:

            with st.expander(
                f"🎪 {event['name']} "
                f"— {event['start_date']}"
            ):

                st.write(
                    f"**Client:** "
                    f"{event.get('client_name') or '-'}"
                )

                st.write(
                    f"**Location:** "
                    f"{event.get('venue') or '-'}"
                )

                location_status = (
                    "🟢 ON"
                    if event.get(
                        "show_location_to_workers"
                    )
                    else "🔴 OFF"
                )

                item_status = (
                    "🟢 ON"
                    if event.get(
                        "show_items_to_workers"
                    )
                    else "🔴 OFF"
                )

                st.write(
                    f"📍 Location to Workers: "
                    f"{location_status}"
                )

                st.write(
                    f"📦 Samaan to Workers: "
                    f"{item_status}"
                )

                # =========================================
                # WORKER ASSIGNMENT
                # =========================================

                st.markdown(
                    "### 👷 Assign Workers"
                )

                active_workers = (
                    supabase
                    .table("workers")
                    .select("id,name")
                    .eq("active", True)
                    .order("name")
                    .execute()
                )

                selected_workers = st.multiselect(
                    "Select Workers",
                    active_workers.data or [],
                    format_func=lambda x: x["name"],
                    key=f"event_workers_{event['id']}",
                )

                if st.button(
                    "Save Worker Assignment",
                    key=f"save_workers_{event['id']}",
                ):

                    supabase.table(
                        "event_workers"
                    ).delete().eq(
                        "event_id",
                        event["id"],
                    ).execute()

                    if selected_workers:

                        supabase.table(
                            "event_workers"
                        ).insert(
                            [
                                {
                                    "event_id": event["id"],
                                    "worker_id": worker["id"],
                                }
                                for worker in selected_workers
                            ]
                        ).execute()

                    st.success(
                        "Workers assigned."
                    )

                    st.rerun()

                # =========================================
                # EVENT SAMAAN SELECTION
                # =========================================

                st.markdown("### 📦 Add Samaan")

                categories = (
                    supabase
                    .table("item_categories")
                    .select("*")
                    .eq("active", True)
                    .order("sort_order")
                    .order("name")
                    .execute()
                )

                if not categories.data:

                    st.warning(
                        "No Samaan categories found. "
                        "Create them in ⚙️ Samaan Master."
                    )

                for category in categories.data:

                    items = (
                        supabase
                        .table("master_items")
                        .select("*")
                        .eq(
                            "category_id",
                            category["id"],
                        )
                        .eq("active", True)
                        .order("sort_order")
                        .order("item_name")
                        .execute()
                    )

                    if not items.data:
                        continue

                    with st.expander(
                        f"📁 {category['name']}",
                        expanded=True,
                    ):

                        # TABLE HEADER
                        h1, h2, h3, h4 = st.columns(
                            [4, 1.5, 1.5, 4]
                        )

                        h1.markdown("**Item**")
                        h2.markdown("**Select**")
                        h3.markdown("**Qty**")
                        h4.markdown("**Note / Status**")

                        st.divider()

                        selected_items = []

                        for item in items.data:

                            c1, c2, c3, c4 = st.columns(
                                [4, 1.5, 1.5, 4]
                            )

                            # ITEM
                            c1.write(
                                item["item_name"]
                            )

                            # SELECT
                            selected = c2.checkbox(
                                "Select",
                                key=(
                                    f"select_"
                                    f"{event['id']}_"
                                    f"{item['id']}"
                                ),
                                label_visibility="collapsed",
                            )

                            # QUANTITY
                            quantity = c3.number_input(
                                "Qty",
                                min_value=1,
                                value=1,
                                step=1,
                                disabled=not selected,
                                key=(
                                    f"qty_"
                                    f"{event['id']}_"
                                    f"{item['id']}"
                                ),
                                label_visibility="collapsed",
                            )

                            # NOTE
                            note = c4.text_input(
                                "Note / Status",
                                key=(
                                    f"note_"
                                    f"{event['id']}_"
                                    f"{item['id']}"
                                ),
                                label_visibility="collapsed",
                            )

                            # NOTE HIGHLIGHT
                            if note.strip():

                                c4.markdown(
                                    f"""
                                    <div style="
                                        margin-top:-8px;
                                        padding:6px 10px;
                                        border-radius:6px;
                                        background:#fff3cd;
                                        border:1px solid #ffc107;
                                        color:#856404;
                                        font-size:13px;
                                    ">
                                    📝 {note}
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                            if selected:

                                selected_items.append(
                                    {
                                        "item": item,
                                        "quantity": quantity,
                                        "note": note.strip(),
                                    }
                                )

                        st.divider()

                        if st.button(
                            f"➕ Add Selected {category['name']}",
                            key=(
                                f"add_category_"
                                f"{event['id']}_"
                                f"{category['id']}"
                            ),
                            width="stretch",
                        ):

                            if not selected_items:

                                st.warning(
                                    "Select at least one item."
                                )

                            else:

                                try:

                                    for selected_item in selected_items:

                                        item = selected_item["item"]

                                        quantity = selected_item[
                                            "quantity"
                                        ]

                                        note = selected_item[
                                            "note"
                                        ]

                                        existing = (
                                            supabase
                                            .table("event_items")
                                            .select("id")
                                            .eq(
                                                "event_id",
                                                event["id"],
                                            )
                                            .eq(
                                                "master_item_id",
                                                item["id"],
                                            )
                                            .execute()
                                        )

                                        row = {
                                            "event_id":
                                                event["id"],
                                            "master_item_id":
                                                item["id"],
                                            "item_name":
                                                item["item_name"],
                                            "quantity":
                                                quantity,
                                            "note":
                                                note or None,
                                        }

                                        if existing.data:

                                            (
                                                supabase
                                                .table("event_items")
                                                .update(row)
                                                .eq(
                                                    "id",
                                                    existing.data[0]["id"],
                                                )
                                                .execute()
                                            )

                                        else:

                                            (
                                                supabase
                                                .table("event_items")
                                                .insert(row)
                                                .execute()
                                            )

                                    st.success(
                                        "Selected Samaan added to event."
                                    )

                                    st.rerun()

                                except Exception as e:

                                    st.error(
                                        f"Could not save Samaan: {e}"
                                    )

                # =========================================
                # SELECTED EVENT SAMAAN
                # =========================================

                st.markdown("### 📋 Event Samaan List")

                selected_event_items = (
                    supabase
                    .table("event_items")
                    .select("*")
                    .eq(
                        "event_id",
                        event["id"],
                    )
                    .order("item_name")
                    .execute()
                )

                if not selected_event_items.data:

                    st.info(
                        "No Samaan selected for this event."
                    )

                else:

                    # HEADER
                    h1, h2, h3 = st.columns(
                        [5, 2, 5]
                    )

                    h1.markdown("**Item**")
                    h2.markdown("**Qty**")
                    h3.markdown("**Note / Status**")

                    st.divider()

                    for item in selected_event_items.data:

                        c1, c2, c3 = st.columns(
                            [5, 2, 5]
                        )

                        c1.write(
                            item["item_name"]
                        )

                        c2.write(
                            item["quantity"]
                        )

                        current_note = (
                            item.get("note")
                            or ""
                        )

                        note = c3.text_input(
                            "Note / Status",
                            value=current_note,
                            key=(
                                f"event_note_"
                                f"{item['id']}"
                            ),
                            label_visibility="collapsed",
                        )

                        # NORMAL / HIGHLIGHTED STATUS
                        if note.strip():

                            c3.markdown(
                                f"""
                                <div style="
                                    margin-top:-8px;
                                    padding:7px 10px;
                                    border-radius:6px;
                                    background:#fff3cd;
                                    border:1px solid #ffc107;
                                    color:#856404;
                                ">
                                📝 {note}
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        if note != current_note:

                            try:

                                (
                                    supabase
                                    .table("event_items")
                                    .update(
                                        {
                                            "note":
                                                note.strip()
                                                or None
                                        }
                                    )
                                    .eq(
                                        "id",
                                        item["id"],
                                    )
                                    .execute()
                                )

                            except Exception as e:

                                st.error(
                                    f"Could not update note: {e}"
                                )

# =========================================================
# SAMAAN MASTER
# =========================================================

with master_tab:

    st.subheader(
        "⚙️ Samaan Master"
    )

    st.caption(
        "Samaan ek baar yahan add karo. "
        "Har event mein dobara naam likhne ki zarurat nahi."
    )

    # -----------------------------------------------------
    # ADD CATEGORY
    # -----------------------------------------------------

    st.markdown(
        "### 📁 Add Category"
    )

    with st.form("add_category_form"):

        category_name = st.text_input(
    "Category Name"
)

        add_category = st.form_submit_button(
            "➕ Add Category"
        )

        if add_category:

            if not category_name.strip():

                st.error(
                    "Category name required."
                )

            else:

                try:

                    supabase.table(
                        "item_categories"
                    ).insert(
                        {
                            "id":
                                __import__(
                                    "uuid"
                                ).uuid4().__str__(),
                            "name":
                                category_name.strip(),
                            "active": True,
                            "sort_order": 0,
                            "created_at":
                                date.today().isoformat(),
                        }
                    ).execute()

                    st.success(
                        "Category added."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Could not add category: {e}"
                    )

    # -----------------------------------------------------
    # CATEGORY LIST
    # -----------------------------------------------------

    categories = (
        supabase
        .table("item_categories")
        .select("*")
        .eq("active", True)
        .order("sort_order")
        .order("name")
        .execute()
    )

    for category in categories.data or []:

        with st.expander(
            f"📁 {category['name']}"
        ):

            # =============================================
            # ADD ITEM
            # =============================================

            with st.form(
                f"add_item_form_{category['id']}"
            ):

                new_item_name = st.text_input(
    "Item Name"
)

                add_item = st.form_submit_button(
                    "➕ Add Item"
                )

                if add_item:

                    if not new_item_name.strip():

                        st.error(
                            "Item name required."
                        )

                    else:

                        try:

                            supabase.table(
                                "master_items"
                            ).insert(
                                {
                                    "id":
                                        __import__(
                                            "uuid"
                                        ).uuid4().__str__(),
                                    "category_id":
                                        category["id"],
                                    "item_name":
                                        new_item_name.strip(),
                                    "active": True,
                                    "sort_order": 0,
                                }
                            ).execute()

                            st.success(
                                "Item added."
                            )

                            st.rerun()

                        except Exception as e:

                            st.error(
                                f"Could not add item: {e}"
                            )

            # =============================================
            # ITEMS
            # =============================================

            items = (
                supabase
                .table("master_items")
                .select("*")
                .eq(
                    "category_id",
                    category["id"],
                )
                .eq("active", True)
                .order("sort_order")
                .order("item_name")
                .execute()
            )

            if not items.data:

                st.info(
                    "No items in this category."
                )

            else:

                for item in items.data:

                    col1, col2 = st.columns(
                        [5, 1]
                    )

                    col1.write(
                        f"📦 {item['item_name']}"
                    )

                    if col2.button(
                        "Deactivate",
                        key=(
                            f"deactivate_"
                            f"{item['id']}"
                        ),
                    ):

                        supabase.table(
                            "master_items"
                        ).update(
                            {"active": False}
                        ).eq(
                            "id",
                            item["id"],
                        ).execute()

                        st.rerun()
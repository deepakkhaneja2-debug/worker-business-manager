# Worker & Business Manager — V1

## Current foundation
- Streamlit mobile-friendly UI
- Supabase cloud database
- Workers table + first working Add Worker form
- Database schema prepared for:
  - Workers
  - Attendance
  - Dena/Lena
  - Shop/Godown
  - Rent
  - Events
  - Event worker assignment

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Cloud setup
1. Create a Supabase project.
2. Open SQL Editor.
3. Run `schema.sql`.
4. Add `SUPABASE_URL` and `SUPABASE_KEY` to Streamlit secrets.
5. Run the app.

## Next development order
1. Attendance entry + monthly calculation
2. Worker Dena/Lena ledger + balance
3. Shop/Godown + rent
4. Events + worker assignment
5. Dashboard
6. Login/roles and multi-phone security
7. Reports/export and backups

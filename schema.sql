create extension if not exists pgcrypto;

create table if not exists workers (
    id uuid primary key default gen_random_uuid(),
    name text not null,
    phone text,
    wage_type text not null check (wage_type in ('daily','monthly')),
    wage_amount numeric(12,2) not null default 0,
    joining_date date,
    active boolean not null default true,
    created_at timestamptz not null default now()
);

create table if not exists locations (
    id uuid primary key default gen_random_uuid(),
    name text not null,
    location_type text not null check (location_type in ('shop','godown')),
    address text,
    landlord_name text,
    landlord_phone text,
    monthly_rent numeric(12,2) not null default 0,
    security_deposit numeric(12,2) not null default 0,
    rent_due_day int check (rent_due_day between 1 and 31),
    agreement_start date,
    agreement_end date,
    active boolean not null default true,
    created_at timestamptz not null default now()
);

create table if not exists attendance (
    id uuid primary key default gen_random_uuid(),
    worker_id uuid not null references workers(id) on delete cascade,
    attendance_date date not null,
    status text not null check (status in ('present','absent','half_day')),
    overtime_hours numeric(6,2) not null default 0,
    location_id uuid references locations(id) on delete set null,
    notes text,
    created_at timestamptz not null default now(),
    unique(worker_id, attendance_date)
);

create table if not exists transactions (
    id uuid primary key default gen_random_uuid(),
    worker_id uuid references workers(id) on delete set null,
    location_id uuid references locations(id) on delete set null,
    event_id uuid,
    transaction_date date not null default current_date,
    transaction_type text not null check (transaction_type in ('given','received')),
    amount numeric(12,2) not null check (amount >= 0),
    reason text,
    payment_mode text,
    notes text,
    created_at timestamptz not null default now()
);

create table if not exists events (
    id uuid primary key default gen_random_uuid(),
    name text not null,
    client_name text,
    venue text,
    start_date date not null,
    end_date date,
    event_type text,
    total_amount numeric(12,2) not null default 0,
    advance_received numeric(12,2) not null default 0,
    status text not null default 'upcoming'
        check (status in ('upcoming','running','completed','cancelled')),
    notes text,
    created_at timestamptz not null default now()
);

create table if not exists event_workers (
    id uuid primary key default gen_random_uuid(),
    event_id uuid not null references events(id) on delete cascade,
    worker_id uuid not null references workers(id) on delete cascade,
    role text,
    agreed_amount numeric(12,2) not null default 0,
    notes text,
    unique(event_id, worker_id)
);

create table if not exists rent_payments (
    id uuid primary key default gen_random_uuid(),
    location_id uuid not null references locations(id) on delete cascade,
    payment_date date not null default current_date,
    amount numeric(12,2) not null check (amount >= 0),
    payment_mode text,
    notes text,
    created_at timestamptz not null default now()
);

create index if not exists idx_attendance_date on attendance(attendance_date);
create index if not exists idx_attendance_worker on attendance(worker_id);
create index if not exists idx_transactions_worker on transactions(worker_id);
create index if not exists idx_events_dates on events(start_date, end_date);
create index if not exists idx_event_workers_event on event_workers(event_id);

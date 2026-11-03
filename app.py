import streamlit as st
from datetime import date

st.set_page_config(page_title="Spendwise | Expense Tracker", page_icon="💳", layout="wide")

# Visual design: soft neutral canvas, deep navy sidebar, blue action color.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:#f5f7fb;color:#182230;}
[data-testid="stHeader"] {background:rgba(245,247,251,.85);}
[data-testid="stSidebar"] {background:#111827;border-right:1px solid #253044;}
[data-testid="stSidebar"] * {color:#e5e7eb !important;}
[data-testid="stSidebar"] input,[data-testid="stSidebar"] div[data-baseweb="select"]>div {background:#1f2937 !important;border-color:#374151 !important;}
h1,h2,h3 {font-family:'Manrope',sans-serif !important;letter-spacing:-.6px;}
h1 {font-size:2.25rem !important;font-weight:800 !important;color:#111827 !important;}
h2,h3 {color:#172033 !important;font-weight:700 !important;}
.eyebrow,.kicker {font-size:.76rem;font-weight:700;letter-spacing:1.5px;color:#64748b;margin-bottom:6px;}
.hero-note {color:#64748b;margin-top:-10px;margin-bottom:22px;}
div[data-testid="stMetric"] {background:white;border:1px solid #e7ebf2;border-radius:16px;padding:18px 20px;box-shadow:0 5px 18px rgba(15,23,42,.035);}
div[data-testid="stMetricLabel"] {color:#64748b !important;font-weight:600 !important;}
div[data-testid="stMetricValue"] {color:#111827 !important;font-family:'Manrope',sans-serif !important;font-weight:800 !important;}
div[data-testid="stForm"] {background:white;border:1px solid #e7ebf2;border-radius:16px;padding:20px;box-shadow:0 5px 18px rgba(15,23,42,.035);}
div[data-testid="stDataFrame"] {border:1px solid #e7ebf2;border-radius:13px;overflow:hidden;background:white;}
.stButton>button,.stFormSubmitButton>button {border-radius:10px;font-weight:700;min-height:42px;}
.stFormSubmitButton>button {background:#2563eb;color:white;border:1px solid #2563eb;}
.stFormSubmitButton>button:hover {background:#1d4ed8;color:white;}
hr {border-color:#e5eaf1;margin:1.5rem 0;}
.brand {font-family:'Manrope',sans-serif;font-size:1.35rem;font-weight:800;color:white;}
.side-note {color:#9ca3af;font-size:.82rem;margin-bottom:25px;}
.empty {background:white;border:1px dashed #cbd5e1;border-radius:14px;padding:28px;text-align:center;color:#64748b;}
.cat {display:flex;justify-content:space-between;padding:12px 14px;margin:7px 0;background:white;border:1px solid #e7ebf2;border-radius:11px;}
.cat b {color:#111827;}
.footer {text-align:center;color:#94a3b8;font-size:.78rem;padding:24px 0 8px;}
</style>
""", unsafe_allow_html=True)

CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Other"]
if "expenses" not in st.session_state:
    st.session_state.expenses = []
if "next_id" not in st.session_state:
    st.session_state.next_id = 1

def money(value):
    return f"Rs. {value:,.2f}"

def add_expense(name, amount, category, expense_date):
    st.session_state.expenses.append({
        "id": st.session_state.next_id,
        "Expense Name": name.strip(),
        "Amount": float(amount),
        "Category": category,
        "Date": expense_date
    })
    st.session_state.next_id += 1

def delete_expense(expense_id):
    st.session_state.expenses = [
        expense for expense in st.session_state.expenses
        if expense["id"] != expense_id
    ]

def dashboard_stats(records):
    if not records:
        return 0.0, 0, 0.0
    return (
        sum(item["Amount"] for item in records),
        len(records),
        max(item["Amount"] for item in records)
    )

def category_summary(records):
    totals = {category: 0.0 for category in CATEGORIES}
    for item in records:
        totals[item["Category"]] += item["Amount"]
    return totals

# Sidebar filters
with st.sidebar:
    st.markdown('<div class="brand">◈ Spendwise</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-note">PERSONAL FINANCE DASHBOARD</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Search & filters")
    search_text = st.text_input("Search expense", placeholder="e.g. Groceries, fuel")
    category_filter = st.selectbox("Category", ["All Categories"] + CATEGORIES)

    amounts = [item["Amount"] for item in st.session_state.expenses]
    if amounts:
        low, high = min(amounts), max(amounts)
        if low == high:
            amount_filter = st.slider("Amount range (Rs.)", 0.0, max(1.0, high), (0.0, max(1.0, high)), step=1.0)
        else:
            amount_filter = st.slider(
                "Amount range (Rs.)", float(low), float(high),
                (float(low), float(high)),
                step=max(1.0, round((high-low)/100, 2))
            )
    else:
        amount_filter = (0.0, 100000.0)
        st.caption("Add an expense to activate amount filtering.")
    st.markdown("---")
    st.caption("All filters work together. Reset the search and category to view every record.")

# Header and live metrics
st.markdown('<div class="eyebrow">PERSONAL FINANCE / OVERVIEW</div>', unsafe_allow_html=True)
st.title("Expense Tracker")
st.markdown('<div class="hero-note">A clear view of your spending. Track every rupee, make better decisions.</div>', unsafe_allow_html=True)

total, transactions, highest = dashboard_stats(st.session_state.expenses)
m1, m2, m3 = st.columns(3)
m1.metric("Total Expenses", money(total))
m2.metric("Total Transactions", transactions)
m3.metric("Highest Expense", money(highest))

st.markdown("---")
st.markdown('<div class="kicker">NEW TRANSACTION</div>', unsafe_allow_html=True)
st.header("Add an expense")

with st.form("expense_form", clear_on_submit=True):
    expense_name = st.text_input("Expense name", placeholder="e.g. Weekly groceries")
    c1, c2, c3 = st.columns(3)
    with c1:
        expense_amount = st.number_input("Amount (Rs.)", min_value=0.0, value=0.0, step=100.0, format="%.2f")
    with c2:
        expense_category = st.selectbox("Category", CATEGORIES)
    with c3:
        expense_date = st.date_input("Date", value=date.today())
    submit = st.form_submit_button("＋  Add expense", use_container_width=True)

if submit:
    if not expense_name.strip():
        st.error("Please enter an expense name.")
    elif expense_amount <= 0:
        st.error("Amount must be greater than zero.")
    else:
        add_expense(expense_name, expense_amount, expense_category, expense_date)
        st.success(f"'{expense_name.strip()}' was added successfully.")
        st.rerun()

# Combined filtering
filtered = []
for item in st.session_state.expenses:
    name_match = search_text.lower() in item["Expense Name"].lower()
    category_match = category_filter == "All Categories" or item["Category"] == category_filter
    amount_match = amount_filter[0] <= item["Amount"] <= amount_filter[1]
    if name_match and category_match and amount_match:
        filtered.append(item)

st.markdown("---")
st.markdown('<div class="kicker">TRANSACTION HISTORY</div>', unsafe_allow_html=True)
st.header("Expense records")
if not st.session_state.expenses:
    st.markdown('<div class="empty"><b>No expenses yet</b><br><br>Your transactions will appear here after you add your first expense.</div>', unsafe_allow_html=True)
elif not filtered:
    st.warning("No expenses match the selected search and filters.")
else:
    table_rows = [{
        "Expense Name": item["Expense Name"],
        "Amount": money(item["Amount"]),
        "Category": item["Category"],
        "Date": item["Date"].strftime("%d %b %Y")
    } for item in filtered]
    st.dataframe(table_rows, use_container_width=True, hide_index=True)
    st.caption(f"Showing {len(filtered)} of {len(st.session_state.expenses)} transactions.")

# Delete controls
st.markdown("---")
st.markdown('<div class="kicker">RECORD MANAGEMENT</div>', unsafe_allow_html=True)
st.header("Delete an expense")
if not st.session_state.expenses:
    st.info("There are no records to delete.")
else:
    delete_labels = {
        f'{item["Expense Name"]} • {money(item["Amount"])} • {item["Date"].strftime("%d %b %Y")} • ID {item["id"]}': item["id"]
        for item in st.session_state.expenses
    }
    chosen_label = st.selectbox("Select a transaction", list(delete_labels.keys()))
    if st.button("Delete selected expense", type="primary"):
        delete_expense(delete_labels[chosen_label])
        st.success("Expense deleted successfully.")
        st.rerun()

# Category totals
st.markdown("---")
st.markdown('<div class="kicker">SPENDING BREAKDOWN</div>', unsafe_allow_html=True)
st.header("Category-wise summary")
if not st.session_state.expenses:
    st.warning("Category totals will be available after you add expenses.")
else:
    totals = category_summary(st.session_state.expenses)
    for category in CATEGORIES:
        st.markdown(
            f'<div class="cat"><span>{category}</span><b>{money(totals[category])}</b></div>',
            unsafe_allow_html=True
        )

st.markdown('<div class="footer">SPENDWISE · KEEP TRACK. STAY INTENTIONAL.</div>', unsafe_allow_html=True)

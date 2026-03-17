import streamlit as st
st.set_page_config(
    page_title="Personal Financial Discipline Advisor",
    layout="centered"
)
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.markdown("""
<style>

/* Hide Streamlit menu */
#MainMenu {visibility: hidden;}

/* Hide footer */
footer {visibility: hidden;}

/* Hide header toolbar (edit, github, menu icons) */
header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# ---------- Currency conversion ----------
def convert_indian_currency(value):
    value = value.lower().strip()
    if "crore" in value or "cr" in value:
        number = float(value.split()[0])
        return int(number * 10000000)
    elif "lakh" in value:
        number = float(value.split()[0])
        return int(number * 100000)
    else:
        return int(value)

# ---------- Government schemes ----------
def government_schemes(age):
    if age < 30:
        return [
            ("National Pension System (NPS)", "Expected return ~9–12%"),
            ("Public Provident Fund (PPF)", "Interest ~7.1%"),
            ("Equity Mutual Fund SIP", "Expected return ~10–12%")
        ]
    elif age < 45:
        return [
            ("National Pension System (NPS)", "Expected return ~9–12%"),
            ("Balanced Mutual Funds", "Expected return ~8–10%"),
            ("Public Provident Fund (PPF)", "Interest ~7.1%")
        ]
    elif age < 60:
        return [
            ("National Pension System (NPS)", "Expected return ~9–12%"),
            ("Debt Mutual Funds", "Expected return ~6–8%"),
            ("Public Provident Fund (PPF)", "Interest ~7.1%")
        ]
    else:
        return [
            ("Senior Citizen Savings Scheme (SCSS)", "Interest ~8.2%"),
            ("Pradhan Mantri Vaya Vandana Yojana (PMVVY)", "Interest ~7.4%"),
            ("Post Office Monthly Income Scheme", "Interest ~7.4%")
        ]

# ---------- Title ----------
st.markdown(
"<h1 style='text-align:center; white-space:nowrap;'>💰 Personal Financial Discipline Advisor</h1>",
unsafe_allow_html=True
)
st.markdown(
"<h5 style='text-align:center;'>Designed & Developed by – Ambika, Infant, Madhushree (AIM)</h5>",
unsafe_allow_html=True
)

# ---------- User Inputs ----------
st.subheader("User Financial Information")

age = st.number_input("Current Age", min_value=18, max_value=100)
gender = st.radio("Gender", ["Male","Female"])
income = st.number_input("Monthly Income (₹)", min_value=0)
expenses = st.number_input("Monthly Expenses (₹)", min_value=0)
savings = st.number_input("Current Savings (₹)", min_value=0)
retirement_age = st.number_input("Desired Retirement Age", min_value=40, max_value=80)

ret_goal_input = st.text_input("Retirement Goal Corpus (Example: 2 crore / 20000000)")

risk = st.radio("Risk Tolerance", ["Low","Medium","High"])

if st.button("Analyze Financial Plan"):

    retirement_goal = convert_indian_currency(ret_goal_input)

    monthly_savings = income - expenses
    years_left = retirement_age - age

    corpus = (monthly_savings * 12 * years_left) + savings

    # ---------- Retirement feasibility ----------
    if retirement_age <= age:
        feasibility_msg = "⚠ Retirement age is lower than current age. Suggested: 55–60."
    else:
        feasibility_msg = "✔ Retirement age appears feasible."

    # ---------- Savings ratio ----------
    savings_ratio = (monthly_savings / income) * 100 if income else 0

    # ---------- Financial health score ----------
    score = 0
    if savings_ratio >= 20:
        score += 30
    if savings > expenses * 6:
        score += 30
    if monthly_savings > 0:
        score += 20
    if income > expenses:
        score += 20

    # ---------- Inflation impact ----------
    inflation = 0.06
    future_goal = retirement_goal * ((1 + inflation) ** years_left)

    # ---------- Retirement income ----------
    monthly_ret_income = corpus * 0.04 / 12

    # ---------- Financial alerts ----------
    alerts = ""
    if expenses > income:
        alerts += "⚠ Expenses exceed income.\n"
    if savings_ratio < 10:
        alerts += "⚠ Savings rate extremely low.\n"
    if alerts == "":
        alerts = "✔ No major financial alerts."

    # ---------- Goal timeline ----------
    if monthly_savings > 0:
        years_to_goal = retirement_goal / (monthly_savings * 12)
    else:
        years_to_goal = 0

    # ---------- Portfolio allocation ----------
    if risk == "Low":
        portfolio = {"Government Schemes":50,"Debt Funds":30,"Gold":20}
    elif risk == "Medium":
        portfolio = {"Equity Funds":50,"Debt Funds":30,"Gold":20}
    else:
        portfolio = {"Equity Funds":70,"Index Funds":20,"Gold":10}

    # ---------- Wealth projection ----------
    annual_return = 0.10
    balance = savings
    projection = []

    for year in range(1, years_left + 1):
        balance = (balance + monthly_savings * 12) * (1 + annual_return)
        projection.append(balance)

    df = pd.DataFrame({
        "Year": list(range(1, years_left + 1)),
        "Projected Wealth": projection
    })

    # ---------- Dashboard ----------
    st.subheader("📊 Financial Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Income", f"₹{income:,}")
    col2.metric("Expenses", f"₹{expenses:,}")
    col3.metric("Monthly Savings", f"₹{monthly_savings:,}")
    col4.metric("Savings Ratio", f"{savings_ratio:.1f}%")

    col1, col2, col3 = st.columns(3)

    col1.metric("Years to Retirement", years_left)
    col2.metric("Retirement Goal", f"₹{retirement_goal:,}")
    col3.metric("Projected Corpus", f"₹{corpus:,}")

    # ---------- Financial Health ----------
    st.subheader("Financial Health Score")
    st.progress(score/100)
    st.write(f"Score: **{score}/100**")

    # ---------- Feasibility ----------
    st.subheader("Retirement Feasibility")
    st.write(feasibility_msg)

    # ---------- Portfolio chart ----------
    st.subheader("Portfolio Allocation")

    pie = px.pie(values=list(portfolio.values()), names=list(portfolio.keys()))
    st.plotly_chart(pie)

    # ---------- Readiness gauge ----------
readiness_percent = min(int((corpus/retirement_goal)*100),100)

st.subheader("Retirement Readiness")

if readiness_percent <= 30:
    bar_color = "red"
    needle_color = "darkred"
elif readiness_percent <= 59:
    bar_color = "orange"
    needle_color = "darkorange"
else:
    bar_color = "green"
    needle_color = "darkgreen"

gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=readiness_percent,
    title={'text': "Readiness %"},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': bar_color},
        'steps': [
            {'range': [0, 30],  'color': '#ffcccc'},   # light red
            {'range': [30, 60], 'color': '#ffe5b4'},   # light orange
            {'range': [60, 100],'color': '#ccffcc'},   # light green
        ],
        'threshold': {
            'line': {'color': needle_color, 'width': 4},
            'thickness': 0.75,
            'value': readiness_percent
        }
    }
))

st.plotly_chart(gauge)
    # ---------- Wealth graph ----------
    st.subheader("Retirement Wealth Projection")

    fig = px.line(df, x="Year", y="Projected Wealth", markers=True)
    st.plotly_chart(fig)

    # ---------- Inflation ----------
    st.subheader("Inflation Impact")
    st.write(f"Future value of retirement goal: ₹{int(future_goal):,}")

    # ---------- Retirement income ----------
    st.subheader("Estimated Retirement Income")
    st.write(f"Approx monthly retirement income: ₹{int(monthly_ret_income):,}")

    # ---------- Tax savings ----------
    st.subheader("Tax Saving Options")
    st.write("""
    • National Pension System (NPS) – Section 80CCD  
    • Public Provident Fund (PPF) – Section 80C  
    • Equity Linked Savings Scheme (ELSS) – Section 80C
    """)

    # ---------- Alerts ----------
    st.subheader("Financial Alerts")
    st.write(alerts)

    # ---------- Goal timeline ----------
    st.subheader("Goal Achievement Timeline")
    st.write(f"Estimated years to reach goal: **{years_to_goal:.1f} years**")

    # ---------- Government schemes ----------
    st.subheader("Recommended Government Schemes")

    schemes = government_schemes(age)
    for s in schemes:
        st.write(f"• {s[0]} — {s[1]}")

    # ---------- Advisor summary ----------
    st.subheader("Smart Advisor Summary")

    st.info(f"""
    • Increase savings ratio to at least 20%  
    • Maintain emergency fund of 6 months expenses  
    • Diversify investments across equity, debt, and government schemes  
    • Increase monthly savings to reach retirement goal faster
    """)


# ---------- Footer ----------
st.markdown("---")

st.markdown(
"<h5 style='text-align:center;'>A Project of Personal Finance & Wealth Management</h5>",
unsafe_allow_html=True
)

st.markdown(
"<h6 style='text-align:center;'>Designed & Developed by – Ambika, Infant, Madhushree (AIM)</h6>",
unsafe_allow_html=True
)

st.markdown(
"<h6 style='text-align:center;'>Faculty: Dr. K. Nigama</h6>",
unsafe_allow_html=True
)

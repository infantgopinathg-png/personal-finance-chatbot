import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# Currency converter
# -----------------------------
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


# -----------------------------
# Government scheme logic
# -----------------------------
def government_schemes(age, risk):

    if age < 30:

        schemes = [
        ("National Pension System (NPS)", "Expected return ~9–12%"),
        ("Public Provident Fund (PPF)", "Interest ~7.1%"),
        ("Equity Mutual Fund SIP", "Expected return ~10–12%")
        ]

    elif age < 45:

        schemes = [
        ("National Pension System (NPS)", "Expected return ~9–12%"),
        ("Balanced Mutual Funds", "Expected return ~8–10%"),
        ("Public Provident Fund (PPF)", "Interest ~7.1%")
        ]

    elif age < 60:

        schemes = [
        ("National Pension System (NPS)", "Expected return ~9–12%"),
        ("Debt Mutual Funds", "Expected return ~6–8%"),
        ("Public Provident Fund (PPF)", "Interest ~7.1%")
        ]

    else:

        schemes = [
        ("Senior Citizen Savings Scheme (SCSS)", "Interest ~8.2%"),
        ("Pradhan Mantri Vaya Vandana Yojana (PMVVY)", "Interest ~7.4%"),
        ("Post Office Monthly Income Scheme", "Interest ~7.4%")
        ]

    return schemes


# -----------------------------
# Title
# -----------------------------
st.markdown(
"""
<h1 style='text-align:center; white-space:nowrap;'>
💰 Personal Financial Discipline Advisor
</h1>
""",
unsafe_allow_html=True
)

st.markdown(
"<h5 style='text-align:center;'>Designed & Developed by – Ambika, Infant, Madhushree (AIM)</h5>",
unsafe_allow_html=True
)


# -----------------------------
# Session state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.step = 0


questions = [

"Hello! I will help you plan your savings and retirement. What is your age?",

"Select your gender:",

"What is your monthly income (₹)?",

"What are your monthly expenses (₹)?",

"How much savings do you currently have (₹)?",

"At what age do you want to retire?",

"What is your retirement goal corpus? (Example: 2 crore / 20000000)",

"Select your risk tolerance:"
]


# -----------------------------
# Chat history
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


user_input = st.chat_input("Type your answer")


# -----------------------------
# Start chatbot
# -----------------------------
if st.session_state.step == 0 and len(st.session_state.messages) == 0:

    st.session_state.messages.append({
        "role":"assistant",
        "content":questions[0]
    })

    st.rerun()


# -----------------------------
# User input handling
# -----------------------------
if user_input:

    st.session_state.messages.append({"role":"user","content":user_input})

    step = st.session_state.step

    if step == 0:
        st.session_state.age = int(user_input)
        reply = questions[1]

    elif step == 2:
        st.session_state.income = int(user_input)
        reply = questions[3]

    elif step == 3:
        st.session_state.expenses = int(user_input)
        reply = questions[4]

    elif step == 4:
        st.session_state.savings = int(user_input)
        reply = questions[5]

    elif step == 5:
        st.session_state.retirement_age = int(user_input)
        reply = questions[6]

    elif step == 6:
        st.session_state.retirement_goal = convert_indian_currency(user_input)
        reply = questions[7]

    st.session_state.messages.append({"role":"assistant","content":reply})

    st.session_state.step += 1
    st.rerun()


# -----------------------------
# Gender selection
# -----------------------------
if st.session_state.step == 1:

    gender = st.radio("Select Gender", ["Male","Female","Other"])

    if st.button("Confirm Gender"):

        st.session_state.gender = gender

        st.session_state.messages.append({
            "role":"assistant",
            "content":f"Gender selected: {gender}"
        })

        st.session_state.step = 2

        st.session_state.messages.append({
            "role":"assistant",
            "content":questions[2]
        })

        st.rerun()


# -----------------------------
# Risk tolerance selection
# -----------------------------
if st.session_state.step == 7:

    risk = st.radio("Select Risk Tolerance", ["Low","Medium","High"])

    if st.button("Confirm Risk"):

        st.session_state.risk = risk.lower()

        monthly_savings = st.session_state.income - st.session_state.expenses
        years_left = st.session_state.retirement_age - st.session_state.age
        corpus = (monthly_savings * 12 * years_left) + st.session_state.savings

        # -----------------------------
        # Financial health score
        # -----------------------------
        savings_ratio = monthly_savings / st.session_state.income
        expense_ratio = st.session_state.expenses / st.session_state.income

        score = int((savings_ratio * 50) + ((1 - expense_ratio) * 50))

        # -----------------------------
        # Emergency fund
        # -----------------------------
        emergency_needed = st.session_state.expenses * 6
        emergency_gap = emergency_needed - st.session_state.savings

        # -----------------------------
        # Retirement readiness
        # -----------------------------
        readiness_ratio = corpus / st.session_state.retirement_goal
        readiness_percent = min(int(readiness_ratio * 100), 100)

        # -----------------------------
        # Government scheme suggestions
        # -----------------------------
        schemes = government_schemes(st.session_state.age, risk)

        scheme_text = ""

        for s in schemes:
            scheme_text += f"• {s[0]} — {s[1]}\n"

        # -----------------------------
        # Portfolio allocation
        # -----------------------------
        if risk == "Low":

            portfolio = {
            "PPF":40,
            "Debt Funds":40,
            "Gold":20
            }

        elif risk == "Medium":

            portfolio = {
            "Equity Funds":50,
            "Debt Funds":30,
            "Gold":20
            }

        else:

            portfolio = {
            "Equity Funds":70,
            "Index Funds":20,
            "Gold":10
            }


        # -----------------------------
        # Wealth projection graph
        # -----------------------------
        annual_return = 0.10

        balance = st.session_state.savings
        projection = []

        for year in range(1, years_left + 1):

            balance = (balance + monthly_savings * 12) * (1 + annual_return)
            projection.append(balance)

        df = pd.DataFrame({
        "Year": list(range(1, years_left + 1)),
        "Projected Wealth": projection
        })

        st.subheader("📈 Retirement Wealth Projection")

        fig = px.line(df, x="Year", y="Projected Wealth", markers=True)

        st.plotly_chart(fig, use_container_width=True)


        # -----------------------------
        # Portfolio pie chart
        # -----------------------------
        st.subheader("📊 Portfolio Allocation")

        pie = px.pie(
        values=list(portfolio.values()),
        names=list(portfolio.keys())
        )

        st.plotly_chart(pie, use_container_width=True)


        # -----------------------------
        # Retirement readiness gauge
        # -----------------------------
        st.subheader("🎯 Retirement Readiness")

        gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=readiness_percent,
        title={'text': "Retirement Readiness %"},
        gauge={'axis': {'range': [0, 100]}}
        ))

        st.plotly_chart(gauge, use_container_width=True)


        # -----------------------------
        # Final response
        # -----------------------------
        reply = f"""

### 📋 Financial Plan

Selected Risk Profile: **{risk.title()}**

Retirement Goal: ₹{st.session_state.retirement_goal:,}

Monthly Savings: ₹{monthly_savings:,}

Years to Retirement: {years_left}

Estimated Retirement Corpus: ₹{corpus:,}


### 🧠 Financial Health Score

{score}/100


### 🚑 Emergency Fund

Required: ₹{emergency_needed:,}

Gap: ₹{max(emergency_gap,0):,}


### 🇮🇳 Recommended Government Schemes

{scheme_text}

"""

        st.session_state.messages.append({
        "role":"assistant",
        "content":reply
        })

        st.session_state.step += 1

        st.rerun()

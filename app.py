import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.markdown(
"<h1 style='text-align:center; white-space:nowrap;'>💰 Personal Financial Discipline Advisor</h1>",
unsafe_allow_html=True
)

# Developer credit
st.markdown(
"<h5 style='text-align:center; margin-top:-10px;'>Designed & Developed by – Ambika, Infant, Madhushree (AIM)</h5>",
unsafe_allow_html=True
)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.step = 0

questions = [
"Hello! I will help you plan your savings and retirement. What is your age?",
"Please select your gender:",
"What is your monthly income (₹)?",
"What are your monthly expenses (₹)?",
"How much current savings do you have (₹)?",
"At what age do you want to retire?",
"What is your retirement goal corpus? (Example: 30000000 for ₹3 Crore)",
"Select your investment risk tolerance:"
]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Type your answer")

# Start conversation
if st.session_state.step == 0 and len(st.session_state.messages) == 0:
    st.session_state.messages.append({"role":"assistant","content":questions[0]})
    st.rerun()

# User input steps
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
        st.session_state.retirement_goal = int(user_input)
        reply = questions[7]

    st.session_state.messages.append({"role":"assistant","content":reply})
    st.session_state.step += 1
    st.rerun()

# Gender selection
if st.session_state.step == 1:

    gender = st.radio(
        "Select your gender",
        ["Male","Female","Other"]
    )

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

# Risk selection
if st.session_state.step == 7:

    risk = st.radio(
        "Select Risk Tolerance",
        ["Low","Medium","High"]
    )

    if st.button("Confirm Risk"):

        st.session_state.risk = risk.lower()

        retirement_goal = st.session_state.retirement_goal
        monthly_savings = st.session_state.income - st.session_state.expenses
        years_left = st.session_state.retirement_age - st.session_state.age

        corpus = (monthly_savings * 12 * years_left) + st.session_state.savings

        # Risk based recommendations
        if st.session_state.risk == "low":

            recommendation = """
Low Risk Portfolio

• Public Provident Fund (PPF) – ~7.1% return  
• Debt Mutual Funds – ~6–7% return  
• Gold ETFs – ~6–7% return
"""

        elif st.session_state.risk == "medium":

            recommendation = """
Moderate Risk Portfolio

• National Pension System (NPS) – ~9–12% return  
• Balanced Mutual Funds – ~8–10% return  
• Public Provident Fund (PPF) – ~7.1% return
"""

        else:

            recommendation = """
High Risk Growth Portfolio

• Equity Mutual Fund SIP – ~10–12% return  
• National Pension System (NPS) – ~9–12% return  
• Index Funds – ~10–11% return
"""

        # Financial health
        savings_ratio = monthly_savings / st.session_state.income
        expense_ratio = st.session_state.expenses / st.session_state.income
        emergency_needed = st.session_state.expenses * 6

        score = 0

        if savings_ratio >= 0.3:
            score += 30
        elif savings_ratio >= 0.2:
            score += 20
        else:
            score += 10

        if expense_ratio <= 0.6:
            score += 25
        elif expense_ratio <= 0.8:
            score += 15
        else:
            score += 5

        if st.session_state.savings >= emergency_needed:
            score += 20
        else:
            score += 10

        if years_left >= 20:
            score += 25
        else:
            score += 15

        health_message = f"Your Financial Health Score: {score}/100"

        # Expense analysis
        if expense_ratio > 0.8:
            expense_message = "⚠️ Your expenses are very high. Reduce discretionary spending."
        elif expense_ratio > 0.6:
            expense_message = "Your expenses are moderate."
        else:
            expense_message = "Excellent expense discipline."

        # Emergency fund
        emergency_gap = emergency_needed - st.session_state.savings

        if emergency_gap > 0:
            emergency_message = f"You need ₹{emergency_gap:,} more for a proper emergency fund."
        else:
            emergency_message = "You already have sufficient emergency savings."

        # Retirement readiness
        readiness_ratio = corpus / retirement_goal

        if readiness_ratio >= 1:
            readiness = "🟢 Retirement Ready"
        elif readiness_ratio >= 0.6:
            readiness = "🟡 Moderately Prepared"
        else:
            readiness = "🔴 Increase savings"

        # Savings suggestion
        required_monthly = retirement_goal / (years_left * 12)

        savings_recommendation = f"""
To reach your retirement goal of ₹{retirement_goal:,}

You should save approximately ₹{int(required_monthly):,} per month.
"""

        # Graph
        annual_return = 0.10
        balance = st.session_state.savings
        projection = []

        for year in range(1, years_left + 1):
            balance = (balance + monthly_savings * 12) * (1 + annual_return)
            projection.append(balance)

        data = pd.DataFrame({
            "Year": list(range(1, years_left + 1)),
            "Projected Wealth": projection
        })

        fig = px.line(
            data,
            x="Year",
            y="Projected Wealth",
            markers=True,
            title="Retirement Wealth Projection"
        )

        st.plotly_chart(fig, use_container_width=True)

        reply = f"""
### 📊 Financial Plan

Retirement Goal: ₹{retirement_goal:,}

Monthly Savings: ₹{monthly_savings:,}

Years to Retirement: {years_left}

Estimated Retirement Corpus: ₹{corpus:,}

### 📈 Investment Recommendations
{recommendation}

### 💡 Financial Health
{health_message}

### 📉 Expense Analysis
{expense_message}

### 🚑 Emergency Fund
{emergency_message}

### 📊 Retirement Readiness
{readiness}

### 💰 Savings Strategy
{savings_recommendation}
"""

        st.session_state.messages.append({"role":"assistant","content":reply})
        st.session_state.step += 1
        st.rerun()

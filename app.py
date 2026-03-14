import streamlit as st
import pandas as pd

st.title("💰 Personal Financial Discipline Advisor")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.step = 0

questions = [
    "Hello! I will help you plan your savings and retirement. What is your age?",
    "What is your gender? (Male/Female/Other)",
    "What is your monthly income (₹)?",
    "What are your monthly expenses (₹)?",
    "How much current savings do you have (₹)?",
    "At what age do you want to retire?",
    "What retirement lifestyle do you want? (Basic / Comfortable / Luxury)"
]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Type your answer")

# Start conversation
if st.session_state.step == 0 and len(st.session_state.messages) == 0:
    st.session_state.messages.append({
        "role": "assistant",
        "content": questions[0]
    })
    st.rerun()

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    step = st.session_state.step

    if step == 0:
        st.session_state.age = int(user_input)
        reply = questions[1]

    elif step == 1:
        st.session_state.gender = user_input
        reply = questions[2]

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

        lifestyle = user_input.lower()

        if "basic" in lifestyle:
            retirement_goal = 15000000
        elif "luxury" in lifestyle:
            retirement_goal = 50000000
        else:
            retirement_goal = 30000000

        monthly_savings = st.session_state.income - st.session_state.expenses
        years_left = st.session_state.retirement_age - st.session_state.age

        corpus = (monthly_savings * 12 * years_left) + st.session_state.savings

        # Customized scheme recommendation
        recommendation = ""

        if st.session_state.age < 35:
            recommendation += """
Young Investor Strategy:
• National Pension System (NPS)
• Equity Mutual Fund SIP
• Public Provident Fund (PPF)
"""

        elif st.session_state.age < 50:
            recommendation += """
Mid-Career Strategy:
• National Pension System (NPS)
• Public Provident Fund (PPF)
• Balanced Mutual Funds
"""

        else:
            recommendation += """
Retirement Focus Strategy:
• Senior Citizen Savings Scheme (SCSS)
• Pradhan Mantri Vaya Vandana Yojana (PMVVY)
"""

        if st.session_state.income < 30000:
            recommendation += """
Additional Scheme:
• Atal Pension Yojana (APY)
"""

        if st.session_state.gender.lower() == "female":
            recommendation += """
Women-Specific Scheme:
• Sukanya Samriddhi Yojana (for girl child planning)
"""

        # Financial Health Score
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
            expense_message = """
⚠️ Your expenses are very high.

Recommended ratio: 50–60%

Suggestions:
• Reduce discretionary spending
• Follow 50-30-20 budgeting rule
"""
        elif expense_ratio > 0.6:
            expense_message = "Your expenses are moderate but can be optimized."
        else:
            expense_message = "Excellent expense discipline."

        # Emergency fund planner
        emergency_gap = emergency_needed - st.session_state.savings

        if emergency_gap > 0:
            emergency_message = f"""
Emergency fund required: ₹{emergency_needed}

You still need ₹{emergency_gap} to reach financial security.
"""
        else:
            emergency_message = "You already have sufficient emergency savings."

        # Retirement readiness
        readiness_ratio = corpus / retirement_goal

        if readiness_ratio >= 1:
            readiness = "🟢 You are ready for retirement!"
        elif readiness_ratio >= 0.6:
            readiness = "🟡 Moderately prepared for retirement."
        else:
            readiness = "🔴 High risk – increase savings."

        # Monthly savings recommendation
        required_monthly = retirement_goal / (years_left * 12)

        savings_recommendation = f"""
To reach a retirement goal of ₹{retirement_goal:,}

You should save approximately ₹{int(required_monthly):,} per month.

Consider investing in SIP with ~10% expected annual return.
"""

        # Retirement wealth projection graph
        annual_return = 0.10
        balance = st.session_state.savings
        projection = []

        for year in range(1, years_left + 1):
            balance = (balance + monthly_savings * 12) * (1 + annual_return)
            projection.append(balance)

        data = pd.DataFrame({
            "Year": list(range(1, years_left + 1)),
            "Projected Savings": projection
        })

        reply = f"""
### 📊 Financial Plan

Monthly Savings: ₹{monthly_savings:,}

Years to Retirement: {years_left}

Estimated Retirement Corpus: ₹{corpus:,}

### 🏦 Customized Investment Recommendations
{recommendation}

### 💡 Financial Health
{health_message}

### 📉 Expense Analysis
{expense_message}

### 🚑 Emergency Fund
{emergency_message}

### 📈 Retirement Readiness
{readiness}

### 💰 Savings Strategy
{savings_recommendation}
"""

        st.subheader("📈 Retirement Wealth Projection")
        st.line_chart(data.set_index("Year"))

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    st.session_state.step += 1
    st.rerun()

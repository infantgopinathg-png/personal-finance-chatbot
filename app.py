import streamlit as st

st.title("💰 Personal Financial Discipline Advisor")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.step = 0

questions = [
"Hello! I will help you plan your savings and retirement. What is your age?",
"What is your gender? (Male/Female/Other)",
"What is your monthly income (₹)?",
"What are your monthly expenses (₹)?",
"How much current savings do you have (₹)?",
"What is your retirement age?"
]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Type your answer")

if st.session_state.step == 0 and len(st.session_state.messages) == 0:
    st.session_state.messages.append({"role":"assistant","content":questions[0]})
    st.rerun()

if user_input:

    st.session_state.messages.append({"role":"user","content":user_input})
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

        retirement_age = int(user_input)

        monthly_savings = st.session_state.income - st.session_state.expenses
        years_left = retirement_age - st.session_state.age
        corpus = (monthly_savings * 12 * years_left) + st.session_state.savings

    if st.session_state.age < 40:
        recommendation = """
Recommended Government Retirement Schemes:

• National Pension System (NPS)
• Public Provident Fund (PPF)
• Atal Pension Yojana (APY)
"""
    else:
        recommendation = """
Recommended Government Retirement Schemes:

• National Pension System (NPS)
• Senior Citizen Savings Scheme (SCSS)
• Pradhan Mantri Vaya Vandana Yojana (PMVVY)
"""

    savings_rate = monthly_savings / st.session_state.income

    if savings_rate < 0.2:
        advice = "⚠ Increase savings to at least 20% of income."
    elif savings_rate < 0.4:
        advice = "👍 Good savings discipline."
    else:
        advice = "🎉 Excellent financial discipline."

    reply = f"""
### Financial Plan

Monthly Savings: ₹{monthly_savings}

Years to Retirement: {years_left}

Estimated Retirement Corpus: ₹{corpus}

### Recommended Government Schemes
{recommendation}

Advice: {advice}
"""

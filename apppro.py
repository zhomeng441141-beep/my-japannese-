import streamlit as st
import pandas as pd

st.set_page_config(page_title="房贷计算器 Pro", layout="wide")

def calculate_mortgage(principal, annual_rate, years):
    monthly_rate = annual_rate / 100 / 12
    months = years * 12

    if monthly_rate == 0:
        return principal / months

    return principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)


def generate_schedule(principal, annual_rate, years, extra_payment=0):
    monthly_rate = annual_rate / 100 / 12
    months = years * 12
    payment = calculate_mortgage(principal, annual_rate, years)

    balance = principal
    data = []

    for m in range(1, months + 1):
        interest = balance * monthly_rate
        principal_payment = payment - interest + extra_payment

        if balance <= 0:
            break

        balance -= principal_payment

        data.append([
            m,
            round(payment + extra_payment, 2),
            round(principal_payment, 2),
            round(interest, 2),
            round(max(balance, 0), 2)
        ])

    df = pd.DataFrame(data, columns=["期数", "月供", "本金", "利息", "剩余贷款"])
    return df


# ================= UI =================

st.title("🏠 房贷计算器 Pro")

col1, col2 = st.columns(2)

with col1:
    principal = st.number_input("贷款金额", value=1000000)
    rate = st.number_input("年利率 (%)", value=4.5)
    years = st.number_input("贷款年限（年）", value=30)

with col2:
    extra_payment = st.number_input("每月额外还款（提前还）", value=0)

if st.button("开始计算"):

    monthly_payment = calculate_mortgage(principal, rate, years)
    df = generate_schedule(principal, rate, years, extra_payment)

    total_payment = df["月供"].sum()
    total_interest = df["利息"].sum()

    # ===== 核心指标 =====
    st.subheader("📊 核心结果")

    c1, c2, c3 = st.columns(3)
    c1.metric("月供", f"{monthly_payment:.2f}")
    c2.metric("总利息", f"{total_interest:,.0f}")
    c3.metric("总还款", f"{total_payment:,.0f}")

    # ===== 图表 =====
    st.subheader("📈 本金 vs 利息")

    chart_data = df[["本金", "利息"]]
    st.area_chart(chart_data)

    # ===== 剩余贷款趋势 =====
    st.subheader("📉 剩余贷款变化")
    st.line_chart(df["剩余贷款"])

    # ===== 表格 =====
    st.subheader("📋 还款明细（可滚动）")
    st.dataframe(df, use_container_width=True)
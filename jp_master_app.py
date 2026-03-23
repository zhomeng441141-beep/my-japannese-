import streamlit as st
import pandas as pd
import datetime

# ==============================
# 🎨 页面配置与样式 (保持不变)
# ==============================
st.set_page_config(page_title="全能日语语法查询 App", page_icon="📖", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #eee; border-radius: 4px 4px 0 0; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# ==============================
# 📊 数据库集成 (保持不变)
# ==============================
masu_data = [
    {"分类": "愿望/倾向", "语法": "～たい/たがる", "级别": "N5", "意义": "想做/他人想做"},
    {"分类": "愿望/倾向", "语法": "～やすい/にくい", "级别": "N4", "意义": "易于/难于"},
    {"分类": "时段/过程", "语法": "～始める/続ける/終わる", "级别": "N4", "意义": "开始/持续/结束"},
    {"分类": "时段/过程", "语法": "～きる", "级别": "N2", "意义": "彻底完结"},
    {"分类": "方式/程度", "语法": "～方 (かた)", "级别": "N4", "意义": "方法"},
    {"分类": "状态/残留", "语法": "～核心/たて/っぱなし", "级别": "N3/N2", "意义": "刚做完/放任不管"},
    {"分类": "状态/残留", "语法": "～かける", "级别": "N3", "意义": "刚开始/还没做完"},
    {"分类": "状态/残留", "语法": "～抜く", "级别": "N2", "意义": "坚持到底"},
    {"分类": "关键衔接", "语法": "～次第 (しだい)", "级别": "N2", "意义": "立即/一...就"},
    {"分类": "风险/委婉", "语法": "～がたい", "级别": "N2", "意义": "心理上难接受"},
    {"分类": "风险/委婉", "语法": "～核心/かねる/かねない", "级别": "N2", "意义": "难以做到/恐怕会"},
    {"分类": "商务敬语", "语法": "核心/お～になる/する", "级别": "N4", "意义": "尊他/谦让"}
]

te_data = [
    {"分类": "基础/请求", "语法": "～ている", "级别": "N5", "意义": "正在进行/持续"},
    {"分类": "基础/请求", "语法": "～てください", "级别": "N5", "意义": "请做..."},
    {"分类": "准备/遗憾", "语法": "～ておく/しまう", "级别": "N4", "意义": "事先准备/遗憾"},
    {"分类": "尝试/方向", "语法": "～てみる/いく/くる", "级别": "N4", "意义": "尝试/持续变化"},
    {"分类": "授受关系", "语法": "～てくださる/いただく", "级别": "N4", "意义": "他人为我做(敬语)"},
    {"分类": "逻辑关系", "语法": "～てはじめて", "级别": "N3", "意义": "之后才发现"},
    {"分类": "逻辑关系", "语法": "～てからでないと", "级别": "N3", "意义": "不先...就不能"},
    {"分类": "情感/语感", "语法": "～てたまらない/仕方がない", "级别": "N2", "意义": "...得受不了"},
    {"分类": "情感/语感", "语法": "～てみせる", "级别": "N2", "意义": "做给...看/决意"},
    {"分类": "高级表达", "语法": "～てまでも", "级别": "N1", "意义": "甚至不惜...也要"},
    {"分类": "高级表达", "语法": "～てやまない", "级别": "N1", "意义": "衷心地"},
    {"分类": "高级表达", "语法": "～てまえ", "级别": "N1", "意义": "正因为立场"}
]

# ==============================
# 🧠 智能活用逻辑 (新增核心引擎)
# ==============================
def conjugate_logic(verb):
    """处理日语动词变形逻辑"""
    # Group 3: 不规则
    if verb == "来る" or verb == "くる": return "き", "きて", "きます"
    if verb == "する": return "し", "して", "します"
    if verb == "行く" or verb == "いく": return "いき", "いって", "いきます"

    # 简单的一段动词判断 (以 e/i + る结尾)
    ichidan_endings = ["べる", "ねる", "める", "れる", "ける", "てる", "いる", "きる", "みる", "しる"]
    if any(verb.endswith(e) for e in ichidan_endings):
        stem = verb[:-1]
        return stem, stem + "て", stem + "ます"

    # 五段动词变形
    stem_map = {"う":"い", "く":"ki", "ぐ":"gi", "す":"し", "つ":"ち", "ぬ":"に", "む":"み", "る":"り", "ぶ":"び"}
    te_map = {"う":"って", "つ":"って", "る":"って", "む":"んで", "ぶ":"んで", "ぬ":"んで", "く":"いて", "ぐ":"いで", "す":"して"}
    
    last_char = verb[-1]
    base = verb[:-1]
    
    if last_char in te_map:
        masu_stem = base + stem_map.get(last_char, "")
        return masu_stem, base + te_map[last_char], masu_stem + "ます"
    
    return verb, verb, verb # 兜底逻辑

# ==============================
# 🖥️ 主页面逻辑
# ==============================
st.title("🏯 2026 宅建士·全能日语语法查询 App")
st.write(f"欢迎回来！现在是：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")

tab_masu, tab_te, tab_lab = st.tabs(["📘 去ます形 (Renyoukei)", "📗 ～て形 (Te-Form)", "🧪 智能动词实验室"])

with tab_masu:
    st.subheader("『去ます形』语法百科")
    df_masu = pd.DataFrame(masu_data)
    search_masu = st.text_input("搜索去ます语法", key="search_masu")
    if search_masu:
        df_masu = df_masu[df_masu.astype(str).apply(lambda x: x.str.contains(search_masu)).any(axis=1)]
    st.table(df_masu)

with tab_te:
    st.subheader("『～て形』语法百科")
    df_te = pd.DataFrame(te_data)
    search_te = st.text_input("搜索～て语法", key="search_te")
    if search_te:
        df_te = df_te[df_te.astype(str).apply(axis=1, func=lambda x: x.str.contains(search_te)).any(axis=1)]
    st.table(df_te)

# --- Tab 3: 智能动词实验室 (升级部分) ---
with tab_lab:
    st.subheader("🧪 智能活用自动生成器 (v2.0)")
    st.caption("输入动词原形（辞书形），自动推导所有语法接续形式")
    
    col1, col2 = st.columns(2)
    
    with col1:
        v_input = st.text_input("输入动词原形 (如: 買う, 食べる, 相談する)", value="買う")
        m_stem, te_form, full_masu = conjugate_logic(v_input)
        
        st.markdown(f"""
        ### 📋 变形结果
        - **辞书形:** `{v_input}`
        - **ます形:** `{full_masu}`
        - **去ます语干:** `{m_stem}`
        - **て形:** `{te_form}`
        """)

    with col2:
        st.markdown("### 🛠️ 自动语法接续样例")
        if v_input:
            st.info(f"**[愿望]** {m_stem}たい (想{v_input})")
            st.success(f"**[状态]** {te_form}いる (正在{v_input})")
            st.warning(f"**[时段]** {m_stem}始める (开始{v_input})")
            st.error(f"**[风险]** {m_stem}かねない (恐怕会{v_input})")
            st.markdown(f"""
<div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; border-left: 5px solid #6c757d;">
    <strong>[请求]</strong> {te_form}ください (请{v_input})
</div>
""", unsafe_allow_html=True)

# --- 侧边栏：宅建实战练习 ---
st.sidebar.header("🎯 宅建实战练习")
st.sidebar.info("场景：客户一交保修金，我们就立即交房。")
if st.sidebar.button("显示参考译文"):
    st.sidebar.code("手付金（てつけきん）を【受け取り次第】、引き渡します。")
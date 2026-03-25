import streamlit as st
import pandas as pd

# ==============================
# 📊 敬语核心数据库 (全量集成)
# ==============================
keigo_data = [
    {"动词": "行く (去)", "尊他语 (抬高对方)": "いらっしゃる / おいでになる", "自谦语 (降低自己)": "伺う / 参る"},
    {"动词": "来る (来)", "尊他语 (抬高对方)": "いらっしゃる / おいでになる", "自谦语 (降低自己)": "参る"},
    {"动词": "居る (在)", "尊他语 (抬高对方)": "いらっしゃる", "自谦语 (降低自己)": "居る (おる)/ おります"},
    {"动词": "言う (说)", "尊他语 (抬高对方)": "おっしゃる", "自谦语 (降低自己)": "申す / 申し上げる"},
    {"动词": "する (做)", "尊他语 (抬高对方)": "なさる", "自谦语 (降低自己)": "致す (いたす)"},
    {"动词": "食べる (吃)", "尊他语 (抬高对方)": "召し上がる", "自谦语 (降低自己)": "いただく"},
    {"动词": "見る (看)", "尊他语 (抬高对方)": "ご覧になる", "自谦语 (降低自己)": "拝見する"},
    {"动词": "聞く (听/问)", "尊他语 (抬高对方)": "お聞きになる", "自谦语 (降低自己)": "伺う / 拝聴する"},
    {"动词": "知る (知道)", "尊他语 (抬高对方)": "ご存じだ", "自谦语 (降低自己)": "存じ上げる"},
    {"动词": "会う (见面)", "尊他语 (抬高对方)": "お会いになる", "自谦语 (降低自己)": "お目にかかる"},
    {"动词": "与える (给)", "尊他语 (抬高对方)": "くださる", "自谦语 (降低自己)": "差し上げる"},
]

# ==============================
# 🖥️ 敬语页面逻辑 (Tab 4)
# ==============================
# 假设你在主程序的 tabs 中增加了 tab_keigo
# with tab_keigo:

st.header("👑 宅建士商务敬语专家系统")
st.caption("2026年实战版：包含特殊不规则动词与通用公式转换")

col_table, col_trans = st.columns([1.2, 0.8])

# --- 左侧：固定表格查询 ---
with col_table:
    st.subheader("📚 核心不规则动词对照表")
    df_keigo = pd.DataFrame(keigo_data)
    st.dataframe(df_keigo, use_container_width=True, hide_index=True)
    
    st.markdown("""
    > **💡 通用公式提醒：**
    > * **尊他：** `お + 去ます形 + になる` (例：お帰りになる)
    > * **自谦：** `お + 去ます形 + する` (例：お持ちする)
    """)

# --- 右侧：一键敬语翻译机 ---
with col_trans:
    st.subheader("🧪 交互式敬语转换器")
    st.write("选择一个常用动词，查看标准职场表达：")
    
    # 构建转换字典
    keigo_dict = {item["动词"].split(" ")[0]: item for item in keigo_data}
    
    v_choice = st.selectbox("请选择要转换的动词：", list(keigo_dict.keys()))
    
    if v_choice:
        res = keigo_dict[v_choice]
        
        # 尊他展示卡片
        st.markdown(f"""
        <div style="background-color: #f3e5f5; padding: 15px; border-left: 6px solid #9c27b0; border-radius: 8px; margin-bottom: 15px;">
            <p style="color: #7b1fa2; font-weight: bold; margin-bottom: 5px;">⬆️ 尊他语 (抬高客户/上司)</p>
            <h3 style="margin: 0;">{res['尊他语 (抬高对方)']}</h3>
            <small>场景：客户{v_choice}、社长{v_choice}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # 自谦展示卡片
        st.markdown(f"""
        <div style="background-color: #e3f2fd; padding: 15px; border-left: 6px solid #2196f3; border-radius: 8px;">
            <p style="color: #1976d2; font-weight: bold; margin-bottom: 5px;">⬇️ 自谦语 (降低自己)</p>
            <h3 style="margin: 0;">{res['自谦语 (降低自己)']}</h3>
            <small>场景：我{v_choice}、我司职员{v_choice}</small>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.warning("**⚠️ 宅建忌语：** 禁止对自己使用尊他语！(例如：❌「私が召し上がります」)")
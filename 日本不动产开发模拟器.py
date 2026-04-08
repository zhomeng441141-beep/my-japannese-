import streamlit as st
import math
import pandas as pd

# 页面配置
st.set_page_config(page_title="Japan Dev Simulator", layout="wide")

st.title("🏗️ 日本不动产开发模拟器 (Beta 2026)")
st.markdown("---")

# --- Sidebar: 输入参数 ---
with st.sidebar:
    st.header("📍 土地基本信息")
    site_area = st.number_input("基地面积 (m²)", value=300.0, step=10.0)
    land_price_per_m2 = st.number_input("土地单价 (JPY/m²)", value=100000)
    
    st.header("⚖️ 城市规划限制")
    district_type = st.selectbox("用途地域类型", ["住宅系 (0.4)", "商业/工业系 (0.6)"])
    zoning_bcr = st.slider("指定建蔽率 (%)", 30, 80, 60)
    zoning_far = st.slider("指定容积率 (%)", 50, 500, 200)
    
    st.header("🛣️ 道路条件")
    road_count = st.number_input("接触道路数量", min_value=1, max_value=4, value=1)
    road_widths = []
    for i in range(road_count):
        road_widths.append(st.number_input(f"道路 {i+1} 宽度 (m)", value=4.0, step=0.1))
    
    is_corner = st.checkbox("是否为角地 (BCR +10%)")
    
    st.header("💰 财务假设")
    const_cost_m2 = st.number_input("建筑单价 (JPY/m²)", value=350000)
    is_niseko = st.toggle("启用季节性收益模型 (Niseko/Rusutsu)")

# --- 核心计算逻辑 ---
def run_simulation():
    # 1. 道路后退计算 (Set-back)
    lost_area = 0
    for w in road_widths:
        if w < 4.0:
            # 简化逻辑：假设临边长度为面积开平方
            edge_length = math.sqrt(site_area)
            lost_area += (4.0 - w) / 2 * edge_length
    
    effective_site_area = site_area - lost_area
    
    # 2. 法律限制判定
    # 容积率判定
    coeff = 0.4 if "住宅" in district_type else 0.6
    road_limited_far = (max(road_widths) * coeff) * 100
    final_far = min(zoning_far, road_limited_far)
    
    # 建蔽率判定
    final_bcr = zoning_bcr + (10 if is_corner else 0)
    final_bcr = min(final_bcr, 100)
    
    # 3. 规模计算
    max_building_area = effective_site_area * (final_bcr / 100)
    max_total_floor_area = effective_site_area * (final_far / 100)
    
    # 4. 财务模拟
    total_land_cost = site_area * land_price_per_m2
    total_build_cost = max_total_floor_area * const_cost_m2
    total_inv = total_land_cost + total_build_cost
    
    # 收益模型
    if is_niseko:
        # 假设：冬季4个月高收益，夏季6个月低收益，2个月淡季
        annual_rev = (max_total_floor_area * 10000 * 4) + (max_total_floor_area * 2000 * 6)
    else:
        annual_rev = max_total_floor_area * 4000 * 12
        
    yield_rate = (annual_rev / total_inv) * 100 if total_inv > 0 else 0
    
    return {
        "eff_area": effective_site_area,
        "lost_area": lost_area,
        "final_far": final_far,
        "final_bcr": final_bcr,
        "max_gfa": max_total_floor_area,
        "max_ba": max_building_area,
        "total_inv": total_inv,
        "annual_rev": annual_rev,
        "yield_rate": yield_rate
    }

res = run_simulation()

# --- Main UI: 结果展示 ---
col1, col2, col3 = st.columns(3)
col1.metric("有效基地面积", f"{res['eff_area']:.2f} m²", f"-{res['lost_area']:.1f} m²")
col2.metric("最大总建筑面积 (GFA)", f"{res['max_gfa']:.2f} m²")
col3.metric("预估表面收益率", f"{res['yield_rate']:.2f} %")

st.markdown("### 📊 详细测算数据")
df_res = pd.DataFrame({
    "项目": ["法定容积率", "法定建蔽率", "土地总价", "建筑总价", "总投资额", "预估年收入"],
    "数值": [
        f"{res['final_far']}%", 
        f"{res['final_bcr']}%", 
        f"¥{res['total_inv']*0.3:,.0f} (约30%)", # 假设土地占比
        f"¥{res['total_inv']*0.7:,.0f} (约70%)",
        f"¥{res['total_inv']:,.0f}",
        f"¥{res['annual_rev']:,.0f}"
    ]
})
st.table(df_res)

st.info(f"💡 法律公式参考：容积率判定 $FAR_{{final}} = \min(FAR_{{zoning}}, W_{{road}} \\times {0.4 if '住宅' in district_type else 0.6} \\times 100\%)$")

st.success("📝 实务提醒：如果是民宿用途，请务必确认《区分所有法》规约或地方《上乘条例》对营业天数的限制。")
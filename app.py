import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime

# ==========================================
# CẤU HÌNH GIAO DIỆN
# ==========================================
st.set_page_config(page_title="Sun PhuQuoc Airways - APIS", page_icon="☀️", layout="wide")

# CSS TUỲ CHỈNH
st.markdown("""
<style>
    .stButton > button { border-radius: 8px; font-weight: 600; border: 1px solid #d4af37; }
    .stButton > button:hover { background-color: #fffaf0; }
</style>
""", unsafe_allow_html=True)

# HEADER: HIỂN THỊ ĐỦ 8 MÚI GIỜ
header_html = """
<div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 15px; background: #fffaf0; border-radius: 10px; border-bottom: 3px solid #d4af37; font-family: sans-serif; font-size: 10px;">
    <div style="flex: 1;">
        <div style="color: #1a2a6c; font-size: 16px; font-weight: 800;">SUN PHUQUOC AIRWAYS</div>
        <div style="color: #d4af37; font-weight: 700;">APIS OPERATIONS CENTER</div>
    </div>
    <div style="display: flex; gap: 8px; text-align: center;">
        <div><b>VN:</b><br><span id="time-vn"></span></div>
        <div><b>UTC:</b><br><span id="time-utc"></span></div>
        <div><b>HK:</b><br><span id="time-hk"></span></div>
        <div><b>TP:</b><br><span id="time-tp"></span></div>
        <div><b>KR:</b><br><span id="time-kr"></span></div>
        <div><b>TH:</b><br><span id="time-th"></span></div>
        <div><b>SG:</b><br><span id="time-sg"></span></div>
        <div><b>MY:</b><br><span id="time-my"></span></div>
        <div><b>CN:</b><br><span id="time-cn"></span></div>
    </div>
</div>
<script>
    function updateTime() {
        const now = new Date();
        const opts = {hour: '2-digit', minute: '2-digit', hour12: false};
        document.getElementById('time-utc').innerText = now.toLocaleTimeString('en-GB', {timeZone: 'UTC', ...opts});
        document.getElementById('time-vn').innerText = now.toLocaleTimeString('en-GB', {timeZone: 'Asia/Ho_Chi_Minh', ...opts});
        document.getElementById('time-hk').innerText = now.toLocaleTimeString('en-GB', {timeZone: 'Asia/Hong_Kong', ...opts});
        document.getElementById('time-tp').innerText = now.toLocaleTimeString('en-GB', {timeZone: 'Asia/Taipei', ...opts});
        document.getElementById('time-kr').innerText = now.toLocaleTimeString('en-GB', {timeZone: 'Asia/Seoul', ...opts});
        document.getElementById('time-th').innerText = now.toLocaleTimeString('en-GB', {timeZone: 'Asia/Bangkok', ...opts});
        document.getElementById('time-sg').innerText = now.toLocaleTimeString('en-GB', {timeZone: 'Asia/Singapore', ...opts});
        document.getElementById('time-my').innerText = now.toLocaleTimeString('en-GB', {timeZone: 'Asia/Kuala_Lumpur', ...opts});
        document.getElementById('time-cn').innerText = now.toLocaleTimeString('en-GB', {timeZone: 'Asia/Shanghai', ...opts});
    }
    setInterval(updateTime, 1000);
    updateTime();
</script>
"""
components.html(header_html, height=80)

# ==========================================
# DANH SÁCH QUỐC GIA MỚI
# ==========================================
st.subheader("🌍 Chọn quốc gia đến:")

COUNTRY_CONFIG = {
    "Việt Nam": "vn", "HongKong": "hk", "Taipei": "tw", 
    "Korean": "kr", "Thailand": "th", "Singapore": "sg", 
    "Malaysia": "my", "China": "cn"
}

if 'sel' not in st.session_state: st.session_state.sel = "Việt Nam"

# Chia grid 4 cột để hiển thị 8 nước gọn gàng
cols = st.columns(4)
keys = list(COUNTRY_CONFIG.keys())

for i, key in enumerate(keys):
    with cols[i % 4]:
        flag = f"https://flagcdn.com/w40/{COUNTRY_CONFIG[key]}.png"
        if st.button(f"{key}", key=f"btn_{key}", use_container_width=True):
            st.session_state.sel = key
            st.rerun()

st.markdown(f"### Đang làm việc với: **{st.session_state.sel}**")
st.file_uploader(f"Tải lên file GD cho {st.session_state.sel}")

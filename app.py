import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime

# ==========================================
# CẤU HÌNH GIAO DIỆN
# ==========================================
st.set_page_config(page_title="Sun PhuQuoc Airways - APIS", page_icon="☀️", layout="wide")

# CSS ĐỂ LÀM MỚI GIAO DIỆN
st.markdown("""
<style>
    .stButton > button { border-radius: 10px; font-weight: 600; border: 1px solid #d4af37; height: 60px; background-color: white; }
    .stButton > button:hover { background-color: #fffaf0; border: 2px solid #d4af37; }
</style>
""", unsafe_allow_html=True)

# HEADER: MỞ RỘNG VÀ HIỂN THỊ ĐẦY ĐỦ THÔNG TIN
header_html = """
<div style="background: linear-gradient(135deg, #1a2a6c, #001f3f); padding: 20px; border-radius: 15px; color: white; font-family: sans-serif; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
    <div style="text-align: center; margin-bottom: 15px;">
        <div style="font-size: 24px; font-weight: 900; letter-spacing: 2px; color: #d4af37;">☀️ SUN PHUQUOC AIRWAYS</div>
        <div style="font-size: 14px; letter-spacing: 4px; opacity: 0.8;">APIS OPERATIONS CENTER</div>
    </div>
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; font-size: 12px; text-align: center;">
        <div><b>VietNam (VN):</b><br><span id="time-vn" style="font-size: 16px; font-weight: bold;"></span></div>
        <div><b>UTC:</b><br><span id="time-utc" style="font-size: 16px; font-weight: bold;"></span></div>
        <div><b>HongKong (HK):</b><br><span id="time-hk" style="font-size: 16px; font-weight: bold;"></span></div>
        <div><b>Taipei (TW):</b><br><span id="time-tp" style="font-size: 16px; font-weight: bold;"></span></div>
        <div><b>Korean (KR):</b><br><span id="time-kr" style="font-size: 16px; font-weight: bold;"></span></div>
        <div><b>Thailand (TH):</b><br><span id="time-th" style="font-size: 16px; font-weight: bold;"></span></div>
        <div><b>Singapore (SG):</b><br><span id="time-sg" style="font-size: 16px; font-weight: bold;"></span></div>
        <div><b>Malaysia (MY):</b><br><span id="time-my" style="font-size: 16px; font-weight: bold;"></span></div>
    </div>
</div>
<script>
    function updateTime() {
        const now = new Date();
        const opts = {hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false};
        const zones = ['Asia/Ho_Chi_Minh', 'UTC', 'Asia/Hong_Kong', 'Asia/Taipei', 'Asia/Seoul', 'Asia/Bangkok', 'Asia/Singapore', 'Asia/Kuala_Lumpur'];
        const ids = ['vn', 'utc', 'hk', 'tp', 'kr', 'th', 'sg', 'my'];
        ids.forEach((id, i) => {
            document.getElementById('time-'+id).innerText = now.toLocaleTimeString('en-GB', {timeZone: zones[i], ...opts});
        });
    }
    setInterval(updateTime, 1000);
    updateTime();
</script>
"""
components.html(header_html, height=220)

# ==========================================
# CẤU HÌNH QUỐC GIA & GRID
# ==========================================
COUNTRY_DATA = {
    "Việt Nam": "vn", "HongKong": "hk", "Taipei": "tw", "Korean": "kr",
    "Thailand": "th", "Singapore": "sg", "Malaysia": "my", "China": "cn"
}

if 'sel' not in st.session_state: st.session_state.sel = "Việt Nam"

st.markdown("---")
# Cấu hình trạng thái đã có template hay chưa
TEMPLATE_READY = {
    "Việt Nam": True, "HongKong": False, "Taipei": False, "Korean": False,
    "Thailand": False, "Singapore": False, "Malaysia": False, "China": False
}

if TEMPLATE_READY[st.session_state.sel]:
    uploaded = st.file_uploader(f"Tải lên file GD (.xls, .xlsx) cho {st.session_state.sel}")
    if uploaded:
        st.info(f"Đang xử lý dữ liệu APIS cho {st.session_state.sel}...")
        # Gọi hàm xử lý tương ứng ở đây
else:
    st.warning(f"🚧 Chức năng xuất APIS cho **{st.session_state.sel}** đang chờ cập nhật Template chuẩn. Vui lòng liên hệ Admin để thêm mẫu!")

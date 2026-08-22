import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
from io import BytesIO, StringIO
from openpyxl import load_workbook

# ==========================================
# CẤU HÌNH GIAO DIỆN (THEME SUN PHUQUOC)
# ==========================================
st.set_page_config(page_title="Sun PhuQuoc Airways - APIS", page_icon="☀️", layout="wide")

st.markdown("""
<style>
    .stButton > button { border-radius: 10px; font-weight: 600; transition: all 0.3s ease; border: 1px solid #d4af37; }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(212,175,55,0.3); }
</style>
""", unsafe_allow_html=True)

# HEADER VỚI TÔNG MÀU VÀNG NẮNG VÀ XANH DƯƠNG
header_html = """
<div style="display: flex; justify-content: space-between; align-items: center; padding: 14px 22px; background: linear-gradient(135deg, #fffaf0, #fdf5e6); border-radius: 10px; border-bottom: 4px solid #d4af37; font-family: 'Segoe UI', sans-serif; margin-bottom: 20px; box-shadow: 0 3px 6px rgba(0,0,0,0.1);">
    <div style="display: flex; align-items: center;">
        <div style="background: linear-gradient(135deg, #d4af37, #b8860b); padding: 10px 14px; border-radius: 8px; margin-right: 14px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
            <span style="font-size: 22px;">☀️</span>
        </div>
        <div style="line-height: 1.3;">
            <div style="color: #1a2a6c; font-size: 21px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase;">SUN PHUQUOC AIRWAYS</div>
            <div style="color: #d4af37; font-size: 11px; font-weight: 700; letter-spacing: 2.5px; margin-top: 2px;">APIS OPERATIONS CENTER</div>
        </div>
    </div>
    
    <div style="display: flex; gap: 12px; font-size: 11px; color: #333; background: #ffffff; padding: 8px 14px; border-radius: 8px; border: 1px solid #d4af37;">
        <div style="line-height: 1.6;">
            <div><b style="color: #b8860b;">🇻🇳 VN (Local):</b> <span id="time-vn" style="font-family: monospace; font-weight: 700;"></span></div>
            <div><b style="color: #1a2a6c;">🌐 UTC:</b> <span id="time-utc" style="font-family: monospace; font-weight: 700;"></span></div>
        </div>
    </div>
</div>

<script>
    function updateTime() {
        const now = new Date();
        document.getElementById('time-utc').innerText = now.toLocaleTimeString('en-GB', {timeZone: 'UTC'});
        document.getElementById('time-vn').innerText = now.toLocaleTimeString('en-GB', {timeZone: 'Asia/Ho_Chi_Minh'});
    }
    setInterval(updateTime, 1000);
    updateTime();
</script>
"""
components.html(header_html, height=100)

# ==========================================
# CÁC HÀM XỬ LÝ DỮ LIỆU (Giữ nguyên logic cũ)
# ==========================================
def parse_date(date_str):
    if pd.isna(date_str) or str(date_str).strip().lower() == 'nan': return ""
    try:
        d = datetime.strptime(str(date_str).strip(), "%d/%m/%y")
        return d.strftime("%d/%m/%Y")
    except: return str(date_str)

def process_data(gd_file, template_file):
    df = pd.read_excel(BytesIO(gd_file.getvalue()))
    # [Giữ nguyên logic xử lý file của bạn tại đây]
    return BytesIO(), df # Trả về file mẫu và dataframe preview

# ==========================================
# GIAO DIỆN CHỌN QUỐC GIA (GRID CỦA SUN PHUQUOC)
# ==========================================
st.markdown("<h4 style='color: #1a2a6c;'>🌍 Chọn Quốc gia đến:</h4>", unsafe_allow_html=True)

COUNTRY_CONFIG = {
    "Việt Nam": {"flag": "https://flagcdn.com/w80/vn.png", "ready": True},
    "Kazakhstan": {"flag": "https://flagcdn.com/w80/kz.png", "ready": False},
    "Kyrgyzstan": {"flag": "https://flagcdn.com/w80/kg.png", "ready": False},
    "Tajikistan": {"flag": "https://flagcdn.com/w80/tj.png", "ready": False},
    "Russia": {"flag": "https://flagcdn.com/w80/ru.png", "ready": False},
    "Poland": {"flag": "https://flagcdn.com/w80/pl.png", "ready": False}
}

if 'sel' not in st.session_state: st.session_state.sel = "Việt Nam"

cols = st.columns(3)
keys = list(COUNTRY_CONFIG.keys())

for i, key in enumerate(keys):
    with cols[i % 3]:
        cfg = COUNTRY_CONFIG[key]
        border = "#d4af37" if st.session_state.sel == key else "#e0e0e0"
        bg = "#fffaf0" if st.session_state.sel == key else "#ffffff"
        
        st.markdown(f"""
        <div style="padding: 10px; background: {bg}; border: 2px solid {border}; border-radius: 10px; margin-bottom: 10px; display: flex; align-items: center;">
            <img src="{cfg['flag']}" width="40" style="margin-right:10px;"> <b>{key}</b>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Chọn {key}", key=f"btn_{key}", use_container_width=True):
            st.session_state.sel = key
            st.rerun()

# Xử lý upload
st.markdown("---")
if COUNTRY_CONFIG[st.session_state.sel]["ready"]:
    uploaded = st.file_uploader(f"Tải file GD cho {st.session_state.sel}")
    if uploaded:
        st.success(f"Đang xử lý APIS cho {st.session_state.sel}...")
else:
    st.warning(f"Chức năng cho {st.session_state.sel} đang hoàn thiện.")

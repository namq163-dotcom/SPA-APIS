import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
from io import BytesIO, StringIO
from openpyxl import load_workbook

# ==========================================
# CẤU HÌNH GIAO DIỆN
# ==========================================
st.set_page_config(page_title="Sun PhuQuoc Airways - APIS", page_icon="☀️", layout="wide")

st.markdown("""
<style>
    .stButton > button { border-radius: 10px; font-weight: 600; border: 1px solid #d4af37; height: 50px; background-color: white; }
    .stButton > button:hover { background-color: #fffaf0; border: 2px solid #d4af37; }
</style>
""", unsafe_allow_html=True)

# Header đồng hồ
header_html = """
<div style="background: linear-gradient(135deg, #1a2a6c, #001f3f); padding: 20px; border-radius: 15px; color: white; text-align: center;">
    <h2 style="margin:0; color: #d4af37;">SUN PHUQUOC AIRWAYS</h2>
    <p style="margin:0; opacity: 0.8;">APIS OPERATIONS CENTER</p>
</div>
"""
components.html(header_html, height=120)

# ==========================================
# CÁC HÀM XỬ LÝ DỮ LIỆU
# ==========================================
def parse_date(date_str):
    if pd.isna(date_str) or not str(date_str).strip() or str(date_str).strip().lower() == 'nan': return ""
    try:
        d = datetime.strptime(str(date_str).strip(), "%d/%m/%y")
        return d.strftime("%d/%m/%Y")
    except: return str(date_str)

def process_roster_data_vn(gd_file, template_file_path, departure, arrival):
    content = gd_file.getvalue()
    df_gd = None
    
    # Đa định dạng đọc file
    try: df_gd = pd.read_excel(BytesIO(content), engine='openpyxl')
    except:
        try: df_gd = pd.read_excel(BytesIO(content), engine='xlrd')
        except:
            try: df_gd = pd.read_html(StringIO(content.decode('utf-8', errors='ignore')))[0]
            except: df_gd = pd.read_csv(BytesIO(content), sep=None, engine='python', header=None)

    # Tìm header
    header_idx = None
    for idx, row in df_gd.iterrows():
        row_str = row.fillna("").astype(str).str.lower()
        if any('passport' in s for s in row_str) and any('name' in s for s in row_str):
            header_idx = idx; break
            
    header_row = df_gd.iloc[header_idx].fillna("").astype(str).str.lower()
    col_name = next((i for i, v in enumerate(header_row) if 'name' in v), None)
    col_passport = next((i for i, v in enumerate(header_row) if 'passport' in v and 'expiry' not in v), None)
    
    crew_data = []
    for idx in range(header_idx + 1, len(df_gd)):
        row = df_gd.iloc[idx]
        name = str(row.iloc[col_name]).strip()
        passport = str(row.iloc[col_passport]).strip()
        if name and name.lower() != 'nan':
            crew_data.append([name.split()[0], None, " ".join(name.split()[1:]), "", "", "", "P", passport, "", ""])

    # Ghi vào template
    output = BytesIO()
    book = load_workbook(template_file_path)
    sheet = book.active
    
    # Ghi Nơi đi/Nơi đến vào ô B6, B7 (Thay đổi nếu cần)
    sheet['B6'] = departure
    sheet['B7'] = arrival
    
    # Ghi danh sách
    for r_idx, row_data in enumerate(crew_data, 14):
        for c_idx, value in enumerate(row_data, 1):
            sheet.cell(row=r_idx, column=c_idx, value=value)
            
    book.save(output)
    return output.getvalue(), pd.DataFrame(crew_data)

# ==========================================
# GIAO DIỆN CHÍNH
# ==========================================
st.session_state.sel = st.session_state.get('sel', "Việt Nam")

st.subheader("🌍 Chọn Quốc gia & Nhập thông tin bay")
cols = st.columns(4)
for i, country in enumerate(["Việt Nam", "HongKong", "Taipei", "Korean"]):
    if cols[i].button(country, use_container_width=True):
        st.session_state.sel = country

st.markdown("---")

if st.session_state.sel == "Việt Nam":
    col1, col2 = st.columns(2)
    dep = col1.text_input("📍 Nơi khởi hành (ví dụ: PQC)", "PQC")
    arr = col2.text_input("📍 Nơi đến (ví dụ: SGN)", "SGN")
    
    uploaded_gd = st.file_uploader("Tải lên file dữ liệu bay", type=["xls", "xlsx", "csv"])
    
    if uploaded_gd:
        try:
            excel_data, df_preview = process_roster_data_vn(uploaded_gd, "Template_VNAPIS.xlsx", dep, arr)
            st.success("✅ Đã xử lý xong!")
            st.download_button("⬇️ Tải file kết quả", excel_data, "APIS_Export.xlsx")
        except Exception as e:
            st.error(f"Lỗi: {e}")
else:
    st.warning("Tính năng cho quốc gia này đang được phát triển.")

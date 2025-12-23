import streamlit as st
from datetime import datetime, date
import json
from typing import List, Dict
import pandas as pd
import io

# Cấu hình trang
st.set_page_config(
    page_title="To-Do List App",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Khởi tạo session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'task_id_counter' not in st.session_state:
    st.session_state.task_id_counter = 0

# Khởi tạo order cho các tasks cũ (nếu chưa có)
for idx, task in enumerate(st.session_state.tasks):
    if 'order' not in task:
        task['order'] = idx

# Định nghĩa priority colors
PRIORITY_COLORS = {
    "Gấp": "🔴",
    "Quan trọng": "🟡",
    "Bình thường": "🟢"
}

PRIORITY_COLORS_HEX = {
    "Gấp": "#FF4444",
    "Quan trọng": "#FFAA00",
    "Bình thường": "#44FF44"
}

CATEGORIES = ["Công việc", "Cá nhân", "Học tập", "Khác"]

def add_task(task_name: str, priority: str, category: str, due_date: date = None):
    """Thêm task mới vào danh sách"""
    max_order = max([t.get('order', 0) for t in st.session_state.tasks], default=-1)
    task = {
        'id': st.session_state.task_id_counter,
        'name': task_name,
        'completed': False,
        'priority': priority,
        'category': category,
        'due_date': due_date.isoformat() if due_date else None,
        'created_at': datetime.now().isoformat(),
        'order': max_order + 1
    }
    st.session_state.tasks.append(task)
    st.session_state.task_id_counter += 1

def update_task(task_id: int, **kwargs):
    """Cập nhật thông tin task"""
    for task in st.session_state.tasks:
        if task['id'] == task_id:
            for key, value in kwargs.items():
                if key == 'due_date' and value:
                    task[key] = value.isoformat() if isinstance(value, date) else value
                else:
                    task[key] = value
            break

def delete_task(task_id: int):
    """Xóa task khỏi danh sách"""
    st.session_state.tasks = [t for t in st.session_state.tasks if t['id'] != task_id]

def toggle_task_completion(task_id: int):
    """Chuyển đổi trạng thái hoàn thành của task"""
    for task in st.session_state.tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            break

def reorder_tasks(old_index: int, new_index: int):
    """Sắp xếp lại thứ tự tasks"""
    if 0 <= old_index < len(st.session_state.tasks) and 0 <= new_index < len(st.session_state.tasks):
        task = st.session_state.tasks.pop(old_index)
        st.session_state.tasks.insert(new_index, task)
        # Cập nhật lại order cho tất cả tasks
        for idx, t in enumerate(st.session_state.tasks):
            t['order'] = idx

def move_task_up(task_id: int):
    """Di chuyển task lên trên"""
    task_index = next((i for i, t in enumerate(st.session_state.tasks) if t['id'] == task_id), None)
    if task_index is not None and task_index > 0:
        reorder_tasks(task_index, task_index - 1)

def move_task_down(task_id: int):
    """Di chuyển task xuống dưới"""
    task_index = next((i for i, t in enumerate(st.session_state.tasks) if t['id'] == task_id), None)
    if task_index is not None and task_index < len(st.session_state.tasks) - 1:
        reorder_tasks(task_index, task_index + 1)

# Sidebar - Bộ lọc và tìm kiếm
with st.sidebar:
    st.header("🔍 Tìm kiếm & Lọc")
    
    # Tìm kiếm
    search_query = st.text_input("🔎 Tìm kiếm công việc", "")
    
    # Bộ lọc trạng thái
    filter_status = st.selectbox(
        "📊 Lọc theo trạng thái",
        ["Tất cả", "Đang làm", "Đã hoàn thành"]
    )
    
    # Bộ lọc priority
    filter_priority = st.selectbox(
        "⚡ Lọc theo mức độ ưu tiên",
        ["Tất cả", "Gấp", "Quan trọng", "Bình thường"]
    )
    
    # Bộ lọc category
    filter_category = st.selectbox(
        "📁 Lọc theo danh mục",
        ["Tất cả"] + CATEGORIES
    )
    
    # Tùy chọn sắp xếp
    st.divider()
    st.subheader("🔄 Sắp xếp")
    sort_option = st.selectbox(
        "Sắp xếp theo",
        ["Thứ tự thêm", "Mức độ ưu tiên", "Ngày hết hạn", "Tên (A-Z)"],
        key="sort_option"
    )
    
    st.divider()
    
    # Thống kê
    total_tasks = len(st.session_state.tasks)
    completed_tasks = sum(1 for t in st.session_state.tasks if t['completed'])
    pending_tasks = total_tasks - completed_tasks
    
    st.metric("Tổng số công việc", total_tasks)
    st.metric("Đã hoàn thành", completed_tasks)
    st.metric("Đang làm", pending_tasks)
    
    # Export/Import data
    st.divider()
    st.subheader("💾 Quản lý dữ liệu")
    
    # Export
    col_export1, col_export2 = st.columns(2)
    with col_export1:
        if st.button("📥 Xuất Excel", use_container_width=True):
            if st.session_state.tasks:
                # Chuyển đổi tasks sang DataFrame
                tasks_data = []
                for task in st.session_state.tasks:
                    due_date_str = ""
                    if task.get('due_date'):
                        try:
                            due_date_obj = datetime.fromisoformat(task['due_date']).date()
                            due_date_str = due_date_obj.strftime('%Y-%m-%d')
                        except:
                            due_date_str = task.get('due_date', '')
                    
                    tasks_data.append({
                        'ID': task.get('id', ''),
                        'Tên công việc': task.get('name', ''),
                        'Hoàn thành': 'Có' if task.get('completed', False) else 'Không',
                        'Mức độ ưu tiên': task.get('priority', ''),
                        'Danh mục': task.get('category', ''),
                        'Ngày hết hạn': due_date_str,
                        'Ngày tạo': task.get('created_at', '')[:10] if task.get('created_at') else ''
                    })
                
                df = pd.DataFrame(tasks_data)
                
                # Tạo Excel file trong memory
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Danh sách công việc')
                
                output.seek(0)
                
                st.download_button(
                    label="⬇️ Tải file Excel",
                    data=output.getvalue(),
                    file_name=f"todo_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("Không có dữ liệu để xuất!")
    
    with col_export2:
        if st.button("📥 Xuất JSON", use_container_width=True):
            if st.session_state.tasks:
                tasks_json = json.dumps(st.session_state.tasks, ensure_ascii=False, indent=2)
                st.download_button(
                    label="⬇️ Tải file JSON",
                    data=tasks_json,
                    file_name=f"todo_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.warning("Không có dữ liệu để xuất!")
    
    # Import
    st.markdown("**📤 Nhập dữ liệu**")
    uploaded_file = st.file_uploader(
        "Chọn file Excel (.xlsx) hoặc JSON (.json)",
        type=['xlsx', 'xls', 'json'],
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        try:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension in ['xlsx', 'xls']:
                # Đọc file Excel
                df = pd.read_excel(uploaded_file)
                
                # Kiểm tra các cột bắt buộc
                required_columns = ['Tên công việc']
                if not all(col in df.columns for col in required_columns):
                    st.error("File Excel thiếu cột bắt buộc: 'Tên công việc'")
                else:
                    # Chuyển đổi DataFrame sang danh sách tasks
                    imported_tasks = []
                    for idx, row in df.iterrows():
                        # Xử lý ID - xử lý NaN an toàn
                        task_id = st.session_state.task_id_counter + idx
                        if 'ID' in df.columns:
                            id_value = row.get('ID')
                            if pd.notna(id_value):
                                try:
                                    task_id = int(float(id_value))  # Chuyển qua float trước để xử lý NaN
                                except (ValueError, TypeError):
                                    task_id = st.session_state.task_id_counter + idx
                        
                        # Xử lý tên công việc - bắt buộc
                        task_name = str(row.get('Tên công việc', '')).strip()
                        if not task_name or task_name == 'nan':
                            continue  # Bỏ qua dòng không có tên công việc
                        
                        # Xử lý trạng thái hoàn thành
                        completed = False
                        if 'Hoàn thành' in df.columns:
                            hoan_thanh_val = row.get('Hoàn thành')
                            if pd.notna(hoan_thanh_val):
                                hoan_thanh_str = str(hoan_thanh_val).strip().lower()
                                completed = hoan_thanh_str in ['có', 'yes', 'true', '1', 'x', '✓', '✅']
                        
                        # Xử lý mức độ ưu tiên
                        priority = 'Bình thường'
                        if 'Mức độ ưu tiên' in df.columns:
                            priority_val = row.get('Mức độ ưu tiên')
                            if pd.notna(priority_val):
                                priority_str = str(priority_val).strip()
                                if priority_str in ['Gấp', 'Quan trọng', 'Bình thường']:
                                    priority = priority_str
                        
                        # Xử lý danh mục
                        category = 'Khác'
                        if 'Danh mục' in df.columns:
                            category_val = row.get('Danh mục')
                            if pd.notna(category_val):
                                category_str = str(category_val).strip()
                                if category_str in CATEGORIES:
                                    category = category_str
                        
                        # Xử lý ngày hết hạn
                        due_date = None
                        if 'Ngày hết hạn' in df.columns:
                            due_date_val = row.get('Ngày hết hạn')
                            if pd.notna(due_date_val):
                                try:
                                    if isinstance(due_date_val, str):
                                        due_date = datetime.strptime(due_date_val, '%Y-%m-%d').date()
                                    else:
                                        due_date = due_date_val.date() if hasattr(due_date_val, 'date') else None
                                except:
                                    try:
                                        due_date = pd.to_datetime(due_date_val).date()
                                    except:
                                        due_date = None
                        
                        task = {
                            'id': task_id,
                            'name': task_name,
                            'completed': completed,
                            'priority': priority,
                            'category': category,
                            'due_date': due_date.isoformat() if due_date else None,
                            'created_at': datetime.now().isoformat(),
                            'order': idx
                        }
                        
                        imported_tasks.append(task)
                    
                    if imported_tasks:
                        st.session_state.tasks = imported_tasks
                        # Cập nhật task_id_counter
                        max_id = max([t.get('id', 0) for t in imported_tasks])
                        st.session_state.task_id_counter = max_id + 1
                        st.success(f"Đã nhập thành công {len(imported_tasks)} công việc từ file Excel!")
                        st.rerun()
                    else:
                        st.warning("Không có dữ liệu hợp lệ trong file Excel!")
            
            elif file_extension == 'json':
                # Đọc file JSON
                data = json.load(uploaded_file)
                if isinstance(data, list):
                    # Đảm bảo tất cả tasks có field 'order'
                    for idx, task in enumerate(data):
                        if 'order' not in task:
                            task['order'] = idx
                    st.session_state.tasks = data
                    # Cập nhật task_id_counter
                    if data:
                        max_id = max([t.get('id', 0) for t in data])
                        st.session_state.task_id_counter = max_id + 1
                    st.success(f"Đã nhập thành công {len(data)} công việc từ file JSON!")
                    st.rerun()
                else:
                    st.error("File JSON không đúng định dạng!")
            else:
                st.error("Định dạng file không được hỗ trợ!")
                
        except Exception as e:
            st.error(f"Lỗi khi nhập dữ liệu: {str(e)}")
            st.info("💡 Hãy đảm bảo file Excel có các cột: 'Tên công việc' (bắt buộc), 'Hoàn thành', 'Mức độ ưu tiên', 'Danh mục', 'Ngày hết hạn'")

# Main content
st.title("✅ To-Do List App")
st.markdown("---")

# Form thêm task mới
with st.expander("➕ Thêm công việc mới", expanded=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        new_task_name = st.text_input("Tên công việc", key="new_task_input", placeholder="Nhập công việc cần làm...")
    
    with col2:
        new_task_priority = st.selectbox("Mức độ ưu tiên", ["Bình thường", "Quan trọng", "Gấp"], key="new_task_priority")
    
    with col3:
        new_task_category = st.selectbox("Danh mục", CATEGORIES, key="new_task_category")
    
    col4, col5 = st.columns([3, 1])
    with col4:
        new_task_due_date = st.date_input("Ngày hết hạn", value=None, key="new_task_due_date")
    
    with col5:
        st.write("")  # Spacing
        st.write("")  # Spacing
        add_button = st.button("➕ Thêm", type="primary", use_container_width=True)
    
    if add_button and new_task_name:
        add_task(new_task_name, new_task_priority, new_task_category, new_task_due_date)
        st.success(f"Đã thêm: {new_task_name}")
        st.rerun()
    elif add_button and not new_task_name:
        st.warning("Vui lòng nhập tên công việc!")

st.markdown("---")

# Lọc và tìm kiếm tasks
filtered_tasks = st.session_state.tasks.copy()

# Áp dụng bộ lọc trạng thái
if filter_status == "Đang làm":
    filtered_tasks = [t for t in filtered_tasks if not t['completed']]
elif filter_status == "Đã hoàn thành":
    filtered_tasks = [t for t in filtered_tasks if t['completed']]

# Áp dụng bộ lọc priority
if filter_priority != "Tất cả":
    filtered_tasks = [t for t in filtered_tasks if t['priority'] == filter_priority]

# Áp dụng bộ lọc category
if filter_category != "Tất cả":
    filtered_tasks = [t for t in filtered_tasks if t['category'] == filter_category]

# Áp dụng tìm kiếm
if search_query:
    filtered_tasks = [t for t in filtered_tasks if search_query.lower() in t['name'].lower()]

# Hiển thị danh sách tasks
if not filtered_tasks:
    st.info("📝 Không có công việc nào. Hãy thêm công việc mới!")
else:
    st.subheader(f"📋 Danh sách công việc ({len(filtered_tasks)}/{len(st.session_state.tasks)})")
    
    # Sắp xếp tasks
    priority_order = {"Gấp": 0, "Quan trọng": 1, "Bình thường": 2}
    
    if sort_option == "Thứ tự thêm":
        # Tìm order trong danh sách gốc
        task_order_map = {t['id']: t.get('order', 0) for t in st.session_state.tasks}
        filtered_tasks.sort(key=lambda x: (x['completed'], task_order_map.get(x['id'], 0)))
    elif sort_option == "Mức độ ưu tiên":
        filtered_tasks.sort(key=lambda x: (x['completed'], priority_order.get(x['priority'], 3)))
    elif sort_option == "Ngày hết hạn":
        def get_due_date(task):
            if task['due_date']:
                try:
                    return datetime.fromisoformat(task['due_date']).date()
                except:
                    return date.max
            return date.max
        filtered_tasks.sort(key=lambda x: (x['completed'], get_due_date(x)))
    elif sort_option == "Tên (A-Z)":
        filtered_tasks.sort(key=lambda x: (x['completed'], x['name'].lower()))
    
    for idx, task in enumerate(filtered_tasks):
        with st.container():
            # Tìm vị trí thực tế trong danh sách gốc để di chuyển
            original_index = next((i for i, t in enumerate(st.session_state.tasks) if t['id'] == task['id']), None)
            can_move_up = original_index is not None and original_index > 0
            can_move_down = original_index is not None and original_index < len(st.session_state.tasks) - 1
            
            # Tạo layout cho mỗi task
            task_col1, task_col2, task_col3, task_col4, task_col5, task_col6 = st.columns([0.5, 3, 2, 1.5, 1, 0.8])
            
            with task_col1:
                # Checkbox hoàn thành
                is_completed = st.checkbox(
                    "",
                    value=task['completed'],
                    key=f"checkbox_{task['id']}",
                    label_visibility="collapsed"
                )
                if is_completed != task['completed']:
                    toggle_task_completion(task['id'])
                    st.rerun()
            
            with task_col2:
                # Hiển thị tên task với style
                task_name_style = ""
                if task['completed']:
                    task_name_style = "text-decoration: line-through; opacity: 0.6;"
                
                priority_emoji = PRIORITY_COLORS.get(task['priority'], "⚪")
                priority_color = PRIORITY_COLORS_HEX.get(task['priority'], "#CCCCCC")
                
                st.markdown(
                    f"""
                    <div style="padding: 8px; border-left: 4px solid {priority_color}; background-color: {'#f0f0f0' if task['completed'] else '#ffffff'}; border-radius: 4px;">
                        <p style="margin: 0; {task_name_style}">
                            <strong>{priority_emoji} {task['name']}</strong>
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with task_col3:
                # Hiển thị thông tin bổ sung
                info_text = f"📁 {task['category']}"
                if task['due_date']:
                    due_date_obj = datetime.fromisoformat(task['due_date']).date()
                    today = date.today()
                    days_left = (due_date_obj - today).days
                    if days_left < 0:
                        info_text += f" | ⏰ <span style='color: red;'>Quá hạn {abs(days_left)} ngày</span>"
                    elif days_left == 0:
                        info_text += f" | ⏰ <span style='color: orange;'>Hết hạn hôm nay</span>"
                    else:
                        info_text += f" | ⏰ Còn {days_left} ngày"
                
                st.markdown(info_text, unsafe_allow_html=True)
            
            with task_col4:
                # Dropdown để chỉnh sửa
                edit_option = st.selectbox(
                    "Thao tác",
                    ["Chọn...", "✏️ Chỉnh sửa", "🗑️ Xóa"],
                    key=f"action_{task['id']}"
                )
                
                if edit_option == "✏️ Chỉnh sửa":
                    with st.popover("Chỉnh sửa công việc", use_container_width=True):
                        edit_name = st.text_input("Tên công việc", value=task['name'], key=f"edit_name_{task['id']}")
                        edit_priority = st.selectbox(
                            "Mức độ ưu tiên",
                            ["Bình thường", "Quan trọng", "Gấp"],
                            index=["Bình thường", "Quan trọng", "Gấp"].index(task['priority']),
                            key=f"edit_priority_{task['id']}"
                        )
                        edit_category = st.selectbox(
                            "Danh mục",
                            CATEGORIES,
                            index=CATEGORIES.index(task['category']),
                            key=f"edit_category_{task['id']}"
                        )
                        current_due_date = None
                        if task['due_date']:
                            current_due_date = datetime.fromisoformat(task['due_date']).date()
                        edit_due_date = st.date_input(
                            "Ngày hết hạn",
                            value=current_due_date,
                            key=f"edit_due_date_{task['id']}"
                        )
                        
                        if st.button("💾 Lưu", key=f"save_{task['id']}"):
                            update_task(
                                task['id'],
                                name=edit_name,
                                priority=edit_priority,
                                category=edit_category,
                                due_date=edit_due_date
                            )
                            st.success("Đã cập nhật!")
                            st.rerun()
                
                elif edit_option == "🗑️ Xóa":
                    if st.button("Xác nhận xóa", key=f"confirm_delete_{task['id']}", type="secondary"):
                        delete_task(task['id'])
                        st.success("Đã xóa!")
                        st.rerun()
            
            with task_col5:
                # Hiển thị priority badge
                priority_color_hex = PRIORITY_COLORS_HEX.get(task['priority'], "#CCCCCC")
                st.markdown(
                    f"""
                    <div style="padding: 4px 8px; background-color: {priority_color_hex}; color: white; border-radius: 12px; text-align: center; font-size: 12px;">
                        {task['priority']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with task_col6:
                # Nút di chuyển lên/xuống (chỉ hiển thị khi không filter hoặc filter = "Tất cả")
                if filter_status == "Tất cả" and filter_priority == "Tất cả" and filter_category == "Tất cả" and not search_query:
                    col_up, col_down = st.columns(2)
                    with col_up:
                        if st.button("⬆️", key=f"up_{task['id']}", disabled=not can_move_up, use_container_width=True):
                            move_task_up(task['id'])
                            st.rerun()
                    with col_down:
                        if st.button("⬇️", key=f"down_{task['id']}", disabled=not can_move_down, use_container_width=True):
                            move_task_down(task['id'])
                            st.rerun()
            
            st.divider()

# Footer
st.markdown("---")
st.caption("💡 Tip: Dữ liệu được lưu tự động trong session. Sử dụng tính năng Export/Import để lưu trữ lâu dài.")


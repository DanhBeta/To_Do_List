# 📝 To-Do List App với Streamlit

Ứng dụng quản lý công việc (To-Do List) được xây dựng bằng Streamlit với đầy đủ các tính năng CRUD và quản lý nâng cao.

## ✨ Tính năng

### 1. Chức năng cốt lõi (CRUD)
- ✅ **Tạo mới (Create)**: Thêm công việc mới với đầy đủ thông tin
- 📋 **Hiển thị (Read)**: Danh sách công việc được hiển thị rõ ràng, có phân loại
- ✏️ **Chỉnh sửa (Update)**: Sửa tên, mức độ ưu tiên, danh mục, ngày hết hạn
- 🗑️ **Xóa (Delete)**: Xóa công việc không còn cần thiết

### 2. Chức năng quản lý và sắp xếp
- ☑️ **Đánh dấu hoàn thành**: Checkbox với hiệu ứng gạch ngang khi hoàn thành
- ⚡ **Mức độ ưu tiên**: 3 mức (Gấp 🔴, Quan trọng 🟡, Bình thường 🟢) với màu sắc phân biệt
- 📁 **Phân loại theo danh mục**: Công việc, Cá nhân, Học tập, Khác
- 📅 **Ngày hết hạn (Due Date)**: Thiết lập deadline và cảnh báo khi sắp hết hạn

### 3. Chức năng trải nghiệm người dùng (UX)
- 🔍 **Tìm kiếm**: Tìm nhanh công việc theo từ khóa
- 📊 **Bộ lọc**: Lọc theo trạng thái (Tất cả, Đang làm, Đã hoàn thành), mức độ ưu tiên, danh mục
- 📈 **Thống kê**: Hiển thị số lượng công việc tổng, đã hoàn thành, đang làm
- 💾 **Lưu trữ**: Dữ liệu được lưu trong session state (tự động lưu khi sử dụng)
- 📥 **Export/Import**: Xuất và nhập dữ liệu dạng Excel (.xlsx) hoặc JSON để backup

## 🚀 Cài đặt và Chạy

### Yêu cầu
- Python 3.7 trở lên
- Streamlit

### Cài đặt

1. Clone hoặc tải project về máy

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

3. Chạy ứng dụng:
```bash
streamlit run app.py
```

4. Mở trình duyệt và truy cập địa chỉ được hiển thị (thường là `http://localhost:8501`)

## 📖 Hướng dẫn sử dụng

### Thêm công việc mới
1. Mở phần "➕ Thêm công việc mới"
2. Nhập tên công việc
3. Chọn mức độ ưu tiên
4. Chọn danh mục
5. (Tùy chọn) Chọn ngày hết hạn
6. Nhấn nút "➕ Thêm"

### Chỉnh sửa công việc
1. Tìm công việc cần chỉnh sửa
2. Chọn "✏️ Chỉnh sửa" từ dropdown "Thao tác"
3. Cập nhật thông tin trong popover
4. Nhấn "💾 Lưu"

### Đánh dấu hoàn thành
- Tích vào checkbox bên trái tên công việc
- Công việc sẽ được gạch ngang và làm mờ

### Xóa công việc
1. Chọn "🗑️ Xóa" từ dropdown "Thao tác"
2. Nhấn "Xác nhận xóa"

### Tìm kiếm và Lọc
- Sử dụng sidebar bên trái để:
  - Tìm kiếm theo từ khóa
  - Lọc theo trạng thái
  - Lọc theo mức độ ưu tiên
  - Lọc theo danh mục

### Export/Import dữ liệu
- **Export Excel**: Nhấn "📥 Xuất Excel" trong sidebar để tải file .xlsx
- **Export JSON**: Nhấn "📥 Xuất JSON" trong sidebar để tải file .json
- **Import**: Chọn file Excel (.xlsx) hoặc JSON (.json) đã export và upload trong phần "📤 Nhập dữ liệu"
  - File Excel cần có cột "Tên công việc" (bắt buộc)
  - Các cột tùy chọn: "Hoàn thành", "Mức độ ưu tiên", "Danh mục", "Ngày hết hạn"

## 🎨 Giao diện

- Giao diện hiện đại, thân thiện với người dùng
- Màu sắc phân biệt theo mức độ ưu tiên
- Responsive layout với sidebar và main content
- Hiệu ứng visual khi hoàn thành công việc

## 📝 Lưu ý

- Dữ liệu được lưu trong Streamlit session state, sẽ mất khi đóng trình duyệt hoặc refresh trang
- Để lưu trữ lâu dài, sử dụng tính năng Export để lưu file Excel hoặc JSON
- Có thể Import lại file Excel hoặc JSON đã export để khôi phục dữ liệu
- Khi nhập từ Excel, cột "Tên công việc" là bắt buộc. Các cột khác là tùy chọn và sẽ dùng giá trị mặc định nếu thiếu

## 🔧 Công nghệ sử dụng

- **Streamlit**: Framework web app Python
- **Python**: Ngôn ngữ lập trình chính
- **Pandas**: Xử lý dữ liệu và Excel
- **OpenPyXL**: Đọc/ghi file Excel
- **JSON**: Format lưu trữ dữ liệu

## 📄 License

MIT License - Tự do sử dụng và chỉnh sửa


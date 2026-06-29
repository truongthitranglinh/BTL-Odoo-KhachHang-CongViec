# BTL Odoo - Quản lý Khách hàng & Công việc tích hợp HRM

## Giới thiệu
Hệ thống ERP nhỏ xây dựng trên Odoo 15, tích hợp 3 module: Quản lý Nhân sự, Quản lý Khách hàng và Quản lý Công việc. Dữ liệu nhân sự là nguồn gốc, đồng bộ sang các module còn lại.

## Modules

### 1. Quản lý Nhân sự (nhan_su)
- Quản lý thông tin nhân viên, phòng ban, chức vụ
- Tự động tạo mã định danh nhân viên
- Là dữ liệu gốc cho toàn hệ thống

### 2. Quản lý Khách hàng (quan_ly_khach_hang)
- Quản lý hồ sơ khách hàng, hợp đồng, chiến dịch
- Gán nhân viên phụ trách từ HRM
- Ghi nhận phản hồi, đánh giá sao
- Tự động tạo chiến dịch sinh nhật
- Tự động tạo công việc khi có phản hồi mới

### 3. Quản lý Công việc (quan_ly_cong_viec)
- Quản lý công việc gắn với khách hàng và nhân viên
- Tự động gán nhân viên rảnh trong phòng ban
- Đồng bộ Google Calendar
- Theo dõi trạng thái, mức độ ưu tiên

### 4. Chatbot AI (chatbot_noiquy)
- Trả lời câu hỏi về nội quy công ty
- Tích hợp Groq API (LLaMA 3)
- Hỗ trợ mọi câu hỏi bằng tiếng Việt

## Luồng nghiệp vụ tự động (Mức 2)
## Cài đặt và chạy

### Yêu cầu
- Python 3.8+
- PostgreSQL
- Odoo 15

### Bước 1: Clone repo
### Bước 2: Lấy Groq API key miễn phí
Vào https://console.groq.com/keys tạo API key

### Bước 3: Chạy Odoo
### Bước 4: Cài modules
Vào Apps, tìm và cài: nhan_su, quan_ly_khach_hang, quan_ly_cong_viec, chatbot_noiquy

## Cải tiến so với bản gốc
- Thêm trigger tự động tạo công việc từ phản hồi khách hàng
- Tích hợp AI chatbot dùng Groq API
- Thêm tab công việc liên quan trong hồ sơ khách hàng
- Tự động gán nhân viên rảnh khi tạo công việc

## Nguồn tham khảo
- Repo gốc: https://github.com/pnguyen1310/TTDN-16-01-N1
- Odoo 15 Documentation: https://www.odoo.com/documentation/15.0

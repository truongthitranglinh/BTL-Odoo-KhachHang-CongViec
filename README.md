# Faculty of Information Technology (DaiNam University)

## He thong quan ly Khach hang, Cong viec tich hop Nhan su tren nen tang Odoo 15

<div align="center">
  <img src="images/aiotlab_logo.png" alt="AIoTLab Logo" width="180"/>
  <img src="images/fitdnu_logo.png" alt="FIT DNU Logo" width="180"/>
  <img src="images/dnu_logo.png" alt="DaiNam University Logo" width="180"/>

  [![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://fit.dainam.edu.vn)
  [![Faculty of IT](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://fit.dainam.edu.vn)
  [![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)
</div>

[![FIT-DNU](https://img.shields.io/badge/FIT-DNU-blue)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![Odoo](https://img.shields.io/badge/ERP-Odoo%2015-purple)](https://www.odoo.com/)
[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)](https://www.postgresql.org/)

## Gioi thieu

He thong ERP nho xay dung tren nen tang Odoo 15, tich hop 3 module chinh: Quan ly Nhan su, Quan ly Khach hang va Quan ly Cong viec, cong them module Chatbot AI. Du lieu nhan su la nguon goc, dong bo sang cac module con lai.

Nguon tham khao: https://github.com/pnguyen1310/TTDN-16-01-N1 - co cai tien va mo rong tinh nang so voi phien ban goc.

## Cac Module

### 1. Quan ly Nhan su (nhan_su)
- Quan ly thong tin nhan vien, phong ban
- Tu dong tao ma dinh danh nhan vien
- Tu dong tao ma phong ban
- Tu tinh ho ten day du, dem so luong nhan vien theo phong ban
- La du lieu goc cho toan he thong, cac module khac deu chon nhan vien tu day (khong nhap tay)

### 2. Quan ly Khach hang (quan_ly_khach_hang)
- Quan ly ho so khach hang
- Gan nhan vien phu trach tu HRM (Many2one)
- Ghi nhan phan hoi, danh gia sao cua khach hang
- Tu dong tao cong viec tuong ung khi co phan hoi moi (theo so sao)
- Tu dong tao ban ghi khieu nai khi phan hoi qua thap
- Nut "Tao lich hen" va "Tao bao gia" tren form khach hang -> tu tao cong viec
- Xuat bao cao Excel danh sach khach hang
- Xem nhanh danh sach cong viec lien quan tu form khach hang (smart button)

### 3. Quan ly Cong viec (quan_ly_cong_viec)
- Quan ly cong viec gan voi khach hang, nhan vien thuc hien va phong ban phu trach
- Quy trinh trang thai cong viec: Bat dau / Hoan thanh / Huy
- Tu dong cap nhat trang thai khach hang khi cong viec hoan thanh (theo loai cong viec)
- Dong bo cong viec voi Google Calendar (tao / cap nhat / xoa event tuong ung)
- Xu ly khieu nai khach hang: quy trinh Bat dau xu ly -> Phan hoi -> Hoan thanh / Tu choi

### 4. Chatbot AI (chatbot_noiquy)
- Tra loi cau hoi ve noi quy cong ty, dua tren du lieu noi quy noi bo (doc tu file)
- Tich hop Groq API (LLaMA 3.1 8B Instant)
- Ho tro cau hoi bang tieng Viet

## Luong nghiep vu tu dong (Muc 2)

Luong du lieu: HRM -> Quan ly Khach hang -> Quan ly Cong viec

| Su kien (Trigger) | Ket qua tu dong |
|---|---|
| Phan hoi 1-2 sao | Tao cong viec "[Khan] Gap mat xu ly" + tao ban ghi Khieu nai |
| Phan hoi 3 sao | Tao cong viec "Goi dien cham soc" |
| Phan hoi 4-5 sao | Tao cong viec "Email cam on" |
| Click "Tao lich hen" | Tao cong viec loai Lich hen |
| Click "Tao bao gia" | Tao cong viec loai Gui bao gia |
| Cong viec hoan thanh (Lich hen) | Cap nhat KH -> "Dang dam phan" |
| Cong viec hoan thanh (Bao gia dong y) | Cap nhat KH -> "Thanh cong" |
| Cong viec hoan thanh (Goi dien/Email) | Cap nhat KH -> "Da lien he" |

## Ung dung AI / External API (Muc 3)

- **Chatbot noi quy**: nhan cau hoi tu nhan vien -> doc du lieu noi quy noi bo -> goi Groq API (LLaMA 3.1) -> tra loi.
- **Google Calendar**: khi tao/sua/huy cong viec co ngay bat dau, he thong tu dong dong bo sang Google Calendar cua nguoi thuc hien.

## Cai tien so voi ban goc

- Them trigger tu dong tao cong viec tu phan hoi khach hang (theo so sao)
- Them trigger tu dong tao khieu nai tu phan hoi tieu cuc
- Tu dong cap nhat trang thai khach hang khi cong viec hoan thanh
- Tich hop AI chatbot dung Groq API, doc du lieu noi quy noi bo
- Dong bo hai chieu voi Google Calendar
- Them tab "Cong viec" va "Phan hoi" trong ho so khach hang
- Xuat bao cao Excel danh sach khach hang
- Quy trinh xu ly khieu nai rieng cho khach hang

## Cai dat va chay

### Yeu cau
- Ubuntu 22.04 / WSL2
- Python 3.10
- Docker
- Git

### Buoc 1: Clone repo
```bash
git clone https://github.com/truongthitranglinh/BTL-Odoo-KhachHang-CongViec.git
cd BTL-Odoo-KhachHang-CongViec
```

### Buoc 2: Tao moi truong ao
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Buoc 3: Khoi dong database
```bash
docker-compose up -d
```

### Buoc 4: Tao file odoo.conf
Tao file `odoo.conf` o thu muc goc, cau hinh `addons_path`, `db_host`, `db_port`, `db_user`, `db_password` phu hop voi moi truong cua ban.

### Buoc 5: Lay Groq API key
Vao https://console.groq.com/keys tao API key mien phi, sau do export truoc khi chay Odoo:
```bash
export GROQ_API_KEY="your-key-here"
```

### Buoc 6: Chay Odoo
```bash
python3 odoo-bin -c odoo.conf --dev=all
```


### Buoc 7: Cau hinh Google Calendar (Muc 3)

He thong dong bo cong viec 2 chieu voi Google Calendar, su dung module `google_calendar` co san cua Odoo.

1. **Tao Google Cloud Project va OAuth Client ID**
   - Truy cap https://console.cloud.google.com/
   - Tao project moi (hoac dung project co san), enable **Google Calendar API**
   - Vao "APIs & Services" > "Credentials" > "Create Credentials" > "OAuth client ID"
   - Chon loai **Web application**
   - Them **Authorized redirect URI**:
http://localhost:8069/google_account/authentication
- Tao xong se nhan duoc **Client ID** va **Client Secret**

2. **Cau hinh trong Odoo**
   - Vao **Settings > General Settings**
   - Tim muc **Google Calendar**, nhap Client ID va Client Secret vua tao
   - Bam **Save**

3. **Ket noi tai khoan Google cho user**
   - Vao app **Calendar**
   - Bam nut **"Google"** (goc phai, duoi lich mini)
   - Dang nhap Google, cap quyen truy cap Calendar
   - Neu gap canh bao "app chua xac minh": vao **Google Cloud Console > OAuth consent screen > Test users**, them dung Gmail se dung de test/demo

4. **Kiem tra**
   - Tao 1 cong viec moi co ngay bat dau, dam bao checkbox "Dong bo voi Google Calendar" duoc bat
   - Kiem tra event xuat hien tren Google Calendar that (calendar.google.com) hoac trong app Calendar cua Odoo

Truy cap: http://localhost:8069

## Thanh vien nhom

| Ho ten | MSSV | Module phu trach chinh | Chuc nang phu tieu bieu da lam |
|---|---|---|---|
| Truong Thi Trang Linh | 1771020425 | Quan ly Khach hang, tich hop Google Calendar, quan ly Git/repo | Xuat bao cao Excel danh sach khach hang (dinh dang mau theo trang thai) |
| Do Thi Phuong Thao | 1771020642 | Quan ly Cong viec, dong bo Google Calendar | Doi mau su kien theo muc uu tien cong viec khi dong bo len Google Calendar (Khan cap: do, Cao: xanh duong dam, Trung binh: vang, Thap: xanh la) |
| Hoang Minh Quan | 1771020563 | Quan ly Nhan su (HRM), Chatbot AI | Tu dong sinh ma dinh danh nhan vien & ma phong ban, tu dem so nhan vien theo phong ban |
| Dinh Anh Truc | 1771020686 | Testing, du lieu mau, Business Flow Diagram | Quy trinh xu ly khieu nai khach hang (Bat dau xu ly -> Phan hoi -> Hoan thanh/Tu choi) |

## Nguon tham khao

- Repo goc: https://github.com/pnguyen1310/TTDN-16-01-N1
- Odoo 15 Documentation: https://www.odoo.com/documentation/15.0/
- Groq API: https://console.groq.com/
- External API Odoo: https://www.odoo.com/documentation/15.0/developer/reference/external_api.html

## Business Flow Diagram
Sơ đồ luồng nghiệp vụ end-to-end (Swimlane) cho đề tài Quản lý khách hàng + Quản lý công việc + HRM (Nhóm 1). Mô tả quy trình từ lúc HR tạo hồ sơ nhân viên, nhân viên kinh doanh tạo khách hàng, đặt lịch hẹn/báo giá (tự động hóa Mức 2, dùng dữ liệu HRM), đến khi tích hợp AI Chatbot và đồng bộ Google Calendar (Mức 3). Xem chi tiết: `docs/business-flow/N1_BusinessFlow_QuanLyKhachHang_CongViec.png`.

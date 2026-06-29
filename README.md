# BTL Odoo - Quan ly Khach hang & Cong viec tich hop HRM

[![FIT-DNU](https://img.shields.io/badge/FIT-DNU-blue)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![Odoo](https://img.shields.io/badge/ERP-Odoo%2015-purple)](https://www.odoo.com/)
[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)](https://www.postgresql.org/)

## Gioi thieu

He thong ERP nho xay dung tren nen tang Odoo 15, tich hop 3 module chinh: Quan ly Nhan su, Quan ly Khach hang va Quan ly Cong viec. Du lieu nhan su la nguon goc, dong bo sang cac module con lai.

Nguon tham khao: https://github.com/pnguyen1310/TTDN-16-01-N1 - co cai tien va mo rong tinh nang so voi phien ban goc.

## Cac Module

### 1. Quan ly Nhan su (nhan_su)
- Quan ly thong tin nhan vien, phong ban, chuc vu
- Tu dong tao ma dinh danh nhan vien
- La du lieu goc cho toan he thong

### 2. Quan ly Khach hang (quan_ly_khach_hang)
- Quan ly ho so khach hang, hop dong, chien dich marketing
- Gan nhan vien phu trach tu HRM
- Ghi nhan phan hoi, danh gia sao
- Tu dong tao chien dich sinh nhat
- Tu dong tao cong viec khi co phan hoi moi
- Nut "Tao lich hen" va "Tao bao gia" tu form khach hang

### 3. Quan ly Cong viec (quan_ly_cong_viec)
- Quan ly cong viec gan voi khach hang va nhan vien
- Tu dong gan nhan vien ranh trong phong ban
- Dong bo Google Calendar
- Tu dong cap nhat trang thai khach hang khi cong viec hoan thanh

### 4. Chatbot AI (chatbot_noiquy)
- Tra loi cau hoi ve noi quy cong ty
- Tich hop Groq API (LLaMA 3)
- Ho tro moi cau hoi bang tieng Viet

## Luong nghiep vu tu dong (Muc 2)

Luong du lieu: HRM -> Quan ly Khach hang -> Quan ly Cong viec

| Su kien (Trigger) | Ket qua tu dong |
|---|---|
| Phan hoi 1-2 sao | Tao cong viec "[Khan] Gap mat xu ly" |
| Phan hoi 3 sao | Tao cong viec "Goi dien cham soc" |
| Phan hoi 4-5 sao | Tao cong viec "Email cam on" |
| Click "Tao lich hen" | Tao cong viec loai Lich hen |
| Click "Tao bao gia" | Tao cong viec loai Gui bao gia |
| Cong viec hoan thanh (Lich hen) | Cap nhat KH -> "Dang dam phan" |
| Cong viec hoan thanh (Bao gia dong y) | Cap nhat KH -> "Thanh cong" |
| Cong viec hoan thanh (Goi dien/Email) | Cap nhat KH -> "Da lien he" |

## Cai tien so voi ban goc

- Them trigger tu dong tao cong viec tu phan hoi khach hang
- Tu dong cap nhat trang thai khach hang khi cong viec hoan thanh
- Tich hop AI chatbot dung Groq API
- Them tab "Cong viec" va "Phan hoi" trong ho so khach hang
- Tu dong gan nhan vien ranh khi tao cong viec

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
### Buoc 5: Lay Groq API key
Vao https://console.groq.com/keys tao API key mien phi

### Buoc 6: Chay Odoo
```bash
python3 odoo-bin -c odoo.conf --dev=all
```

Truy cap: http://localhost:8069

## Thanh vien nhom

| Ho ten | MSSV |
|---|---|
| Truong Thi Trang Linh | 1771020425 |
| Do Thi Phuong Thao | 1771020642 |
| Hoang Minh Quan | 1771020563 |
| Dinh Anh Truc | 1771020686 |

## Nguon tham khao

- Repo goc: https://github.com/pnguyen1310/TTDN-16-01-N1
- Odoo 15 Documentation: https://www.odoo.com/documentation/15.0/
- Groq API: https://console.groq.com/
- External API Odoo: https://www.odoo.com/documentation/15.0/developer/reference/external_api.html

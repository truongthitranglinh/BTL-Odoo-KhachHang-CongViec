import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(20, 11))
ax.set_xlim(0, 20)
ax.set_ylim(0, 11)
ax.axis('off')
lanes = [
    ("HE THONG", 0, 2.2, "#EAF2FB"),
    ("NHAN VIEN KINH DOANH", 2.2, 4.4, "#FFF6E5"),
    ("HR", 4.4, 6.6, "#EAF7EE"),
]
lane_y_center = {}
for name, y0, y1, color in lanes:
    ax.add_patch(mpatches.Rectangle((0.3, y0), 19.4, y1 - y0, facecolor=color, edgecolor="#888888", linewidth=1, zorder=0))
    ax.text(-0.0, (y0 + y1) / 2, name, fontsize=13, fontweight='bold', va='center', ha='right')
    lane_y_center[name] = (y0 + y1) / 2
title_y = 6.6
ax.text(9.85, title_y + 0.55, "LUONG NGHIEP VU: QUAN LY KHACH HANG + QUAN LY CONG VIEC (tich hop HRM)",
        fontsize=15, fontweight='bold', ha='center')
ax.text(9.85, title_y + 0.15, "Nhom 1  -  Happy path (luong chinh)", fontsize=10, ha='center', style='italic', color='#555555')

BLUE = "#BFD7ED"
GREEN = "#B6E3C6"
ORANGE = "#F7C77E"
steps = [
    (1, "HR", 1.6, "Tao ho so nhan vien\n+ phong ban (HRM)", BLUE),
    (2, "NHAN VIEN KINH DOANH", 4.0, "Tao khach hang moi,\nchon NV phu trach tu HRM", BLUE),
    (3, "NHAN VIEN KINH DOANH", 6.6, "Bam Tao lich hen\ntren form khach hang", BLUE),
    (4, "HE THONG", 9.2, "Tu dong tao Cong viec\nLich hen (gan KH + NV tu HRM)", GREEN),
    (5, "HE THONG", 11.6, "Dong bo cong viec\nsang Google Calendar", ORANGE),
    (6, "NHAN VIEN KINH DOANH", 9.2, "Gap khach hang,\nghi nhan phan hoi/danh gia sao", BLUE),
    (7, "HE THONG", 6.6, "Sao thap: tu dong tao\nKhieu nai + Cong viec khan", GREEN),
    (8, "NHAN VIEN KINH DOANH", 14.2, "Xu ly cong viec,\nbam Hoan thanh", BLUE),
    (9, "HE THONG", 16.8, "Tu dong cap nhat trang thai\nkhach hang (qua HRM->KH->CV)", GREEN),
    (10, "NHAN VIEN KINH DOANH", 16.8, "Co thac mac ve noi quy\n-> hoi Chatbot", BLUE),
    (11, "HE THONG", 19.0, "Chatbot doc noi quy noi bo,\ngoi Groq API, tra loi", ORANGE),
]
box_w, box_h = 2.0, 1.5
positions = {}

for step_no, lane, x, text, color in steps:
    y = lane_y_center[lane]
    positions[step_no] = (x, y)
    box = FancyBboxPatch((x - box_w/2, y - box_h/2), box_w, box_h,
                          boxstyle="round,pad=0.05,rounding_size=0.12",
                          facecolor=color, edgecolor="#444444", linewidth=1.3, zorder=3)
    ax.add_patch(box)
    ax.text(x, y + box_h/2 - 0.22, str(step_no), fontsize=11, fontweight='bold',
             ha='center', va='center', color="#222222", zorder=4)
    ax.text(x, y - 0.12, text, fontsize=9.3, ha='center', va='center', zorder=4, linespacing=1.3)
seq = [1,2,3,4,5,6,7,8,9,10,11]
for a, b in zip(seq[:-1], seq[1:]):
    x1, y1 = positions[a]
    x2, y2 = positions[b]
    rad = 0.15 if y1 != y2 else 0
    arrow = FancyArrowPatch((x1 + box_w/2 * (0.95 if x2>=x1 else -0.95), y1),
                             (x2 - box_w/2 * (0.95 if x2>=x1 else -0.95), y2),
                             connectionstyle="arc3,rad=" + str(rad),
                             arrowstyle='-|>', mutation_scale=15, color="#333333", linewidth=1.4, zorder=2)
    ax.add_patch(arrow)
legend_y = -0.55
legend_items = [
    (BLUE, "Buoc thao tac / du lieu thuong"),
    (GREEN, "Muc 2 - Tu dong hoa (trigger giua module, dung du lieu HRM)"),
    (ORANGE, "Muc 3 - AI / External API"),
]
lx = 0.3
for color, label in legend_items:
    ax.add_patch(mpatches.Rectangle((lx, legend_y - 0.15), 0.35, 0.3, facecolor=color, edgecolor="#444444"))
    ax.text(lx + 0.5, legend_y, label, fontsize=9.5, va='center')
    lx += 0.5 + len(label) * 0.093 + 0.9

note_y = -1.15
ax.text(0.3, note_y, "Ghi chu (ngoai le, khong chi tiet trong luong chinh):", fontsize=9.5, fontweight='bold')
ax.text(0.3, note_y - 0.4, "- Neu khach hang tu choi bao gia: cong viec danh dau Huy, khong cap nhat trang thai KH sang Thanh cong.", fontsize=9)
ax.text(0.3, note_y - 0.75, "- Neu Groq API loi hoac qua quota: chatbot tra ve thong bao loi, khong chan cac luong nghiep vu khac.", fontsize=9)

plt.tight_layout()
plt.savefig("docs/business-flow/Nhom_BusinessFlow_QuanLyKhachHang_CongViec.png",
            dpi=200, bbox_inches='tight', facecolor='white')
print("DA VE XONG")

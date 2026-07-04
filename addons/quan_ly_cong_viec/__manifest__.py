# -*- coding: utf-8 -*-
{
    'name': "quan_ly_cong_viec",

    'summary': """
        Module quản lý công việc""",

    'description': """
        Module quản lý công việc và các hoạt động tương tác với khách hàng.
        Bao gồm: gọi điện, gửi báo giá, lịch hẹn và các công việc khác.
    """,

    'author': "pnguyen",
    'website': "http://www.yourcompany.com",

    'category': 'Productivity',
    'version': '0.1',

    'depends': ['base', 'nhan_su', 'quan_ly_khach_hang', 'google_calendar'],

    'data': [
        'security/ir.model.access.csv',
        'views/cong_viec.xml',
        'views/du_an_tai_nguyen_khieu_nai.xml',
        'views/khach_hang_extend.xml',
        'views/nhan_vien_extend.xml',
        'views/menu.xml',
    ],

    'demo': [],
    'installable': True,
    'application': True,
}
